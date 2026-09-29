from fastapi import FastAPI
from app.routers.books import router as books_router
from app.routers.readers import router as readers_router
from app.routers.loans import router as loans_router

app = FastAPI()
app.include_router(books_router)
app.include_router(readers_router)
app.include_router(loans_router)








