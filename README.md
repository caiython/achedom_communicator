# Achedom Communicator 🚀

O `Achedom Communicator` é um aplicativo web desenvolvido em Python, utilizando Flask e Selenium, projetado para simplificar a comunicação entre a plataforma de ordens de serviço DeskManager e o aplicativo de mensagens WhatsApp. O objetivo principal do projeto é intermediar e facilitar a comunicação dos chamados abertos na plataforma, proporcionando uma experiência mais eficiente para os operadores.

## Funcionalidades 🛠️

Integração com o DeskManager: O Achedom Communicator se integra à plataforma de ordens de serviço DeskManager para obter e processar as informações dos chamados abertos.

Comunicação via WhatsApp: Utilizando automação por meio do Selenium, o aplicativo envia informações relevantes dos chamados diretamente para os operadores por meio do WhatsApp.

Armazenamento local em SQLite: Os dados dos chamados são armazenados de forma segura em um banco de dados local SQLite, garantindo confiabilidade e acesso rápido às informações.

## Requisitos do Sistema 🖥️

Certifique-se de ter o Python instalado na sua máquina.

Você pode instalar as dependências utilizando o arquivo requirements.txt fornecido no projeto.

```
pip install -r requirements.txt
```

## Configuração ⚙️

Para configurar o aplicativo, você pode acessar o arquivo config.py e adaptá-lo para o seu uso.

As configurações de usuário do WhatsApp e chave API de acesso ao DeskManager estão facilitadas na rota `/administrator` do aplicativo.

## Execução ▶️

Para iniciar o Achedom Communicator, execute o seguinte comando no terminal:

```
python main.py
```

O aplicativo estará disponível em http://localhost:5000 (alterável em `config.py`).

## Contribuições 🤝

Contribuições são bem-vindas! Se você encontrar problemas ou tiver sugestões de melhorias, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença 📜

Este projeto é distribuído sob a licença GNU General Public License (GPL). Consulte o arquivo LICENSE para obter mais informações.