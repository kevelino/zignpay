import base64
import json
import requests
import uuid
import time

# Initialize MoMo Api Provisioning
class MomoApiProvisioning():
  def __init__(self, subscription_key, referenceId, environment):
    self.subscription_key = subscription_key
    self.referenceId = referenceId
    self.environment = environment
    self.target_environment = "mtncameroon" if self.environment == "PROD" else "sandbox"
    self.baseUrl = "https://proxy.momoapi.mtn.com" if self.environment == "PROD" else "https://sandbox.momodeveloper.mtn.com"
    self.api_user = None
    self.api_key = None
    
    
  # Create api user
  def create_api_user(self):
    url = self.baseUrl+"/v1_0/apiuser"
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
    url = self.baseUrl+f"/v1_0/apiuser/{self.referenceId}/apikey"
    
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
    
    
class MomoCollection(MomoApiProvisioning):
  def __init__(self, subscription_key, api_user_id, api_key, environment, currency = None):
    self.subscription_key = subscription_key
    self.environment = environment
    self.currency = currency if self.environment == "PROD" else "EUR"
    self.target_environment = "mtncameroon" if self.environment == "PROD" else "sandbox"
    self.baseUrl = "https://proxy.momoapi.mtn.com" if self.environment == "PROD" else "https://sandbox.momodeveloper.mtn.com"
    self.api_user_id = api_user_id
    self.api_key = api_key

  #get access token
  def get_access_token(self):
    url = self.baseUrl+"/collection/token/"
    userid_and_apiKey = self.api_user_id+':'+self.api_key
    encode = base64.b64encode(userid_and_apiKey.encode('utf-8')) 
    headers = {
      "Ocp-Apim-Subscription-Key": self.subscription_key,
      "Authorization": b'Basic ' + encode
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
      access_token = response.json()["access_token"]
      print(access_token)
      return access_token
    else:
      return encode

  #request to pay
  def request_to_pay(self, values):
    url = self.baseUrl+"/collection/v1_0/requesttopay"
    payload = json.dumps({
      "amount": str(values["amount"]),
      "currency": str(values["currency"]),
      "externalId": str(values["reference_id"]),
      "payer": {
      "partyIdType": "MSISDN",
      "partyId": str(values["from"])
    },
      "payerMessage": str(values["description"]),
      "payeeNote": "Thank you for your payment",
    })
    
    Xreference = str(uuid.uuid4())

    headers = {
      'X-Reference-Id': str(Xreference),
      'X-Target-Environment': self.target_environment,
      "Ocp-Apim-Subscription-Key": self.subscription_key,
      "Authorization": 'Bearer '+str(self.get_access_token()),
      # 'X-Callback-Url': 'http://myapp.com/momoapi/callback.com',
      "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, data=payload)
    
    print(response.status_code)

    if response.status_code == 202:
      status = "PENDING"
      status_response = None
      while status == "PENDING":
        time.sleep(5)
        url = self.baseUrl+"/collection/v1_0/requesttopay/"+str(Xreference)

        headers = {
          'Ocp-Apim-Subscription-Key': self.subscription_key,
          'X-Target-Environment': self.target_environment,
          'Authorization': 'Bearer '+str(self.get_access_token())
        }

        status_response = requests.get(url, headers=headers)
        status = status_response.json()['status']
      return status_response.json()
    else:
      return response.status_code