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

# data = '{"query": "{__schema{types{name}}}"}'  #ok
# data = '{"query": "{__schema{queryType{name}}}"}' #ok 

# data = '{"query": "{tasks(query:{state: CREATED}) {id name assignee processName}}"}' #ok data
data = {"query": "{tasks(query:{assignee: \"vivo.contratos\"}) {id name assignee processName taskState}}"} #ok json
# data = """{"query": "{tasks(query:{}){id name taskState assignee formKey}}"}""" #ok data

# data = {"query": "{task(id:\"2251799813686251\"){id name formKey}}"} # ok

# NOK data = {"query": "{form(id:\"_2pa5kvn\", processDefinitionId: \"asdf\"){id processDefinitionId schema}}"}

# data = {"query": "{currentUser{displayName}}"} #ok json

#data = {"query": "mutation {completeTask(taskId:\"2251799813749977\", variables:[]) {id}}"} # ok
 
# data = {"query": "mutation {claimTask(taskId:\"2251799813750702\", assignee: \"vivo.contratos\", allowOverrideAssignment: true) {id}}"} # ok

# data = {"query": "mutation {completeTask(taskId:\"2251799813750702\", variables: [{name: \"entrada\", value: \"2\"}] ) {id}}"} # ok


processos=requests.post(url='http://localhost:8082/graphql', 
            headers=access_token_header, json=data)


pprint.pprint(processos.json())