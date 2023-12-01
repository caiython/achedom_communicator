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


#######################################################################################################################


class DeskManagerObject:

    ###################################################################################################################
    
    # INICIA O OBJETO ATRAVÉS DA CHAVE DO OPERADOR E DA CHAVE DO AMBIENTE
    def __init__(self, chave_do_operador, chave_do_ambiente):
        url = r"https://api.desk.ms/Login/autenticar"
        resposta = post(url,
                        headers={"Authorization": chave_do_operador},
                        json={"PublicKey": chave_do_ambiente})
        self.api_token = resposta.json()

    ###################################################################################################################
    
    # REALIZA UMA PESQUISA ATRAVÉS DOS DADOS INFORMADOS NA VARIÁVEL "PESQUISA"
    def pesquisa_chamados(self, pesquisa):
        url = r"https://api.desk.ms/ChamadosSuporte/lista"
        parametros = {
            "Pesquisa": pesquisa
        }
        resposta = post(url, json=parametros, headers={"Authorization": self.api_token}).json()['root']
        return resposta

    ###################################################################################################################
    
    # RETORNA OS DADOS DE UM CHAMADO A PARTIR DE SUA CHAVE PRIMÁRIA
    def dados_do_chamado(self, chave):
        url = r"https://api.desk.ms/ChamadosSuporte"
        parametros = {
            "Chave": chave
        }
        json = post(url, json=parametros, headers={"Authorization": self.api_token}).json()
        return json

#######################################################################################################################


# APRESENTA O TEXTO NO CONSOLE COM A DATA E O HORÁRIO
def dhprint(text):
    now = datetime.now().strftime("[%d/%m/%Y - %H:%M:%S] ")
    print(now + str(text))
    return True

#######################################################################################################################


# DEFINE O TEXTO DO CHAMADO QUE DEVE SER ESCRITO NO ARQUIVO REFERENTE AO CHAMADO
def txtmsg(dados_novo_chamado, distribuicao_novo_chamado):
    txt = f'''***** NOVO CHAMADO! *****

- DISTRIBUIÇÃO : {unescape(distribuicao_novo_chamado)}

- CÓDIGO: {unescape(dados_novo_chamado['TChamado']['CodChamado'])}
- DATA: {datetime.strptime(unescape(dados_novo_chamado['TChamado']['DataCriacao']), '%Y-%m-%d').strftime('%d/%m/%Y')}
- HORÁRIO: {unescape(dados_novo_chamado['TChamado']['HoraCriacao'][:5])}
- USUÁRIO: {unescape(dados_novo_chamado['TChamado']['CodUsuario'][0]['text'])}
- CLIENTE: {unescape(dados_novo_chamado['TChamado']['CodCliente'][0]['text'])}
- PRIORIDADE: {unescape(dados_novo_chamado['TChamado']['CodPrioridadeAtual'][0]['text'])}

- ASSUNTO: {unescape(dados_novo_chamado['TChamado']['Assunto'])}

- DESCRIÇÃO:

{unescape(dados_novo_chamado['TChamado']['Descricao'])}

*************************'''
    return txt

#######################################################################################################################


# APRESENTA O CABEÇALHO DO SOFTWARE NO CONSOLE
def cabecalho():
    print("********** MONITOR DE ABERTURA DE CHAMADOS **********\n")
    print(f"SEJA BEM VINDO(A) AO MONITOR DE ABERTURA DE CHAMADOS.\n")
    dhprint("INICIANDO...")

#######################################################################################################################


# AJUSTA O SUFIXO DO CHAMADO PARA QUE OS DÍGITOS 0 À ESQUERDA SEJAM INCLUÍDOS EM SEU VALOR
def adjust_sufix(sufix):
    if len(sufix) == 5:
        new_sufix = "0" + sufix
    elif len(sufix) == 4:
        new_sufix = "00" + sufix
    elif len(sufix) == 3:
        new_sufix = "000" + sufix
    elif len(sufix) == 2:
        new_sufix = "0000" + sufix
    elif len(sufix) == 1:
        new_sufix = "00000" + sufix
    else:
        new_sufix = "000000"
    return new_sufix
        
