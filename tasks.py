from pymongo import MongoClient
from models import Book

from worker import app, connection_string

client = MongoClient(connection_string)

library = client.library

book_docs = library.book_docs
person_docs = library.persons


@app.task(name='Add a new book in database')
def add_book(book: Book):
    inserted_id = book_docs.insert_one(book.dict()).inserted_id

    return inserted_id


@app.task(name="list books")
def list_books():
    all_books = book_docs.find()
    book_tables = []
    for book in all_books:
        # book['_id'] = str(book['_id'])
        book_tables.append(Book(**book))
    return list(book_tables)
