from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from os import getlogin
from pyperclip import copy
from config import USER_DATA
import os


class Whatsapp():

    def __init__(self):
        
        self.whatsapp_web_url='https://web.whatsapp.com/'
        self.target_user = None
        self.running=False
        self.driver=None
        self.wait=None
        self.auto_send=None

    def start(self, target_user):

        if self.running==False:

            user_data_dir = str(os.getcwd()).replace('\\', r'\/') + USER_DATA
            chrome_options = Options()
            chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
            chrome_options.add_experimental_option("detach", True)

            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.get(self.whatsapp_web_url)
            self.wait = WebDriverWait(self.driver, 100)
            self.target_user = target_user
            self.running=True

        return
    
    def stop(self):

        # Fecha o navegador
        if self.running==True:
            self.target_user = None
            self.driver.quit()
            self.running=False

        return

    def send_message(self, text):

        if self.running==True:
            
            # Copia o texto a ser enviado para a área de transferência
            copy(text)

            # Seleciona o contato através do nome (contact_name).
            contact_path = '//span[contains(@title,"' + self.target_user + '")]'
            contact=self.wait.until(EC.presence_of_element_located((By.XPATH, contact_path)))
            contact.click()

            # Envia a mensagem (text) ao contato selecionado.
            message_box_path = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'
            message_box=self.wait.until(EC.presence_of_element_located((By.XPATH, message_box_path)))
            message_box.send_keys(Keys.CONTROL, 'v')
            message_box.send_keys(Keys.ENTER)

        return
    
    def build_message(self, service_order_data):
        from .message_builder import build_whatsapp_message
        return build_whatsapp_message(service_order_data)