#######################################################################################################################


def return_keys_oa(credentials):
    
    # FUNÇÃO PARA VERIFICAR SE HOUVE ERRO NA DEFINIÇÃO DAS CHAVES
    had_error = False
    
    # CHAVE DO OPERADOR
    chave_do_operador = credentials[1]
    if len(chave_do_operador) != 40:
        had_error = True
        dhprint("CHAVE DO OPERADOR INCORRETA.\nVERIFIQUE O ARQUIVO \"CREDENTIALS.TXT\"")
        system('pause')
    else:
        dhprint("CHAVE DO OPERADOR DEFINIDA.")
    
    # CHAVE DO AMBIENTE
    chave_do_ambiente = credentials[3]
    if len(chave_do_ambiente) != 40:
        had_error = True
        dhprint("CHAVE DO AMBIENTE INCORRETA.\nVERIFIQUE O ARQUIVO \"CREDENTIALS.TXT\"")
        system('pause')
    else:
        dhprint("CHAVE DO AMBIENTE DEFINIDA.")
        
    return chave_do_operador, chave_do_ambiente, had_error

#######################################################################################################################


def create_dm_object(chave_do_operador, chave_do_ambiente):
    
    had_error = False
    
    try:
        dm = DeskManagerObject(chave_do_operador, chave_do_ambiente)
        
        if dm.api_token == 'Prefixo Expirado ou não Existe':
            had_error = True
            
            dhprint("CHAVE DO AMBIENTE EXPIRADA OU INEXISTENTE. VERIFIQUE SE FOI DIGITADA CORRETAMENTE.")
            system('pause')
            
            return dm, had_error
        
        else:   

            dhprint("CONEXÃO COM A API DO DESK MANAGER ESTABELECIDA.")
            
            return dm, had_error
    
    except:
        
        had_error = True
        dm = False
        
        dhprint("HOUVE UM ERRO AO TENTAR CRIAR O OBJETO DO DESK MANAGER. RELATE O PROBLEMA AO PROGRAMADOR.")
        
        return dm, had_error
    
#######################################################################################################################


def get_lc_and_write_to_file(lcpath, dm):
    
    had_error = False
    
    try:
        lc = dm.pesquisa_chamados('')[0]['CodChamado']
        
    except:
        
        had_error = True
        
        dhprint("HOUVE UM ERRO AO TENTAR REALIZAR UMA PESQUISA NA LISTA DE CHAMADOS DO DESK MANAGER.")
        system('pause')
        
        return had_error
    
    f = open(lcpath, "w")
    f.write(str(lc))
    f.close()
    
    dhprint("ÚLTIMA CHAVE PRIMÁRIA DE CHAMADO REGISTRADA: " + str(lc) + '.')
    
    return had_error

#######################################################################################################################


def retorna_cod_novo_chamado(lc):
            
    prefix_cod_novo_chamado = lc[:4]
    sufix_cod_novo_chamado = adjust_sufix(str(int(lc[5:]) + 1))

    cod_novo_chamado = prefix_cod_novo_chamado + "-" + sufix_cod_novo_chamado
    
    return cod_novo_chamado
    
#######################################################################################################################


def lc_outdated(lc):

    mes_atual = datetime.now().strftime("%m")
    ano_atual = datetime.now().strftime("%Y")[2:]

    mes_gravado = lc[:2]
    ano_gravado = lc[2:4]

    if (mes_atual != mes_gravado) or (ano_atual != ano_gravado):
        dhprint("FOI IDENTIFICADO UMA ALTERAÇÃO NO MÊS OU NO ANO.")
        return True
    else:
        return False

#######################################################################################################################


# REDEFINE O ÚLTIMO CÓDIGO DE CHAMADO DO MÊS/ANO PARA O CÓDIGO 0
def update_lc(lcpath):

    mes_atual = datetime.now().strftime("%m")
    ano_atual = datetime.now().strftime("%Y")[2:]

    novo_cod_chamado = f'{mes_atual}{ano_atual}-000000'

    f = open(lcpath, "w")
    f.write(str(novo_cod_chamado))
    f.close()

    return novo_cod_chamado

