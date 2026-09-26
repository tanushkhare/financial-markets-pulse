from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from backend.api.routes import market, anomalies, config
from backend.graphql.schema import schema

app = FastAPI(title="Financial Markets Pulse API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include REST API routers
app.include_router(market.router)
app.include_router(anomalies.router)
app.include_router(config.router)

# Include GraphQL router
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "backend-api"}