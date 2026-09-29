from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.crud import lend_book, return_book, get_active_loans

router = APIRouter(prefix="/loans", tags=["loans"])

class LoanCreateShema(BaseModel):
    reader_id: int
    book_id: int

@router.post("")
async def create_loan(loan: LoanCreateShema, session: AsyncSession = Depends(get_session)):
    try:
        new_loan = await lend_book(session, loan.reader_id, loan.book_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return {"id": new_loan.id, "borrowed_at": new_loan.borrowed_at}

@router.post("/{book_id}/return")
async def return_load(book_id: int, session: AsyncSession = Depends(get_session)):
    loan = await return_book(session, book_id)
    if not loan:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Активная выдача не найдена")
    return {"id": loan.id, "returned_at": loan.returned_at}

@router.get("/active")
async def active_loans(session: AsyncSession = Depends(get_session)):
    loans = await get_active_loans(session)
    return [
        {"loan_id": loan.id, "reader": loan.reader.name, "book": loan.book.title, "borrowed_at": loan.borrowed_at}
        for loan in loans
    ]