#######################################################################################################################


def initial_params(cpath="chamados", oa_keys='keys.txt', lcpath="src/lc.key"):

    # VERIFICA SE A PASTA "CHAMADOS" ESTÁ CRIADA E, SE NÃO ESTIVER, CRIA A MESMA.
    if not exists(cpath):
        makedirs(cpath)

    # RESGATA AS CHAVES DO ARQUIVO KEYS.TXT
    if not exists(oa_keys):
        dhprint(f"O ARQUIVO \"{oa_keys}\" NÃO FOI ENCONTRADO")
        return False
    else:
        credentials = open(oa_keys).read().split()

    # DEFINE AS CHAVES DO OPERADOR E DO AMBIENTE A PARTIR DO ARQUIVO KEYS.TXT.
    # CASO UM ERRO SEJA IDENTIFICADO O PROGRAMA IRÁ ALERTAR E PARAR A EXECUÇÃO.
    chave_do_operador, chave_do_ambiente, had_error = return_keys_oa(credentials)
    if had_error:
        return False

    # CRIA O OBJETO DM.
    # CASO UM ERRO SEJA IDENTIFICADO O PROGRAMA IRÁ ALERTAR E PARAR A EXECUÇÃO.
    dm, had_error = create_dm_object(chave_do_operador, chave_do_ambiente)
    if had_error:
        return False

    # BUSCA O ÚLTIMO CHAMADO ABERTO NO DESK MANAGER, GRAVA O SEU CÓDIGO NA VARIÁVEL LC E NO ARQUIVO INFORMADO NO
    # PARÂMETRO ("LC.KEY"). CASO UM ERRO SEJA IDENTIFICADO O PROGRAMA IRÁ ALERTAR E PARAR A EXECUÇÃO.
    had_error = get_lc_and_write_to_file(lcpath, dm)
    if had_error:
        return False

    # APRESENTA A MENSAGEM NO CONSOLE INDICANDO O INÍCIO DO MONITORAMENTO DE NOVOS CHAMADOS
    dhprint("MONITORANDO NOVOS CHAMADOS...")

    return dm

#######################################################################################################################


