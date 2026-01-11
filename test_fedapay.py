import requests
import json

SECRET_KEY = 'sk_sandbox_nP3mw6xuMuGF8K1QBwmX3xjp'

def test_fedapay_flow():
    # 1. Create Transaction
    url = "https://sandbox-api.fedapay.com/v1/transactions"
    headers = {
        "Authorization": f"Bearer {SECRET_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "description": "Test Transaction",
        "amount": 500,
        "currency": {"iso": "XOF"},
        "callback_url": "http://localhost:8000/payment/done/",
        "customer": {
            "firstname": "Test",
            "lastname": "User",
            "email": "test@example.com",
            "phone_number": {
                "number": "97000000",
                "country": "bj"
            }
        }
    }
    
    print("--- Creating Transaction ---")
    resp = requests.post(url, headers=headers, json=payload)
    print(f"Status: {resp.status_code}")
    data = resp.json()
    print(json.dumps(data, indent=2))
    
    if resp.status_code not in [200, 201]:
        print("Failed to create transaction")
        return

    transaction_id = data.get('v1/transaction', data).get('id')
    print(f"\nTransaction ID: {transaction_id}")

    # 2. Generate Token
    token_url = f"https://sandbox-api.fedapay.com/v1/transactions/{transaction_id}/token"
    print(f"\n--- Generating Token at {token_url} ---")
    
    token_resp = requests.post(token_url, headers=headers, json={})
    print(f"Status: {token_resp.status_code}")
    token_data = token_resp.json()
    print(json.dumps(token_data, indent=2))

if __name__ == "__main__":
    test_fedapay_flow()
