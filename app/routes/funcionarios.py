from flask import Blueprint,jsonify,request
from app import db
from app.models import Funcionario, StatusFuncionario

funcionarios_bp = Blueprint('funcionarios',__name__)

@funcionarios_bp.route('/', methods=['GET'])
def get_employees():
    try:
        search_name = request.args.get('nome')
        query = Funcionario.query

        if search_name:
            query = query.filter(Funcionario.nome.ilike(f'%{search_name}%'))

        list_employees = query.all()

        output = []

        for user in list_employees:
            output.append({
                'id': user.id,
                'nome': user.nome,
                'especialidade': user.especialidade,
                'status': user.status.value
            })
        return jsonify(output), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@funcionarios_bp.route('/novo', methods=['POST'])
def create_employees():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'requisição sem corpo JSON'}), 400
        
        nome = data.get('nome')
        especialidade = data.get('especialidade')
        # status já vem inativo por padrão (models.py)
        if not nome:
            return jsonify({'error': 'preencha todos os campos obrigatórios!'}), 400
        
        novo_funcionario = Funcionario(nome=nome,especialidade=especialidade)

        db.session.add(novo_funcionario)
        db.session.commit()
        return jsonify({'message': 'funcionario criado com sucesso!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@funcionarios_bp.route('/<int:id>', methods=['GET'])
def get_specific_employee(id):
    try:
        user = Funcionario.query.get_or_404(id)

        return jsonify({
            'id': user.id,
            'nome': user.nome,
            'especialidade': user.especialidade,
            'status': user.status.value
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@funcionarios_bp.route('/<int:id>/status', methods=['PATCH'])
def update_status(id):
    try:
        funcionario = Funcionario.query.get_or_404(id)
        data = request.get_json()
        novo_status = data.get('status')

        if not novo_status:
            return jsonify({'error': 'Você precisa informar o novo status'}), 400

        try:
            # ATIVO / INATIVO -> precisa do upper()
            funcionario.status = StatusFuncionario[novo_status.upper()]
        except KeyError:
            return jsonify({'error': f'Status "{novo_status}" é inválido'}), 400

        db.session.commit()
        
        return jsonify({
            'message': f'Funcionario {funcionario.nome}', 'status_atual': funcionario.status.value}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
