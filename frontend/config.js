// config.js - Global Production Endpoints
const CONFIG = {
  // Live Render FastAPI Backend URL
  API_BASE_URL: "https://financial-markets-pulse-api-v2.onrender.com",

  // Public Endpoints
  ENDPOINTS: {
    HEALTH: "https://financial-markets-pulse-api-v2.onrender.com/health",
    LATEST_MARKET: "https://financial-markets-pulse-api-v2.onrender.com/api/v1/market/latest",
    ANOMALIES: "https://financial-markets-pulse-api-v2.onrender.com/api/v1/anomalies",
    GRAPHQL: "https://financial-markets-pulse-api-v2.onrender.com/graphql"
  },

  // Polling Frequency (2 seconds)
  POLL_INTERVAL_MS: 2000
};

// Freeze configuration so scripts cannot overwrite it
Object.freeze(CONFIG);