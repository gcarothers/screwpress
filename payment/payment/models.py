import os

from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    LargeBinary,
    Numeric,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref
    )

from zope.sqlalchemy import ZopeTransactionExtension

from Crypto.Random import get_random_bytes

import transaction

from .crypto import encrypt, decrypt


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    aes_key = Column(LargeBinary(length=32), unique=True)

    def __str__(self):
        return self.name

    def __init__(self, name):
        self.name = name
        self.key = get_random_bytes(32)

    def validate_token(self, token):
        return decrypt(self.key, token)

class Purchase(Base):
    __tablename__ = 'purchases'
    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    customer_email = Column(Text, primary_key=True)
    price = Column(Numeric)

    item = relationship(Item, backref=backref('purchases'))

    def __init__(self, item, customer_email, price):
        self.item = item
        self.customer_email = customer_email
        self.price = price
    
    def make_files(self, books_directory, purchases_directory):
        purchase_directory = os.path.join(purchases_directory, self.encrypted_token)
        os.mkdir(purchase_directory)
        os.symlink(os.path.join(books_directory, self.item.name),
                   os.path.join(purchase_directory, 'book')
        with open(os.path.join(purchase_directory, 'purchase.js'), 'w') as f:
            self.write_purchase_js(f)
    
    def write_purchase_js(f):
        pass

    def __str__(self):
        return "{item}:{email}".format(item=self.item,
                                              email=self.customer_email)

    @property
    def encrypted_token(self):
        plain_text = unicode(self)
        key = self.item.key
        return encrypt(key, plain_text)


