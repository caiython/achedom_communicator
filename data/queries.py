CREATE_TABLE = 'CREATE TABLE chamados (id INTEGER PRIMARY KEY, cod_chamado INT NOT NULL, data TEXT, hora TEXT, usuario TEXT, cliente TEXT, prioridade TEXT, assunto TEXT, descricao TEXT, whatsapp INTEGER, distribuicao TEXT)'

FIRST_ENTRY = 'INSERT INTO chamados(cod_chamado) VALUES (?)'

SELECT_SERVICE_ORDERS = 'SELECT cod_chamado, distribuicao, assunto, data, hora, usuario, cliente, prioridade, whatsapp, id FROM chamados ORDER BY id DESC LIMIT ?, ?'

SELECT_SERVICE_ORDER_BY_CODE = 'SELECT distribuicao, cod_chamado, data, hora, usuario, cliente, prioridade, assunto, descricao FROM chamados WHERE cod_chamado = ?'

UPDATE_SERVICE_ORDER_WHATSAPP_STATUS_BY_CODE = 'UPDATE chamados SET whatsapp = 1 WHERE cod_chamado = ?'

SELECT_LAST_SERVICE_ORDER_CODE_BY_ID = 'SELECT cod_chamado FROM chamados ORDER BY ID DESC LIMIT 1'

INSERT_SERVICE_ORDER_INTO_DATABASE = 'INSERT INTO chamados(cod_chamado, data, hora, usuario, cliente, prioridade, assunto, descricao, distribuicao) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'

COUNT_TOTAL_SERVICE_ORDERS = 'SELECT COUNT(*) FROM chamados'

UPDATE_SERVICE_ORDER_DATA = 'UPDATE chamados SET data = ?, hora = ?, usuario = ?, cliente = ?, prioridade = ?, assunto = ?, descricao = ?, distribuicao = ? WHERE cod_chamado = ?'
