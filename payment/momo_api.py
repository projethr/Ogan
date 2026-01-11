import requests
import uuid
import json
from django.conf import settings

class MoMoAPI:
    def __init__(self):
        # In a real scenario, these would come from settings
        # and we would handle token generation.
        self.base_url = "https://sandbox.momodeveloper.mtn.com/collection/v1_0"
        self.api_user = getattr(settings, 'MOMO_API_USER', 'user_id_here')
        self.api_key = getattr(settings, 'MOMO_API_KEY', 'api_key_here')
        self.subscription_key = getattr(settings, 'MOMO_SUBSCRIPTION_KEY', 'sub_key_here')
        self.token = None 

    def get_token(self):
        # Mock token for now or implement real logic
        return "mock_token"

    def request_to_pay(self, order_id, amount, phone_number):
        # Implementation of RequestToPay
        # For this MVP, we might simulate a success or print the logic
        reference_id = str(uuid.uuid4())
        
        # Payload
        payload = {
            "amount": str(amount),
            "currency": "EUR", # or XOF if supported by sandbox setup
            "externalId": str(order_id),
            "payer": {
                "partyIdType": "MSISDN",
                "partyId": phone_number
            },
            "payerMessage": f"Paiement commande {order_id}",
            "payeeNote": "OGAN"
        }
        
        # In production we would make the POST request here.
        # response = requests.post(...)
        
        # Returning a mock success for the MVP flow to proceed
        return {
            "success": True,
            "reference_id": reference_id,
            "status": "PENDING" # MoMo is async
        }

    def get_transaction_status(self, reference_id):
        # Mock status check
        return "SUCCESSFUL"
