from fastapi import FastAPI
from routers import posts, users, auth
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)
