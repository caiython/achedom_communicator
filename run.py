#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from requests.api import post
from html import unescape
from time import sleep
from datetime import datetime
from playsound import playsound
from os import system
from os import makedirs
from os.path import exists

class DeskManagerObject:
    
    # INICIA O OBJETO ATRAVÉS DA CHAVE DO OPERADOR E DA CHAVE DO AMBIENTE
    def __init__(self, chave_do_operador, chave_do_ambiente):
        url = r"https://api.desk.ms/Login/autenticar"
        resposta = post(url,
                        headers={"Authorization": chave_do_operador},
                        json={"PublicKey": chave_do_ambiente})
        self.api_token = resposta.json()
    
    # REALIZA UMA PESQUISA ATRAVÉS DOS DADOS INFORMADOS NA VARIÁVEL "PESQUISA"
    def pesquisa_chamados(self, pesquisa):
        url = r"https://api.desk.ms/ChamadosSuporte/lista"
        parametros = {
            "Pesquisa": pesquisa
        }
        resposta = post(url, json=parametros, headers={"Authorization": self.api_token}).json()['root']
        return resposta
    
    def dados_do_chamado(self, chave):
        url = r"https://api.desk.ms/ChamadosSuporte"
        parametros = {
            "Chave": chave
        }
        json = post(url, json=parametros, headers={"Authorization": self.api_token}).json()
        return json

# PRINTA COM A DATA E HORA ATUAL
def dhprint(text):
    now = datetime.now().strftime("[%d/%m/%Y - %H:%M:%S] ")
    print(now + str(text))
    return True

def txtmsg(novo_chamado, distribuicao_novo_chamado):
    txt = mensagem = f'''***** NOVO CHAMADO! *****

- DISTRIBUIÇÃO : {unescape(distribuicao_novo_chamado)}

- CÓDIGO: {unescape(novo_chamado['TChamado']['CodChamado'])}
- DATA: {datetime.strptime(unescape(novo_chamado['TChamado']['DataCriacao']), '%Y-%m-%d').strftime('%d/%m/%Y')}
- HORÁRIO: {unescape(novo_chamado['TChamado']['HoraCriacao'][:5])}
- USUÁRIO: {unescape(novo_chamado['TChamado']['CodUsuario'][0]['text'])}
- CLIENTE: {unescape(novo_chamado['TChamado']['CodCliente'][0]['text'])}
- PRIORIDADE: {unescape(novo_chamado['TChamado']['CodPrioridadeAtual'][0]['text'])}

- ASSUNTO: {unescape(novo_chamado['TChamado']['Assunto'])}

- DESCRIÇÃO:

{unescape(novo_chamado['TChamado']['Descricao'])}

*************************'''
    return txt

