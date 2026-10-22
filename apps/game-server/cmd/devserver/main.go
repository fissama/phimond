// devserver chạy server game thật (luật thật, catalog thật) với kho dữ liệu trong bộ nhớ.
// Chỉ dùng cho dev/e2e: không cần MySQL, không lưu dữ liệu. Mặc định 127.0.0.1:8090.
package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	"phimond/server/internal/character"
	"phimond/server/internal/content"
	"phimond/server/internal/devstore"
	"phimond/server/internal/transport"
	"strconv"
	"strings"
	"syscall"
)

func main() {
	dataDir := os.Getenv("GAME_DATA_DIR")
	if dataDir == "" {
		dataDir = "../../data"
	}
	catalog, err := content.Load(dataDir)
	if err != nil {
		log.Fatal(err)
	}
	// Chỉ dev/e2e: GAME_ENCOUNTER_WEIGHTS="1" ép encounter 1 quái (test đi bộ không bị 3 quái hạ trước khi chạy kịp).
	if w := os.Getenv("GAME_ENCOUNTER_WEIGHTS"); w != "" {
		catalog.Rules.EncounterWeights = nil
		for _, part := range strings.Split(w, ",") {
			n, convErr := strconv.Atoi(strings.TrimSpace(part))
			if convErr != nil {
				log.Fatalf("GAME_ENCOUNTER_WEIGHTS: %v", convErr)
			}
			catalog.Rules.EncounterWeights = append(catalog.Rules.EncounterWeights, n)
		}
	}
	addr := os.Getenv("GAME_ADDR")
	if addr == "" {
		addr = "127.0.0.1:8090"
	}
	ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer cancel()
	log.Println("DEVSERVER: kho dữ liệu trong bộ nhớ, không dùng cho sản xuất")
	if err = transport.Run(ctx, transport.New(devstore.New(), character.NewEngine(catalog)), addr); err != nil {
		log.Fatal(err)
	}
}
