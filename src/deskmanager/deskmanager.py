from requests.api import post
from .auxiliar_funcs import AuxiliarFunctions
from datetime import datetime
from dateutil.relativedelta import relativedelta

aux_funcs = AuxiliarFunctions()


class DeskManager:

    def __init__(self):
        self.operator_key = None
        self.ambient_key = None
        self.api_token = None
        self.auto_update_data = None

    def set_api_token(self, chave_do_operador, chave_do_ambiente):
        self.operator_key = chave_do_operador
        self.ambient_key = chave_do_ambiente
        api_response = post(r"https://api.desk.ms/Login/autenticar",
                            headers={"Authorization": self.operator_key},
                            json={"PublicKey": self.ambient_key})
        self.api_token = api_response.json()
        return 1

    # Realiza uma pesquisa através dos dados informados na variável "pesquisa"
    def service_order_search(self, search):
        parameters = {"Pesquisa": search}
        try:
            api_response = post(r"https://api.desk.ms/ChamadosSuporte/lista",
                                json=parameters,
                                headers={"Authorization": self.api_token}).json()['root']
        except KeyError:
            self.set_api_token(self.operator_key, self.ambient_key)
            api_response = post(r"https://api.desk.ms/ChamadosSuporte/lista",
                                json=parameters,
                                headers={"Authorization": self.api_token}).json()['root']
        return api_response

    # Retorna os dados de um chamado a partir de sua chave primária
    def service_order_data(self, service_order_key):
        parametros = {"Chave": service_order_key}
        api_response = post(r"https://api.desk.ms/ChamadosSuporte",
                            json=parametros,
                            headers={"Authorization": self.api_token}).json()
        return api_response

    def get_client_by_user_key(self, user_key):
        parametros = {"Chave": user_key}
        api_response = post(r"https://api.desk.ms/Usuarios",
                            json=parametros,
                            headers={"Authorization": self.api_token}).json()
        client = api_response['TUsuario']['Cliente'][0]['text']
        return client

    def new_service_order_code(self, service_order_code):
        prefix = service_order_code[:4]
        sufix = aux_funcs.adjust_sufix(str(int(service_order_code[5:]) + 1))
        new_service_order_code = prefix + "-" + sufix
        return new_service_order_code

    def next_date_service_order_code(self, last_service_order_code):
        current_date = datetime.strptime(last_service_order_code[:4], '%m%y')
        new_date = datetime.strftime(
            current_date + relativedelta(months=1), '%m%y')
        new_service_order_code = new_date + '-000001'
        return new_service_order_code
