# Monitor_de_Chamados
 Este programa é um monitor de abertura de novos chamados na plataforma Desk Manager.
 
 Introdução:
  Meu nome é Caio e este é meu primeiro programa consumindo uma API, tendo como ideia principal praticar este processo. O escolhido foi a API do DeskManager para solucionar um problema de comunicação entre os operadores da empresa que eu atuo através da padronização e agilidade na mensagem. Sou uma pessoa de mente aberta, realize críticas construtivas! Contato: caiocvlopes@gmail.com
 
 Objetivo:
  O objetivo deste programa é facilitar a comunicação com os operadores sobre a abertura de novos chamados através de informações padronizadas dos mesmos para serem copiadas para outras plataformas de mensagens. 
 
 Instruções:
  - Devem ser definidas as chaves de operador e de ambiente no arquivo "keys.txt";
  - A biblioteca playsound deve estar na versão 1.2.2 para funcionar corretamente;
 
 Funcionamento:
  Ao executar o software pela primeira vez, é comunicado com o banco de chamados do DeskManager através da API para resgatar a última chave primária de chamado registrada no banco. A partir disto, é feito uma verificação pelo programa a cada 10 segundos se uma nova chave foi gerada e, caso positivo, informações pertinentes são extraídas deste novo chamado e é salvo em um arquivo de texto na pasta "chamados" do programa.
 
 Melhorias:
  O programa poderia ser melhorado caso o envio das mensagens fosse feito de forma automática. A plataforma de mensagens utilizada pelos operadores é o Whatsapp, que infelizmente não oferece uma API eficiente para esse serviço, optando pela forma manual e estando aberto à soluções alternativas.
