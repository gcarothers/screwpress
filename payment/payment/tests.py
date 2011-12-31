# -*- coding: utf-8 -*-
import unittest
import transaction

from pyramid import testing

from .models import DBSession

# class TestMyView(unittest.TestCase):
#     def setUp(self):
#         self.config = testing.setUp()
#         from sqlalchemy import create_engine
#         engine = create_engine('sqlite://')
#         from .models import (
#             Base,
#             MyModel,
#             )
#         DBSession.configure(bind=engine)
#         Base.metadata.create_all(engine)
#         with transaction.manager:
#             model = MyModel(name='one', value=55)
#             DBSession.add(model)

#     def tearDown(self):
#         DBSession.remove()
#         testing.tearDown()

#     def test_it(self):
#         from .views import my_view
#         request = testing.DummyRequest()
#         info = my_view(request)
#         self.assertEqual(info['one'].name, 'one')
#         self.assertEqual(info['project'], 'payment')


from .models import (
    Base,
    Purchase,
    Item,
    )

class TestPurchase(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)


    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_token(self):
        with transaction.manager:
            item = Item(name='TESTING')
            DBSession.add(item)
            purchase = Purchase(item, "test@example.org", 9.99)
            DBSession.add(purchase)
            encrypted_token = purchase.encrypted_token
            validation = item.validate_token(encrypted_token)
            self.assertEquals(validation, 'TESTING:test@example.org')



from .crypto import encrypt, decrypt
from Crypto.Random import get_random_bytes

class TestEncryption(unittest.TestCase):

    def test_plain_text_roundtrip(self):
        key = get_random_bytes(32)
        plain_text = 'some text'
        ciphertext = encrypt(key, plain_text)
        decrypted_text = decrypt(key, ciphertext)
        self.assertEqual(decrypted_text, plain_text)

    def test_plain_text_unicode(self):
        key = get_random_bytes(32)
        plain_text = u'Iñtërnâtiônàlizætiøn'
        ciphertext = encrypt(key, plain_text)
        decrypted_text = decrypt(key, ciphertext)
        self.assertEqual(decrypted_text, plain_text)