# INICIA O PROGRAMA
def main():
    
    # CABEÇALHO.
    cabecalho()
    
    # DEFINE OS CAMINHOS PARA AS PASTAS E ARQUIVOS.
    cpath = "chamados"
    oa_keys = 'keys.txt'
    lcpath = "src/lc.key"
    
    # INSERE OS PARÂMETROS DE ENTRADA PARA RESGATAR O OBJETO DESK MANAGER
    dm = initial_params(cpath, oa_keys, lcpath)

    if not dm:
        return False
    
    while True:
        
        try:

            # ATRIBUI À VARIÁVEL LC O ÚLTIMO CÓDIGO DE CHAMADO GRAVADO NO CAMINHO DO ARQUIVO ESPECIFICADO EM LCPATH
            lc = open(lcpath).read()

            # REESCREVE O ÚLTIMO CÓDIGO DE CHAMADO NO ARQUIVO CASO A DATA OU O MÊS ESTEJAM DIFERENTES DA DATA ATUAL
            # DO COMPUTADOR
            if lc_outdated(lc):
                lc = update_lc(lcpath)
            
            # RETORNA O CÓDIGO DO NOVO CHAMADO QUE DEVE SER PROCURADO
            cod_novo_chamado = retorna_cod_novo_chamado(lc)
            
            # VERIFICA NA LISTA DE CHAMADOS SE O CÓDIGO DO NOVO CHAMADO EXISTE
            lista_de_chamados = dm.pesquisa_chamados(cod_novo_chamado)
            
            # VERIFICA SE HOUVE ALGUM ERRO DURANTE A PESQUISA
            if "erro" in lista_de_chamados:
                if lista_de_chamados["erro"] == 'Token do operador não existe':
                    dhprint("ERRO: CHAVE DO OPERADOR INEXISTENTE")
                    dhprint("ENCERRANDO PROGRAMA...")
                    break
                else:
                    dhprint(lista_de_chamados["erro"])
                    dhprint("ENCERRANDO PROGRAMA...")
                    break
            
            # VERIFICA SE EXISTE ALGUM CHAMADO NA LISTA DE CHAMADOS PESQUISADA. CASO POSITIVO, SIGNIFICA QUE EXISTE UM
            # CHAMADO COM O NOVO CÓDIGO DE CHAMADO PESQUISADO, DANDO SEQUÊNCIA À UMA SÉRIE DE COMANDOS.
            elif len(lista_de_chamados) > 0:
                
                # SOBRESCREVE O CÓDIGO GRAVADO NO ARQUIVO DESCRITO EM LCPATH COM O ÚLTIMO CÓDIGO ENCONTRADO NA LISTA
                f = open(lcpath, "w")
                f.write(str(cod_novo_chamado))
                f.close()
                
                # ATRIBUI O PRIMEIRO RESULTADO DA LISTA DE CHAMADOS À VARIÁVEL
                novo_chamado = lista_de_chamados[0]
                
                # GRAVA A CHAVE PRIMARIA DO NOVO CHAMADO NA VARIÁVEL
                chave_primaria_novo_chamado = novo_chamado['Chave']
                
                # RESGATA OS DADOS DO NOVO CHAMADO A PARTIR DE SUA CHAVE PRIMÁRIA E ATRIBUI À VARIÁVEL
                dados_novo_chamado = dm.dados_do_chamado(chave_primaria_novo_chamado)
                
                # ATRIBUI O STATUS DO NOVO CHAMADO À VARIÁVEL "STATUS_NOVO_CHAMADO"
                # SE O STATUS DO NOVO CHAMADO FOR "RESOLVIDO" OU "CANCELADO" É PULADO PARA O PRÓXIMO LOOP
                status_novo_chamado = novo_chamado['NomeStatus']
                if (status_novo_chamado == "RESOLVIDO") or (status_novo_chamado == "CANCELADO"):
                    continue
                    
                # ATRIBUI A DISTRIBUICAO DO NOVO CHAMADO À VARIÁVEL DISTRIBUICAO_NOVO_CHAMADO
                distribuicao_novo_chamado = novo_chamado['NomeOperador'] + ' ' + novo_chamado['SobrenomeOperador']
                
                # DEFINE A MENSAGEM DE TEXTO A PARTIR DOS DADOS DO NOVO CHAMADO NA VARIAVEL "MSG"
                msg = txtmsg(dados_novo_chamado, distribuicao_novo_chamado)
                
                # CRIA UM ARQUIVO COM A MENSAGEM CONTENDO OS DADOS DO NOVO CHAMADO
                cf_name = cod_novo_chamado + '-' + distribuicao_novo_chamado.replace(' ', '_')
                cf = open(cpath + '/' + cf_name + '.txt', "a")
                cf.write(msg)
                cf.close()
                
                # APRESENTA NO CONSOLE O NOVO CHAMADO REGISTRADO COM O CÓDIGO E A DISTRIBUIÇÃO FORMATADA
                dhprint(f"NOVO CHAMADO REGISTRADO: {cod_novo_chamado}-{distribuicao_novo_chamado.replace(' ', '_')}")
            
            # AGUARDA 10 SEGUNDOS ANTES DA PRÓXIMA VERIFICAÇÃO
            sleep(10)
            
        # CASO ACONTEÇA QUALQUER EXCEÇÃO, OS PARÂMETRO INICIAIS SÃO REDEFINIDOS.
        except:
            
            # INFORMA NO CONSOLE QUE HOUVE UM ERRO E ENTÃO AGUARDA 1 MINUTO
            dhprint("OCORREU UM ERRO AO TENTAR REALIZAR A BUSCA DE UM NOVO CHAMADO. TENTANDO NOVAMENTE EM 1 MINUTO...")
            sleep(60)

            # REINSERE OS PARÂMETROS DE ENTRADA PARA RESGATAR O OBJETO DESK MANAGER
            dm = initial_params(cpath, oa_keys, lcpath)


if __name__ == '__main__':
    main()
    system('pause')
