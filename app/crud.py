from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Author, Genre, Reader, Book, Loan
from sqlalchemy import select
from datetime import datetime
from sqlalchemy.orm import selectinload

async def add_author(session: AsyncSession, name: str) -> Author:
    """Создаёт нового автора с указанным именем."""
    author = Author(name=name)
    session.add(author)
    await session.commit()
    await session.refresh(author)
    return author

async def add_genre(session: AsyncSession, name: str) -> Genre:
    """Создаёт новый жанр с указанным именем."""
    genre = Genre(name=name)
    session.add(genre)
    await session.commit()
    await session.refresh(genre)
    return genre

async def add_reader(session: AsyncSession, name: str) -> Reader:
    """Создаёт нового читателя с указанным именем."""
    reader = Reader(name=name)
    session.add(reader)
    await session.commit()
    await session.refresh(reader)
    return reader

async def add_book(session: AsyncSession, title: str, author_ids: list[int], genre_ids: list[int], year: int | None = None) -> Book:
    """
        Создаёт книгу и привязывает к ней уже существующих авторов и жанров
        по переданным спискам id (many-to-many).
    """
    result = await session.scalars(select(Author).where(Author.id.in_(author_ids)))
    authors = result.all()

    result2 = await session.scalars(select(Genre).where(Genre.id.in_(genre_ids)))
    genres = result2.all()

    book = Book(title=title, year=year, authors=list(authors), genres=list(genres))
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book

async def lend_book(session: AsyncSession, reader_id: int, book_id: int) -> Loan:
    """
        Выдаёт книгу читателю (создаёт запись Loan с текущим временем выдачи).
        Кидает ValueError, если у книги уже есть активная (не возвращённая) выдача.
    """
    existing_loan = await session.scalar(select(Loan).where(Loan.book_id == book_id, Loan.returned_at.is_(None)))
    if existing_loan:
        raise ValueError("Книга уже выдана и не возвращена")

    loan = Loan(reader_id=reader_id, book_id=book_id, borrowed_at=datetime.now())
    session.add(loan)
    await session.commit()
    await session.refresh(loan)
    return loan



async def return_book(session: AsyncSession, book_id: int) -> Loan | None:
    """
        Возвращает книгу: находит активную (не возвращённую) выдачу этой книги
        и проставляет ей дату возврата. Если активной выдачи нет — возвращает None.
    """
    res = await session.scalar(select(Loan).where(Loan.book_id == book_id, Loan.returned_at.is_(None)))
    if not res:
        return None
    res.returned_at = datetime.now()
    await session.commit()
    await session.refresh(res)
    return res

async def get_active_loans(session: AsyncSession) -> list[Loan]:
    """
        Возвращает список всех активных (не возвращённых) выдач,
        сразу подгружая связанных reader и book (чтобы избежать lazy-load ошибок).
    """
    res = await session.scalars(select(Loan).where(Loan.returned_at.is_(None)).options(selectinload(Loan.reader), selectinload(Loan.book)))
    res = res.all()
    return res

async def get_book_by_id(session: AsyncSession, book_id: int) -> Book | None:
    result = await session.scalar(select(Book).where(Book.id == book_id).options(selectinload(Book.authors), selectinload(Book.genres)))
    return result

async def get_reader_by_id(session: AsyncSession, reader_id: int) -> Reader | None:
    result = await session.scalar(select(Reader).where(Reader.id == reader_id))
    return result