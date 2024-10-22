import psycopg2

def get_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="taskmanager",  # Nome do banco de dados
        user="postgres",  # Usuário do banco de dados
        password="atgdba11i",  # Senha do banco de dados
        port="5432"  # Porta padrão do PostgreSQL
    )
    return connection
