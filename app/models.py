# DB MODELS
from db.database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey,  Integer, String, null, text, BigInteger
from sqlalchemy.orm import relationship

# CREATE MODELS UNDER HERE
#
# USER MODEL
class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    username = Column(String, unique=True)
    name = Column(String)
    home_address = Column(String)

    credit_cards = relationship('CreditCard', back_populates='owner')
    wish_list = relationship('WishList', back_populates='owner')

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class CreditCard(Base):
    __tablename__ = 'credit_cards'

    id = Column(BigInteger, primary_key=True, index=True)
    card_number = Column(String, nullable=False, unique=True)

    owner_username = Column(String, ForeignKey('users.username', ondelete='CASCADE'), nullable=False)
    owner = relationship('User', back_populates='credit_cards')

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class WishList(Base):
    __tablename__ = 'wish_list'

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    books = Column(String)

    owner_username = Column(String, ForeignKey('users.username', ondelete='CASCADE'), nullable=False)
    owner = relationship('User', back_populates='wish_list', )

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# BOOK MODEL
class Book(Base):
    __tablename__ = 'books'

    book_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    isbn = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    author_id = Column(Integer, nullable=False)
    publisher = Column(String, nullable=False)
    publishedDate = Column(TIMESTAMP, nullable=False)
    description = Column(String)
    price = Column(float, nullable=False)
    copiesSold = Column(Integer, nullable=False)

# AUTHOR MODEL
class Author(Base):
    __tablename__ = 'authors'

    author_id = Column(BigInteger, nullable=False, unique=True, primary_key=True, index=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    publisher = Column(String)
    biography = Column(String)
    books = Column(String)

# PUBLISHER MODEL
class Publisher(Base):
    __tablename__ = 'publishers'

    publisher_id = Column(BigInteger, nullable=False, unique=True, primary_key=True, index=True)
    companyName = Column(String, nullable=False)
    book_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    country = Column(String)

# ORDERS
class Orders(Base):
    __tablename__ = 'orders'

    order_id = Column(BigInteger, unique=True, nullable=False, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    orderDate = Column(TIMESTAMP, nullable=False)
    subtotal = Column(float, nullable=False)
    shipping = Column(float, nullable=False)
