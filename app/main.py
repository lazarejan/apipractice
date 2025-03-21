from fastapi import FastAPI
from .routers import posts, users, auth, votes
from .database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# this is not needed in case you use alembic
# Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(votes.router)

@app.get("/")
def test():
    return {"message": "Hello World"}
