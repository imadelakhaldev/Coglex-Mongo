"""
Payment service routes for handling Stripe payment intents and webhooks.
Provides endpoints for creating payment intents and processing Stripe webhook events.
"""


# importing flask's built-in modules
from flask import Blueprint, request, jsonify, abort

# importing blueprint utilities used in current routing context
from coglex import protected
from coglex.services.payment.utils import _session, _subscription


# blueprint instance
_payment = Blueprint("_payment", __name__)


@_payment.route("/service/payment/v1/checkout/", methods=["POST"])
@_payment.route("/service/payment/v1/checkout", methods=["POST"])
@protected()
def checkout():
    """
    create a Stripe Checkout session for one-time or subscription payments

    - mode: either "payment" (one-time) or "subscription"
    - success_url: url to redirect after successful payment
    - cancel_url: url to redirect if payment is cancelled
    - email: customer email address
    - linedata: list of items to purchase

    optional parameters:
    - metadata: additional metadata dictionary (default: {})

    returns:
        response with Checkout session details
    """
    # retreiving required parameters from request json
    mode, success_url, cancel_url, email, linedata = request.json.get("mode"), request.json.get("success_url"), request.json.get("cancel_url"), request.json.get("email"), request.json.get("linedata")

    # checking required paramters
    if not mode or not success_url or not cancel_url or not email or not linedata:
        return abort(400)

    try:
        # creating payment checkout
        req = _session(mode=mode, success_url=success_url, cancel_url=cancel_url, email=email, linedata=linedata, metadata=request.json.get("metadata") or {})
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # returning results
    return jsonify(req), 200


@_payment.route("/service/payment/v1/subscription/", methods=["POST"])
@_payment.route("/service/payment/v1/subscription", methods=["POST"])
@protected()
def subscription():
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
    """
    # retreiving required parameters from request json
    email, linedata = request.json.get("email"), request.json.get("linedata")

    # checking required paramters
    if not email or not linedata:
        return abort(400)

    try:
        # creating payment subscription
        req = _subscription(
            email=email,
            linedata=linedata,
            due=request.json.get("due"),
            metadata=request.json.get("metadata") or {}
        )
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # returning results
    return jsonify(req), 200
