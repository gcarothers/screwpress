from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config

import stripe

from .models import (
    DBSession,
    Item, Purchase
    )

@view_config('purchase_item')
def purchase_item(request):
    item = DBSession.query(Item).get(request.matchdict['item'])
    if not item:
        return HTTPNotFound()
    
    customer_email = request.params['email']
    price = request.params['price'] # In cents
    stripe_token = request.params['stripe_token']

    stripe.api_key = request.registry['stripe.key']
    charge = stripe.Charge.create(
        amount=price, currency='usd', card=stripe_token,
        description='Screwpress Purchase' 
    )
    if charge['paid']:
        purchase = Purchase(item=item, customer_email=customer_email,
                            price=price)
        DBSession.add(purchase)
        purchase.make_files(books_directory=request.registry['books_directory'],
                            purchases_directory=request.registry['purchases_directory'])

