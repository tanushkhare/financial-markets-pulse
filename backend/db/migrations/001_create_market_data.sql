CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS market_data (
    time TIMESTAMPTZ NOT NULL,
    symbol TEXT NOT NULL,
    price DECIMAL(18, 4) NOT NULL,
    volume BIGINT NOT NULL,
    log_return FLOAT,
    volatility FLOAT,
    anomaly_score FLOAT DEFAULT 0.0,
    is_anomaly BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('market_data', 'time', if_not_exists => TRUE);

CREATE INDEX IF NOT EXISTS idx_market_data_symbol_time ON market_data (symbol, time DESC);

CREATE TABLE IF NOT EXISTS system_configs (
    key TEXT PRIMARY KEY,
    value JSONB NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO system_configs (key, value) VALUES 
('supported_symbols', '["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]'::jsonb),
('weighting_coefficients', '{"price_weight": 0.65, "volume_weight": 0.35}'::jsonb),
('anomaly_threshold', '0.75'::jsonb),
('ingestion_interval', '5'::jsonb)
ON CONFLICT (key) DO NOTHING;
