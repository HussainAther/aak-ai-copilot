from fastapi import FastAPI
from api import score_routes

app = FastAPI(title="AAK AI Copilot API")

# Register routes
app.include_router(score_routes.router)

