"""
Payment service routes for handling Stripe payment intents and webhooks.
Provides endpoints for creating payment intents and processing Stripe webhook events.
"""

# importing flask's built-in modules
from flask import Blueprint, request, jsonify, abort

# importing base config parameters, and generic utilities
import config

# importing blueprint utilities used in current routing context
from utils import stripe_webhook_received
from coglex import protected
from coglex.services.payment.utils import create_checkout, create_subscription, verify_webhook


# blueprint instance
payment = Blueprint("payment", __name__)


@payment.route("/service/payment/v1/checkout/", methods=["POST"])
@payment.route("/service/payment/v1/checkout", methods=["POST"])
@protected
def payment_create_checkout():
    """
    create a stripe checkout session for one-time payments
    
    requires the following json parameters in the request:
    - success_url: url to redirect after successful payment
    - cancel_url: url to redirect if payment is cancelled
    - email: customer email address
    - linedata: list of items to purchase
    
    optional parameters:
    - metadata: additional metadata dictionary (default: {})
    
    returns:
        json response with checkout session details
        
    raises:
        400: if required parameters are missing
        500: if checkout creation fails
    """
    # checking required paramters
    if not request.json.get("success_url") or not request.json.get("cancel_url") or not request.json.get("email") or not request.json.get("linedata"):
        return abort(400)

    try:
        # creating payment checkout
        req = create_checkout(
            success_url=request.json.get("success_url"),
            cancel_url=request.json.get("cancel_url"),
            email=request.json.get("email"),
            linedata=request.json.get("linedata"),
            metadata=request.json.get("metadata")
        )
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # returning results
    return jsonify(req), 200


@payment.route("/service/payment/v1/subscription/", methods=["POST"])
@payment.route("/service/payment/v1/subscription", methods=["POST"])
@protected
def payment_create_subscription():
    """
    create a stripe subscription for recurring payments
    
    requires the following json parameters in the request:
    - email: customer email address
    - items: list of items to purchase subscription
    
    optional parameters:
    - due: number of days until invoice is due (default: 7)
    - metadata: additional metadata dictionary (default: {})
    
    returns:
        json response with subscription details
        
    raises:
        400: if required parameters are missing
        500: if subscription creation fails
    """
    # checking required paramters
    if not request.json.get("email") or not request.json.get("items"):
        return abort(400)

    try:
        # creating payment subscription
        req = create_subscription(
            email=request.json.get("email"),
            items=request.json.get("items"),
            due=request.json.get("due"),
            metadata=request.json.get("metadata")
        )
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # returning results
    return jsonify(req), 200


@payment.route("/service/payment/v1/webhook/", methods=["POST"])
@payment.route("/service/payment/v1/webhook", methods=["POST"])
def payment_stripe_webhook():
    """
    handle incoming stripe webhook events

    verifies the webhook signature and processes different event types:
    - checkout.session.completed: handles successful one-time payments
    - invoice.paid: handles successful subscription payments
    - invoice.payment_failed: handles failed subscription payments

    returns:
        tuple: json response with success status and 200 status code
        
    raises:
        400: if webhook signature verification fails
    """
    try:
        req = verify_webhook(request.headers.get("Stripe-Signature"), request.data, config.STRIPE_PUBLISHABLE_KEY)
    except Exception:
        return abort(400)

    # handle obtained events
    payload = req.get("data", {}).get("object")

    # handle one-time checkout completion
    if req.get("type") == "checkout.session.completed":
        if payload.get("mode") == "payment" and payload.get("payment_status") == "paid":
            stripe_webhook_received.send(payload)

    # handle paid invoice (subscription payment)
    elif req.get("type") == "invoice.paid":
        stripe_webhook_received.send(payload)

    # handle failed invoice (subscription not paid)
    elif req.get("type") == "invoice.payment_failed":
        stripe_webhook_received.send(payload)

    return jsonify(success=True), 200
