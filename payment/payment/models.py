from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref
    )

from zope.sqlalchemy import ZopeTransactionExtension

from .crypto import encrypt, decrypt


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Purchase(Base):
    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items'))
    customer_email = Column(Text)

    item = relationship("Item", backref=backref('purchases'))

    def __str__(self):
        return "{id:x}:{item}:{email}".format(id=self.id,
                                              item=self.item,
                                              email=self.customer_email)

    def encrypted_token(self):
        plain_text = str(self)
        key = self.item.key
        return encrypt(key, plain_text)


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    key = Column(Text, unique=True)