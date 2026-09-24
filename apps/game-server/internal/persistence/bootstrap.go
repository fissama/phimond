package persistence

import (
	"context"
	"crypto/sha256"
	"crypto/tls"
	"crypto/x509"
	"database/sql"
	"encoding/hex"
	"errors"
	"fmt"
	"net"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"time"

	"github.com/go-sql-driver/mysql"
)

type Config struct {
	Host, Port, User, Password, Database, CAFile string
	TLS                                          bool
	TLSInsecure                                  bool
}

const marker = "phimond-reconstruction-v1"

var identifier = regexp.MustCompile(`^[A-Za-z][A-Za-z0-9_]{0,63}$`)

func validDatabase(s string) bool {
	if !identifier.MatchString(s) {
		return false
	}
	switch strings.ToLower(s) {
	case "mysql", "information_schema", "performance_schema", "sys":
		return false
	}
	return true
}
func ConfigFromEnv() (Config, error) {
	c := Config{TLSInsecure: os.Getenv("MYSQL_TLS_INSECURE") == "true", CAFile: os.Getenv("MYSQL_CA_FILE"), TLS: os.Getenv("MYSQL_TLS") == "true", Host: os.Getenv("MYSQL_HOST"), Port: os.Getenv("MYSQL_PORT"), User: os.Getenv("MYSQL_USER"), Password: os.Getenv("MYSQL_PASSWORD"), Database: os.Getenv("MYSQL_DATABASE")}
	if c.Host == "" {
		c.Host = "127.0.0.1"
	}
	if c.Port == "" {
		c.Port = "3306"
	}
	if c.Database == "" {
		c.Database = os.Getenv("GAME_DB_NAME")
	}
	if c.Database == "" {
		c.Database = "phimond_reconstruction"
	}
	return c, c.validate()
}
func (c Config) validate() error {
	if !validDatabase(c.Database) {
		return errors.New("invalid dedicated database name")
	}
	if c.User == "" {
		return errors.New("MYSQL_USER is required")
	}
	p, e := strconv.Atoi(c.Port)
	if e != nil || p < 1 || p > 65535 {
		return errors.New("invalid MYSQL_PORT")
	}
	return nil
}
func connect(c Config, schema bool) (*sql.DB, error) {
	if e := c.validate(); e != nil {
		return nil, e
	}
	d := mysql.NewConfig()
	if c.TLS || c.TLSInsecure || c.CAFile != "" {
		tlsConfig, name, e := tlsConfiguration(c)
		if e != nil {
			return nil, e
		}
		if e = mysql.RegisterTLSConfig(name, tlsConfig); e != nil {
			return nil, e
		}
		d.TLSConfig = name
	}
	d.User = c.User
	d.Passwd = c.Password
	d.Net = "tcp"
	d.Addr = net.JoinHostPort(c.Host, c.Port)
	// Driver-side escaping avoids prepare/execute/close round trips for each
	// parameterized statement. The driver rejects unsafe multibyte collations.
	d.InterpolateParams = true
	d.ParseTime = true
	d.Timeout = 5 * time.Second
	d.ReadTimeout = 15 * time.Second
	d.WriteTimeout = 15 * time.Second
	if schema {
		d.DBName = c.Database
	}
	db, e := sql.Open("mysql", d.FormatDSN())
	if e == nil {
		db.SetMaxOpenConns(12)
		// Keep the bounded pool warm between action bursts. A lower idle cap
		// discarded healthy connections and repeatedly paid remote TLS setup.
		db.SetMaxIdleConns(12)
		db.SetConnMaxLifetime(3 * time.Minute)
	}
	return db, e
}

// tlsConfiguration verifies the certificate and hostname by default. A custom
// CA augments system roots and enables TLS when MYSQL_TLS is omitted.
// MYSQL_TLS_INSECURE=true is an explicit user-requested local development
// option that enables encrypted TLS without server certificate verification.
func tlsConfiguration(c Config) (*tls.Config, string, error) {
	roots, e := x509.SystemCertPool()
	if e != nil {
		roots = x509.NewCertPool()
	}
	var pem []byte
	if c.CAFile != "" {
		pem, e = os.ReadFile(c.CAFile)
		if e != nil {
			return nil, "", fmt.Errorf("read MYSQL_CA_FILE: %w", e)
		}
		if !roots.AppendCertsFromPEM(pem) {
			return nil, "", errors.New("MYSQL_CA_FILE contains no valid PEM certificates")
		}
	}
	sum := sha256.Sum256(append([]byte(c.Host+"\x00"+strconv.FormatBool(c.TLSInsecure)+"\x00"), pem...))
	return &tls.Config{RootCAs: roots, ServerName: c.Host, MinVersion: tls.VersionTLS12, InsecureSkipVerify: c.TLSInsecure}, "phimond-" + hex.EncodeToString(sum[:]), nil
}

