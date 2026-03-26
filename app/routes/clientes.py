from flask import Blueprint, request, jsonify
from app import db
from app.models import Cliente

clientes_bp = Blueprint('clientes',__name__,url_prefix='/clientes')

@clientes_bp.route('/', methods=['GET'])
def get_all_client():
    try:
        list_client = Cliente.query.all()

        output = []

        for user in list_client:
            output.append({
                'nome': user.nome,
                'telefone': user.telefone,
                'email': user.email,
                'total_visitas': len(user.agendamentos) if hasattr(user, 'agendamentos') else 0
            })

        return jsonify(output), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@clientes_bp.route('/novo', methods=['POST'])
def criar_cliente():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'requisição sem corpo JSON'}), 400

        nome = data.get('nome')
        telefone = data.get('telefone')
        email = data.get('email')
        senha = data.get('senha')
        # data_cadastro já preenche sozinho
        if not nome or not email or not telefone or not senha:
            return jsonify({'erro': 'Preencha todos os campos obrigatórios'}), 400 
        
        # criando novo_cliente via construtor
        novo_cliente = Cliente(nome=nome,telefone=telefone, email=email,senha=senha)
        
        # add cliente e salvando + menssagem de sucesso
        db.session.add(novo_cliente)
        db.session.commit()

        return jsonify({'message': 'cliente cadastrado com sucesso!', 'id': novo_cliente.id }), 201
    # caso dê errado, desfaz tudo
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500