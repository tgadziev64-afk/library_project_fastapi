from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.crud import add_book, get_book_by_id

router = APIRouter(prefix="/books", tags=["books"])

class BookCreateShema(BaseModel):
    title: str
    author_ids: list[int]
    genre_ids: list[int]
    year: int | None = None

@router.post("")
async def create_book(book: BookCreateShema, session: AsyncSession = Depends(get_session)):
    new_book = await add_book(session, book.title, book.author_ids, book.genre_ids, book.year)
    return {"id": new_book.id, "title": new_book.title}

@router.get("/{book_id}")
async def get_book(book_id: int, session: AsyncSession = Depends(get_session)):
    book = await get_book_by_id(session, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    return {
        "id": book.id,
        "title": book.title,
        "year": book.year,
        "authors": [a.name for a in book.authors],
        "genres": [g.name for g in book.genres],
    }