import requests
import pprint

header={'Content-Type': 'application/x-www-form-urlencoded'}
data={'client_id': "connectors", 'client_secret': 'c0nn3ct0rsAr3Aw3s0me',
      'grant_type':'client_credentials'}
token=requests.post(url='http://localhost:18080/auth/realms/camunda-platform/protocol/openid-connect/token', 
                   headers=header, data=data)

access_token = token.json()['access_token']
access_token_header={'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json',
                      'accept': 'application/json'} 

def processos():
    json_post = {
        "filter": {
            "state": "ACTIVE"}
    }
        
    processos=requests.post(url='http://localhost:8081/v1/process-instances/search', 
               headers=access_token_header, json=json_post)
   
    return processos

if __name__=="__main__":
    teste = processos()
    pprint.pprint(teste.json())