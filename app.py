from flask import Flask, jsonify, request, render_template
from database import get_connection

app = Flask(__name__)

#pagina inicial
@app.route('/')
def homepage():
    return render_template('index.html')  # Renderiza o arquivo HTML

# Endpoint: Registrar usuário
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nome_usuario = data['nome_usuario']
    email = data['email']
    senha = data['senha']

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO usuarios (nome_usuario, email, senha)
        VALUES (%s, %s, %s)
    """, (nome_usuario, email, senha))

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Usuário registrado com sucesso!'})

# Endpoint: Login de usuário
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nome_usuario = data['nome_usuario']
    senha = data['senha']

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM usuarios
        WHERE nome_usuario = %s AND senha = %s
    """, (nome_usuario, senha))
    
    usuario = cursor.fetchone()
    cursor.close()
    connection.close()

    if usuario:
        return jsonify({'message': 'Login bem-sucedido!'})
    else:
        return jsonify({'message': 'Credenciais inválidas!'}), 401

# Endpoint: Listar todas as tarefas
@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, titulo, descricao, data_entrega, status
        FROM tarefas
    """)
    tarefas = cursor.fetchall()
    
    tarefas_list = []
    for tarefa in tarefas:
        tarefas_list.append({
            'id': tarefa[0],
            'titulo': tarefa[1],
            'descricao': tarefa[2],
            'data_entrega': tarefa[3],
            'status': tarefa[4]
        })

    cursor.close()
    connection.close()

    return jsonify(tarefas_list)

# Endpoint: Criar nova tarefa
@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    data = request.get_json()
    titulo = data['titulo']
    descricao = data['descricao']
    data_entrega = data['data_entrega']
    id_professor = data['id_professor']
    id_aluno = data.get('id_aluno', None)  # Opcional

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tarefas (titulo, descricao, data_entrega, id_professor, id_aluno, status)
        VALUES (%s, %s, %s, %s, %s, 'Pendente')
    """, (titulo, descricao, data_entrega, id_professor, id_aluno))

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Tarefa criada com sucesso!'})

# Endpoint: Visualizar detalhes de uma tarefa
@app.route('/tarefas/<int:id>', methods=['GET'])
def detalhes_tarefa(id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, titulo, descricao, data_entrega, status
        FROM tarefas
        WHERE id = %s
    """, (id,))
    
    tarefa = cursor.fetchone()
    cursor.close()
    connection.close()

    if tarefa:
        return jsonify({
            'id': tarefa[0],
            'titulo': tarefa[1],
            'descricao': tarefa[2],
            'data_entrega': tarefa[3],
            'status': tarefa[4]
        })
    else:
        return jsonify({'message': 'Tarefa não encontrada'}), 404

# Endpoint: Marcar tarefa como concluída
@app.route('/tarefas/<int:id>/concluir', methods=['PUT'])
def concluir_tarefa(id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tarefas
        SET status = 'Concluída'
        WHERE id = %s
    """, (id,))

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Tarefa marcada como concluída!'})

# Endpoint: Deletar uma tarefa
@app.route('/tarefas/<int:id>', methods=['DELETE'])
def deletar_tarefa(id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM tarefas
        WHERE id = %s
    """, (id,))

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Tarefa deletada com sucesso!'})

# Endpoint: Atualizar uma tarefa
@app.route('/tarefas/<int:id>', methods=['PUT'])
def atualizar_tarefa(id):
    data = request.get_json()
    titulo = data['titulo']
    descricao = data['descricao']
    data_entrega = data['data_entrega']

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tarefas
        SET titulo = %s, descricao = %s, data_entrega = %s
        WHERE id = %s
    """, (titulo, descricao, data_entrega, id))

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Tarefa atualizada com sucesso!'})

# Iniciar a aplicação
if __name__ == '__main__':
    app.run(debug=True)
