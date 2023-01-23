from keycloak import KeycloakAdmin
from keycloak.exceptions import KeycloakPostError
import pprint as pp


keycloak_admin = KeycloakAdmin(server_url="http://localhost:18080/auth/",
                        username='admin',
                        password='admin',
                        realm_name="camunda-platform",
                        client_id="camunda-identity",
                        client_secret_key="5KsuHVUtLLUtXBvFyO4M74dGxqIxxo1W",
                        verify=True)


# Adicionar usuário
def add_user(): # TODO ajustar as entradas
    try:
        new_user = keycloak_admin.create_user({"email": "vivo.contratos@telefonica.com",
                                                "username": "vivo.contratos",
                                                "enabled": True,
                                                "firstName": "Vivo",
                                                "lastName": "Contratos",
                            "credentials": [{"value": "vivo123","type": "password",}]})
        return(new_user)
    except KeycloakPostError as e:
        erro = eval(e.response_body.decode())['errorMessage']
        return(erro)
        

def get_user_id(user_name):
    return keycloak_admin.get_user_id(user_name)


def logout_name(user_name):
    id=keycloak_admin.get_user_id(user_name)
    keycloak_admin.user_logout(id)


# pp.pprint(keycloak_admin.get_realm_roles_of_user(user_id=usuario))
