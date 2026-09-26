// config.js - Global Production Endpoints
const CONFIG = {
  // Live Render FastAPI Backend URL
  API_BASE_URL: "https://financial-markets-pulse-api.onrender.com",

  // Live Render PostgreSQL / TimescaleDB Connection String (External)
  DATABASE_URL: "postgresql://market_admin:6QFDVbuSxJkUBLijsGXuVHZNvHI4cGGP@dpg-das39r60tbcc73dl53cg-a.singapore-postgres.render.com/markets_vscf",

  // Public Endpoints
  ENDPOINTS: {
    HEALTH: "https://financial-markets-pulse-api.onrender.com/health",
    LATEST_MARKET: "https://financial-markets-pulse-api.onrender.com/api/v1/market/latest",
    ANOMALIES: "https://financial-markets-pulse-api.onrender.com/api/v1/anomalies",
    GRAPHQL: "https://financial-markets-pulse-api.onrender.com/graphql"
  },

  // Polling Frequency (2 seconds)
  POLL_INTERVAL_MS: 2000
};

// Freeze configuration so scripts cannot overwrite it
Object.freeze(CONFIG);