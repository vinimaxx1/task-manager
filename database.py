import psycopg2
from psycopg2 import sql

def get_connection():
    connection = psycopg2.connect(
        host="localhost",  # Altere se o servidor for diferente
        database="task_manager_db",
        user="seu_usuario",
        password="sua_senha"
    )
    return connection

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # Criação das tabelas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professores (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            senha VARCHAR(100)
        );
        
        CREATE TABLE IF NOT EXISTS alunos (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            senha VARCHAR(100)
        );
        
        CREATE TABLE IF NOT EXISTS tarefas (
            id SERIAL PRIMARY KEY,
            titulo VARCHAR(255),
            descricao TEXT,
            data_entrega DATE,
            status VARCHAR(50),
            id_professor INT REFERENCES professores(id),
            id_aluno INT REFERENCES alunos(id)
        );
    """)
    
    connection.commit()
    cursor.close()
    connection.close()
