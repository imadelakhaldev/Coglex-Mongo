"""
utility functions for handling online payment processing through Stripe

this module provides wrapper functions around the Stripe API for creating payment
intents and verifying webhook signatures, it simplifies common payment operations
while maintaining proper error handling
"""

# online payment processing provider
import stripe

# importing global configuration
import config


def _checkout(success_url: str, cancel_url: str, email: str, linedata: [dict], metadata: dict = None):
    """
    create a stripe checkout session for one-time payments

    args:
        success_url (str): url to redirect to after successful payment
        cancel_url (str): url to redirect to if payment is cancelled
        email (str): customer's email address
        linedata (list): list of line item dictionaries, each containing price_data / price_id, and quantity
        metadata (dict, optional): additional metadata to attach, defaults to None

    returns:
        stripe.checkout.Session: created checkout session object
    """
    try:
        return stripe.checkout.Session.create(mode="payment", success_url=success_url, cancel_url=cancel_url, customer_email=email, line_items=linedata, metadata=metadata or {})
    except Exception as ex:
        raise ex


def _subscription(email: str, items: [dict], due: int = 7, metadata: dict = None):
    """
    create a new customer and start a subscription
    stripe will email invoices automatically

    args:
        email (str): customer's email address
        items (list): list of line item dictionaries, each containing price_data / price_id, and quantity
        due (int, optional): number of days until invoice is due, defaults to 7
        metadata (dict, optional): additional metadata to attach, defaults to None

    returns:
        stripe.Subscription: created subscription object
    """
    # create a new customer
    try:
        customer = stripe.Customer.create(email=email, metadata=metadata or {})
    except Exception as ex:
        raise ex

    # create a new subscription
    try:
        return stripe.Subscription.create(
            customer=customer.id,
            items=items,
            collection_method="send_invoice",        # send invoice to email
            days_until_due=due,                      # user has 7 days to pay
            payment_behavior="default_incomplete",   # allow subscription creation with pending payment
            metadata=metadata or {}
        )
    except Exception as ex:
        raise ex


def _verify(signature: str, payload: bytes, secret: str = config.STRIPE_PUBLISHABLE_KEY):
    """
    verify the signature of a stripe webhook event

    args:
        signature (str): stripe signature header from the webhook request
        payload (bytes): raw request body bytes
        secret (str): webhook signing secret from stripe dashboard

    returns:
        stripe.Event or None: constructed event object if signature is valid, None if signature verification fails
    """
    try:
        # verify the signature of the event
        return stripe.Webhook.construct_event(payload=payload, sig_header=signature, secret=secret)
    except stripe.error.SignatureVerificationError:
        return None
    except Exception as ex:
        raise ex
