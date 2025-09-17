"""
Payment service routes for handling Stripe payment intents and webhooks.
Provides endpoints for creating payment intents and processing Stripe webhook events.
"""

# importing flask's built-in modules
from flask import Blueprint, request, jsonify, abort

# importing blueprint utilities used in current routing context
from coglex import protected
from coglex.services.payment.utils import _checkout, _subscription


# blueprint instance
_payment = Blueprint("_payment", __name__)


@_payment.route("/service/payment/v1/checkout/", methods=["POST"])
@_payment.route("/service/payment/v1/checkout", methods=["POST"])
@protected()
def checkout():
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
        req = _checkout(
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
        
    raises:
        400: if required parameters are missing
        500: if subscription creation fails
    """
    # checking required paramters
    if not request.json.get("email") or not request.json.get("items"):
        return abort(400)

    try:
        # creating payment subscription
        req = _subscription(
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
