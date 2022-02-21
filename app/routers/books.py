from fastapi import Depends, status, HTTPException, APIRouter

from typing import List

from sqlalchemy.orm import Session
from db.database import get_db

import models
import schemas

router = APIRouter(
    prefix='/api/users',
    tags=['Profile Management']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Book)
def create_book(book: schemas.Book, db: Session = Depends(get_db)):
    try:
        new_book = models.Book(
            book_id=book.book_id,
            isbn=book.isbn,
            title=book.title,
            author=book.author_id,
            publisher=book.publisher,
            publishedDate=book.publishedDate,
            price=book.price,
            copiesSold=book.copiesSold
        )
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Book already exists')


@router.get('/',  response_model=List[schemas.Book])
def get_all_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    if not books:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Could not find books')
    return books


@router.get('/{isbn}', response_model=schemas.Book)
def get_book(isbn, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.isbn == isbn).first()
    if not book:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'No query found with isbn: {isbn}')
    return book


@router.get('/{title}', response_model=schemas.Book)
def get_book(title, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.title == title).first()
    if not book:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'No query found with title: {title}')
    return book


@router.put('/{isbn}', status_code=status.HTTP_202_ACCEPTED)
def update_book(isbn, book: schemas.Book, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.isbn == isbn).update({
        'title': book.title,
        'author': book.author_id,
        'publisher': book.publisher,
        'publishedDate': book.publishedDate,
        'book_id': book.book_id,
        'description': book.description,
        'price': book.price,
        'copiesSold': book.copiesSold
    })
    if not book:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'No query found with isbn: {isbn}')
    db.commit()
    return {'detail': f'Update book {isbn}'}


@router.delete('/')
def delete_book(isbn, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.isbn == isbn).first()
    if not book:
        raise HTTPException(status.HTTP_204_NO_CONTENT, f'No query found with isbn: {isbn}')
    db.delete(book)
    db.commit()
    return {'detail': f'Deleted book {isbn}'}
