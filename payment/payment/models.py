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


def encrypt(key, plain_text):
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    import base64
    plain_text = plain_text.encode('utf-8')
    pad = AES.block_size - len(plain_text) % AES.block_size 
    data = plain_text + pad * chr(pad)
    iv_bytes = get_random_bytes(AES.block_size)
    key_bytes = key
    encrypted_bytes = iv_bytes + AES.new(key_bytes, AES.MODE_CBC, iv_bytes).encrypt(data)
    encrypted_string = base64.urlsafe_b64encode(encrypted_bytes)
    return encrypted_string

def decrypt(key, encrypted_string):
    from Crypto.Cipher import AES
    import base64
    encrypted_bytes = base64.urlsafe_b64decode(encrypted_string)
    iv_bytes = encrypted_bytes[:AES.block_size]
    encrypted_bytes = encrypted_bytes[AES.block_size:]
    plain_text = AES.new(key, AES.MODE_CBC, iv_bytes).decrypt(encrypted_bytes)
    pad = ord(plain_text[-1])
    plain_text = plain_text[:-pad]
    return plain_text.decode('utf-8')

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    key = Column(Text, unique=True)