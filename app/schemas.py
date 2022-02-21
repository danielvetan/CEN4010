from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

# Oauth2 Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

# User Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# User Schemas
class User(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str]
    home_address: Optional[str]

class ShowUser(BaseModel):
    id: int
    username: EmailStr
    email: EmailStr
    name: str
    home_address: str
    created_at: datetime

    class Config:
        orm_mode = True

# Credit Card Schemas
class CreditCard(BaseModel):
    card_number: str
    owner_username: EmailStr

    class Config:
        orm_mode = True

# Wish List Schema
class WishList(BaseModel):
    name: str
    books: str

class ShowWishList(BaseModel):
    id: int
    name: str
    books: str
    owner_username: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# Book Schema
class Book(BaseModel):
    book_id = int
    isbn =  str
    title = str
    author_id = int
    publisher = str
    publishedDate = datetime
    price = float
    copiesSold = int

    # Optional
    description = str

# Author Schema
class Author(BaseModel):
    author_id = int
    firstName = str
    lastName = str

    # Optional
    publisher = str
    biography = str
    books = str
    
# Publisher Schema
class Publisher(BaseModel):
    publisher_id = int
    book_id = int

    # Optional
    country = str

# Order Schema
class Order(BaseModel):
    order_id = int
    user_id = int
    orderDate = datetime
    subtotal = float
    shipping = float