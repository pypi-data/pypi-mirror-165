from django.conf import settings


class Cart(object):

    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.total_bill = cart.get('total_bill', 0)
        self.discount = cart.get('discount', 0)
        self.discount_type = cart.get('discount_type', 'percent')
        self.items = cart.get('items', dict())

    def add(self, product, quantity=1):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.items.keys():

            self.items[product_id] = {
                'image': product.image.url,
                'product_id': product.id,
                'name': product.name,
                'quantity': quantity,
                'price': product.price,
            }
        else:
            self.items[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        """
        Calculate and save data in the session
        """
        # The user ID is saved in the session.
        # If the user does not have an ID, it will be equal to None
        self.cart['user_id'] = self.request.user.id

        # Calculation of total price and discount
        total_bill = 0.0
        total_items = 0
        for key, value in self.items.items():
            total_bill += (float(value['price']) * value['quantity'])
            total_items += value['quantity']
        self.total_bill = total_bill
        self.cart['amount_payable'] = total_bill
        if self.discount:
            if self.discount_type == 'amount':
                self.cart['amount_payable'] -= float(self.discount)
            else:
                self.cart['amount_payable'] -= (self.total_bill * float(self.discount)) / 100

        # Store the data in the cart variable
        self.cart['total_bill'] = self.total_bill
        self.cart['total_items_quantity'] = total_items
        self.cart['total_items'] = len(self.items)
        self.cart['discount'] = self.discount
        self.cart['discount_type'] = self.discount_type
        self.cart['items'] = self.items

        # Update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart

        # Mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.items:
            del self.items[product_id]
            self.save()

    def decrement(self, product):
        product_id = str(product.id)
        for key, value in self.items.items():
            if key == product_id:
                if self.items[product_id]['quantity'] >= 2:
                    self.items[product_id]['quantity'] -= 1
                    self.save()
                else:
                    self.remove(product)
                break

    def set_discount(self, discount, discount_type='percent'):
        """
        Set discount amount
        """
        self.discount = discount
        self.discount_type = discount_type
        self.save()

    def clear(self):
        """
        Empty session
        """
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
