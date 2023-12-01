from flask import Flask
from src.whatsapp import Whatsapp
from src.deskmanager import DeskManager
from os.path import exists
from config import DB_FILE
import sqlite3
from data.queries import CREATE_TABLE, FIRST_ENTRY

whatsapp = Whatsapp()
deskmanager = DeskManager()

def create_app():

    app = Flask(__name__)

    # Configurações da aplicação
    app.config['SECRET_KEY'] = '123456'
    app.config['DEBUG'] = True
    app.static_folder = 'static'

    # Registro das rotas
    from .routes.index import index_bp
    from .routes.admin import admin_bp
    from .routes.about import about_bp
    from .routes.terms_of_use import terms_of_use_bp
    from .routes.privacy_policy import privacy_policy_bp

    app.register_blueprint(index_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(terms_of_use_bp)
    app.register_blueprint(privacy_policy_bp)

    if not exists(DB_FILE):
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute(CREATE_TABLE)
            connection.commit()
            cod_primeiro_chamado = input('Foi identificado que é a primeira vez que você está executando o Achedom.\nInsira o código do último chamado registrado no DeskManager (formato xxxx-xxxxxx): ')
            cursor.execute(FIRST_ENTRY, (cod_primeiro_chamado,))
            connection.commit()
            cursor.close()

    return app