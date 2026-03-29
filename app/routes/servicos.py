from flask import Blueprint, request,jsonify
from app import db
from app.models import Servico

servicos_bp = Blueprint('servicos', __name__,url_prefix='/servicos')

@servicos_bp.route('/', methods=['GET'])
def get_all_services():
    try:
        list_services = Servico.query.all()

        output = []

        for service in list_services:
            output.append({
                'id': service.id,
                'nome': service.nome,
                'preco': service.preco,
                'duracao_estimada': service.duracao_estimada
            })
        return jsonify(output), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@servicos_bp.route('/novo', methods=['POST'])
def create_service():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'requisição sem corpo JSON'}), 400
        
        nome = data.get('nome')
        servico_nome = Servico.query.filter_by(nome=nome).first()
        # evitar nome duplicado de serviço
        if servico_nome:
            return jsonify({'error': 'Serviço já cadastrado!'}), 409
        
        nome = data.get('nome')
        preco = data.get('preco')
        duracao_estimada = data.get('duracao_estimada',0)

        if not nome or not preco:
            return jsonify({'error': 'Preencha os campos de nome e preço'}), 400
        
        # criando novo_serviço via construtor
        novo_servico = Servico(nome=nome,preco=preco,duracao_estimada=duracao_estimada)

        # add e salvando + mensagem de sucesso
        db.session.add(novo_servico)
        db.session.commit()
        return jsonify({'message': 'serviço cadastrado com sucesso!'}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@servicos_bp.route('/<int:id>', methods=['GET'])
def get_specific_services(id):
    try:
        service = Servico.query.get_or_404(id)
        return jsonify({
            'id': service.id,
            'nome': service.nome,
            'preco': service.preco,
            'duracao_estimada': service.duracao_estimada}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@servicos_bp.route('/<int:id>', methods=['PUT'])
def put_specific_services(id):
    try:
        service = Servico.query.get_or_404(id)
        data = request.get_json()

        novo_servico = data.get('nome')
        if novo_servico and novo_servico != service.nome:
            #filtra se o nome de serviço já existe
            existe_servico = Servico.query.filter_by(nome=novo_servico).first()
            if existe_servico:
                return jsonify({'error': 'Serviço já possui cadastro'}), 409
        
        service.nome = novo_servico if novo_servico else service.nome
        service.preco = data.get('preco', service.preco)
        service.duracao_estimada = data.get('duracao_estimada', service.duracao_estimada)

        db.session.commit()
        return jsonify({'message': 'Serviço atualizado com sucesso!'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@servicos_bp.route('/<int:id>', methods=['DELETE'])
def delete_specific_service(id):
    try:
        user = Servico.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Serviço removido com sucesso!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
    # add id nos gets (esqueci) :( 