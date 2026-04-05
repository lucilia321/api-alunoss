from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'alunoss.json'

def ler_dados():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def salvar_dados(dados):
    with open(DATA_FILE, 'w') as f:
        json.dump(dados, f, indent=4)

@app.route('/alunoss', methods=['POST'])
def cadastrar_aluno():
    aluno = request.get_json()
    dados = ler_dados()
    aluno['id'] = len(dados) + 1
    dados.append(aluno)
    salvar_dados(dados)
    return jsonify(aluno), 201

@app.route('/alunoss', methods=['GET'])
def listar_alunos():
    dados = ler_dados()
    return jsonify(dados)

@app.route('/alunoss/<int:id>', methods=['PUT'])
def atualizar_aluno(id):
    dados = ler_dados()
    novo_aluno = request.get_json()
    for aluno in dados:
        if aluno['id'] == id:
            aluno.update(novo_aluno)
            salvar_dados(dados)
            return jsonify(aluno)
    return jsonify({'erro': 'Aluno não encontrado'}), 404

@app.route('/alunoss/<int:id>', methods=['DELETE'])
def deletar_aluno(id):
    dados = ler_dados()
    for aluno in dados:
        if aluno['id'] == id:
            dados.remove(aluno)
            salvar_dados(dados)
            return jsonify({'mensagem': 'Aluno removido'})
    return jsonify({'erro': 'Aluno não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
