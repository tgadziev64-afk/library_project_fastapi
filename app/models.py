from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Table, Column, ForeignKey, DateTime
from datetime import datetime

class Base(DeclarativeBase):
    pass

book_genre = Table(
    "book_genre",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
)
book_author = Table(
    "book_author",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
)

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    books: Mapped[list["Book"]] = relationship(secondary=book_author, back_populates="authors")

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name!r})"


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    books: Mapped[list["Book"]] = relationship(secondary=book_genre, back_populates="genres")

    def __repr__(self):
        return f"Genre(id={self.id}, name={self.name!r})"

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    year: Mapped[int | None]
    genres: Mapped[list["Genre"]] = relationship(secondary=book_genre, back_populates="books")
    authors: Mapped[list["Author"]] = relationship(secondary=book_author, back_populates="books")
    loans: Mapped[list["Loan"]] = relationship(back_populates="book")

    def __repr__(self):
        return f"Book(id={self.id}, title={self.title!r}, year={self.year})"

class Reader(Base):
    __tablename__ = "readers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    loans: Mapped[list["Loan"]] = relationship(back_populates="reader")

    def __repr__(self):
        return f"Reader(id={self.id}, name={self.name})"

class Loan(Base):
    __tablename__ = "loans"
    id: Mapped[int] = mapped_column(primary_key=True)
    reader_id: Mapped[int] = mapped_column(ForeignKey("readers.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    borrowed_at: Mapped[datetime] = mapped_column(DateTime)  # Дата выдачи
    returned_at: Mapped[datetime | None] = mapped_column(DateTime)  # дата возврата

    reader: Mapped["Reader"] = relationship(back_populates="loans")
    book: Mapped["Book"] = relationship(back_populates="loans")

    def __repr__(self):
        return f"Loan(id={self.id}, book_id={self.book_id}, reader_id={self.reader_id}, borrowed_at={self.borrowed_at}, returned_at={self.returned_at})"
