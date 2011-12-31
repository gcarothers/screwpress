
from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    LargeBinary,
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

from .crypto import encrypt, decrypt


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    aes_key = Column(LargeBinary(length=32), unique=True)

    def __init__(self, name):
        self.name = name
        self.key = get_random_bytes(32)

class Purchase(Base):
    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    customer_email = Column(Text)

    item = relationship(Item, backref=backref('item_purchases'))

    def __str__(self):
        return "{id:x}:{item}:{email}".format(id=self.id,
                                              item=self.item,
                                              email=self.customer_email)

    def encrypted_token(self):
        plain_text = str(self)
        key = self.item.key
        return encrypt(key, plain_text)


