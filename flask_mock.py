import json
import logging
from keycloak import KeycloakOpenID
from flask import Flask, g
from flask_oidc import OpenIDConnect
import requests
from user_mgmt import logout_name
from servico_task_operator import processos


keycloak_openid = KeycloakOpenID(server_url="http://localhost:18080/auth/",
                                 client_id="camunda-identity",
                                 realm_name="camunda-platform",
                                 client_secret_key="5KsuHVUtLLUtXBvFyO4M74dGxqIxxo1W")


logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_USER_INFO_ENABLED': True,
    'OIDC_OPENID_REALM': 'flask-demo',
    'OIDC_SCOPES': ['openid', 'email', 'profile'],
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post'
})

oidc = OpenIDConnect(app)

@app.route('/')
def inicio():
    if oidc.user_loggedin:
        usuario = oidc.user_getfield('preferred_username')
        return (f'Olá, {usuario}, <a href="/private">Lista de Tarefas</a> '
                '<a href="/logout">Log out</a>')         
    else:
        return 'Bem vindo ao VendorPay, <a href="/private">Log in</a>'


@app.route('/private')
@oidc.require_login
def hello_me():
    info = oidc.user_getinfo(['preferred_username', 'email', 'sub'])

    username = info.get('preferred_username')
    email = info.get('email')
    user_id = info.get('sub')
    
    processos_=processos().json()
    print("\n"*10, processos_)

    # if user_id in oidc.credentials_store:
    #     try:
    #         from oauth2client.client import OAuth2Credentials
    #         access_token = OAuth2Credentials.from_json(oidc.credentials_store[user_id]).access_token
    #         # print(access_token)
    #         headers = {'Authorization': f'Bearer {access_token}','Content-Type': 'application/json',
    #                   'accept': 'application/json'}
    #         # YOLO
    #         greeting = requests.get('http://localhost:18080/greeting', headers=headers).text
    #         print("\n"*20, greeting)
    #     except:
    #         print("Could not access greeting-service")
    #         greeting = "Hello %s" % username
    

    return ("""Processos: %s your email is %s and your user_id is %s!
               <ul>
                 <li><a href="/">Home</a></li>
                 <li><a href="//localhost:8082/auth/realms/camunda-platform/account?referrer=flask-app&referrer_uri=http://localhost:5000/private&">Account</a></li>
                </ul>""" %
            (str(processos_), email, user_id))


@app.route('/api', methods=['POST'])
@oidc.accept_token(require_token=True, scopes_required=['openid'])
def hello_api():
    """OAuth 2.0 protected API endpoint accessible via AccessToken"""
    return json.dumps({'hello': 'Welcome %s' % g.oidc_token_info['sub']})


@app.route('/logout')
def logout():
    info = oidc.user_getinfo(['preferred_username', 'email', 'sub'])
    username = info['preferred_username']
    logout_name(username)
    oidc.logout() # Performs local logout by removing the session cookie
    return f'{username}, you have been logged out! <a href="/">Return</a>'


if __name__ == '__main__':
    app.run(debug=True)