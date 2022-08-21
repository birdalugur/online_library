from fastapi import FastAPI
from typing import Union, List
from models import Book
from tasks import list_books, add_book

app = FastAPI()


@app.get("/books/")
async def get_books(_id: Union[str, None] = None) -> List[Book]:
    if _id:
        # @TODO: will be added later
        return {"book": "book"}

    books = list_books.delay()
    return books.get(timeout=1)


@app.post("/add-book/")
def add_new_book(book: Book):
    _id = add_book.delay(book)

    return {"book_id": str(_id.get(timeout=1))}