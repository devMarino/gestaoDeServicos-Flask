from flask import Blueprint,request,jsonify
from app import db
from app.models import Agendamento,AtendimentoItem, Servico
from datetime import datetime

agendamentos_bp = Blueprint('agendamentos',__name__,url_prefix='/agendamentos')

@agendamentos_bp.route('/', methods=['GET'])
def get_schedules():
    try:
        hoje = datetime.now().date()
        list_agendamentos = Agendamento.query.filter(db.func.date(Agendamento.data_hora) == hoje).all()
        output = []
        
        for agendamento in list_agendamentos:
            #pega o agendamento completo + serviços  
            dados = {
                'id': agendamento.id,
                'data_hora': agendamento.data_hora.strftime('%Y-%m-%d %H:%M:%S'),
                'cliente': agendamento.cliente.nome,
                'funcionario_id': agendamento.funcionario_id,
                'status': agendamento.status.value,
                'servicos': []
            }
            
            #pega serviço de cada atendimento da tabela
            for item in agendamento.itens_atendimento:
                dados['servicos'].append({
                    'nome': item.servico.nome,
                    'valor': str(item.valor_aplicado)
                })
                
            output.append(dados)
        return jsonify(output), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@agendamentos_bp.route('/novo', methods=['POST'])
def create_schedule():
    try:
        data = request.get_json()
        data_agendamento = datetime.strptime(data['data_hora'], '%Y-%m-%d %H:%M:%S')
        # verifica horário de agendamento
        conflito = Agendamento.query.filter_by(
        funcionario_id=data['funcionario_id'],
        data_hora=data_agendamento).first()

        if conflito:
            return jsonify({'error': 'Este barbeiro já possui um agendamento neste horário'}), 400
    # cria novo agendamento
        novo_agendamento = Agendamento(
            data_hora=datetime.strptime(data['data_hora'], '%Y-%m-%d %H:%M:%S'),
            cliente_id=data['cliente_id'],
            funcionario_id=data['funcionario_id']            
    )
        
        db.session.add(novo_agendamento)
        # flush reserva o proximo id do banco de dados
        db.session.flush()
    # cria novo Item do atendimento 
        for item in data['servicos']:
            servico_original = Servico.query.get(item['id'])

            if not servico_original:
                db.session.rollback()
                return jsonify({'error': f'Serviço ID: {item['id']} não encontrado'}), 404
            
            novo_item = AtendimentoItem(
            agendamento_id=novo_agendamento.id,
            servico_id = servico_original.id,
            valor_aplicado=servico_original.preco
        )
            db.session.add(novo_item)
        db.session.commit()
        
        return jsonify({'status': 'sucesso', 'agendamento_id': novo_agendamento.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@agendamentos_bp.route('/<int:id>/status', methods=['PATCH'])
def update_status(id):
    try:
        agendamento = Agendamento.query.get_or_404(id)
        data = request.get_json()
        
        # O status = PENDENTE|CONCLUIDO|CANCELADO|AUSENTE
        novo_status = data.get('status').upper()

        if not novo_status:
            db.session.rollback()
            return jsonify({'error': 'status não informado'}), 400
        
        agendamento.status = novo_status
        db.session.commit()

        return jsonify({'message': f'Status do agendamento {id} atualizado para {novo_status}'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'status inválido ou erro do servidor'}), 400
    
@agendamentos_bp.route('/<int:id>', methods=['DELETE'])
def delete_schedule(id):
    try:
        agendamento = Agendamento.query.get_or_404(id)
        db.session.delete(agendamento)
        db.session.commit()
        return jsonify({'message': f'Agendamento {id} e seus itens foram removidos com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500