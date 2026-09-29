from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.crud import add_reader, get_reader_by_id

router = APIRouter(prefix="/readers", tags=["readers"])
class ReaderCreateShema(BaseModel):
    name: str

@router.post("")
async def create_reader(reader: ReaderCreateShema, session: AsyncSession = Depends(get_session)):
    new_reader = await add_reader(session, reader.name)
    return {"id": new_reader.id, "name": new_reader.name}

@router.get("/{reader_id}")
async def get_reader(reader_id: int, session: AsyncSession = Depends(get_session)):
    reader = await get_reader_by_id(session, reader_id)
    if not reader:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Читатель не найден")
    return {
        "id": reader.id,
        "name": reader.name,
    }
