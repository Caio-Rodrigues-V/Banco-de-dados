import sqlite3

# Conectar ao banco (ele cria o arquivo se não existir)
conexao = sqlite3.connect('database/empresa.db')
cursor = conexao.cursor()

# Criar tabela pessoas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pessoas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cargo TEXT,
        cpf TEXT UNIQUE,
        email TEXT,
        celular TEXT,
        horario_entrada TEXT,
        horario_saida TEXT
    )
''')

# Criar tabela registros
cursor.execute('''
    CREATE TABLE IF NOT EXISTS registros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pessoa_id INTEGER NOT NULL,
        entrada DATETIME,
        saida DATETIME,
        FOREIGN KEY (pessoa_id) REFERENCES pessoas(id)
    )
''')
cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pessoa_id INTEGER,
    nome_funcionario TEXT,
    acao TEXT,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
);
               ''')

# Confirmar
conexao.commit()
conexao.close()

print("✅ Banco de dados e tabelas criados com sucesso!")
