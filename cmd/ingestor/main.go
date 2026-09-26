package main

import (
    "log"
    "os"
    "os/signal"
    "syscall"
    "financial-markets-pulse/internal/config"
    "financial-markets-pulse/internal/market"
    "financial-markets-pulse/internal/stream"
)

func main() {
    log.Println("Initializing Go Market Ingestor...")

    cfg := config.LoadConfig()

    publisher, err := stream.NewRedisPubSub(cfg.RedisAddr, cfg.RedisChannel)
    if err != nil {
        log.Fatalf("Critical error connecting to Redis: %v", err)
    }

    symbols := []string{"AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"}
    provider := market.NewLiveProvider(symbols)

    service := market.NewIngestionService(provider, publisher, cfg.IngestionInterval)

    stopChan := make(chan struct{})
    sigChan := make(chan os.Signal, 1)
    signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)

    go service.Start(stopChan)

    sig := <-sigChan
    log.Printf("Received signal %v, shutting down ingestor...", sig)
    close(stopChan)
}
