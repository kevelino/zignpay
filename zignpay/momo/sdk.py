import base64
import json
import requests


# Initialize MoMo Api Provisioning
class MomoApiProvisioning():
  def __init__(self, subscription_key, referenceId):
    self.subscription_key = subscription_key
    self.referenceId = referenceId
    self.api_user = None
    self.api_key = None
    
  # Create api user
  def create_api_user(self):
    url = "https://sandbox.momodeveloper.mtn.com/v1_0/apiuser"
    payload = json.dumps({
      "providerCallbackHost": "https://webhook.site/25701ebb-1340-432e-aa08-1fa457daa70b"
    })
    headers = {
      'Ocp-Apim-Subscription-Key': self.subscription_key,
      'X-Reference-Id': self.referenceId,
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    if response.status_code == 201:
      self.api_user = self.referenceId
      return self.api_user
    else:
      return response.status_code
    
    
   # Create api key 
  def create_api_key(self):
    url = f"https://sandbox.momodeveloper.mtn.com/v1_0/apiuser/{self.referenceId}/apikey"
    
    print(url)
    print(self.referenceId)
    
    headers = {
      'Ocp-Apim-Subscription-Key': self.subscription_key
    }

    response = requests.request("POST", url, headers=headers)
    
    if response.status_code == 201:
      self.api_key = response.json()["apiKey"]
      return self.api_key
    else:
      return response.status_code
    
    
class MomoCollection:
  def __init__(self, subscription_key, api_user_id, api_key):
    self.subscription_key = subscription_key
    self.api_user_id = api_user_id
    self.api_key = api_key
    self.access_token = None

  #get access token
  def get_access_token(self):
    url = "https://sandbox.momodeveloper.mtn.com/collection/token/"
    userid_and_apiKey = self.api_user_id+':'+self.api_key
    encoded = base64.b64encode(userid_and_apiKey.encode('utf-8')) 
    headers = {
      "Ocp-Apim-Subscription-Key": self.subscription_key,
      "Authorization": b'Basic ' + encoded
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
      self.access_token = response.json()["access_token"]
      return self.access_token
    else:
      return encoded

  #request to pay
  def request_to_pay(self, payer, reference_id):
    url = "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay"
    payload = json.dumps({
      "amount": '5.0',
      "currency": 'EUR',
      "externalId": reference_id,
      "payer": {
      "partyIdType": "MSISDN",
      "partyId": payer
    },
      "payerMessage": "Testing Payment",
      "payeeNote": "Thank you for your payment",
    })

    headers = {
      'X-Reference-Id': reference_id,
      'X-Target-Environment': 'sandbox',
      "Ocp-Apim-Subscription-Key": self.subscription_key,
      "Authorization": 'Bearer '+str(self.access_token),
      # 'X-Callback-Url': 'http://myapp.com/momoapi/callback.com',
      "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 202:
      return True
    else:
      return response.status_code