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


def _session(mode: str, success_url: str, cancel_url: str, email: str, linedata: [dict], metadata: dict = None):
    """
    create a Stripe checkout session for one-time payments or subscriptions

    args:
        mode (str): payment mode, either "payment" or "subscription"
        success_url (str): url to redirect to after successful payment
        cancel_url (str): url to redirect to if payment is cancelled
        email (str): customer's email address
        linedata (list): list of line-item dictionaries, each containing, price_data or price_id, and quantity
        metadata (dict, optional): additional metadata to attach, defaults to None

    returns:
        stripe.checkout.Session: created checkout session object
    """
    try:
        # creating a stripe hosted checkout session
        return stripe.checkout.Session.create(mode=mode, success_url=success_url, cancel_url=cancel_url, customer_email=email, line_items=linedata, metadata=metadata or {})
    except Exception as ex:
        raise ex


def _subscription(email: str, linedata: [dict], due: int = 7, metadata: dict = None):
    """
    create or reuse a customer and start a subscription
    stripe will email invoices automatically

    args:
        email (str): customer's email address
        linedata (list): list of line item dictionaries, each containing price_data / price_id, and quantity
        due (int, optional): number of days until invoice is due, defaults to 7
        metadata (dict, optional): additional metadata to attach, defaults to None

    returns:
        stripe.Subscription: created subscription object
    """
    try:
        # check if customer already exists
        customers = stripe.Customer.list(email=email, limit=1).data

        # if customer exists, use the existing customer
        if customers:
            customer = customers[0]
        else:
            # else create a new customer
            customer = stripe.Customer.create(email=email, metadata=metadata or {})
    except Exception as ex:
        raise ex

    try:
        # create a new subscription for the customer, payment collection manually (via email invoices)
        return stripe.Subscription.create(
            customer=customer.id,
            items=linedata,
            collection_method="send_invoice",
            days_until_due=due,
            payment_behavior="default_incomplete",
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