def main():
    
    # CABEÇALHO
    print("********** MONITOR DE ABERTURA DE CHAMADOS **********\n")
    print(f"SEJA BEM VINDO(A) AO MONITOR DE ABERTURA DE CHAMADOS.\n")
    
    # VALIDANDO CREDENCIAIS
    dhprint("INICIANDO...")

    # VERIFICA SE A PASTA "CHAMADOS" ESTÁ CRIADA E, SE NÃO ESTIVER, CRIA A MESMA.
    cpath = "chamados"
    if not exists(cpath):
        makedirs(cpath)

    # RESGATA AS CHAVES DO ARQUIVO KEYS.TXT
    credentials = open('keys.txt').read().split()

    # CHAVE DO OPERADOR
    chave_do_operador = credentials[1]
    if len(chave_do_operador) != 40:
        dhprint("CHAVE DO OPERADOR INCORRETA.\nVERIFIQUE O ARQUIVO \"CREDENTIALS.TXT\"")
        system('pause')
        return False
    else:
        dhprint("CHAVE DO OPERADOR DEFINIDA.")

    # CHAVE DO AMBIENTE
    chave_do_ambiente = credentials[3]
    if len(chave_do_ambiente) != 40:
        dhprint("CHAVE DO AMBIENTE INCORRETA.\nVERIFIQUE O ARQUIVO \"CREDENTIALS.TXT\"")
        system('pause')
        return False
    else:
        dhprint("CHAVE DO AMBIENTE DEFINIDA.")

    # CRIA O OBJETO DM
    try:
        dm = DeskManagerObject(chave_do_operador, chave_do_ambiente)
        dhprint("CONEXÃO COM A API DO DESK MANAGER ESTABELECIDA.")
    except:
        dhprint("HOUVE UM ERRO AO TENTAR CONECTAR COM A API DO DESK MANAGER")
        system('pause')
        return False

    # DEFINE A CHAVE PRIMÁRIA DO ÚLTIMO CHAMADO "LK.TXT"
    fpath = "src/lpk.key"
    if exists(fpath):
        lpk = int(open(fpath).read())
        dhprint("ÚLTIMA CHAVE PRIMÁRIA DE CHAMADO REGISTRADA: " + str(lpk) + '.')
    else:
        lpk = dm.pesquisa_chamados('')[0]['Chave']
        f = open(fpath, "a")
        f.write(str(lpk))
        f.close()
        dhprint("ÚLTIMA CHAVE PRIMÁRIA DE CHAMADO REGISTRADA: " + str(lpk) + '.')
        dhprint("MONITORANDO NOVOS CHAMADOS...")
    while True:
        try:
            dm = DeskManagerObject(chave_do_operador, chave_do_ambiente)
            novo_chamado = dm.dados_do_chamado(lpk+1)
            if novo_chamado != []:

                # ACRESCENTA UMA UNIDADE À ÚLTIMA CHAVE PRIMÁRIA DE CHAMADO REGISTRADA E REGISTRA O NOVO VALOR DA CHAVE PRIMÁRIA NO ARQUIVO
                lpk += 1 
                f = open(fpath, "w")
                f.write(str(lpk))
                f.close()

                # CASO SEJA IDENTIFICADA A CHAVE "ERRO", É EXIBIDA A MENSAGEM DE QUE A CHAVE DO OPERADOR É INEXISTENTE
                if "erro" in novo_chamado:
                    dhprint("ERRO: CHAVE DO OPERADOR INEXISTENTE")
                    dhprint("ENCERRANDO PROGRAMA...")
                    break

                # ATRIBUI O STATUS DO NOVO CHAMADO À VARIÁVEL "STATUS_NOVO_CHAMADO"
                status_novo_chamado = dm.pesquisa_chamados(f"{novo_chamado['TChamado']['CodChamado']}")[0]['NomeStatus']

                # SE O STATUS DO NOVO CHAMADO FOR "RESOLVIDO" OU "CANCELADO" É PULADO PARA O PRÓXIMO LOOP
                if (status_novo_chamado == "RESOLVIDO") or (status_novo_chamado == "CANCELADO"):
                    continue

                # ATRIBUI A DISTRIBUICAO DO NOVO CHAMADO À VARIÁVEL DISTRIBUICAO_NOVO_CHAMADO
                distribuicao_novo_chamado = dm.pesquisa_chamados(f"{novo_chamado['TChamado']['CodChamado']}")[0]['NomeOperador'] + ' ' + dm.pesquisa_chamados(f"{novo_chamado['TChamado']['CodChamado']}")[0]['SobrenomeOperador']

                # DEFINE A MENSAGEM DE TEXTO A PARTIR DOS DADOS DO NOVO CHAMADO NA VARIAVEL "MSG"
                msg = txtmsg(novo_chamado, distribuicao_novo_chamado)

                # ATRIBUI O CÓDIGO DO NOVO CHAMADO À VARIÁVEL "COD_NOVO_CHAMADO"
                cod_novo_chamado = novo_chamado['TChamado']['CodChamado']

                # CRIA UM ARQUIVO COM A MENSAGEM CONTENDO OS DADOS DO NOVO CHAMADO
                cf = open(cpath + '/' + cod_novo_chamado + '.txt', "a")
                cf.write(msg)
                cf.close()
                dhprint(f"NOVO CHAMADO REGISTRADO: {cod_novo_chamado}")

            # PAUSA DE 10 SEGUNDOS PARA NÃO SOBRECARREGAR BANCO COM PESQUISAS
            sleep(10)

        # QUALQUER OUTRA EXCEÇÃO É CLASSIFICADA COM CHAVE DO AMBIENTE INEXISTENTE.
        except:
            dhprint("ERRO: CHAVE DO AMBIENTE INEXISTENTE")
            dhprint("ENCERRANDO PROGRAMA...")
            break

    # PAUSA O PROGRAMA ANTES DELE SER FECHADO
    system('pause')
    remove("src/already.running")

if __name__ == '__main__':
    main()


# In[ ]:




