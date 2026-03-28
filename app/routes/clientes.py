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
def create_client():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'requisição sem corpo JSON'}), 400
        
        email = data.get('email')
        user_email = Cliente.query.filter_by(email=email).first()
        # evita duplicata de email
        if user_email:
            return jsonify({'erro': 'Email já cadastrado!'}), 409
        nome = data.get('nome')
        telefone = data.get('telefone')
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
    
@clientes_bp.route('/<int:id>', methods=['GET'])
def get_specific_client(id):
    try:
        # get_or_404  = se o id não existir, o flask retorna 404 not found
        user = Cliente.query.get_or_404(id)
        return jsonify({
            'id': user.id,
            'nome': user.nome,
            'email': user.email,
            'telefone': user.telefone}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@clientes_bp.route('/<int:id>', methods=['PUT'])
def put_specific_client(id):
    try:
        user = Cliente.query.get_or_404(id)
        data = request.get_json()

        novo_email = data.get('email')

        if novo_email and novo_email != user.email:
            # filtra se email já possui cadastro
            email_existe = Cliente.query.filter_by(email=novo_email).first()
            if email_existe:
                return jsonify({'error':'E-mail já possui cadastro'}), 409
            
        user.nome = data.get('nome', user.nome)
        user.email = novo_email if novo_email else user.email
        
        user.telefone = data.get('telefone', user.telefone)
        
        db.session.commit()
        return jsonify({'message': 'Cliente atualizado com sucesso!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@clientes_bp.route('/<int:id>', methods=['DELETE'])
def delete_specific_client(id):
    try:
        user = Cliente.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'cliente removido com sucesso!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500