def build_whatsapp_message(service_order_data):
    message = f'''***** NOVO CHAMADO! *****

- DISTRIBUIÇÃO : {service_order_data[0]}

- CÓDIGO: {service_order_data[1]}
- DATA: {service_order_data[2]}
- HORÁRIO: {service_order_data[3]}
- USUÁRIO: {service_order_data[4]}
- CLIENTE: {service_order_data[5]}
- PRIORIDADE: {service_order_data[6]}

- ASSUNTO: {service_order_data[7]}

- DESCRIÇÃO:

{service_order_data[8]}

*************************
'''
    return message
