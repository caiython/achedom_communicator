from config import DB_FILE
from data.queries import SELECT_SERVICE_ORDERS, SELECT_SERVICE_ORDER_BY_CODE, UPDATE_SERVICE_ORDER_WHATSAPP_STATUS_BY_CODE, SELECT_LAST_SERVICE_ORDER_CODE_BY_ID, INSERT_SERVICE_ORDER_INTO_DATABASE, COUNT_TOTAL_SERVICE_ORDERS, UPDATE_SERVICE_ORDER_DATA
from flask import Blueprint, render_template, request, redirect
from html import unescape
from datetime import datetime
from math import ceil
import sqlite3
from app import whatsapp
from app import deskmanager


index_bp = Blueprint('index', __name__)


def get_latest_service_orders(page, per_page=5):
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        offset = (page-1) * per_page
        cursor.execute(SELECT_SERVICE_ORDERS, (offset, per_page))
        data = cursor.fetchall()
        cursor.execute(COUNT_TOTAL_SERVICE_ORDERS)
        total_records = cursor.fetchone()[0]
        total_pages = ceil(total_records / per_page)
    return data, total_pages


def send_whatsapp_message_and_update_service_order_whatsapp_status(cod_chamado):

    service_order_search = deskmanager.service_order_search(cod_chamado)
    service_order_data = service_order_search[0]
    new_service_order_data = process_service_order_data(service_order_data)

    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute(UPDATE_SERVICE_ORDER_DATA,(
            new_service_order_data['data'],
            new_service_order_data['hora'],
            new_service_order_data['usuario'],
            new_service_order_data['cliente'],
            new_service_order_data['prioridade'],
            new_service_order_data['assunto'],
            new_service_order_data['descricao'],
            new_service_order_data['distribuicao'],
            new_service_order_data['cod_chamado'],
            )
        )
        connection.commit()

    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_SERVICE_ORDER_BY_CODE, (cod_chamado,))
        service_order_data = cursor.fetchone()
        cursor.execute(
            UPDATE_SERVICE_ORDER_WHATSAPP_STATUS_BY_CODE, (cod_chamado,))
        connection.commit()
    message = whatsapp.build_message(service_order_data)
    whatsapp.send_message(message)
    return 1


def update_service_order_database(whatsapp_auto_send):
    while (True):
        last_service_order_code = get_last_service_order_from_database()
        new_service_order_code = deskmanager.new_service_order_code(
            last_service_order_code)
        search_result = deskmanager.service_order_search(
            new_service_order_code)
        if len(search_result) == 0:
            next_date_service_order_code = deskmanager.next_date_service_order_code(
                last_service_order_code)
            search_result = deskmanager.service_order_search(
                next_date_service_order_code)
            if len(search_result) == 0:
                break
            else:
                new_service_order_data = search_result[0]
                processed_new_service_order_data = process_service_order_data(
                    new_service_order_data)
                insert_service_order_into_database(
                    processed_new_service_order_data)
                
        else:
            new_service_order_data = search_result[0]
            processed_new_service_order_data = process_service_order_data(
                new_service_order_data)
            insert_service_order_into_database(
                processed_new_service_order_data)
            
        if whatsapp_auto_send:
            send_whatsapp_message_and_update_service_order_whatsapp_status(
                cod_chamado=processed_new_service_order_data['cod_chamado'])
    return 1


def get_last_service_order_from_database():
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_LAST_SERVICE_ORDER_CODE_BY_ID)
        last_service_order_code = cursor.fetchone()[0]
    return last_service_order_code


def insert_service_order_into_database(service_order):
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute(
            INSERT_SERVICE_ORDER_INTO_DATABASE, (
                service_order['cod_chamado'],
                service_order['data'],
                service_order['hora'],
                service_order['usuario'],
                service_order['cliente'],
                service_order['prioridade'],
                service_order['assunto'],
                service_order['descricao'],
                service_order['distribuicao'],
            )
        )
        connection.commit()
    return 1


def process_service_order_data(service_order_data):
    processed_service_order_data = {
        'cod_chamado': service_order_data['CodChamado'],
        'data': datetime.strptime(service_order_data['DataCriacao'], '%Y-%m-%d').strftime('%d/%m/%Y'),
        'hora': service_order_data['HoraCriacao'][:5],
        'usuario': service_order_data['NomeUsuario'] + ' ' + service_order_data['SobrenomeUsuario'],
        'cliente': deskmanager.get_client_by_user_key(service_order_data['ChaveUsuario']),
        'prioridade': service_order_data['NomePrioridade'],
        'assunto': service_order_data['Assunto'],
        'descricao': unescape(service_order_data['Descricao']),
    }

    if 'NomeOperador' in service_order_data:
        processed_service_order_data['distribuicao'] = service_order_data['NomeOperador'] + ' ' + service_order_data['SobrenomeOperador']
    else:
        processed_service_order_data['distribuicao'] = 'SERVICE DESK'

    return processed_service_order_data


@index_bp.route('/')
def index():
    page = int(request.args.get('page', 1))
    data, total_pages = get_latest_service_orders(page)
    return render_template('index.html', page=page, total_pages=total_pages, chamados=data, whatsapp_running=whatsapp.running, deskmanager_api_token=deskmanager.api_token, current_year=datetime.now().year)


@index_bp.route('/send_button', methods=['POST'])
def send_button():
    send_whatsapp_message_and_update_service_order_whatsapp_status(
        cod_chamado=request.form['botao'])
    return redirect(request.referrer)


@index_bp.route('/update_data', methods=['POST'])
def update_data():
    update_service_order_database(whatsapp.auto_send)
    return redirect(request.referrer)
