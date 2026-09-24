package main

import (
	"context"
	"flag"
	"log"
	"os"
	"os/signal"
	"phimond/server/internal/character"
	"phimond/server/internal/content"
	"phimond/server/internal/persistence"
	"phimond/server/internal/transport"
	"syscall"
	"time"
)

func main() {
	migrate := flag.Bool("migrate", false, "create dedicated database and apply versioned migrations")
	dir := flag.String("migrations", "../../migrations", "migration directory")
	flag.Parse()
	cfg, err := persistence.ConfigFromEnv()
	if err != nil {
		log.Fatal(err)
	}
	ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer cancel()
	if *migrate {
		ctx, cancel := context.WithTimeout(ctx, 2*time.Minute)
		defer cancel()
		if err = persistence.Bootstrap(ctx, cfg, *dir); err != nil {
			log.Fatal(err)
		}
		log.Printf("Dedicated Phimond schema %s ready", cfg.Database)
		return
	}
	dataDir := os.Getenv("GAME_DATA_DIR")
	if dataDir == "" {
		dataDir = "../../data"
	}
	catalog, err := content.Load(dataDir)
	if err != nil {
		log.Fatal(err)
	}
	store, err := persistence.Open(ctx, cfg)
	if err != nil {
		log.Fatal(err)
	}
	store.MovementAllowedKeys = catalog.Rules.MovementAllowedKeys
	defer store.Close()
	addr := os.Getenv("GAME_ADDR")
	if addr == "" {
		addr = "127.0.0.1:8090"
	}
	if err = transport.Run(ctx, transport.New(store, character.NewEngine(catalog)), addr); err != nil {
		log.Fatal(err)
	}
}
