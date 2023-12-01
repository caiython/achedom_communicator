from flask import Blueprint, render_template, request, redirect
from app import whatsapp
from app import deskmanager
from zipfile import ZipFile
import os
from shutil import rmtree

admin_bp = Blueprint('admin', __name__)

def check_uploaded_file_name(file):
    if file.filename == '':
        return False
    else:
        return True

@admin_bp.route('/administrator')
def administrator():
    return render_template('admin.html',
                           whatsapp_running=whatsapp.running,
                           deskmanager_apitoken=False if deskmanager.api_token is None else True,
                           target_user=whatsapp.target_user,
                           whatsapp_send_mode = 'Envio Automático' if whatsapp.auto_send else 'Envio Manual',
                           deskmanager_update_mode = 'Atualização Automática' if deskmanager.auto_update_data else 'Atualização Manual')

@admin_bp.route('/admin/whatsapp', methods=['POST'])
def admin_whatsapp():
    botao_clicado = request.form['botao']

    if botao_clicado == 'enviar_arquivo':
        file = request.files['file']
        if file.filename == '':
            return redirect(request.referrer)
        if file:
            if not os.path.exists('uploads'):
                os.makedirs('uploads')
            file.save(os.path.join('uploads', file.filename))
            if os.path.exists('uploads/User Data'):
                rmtree('uploads/User Data')
            with ZipFile(os.path.join('uploads', file.filename), 'r') as zip_ref:
                for member in zip_ref.infolist():
                    if member.filename.startswith('User Data' + '/'):
                        zip_ref.extract(member, 'uploads')
            os.remove(os.path.join('uploads', file.filename))
            return redirect(request.referrer)

    elif botao_clicado == 'iniciar' and whatsapp.running == False:
        modo = request.form.get('auto-or-manual')
        if modo == 'automatico':
            whatsapp.start(request.form['target_user'])
            whatsapp.running = True
            whatsapp.auto_send = True
        else:
            whatsapp.start(request.form['target_user'])
            whatsapp.running = True
            whatsapp.auto_send = False

    elif botao_clicado == 'parar' and whatsapp.running == True:
        whatsapp.stop()
        whatsapp.running = False
    return redirect(request.referrer)

@admin_bp.route('/admin/deskmanager', methods=['POST'])
def admin_deskmanager():
    botao_clicado = request.form['botao']
    modo = request.form.get('auto-or-manual')
    if botao_clicado == 'iniciar' and deskmanager.api_token is None:
        if modo == 'automatico':
            deskmanager.auto_update_data = True
            deskmanager.set_api_token(request.form['operator_key'], request.form['ambient_key'])
            return redirect(request.referrer)
        else:
            deskmanager.auto_update_data = False
            deskmanager.set_api_token(request.form['operator_key'], request.form['ambient_key'])
            return redirect(request.referrer)
    else:
        deskmanager.auto_update_data = None
        deskmanager.api_token = None
        return redirect(request.referrer)