type queryer interface {
	QueryRowContext(context.Context, string, ...any) *sql.Row
}

func verifyMarker(ctx context.Context, q queryer, schema string) error {
	var got string
	if e := q.QueryRowContext(ctx, "SELECT marker FROM `"+schema+"`.`phimond_ownership` WHERE id=1").Scan(&got); e != nil || got != marker {
		return errors.New("database is not a marked Phimond schema; refusing access")
	}
	return nil
}

// Bootstrap creates a new dedicated schema or migrates an already marked one.
// Existing unmarked schemas are never adopted, including a failed partial bootstrap.
func Bootstrap(ctx context.Context, c Config, dir string) error {
	db, e := connect(c, false)
	if e != nil {
		return e
	}
	defer db.Close()
	conn, e := db.Conn(ctx)
	if e != nil {
		return e
	}
	defer conn.Close()
	lockHash := sha256.Sum256([]byte(c.Database))
	lock := "phimond:" + hex.EncodeToString(lockHash[:])[:48]
	var locked int
	if e = conn.QueryRowContext(ctx, "SELECT GET_LOCK(?,30)", lock).Scan(&locked); e != nil {
		return e
	}
	if locked != 1 {
		return errors.New("migration lock unavailable")
	}
	defer conn.ExecContext(context.Background(), "SELECT RELEASE_LOCK(?)", lock)
	var count int
	if e = conn.QueryRowContext(ctx, "SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME=?", c.Database).Scan(&count); e != nil {
		return e
	}
	if count == 0 {
		if _, e = conn.ExecContext(ctx, "CREATE DATABASE `"+c.Database+"` CHARACTER SET utf8mb4 COLLATE utf8mb4_bin"); e != nil {
			return e
		}
		if _, e = conn.ExecContext(ctx, "CREATE TABLE `"+c.Database+"`.`phimond_ownership` (id TINYINT PRIMARY KEY, marker VARCHAR(64) NOT NULL) ENGINE=InnoDB"); e != nil {
			return e
		}
		if _, e = conn.ExecContext(ctx, "INSERT INTO `"+c.Database+"`.`phimond_ownership` VALUES (1,?)", marker); e != nil {
			return e
		}
	}
	if e = verifyMarker(ctx, conn, c.Database); e != nil {
		return e
	}
	if _, e = conn.ExecContext(ctx, "USE `"+c.Database+"`"); e != nil {
		return e
	}
	if _, e = conn.ExecContext(ctx, "CREATE TABLE IF NOT EXISTS schema_migrations (version VARCHAR(128) PRIMARY KEY, checksum CHAR(64) NOT NULL, applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP) ENGINE=InnoDB"); e != nil {
		return e
	}
	files, e := filepath.Glob(filepath.Join(dir, "*.sql"))
	if e != nil {
		return e
	}
	sort.Strings(files)
	if len(files) == 0 {
		return errors.New("no migrations found")
	}
	for _, file := range files {
		b, e := os.ReadFile(file)
		if e != nil {
			return e
		}
		sum := sha256.Sum256(b)
		checksum := hex.EncodeToString(sum[:])
		version := filepath.Base(file)
		var existing string
		e = conn.QueryRowContext(ctx, "SELECT checksum FROM schema_migrations WHERE version=?", version).Scan(&existing)
		if e == nil {
			if existing != checksum {
				return fmt.Errorf("migration checksum changed: %s", version)
			}
			continue
		}
		if !errors.Is(e, sql.ErrNoRows) {
			return e
		}
		// Migrations are checked-in simple DDL, no routines or semicolons in strings.
		for _, statement := range strings.Split(string(b), ";") {
			if strings.TrimSpace(statement) == "" {
				continue
			}
			if _, e = conn.ExecContext(ctx, statement); e != nil {
				return fmt.Errorf("migration %s failed: %w", version, e)
			}
		}
		if _, e = conn.ExecContext(ctx, "INSERT INTO schema_migrations(version,checksum) VALUES (?,?)", version, checksum); e != nil {
			return e
		}
	}
	return nil
}
