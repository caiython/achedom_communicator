import time
import requests
from . import deskmanager
from config import HOST, PORT, AUTO_UPDATE_DELAY

def update_data():
    while True:
        if deskmanager.auto_update_data == True:
            print('Auto Updating Data...')
            try:
                requests.post(f'http://{HOST}:{PORT}/update_data')
                print('Data Updated Successfully.')
            except requests.exceptions.RequestException as e:
                print(f"Erro ao enviar requisição: {e}")
        time.sleep(AUTO_UPDATE_DELAY)