from app import db
from datetime import datetime, timezone
import enum

class StatusAgendamento(enum.Enum):
    PENDENTE = 'PENDENTE'
    CONCLUIDO = 'CONCLUIDO'
    CANCELADO = 'CANCELADO'
    AUSENTE = 'AUSENTE'

class StatusFuncionario(enum.Enum):
    ATIVO = 'Ativo'
    INATIVO = 'Inativo'
    
class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(320), nullable=False, unique=True)
    senha = db.Column(db.String(128),nullable=False)
    data_cadastro = db.Column(db.Date, default=lambda: datetime.now(timezone.utc), nullable=False)

    agendamentos = db.relationship('Agendamento', backref='cliente', lazy=True)
class Funcionario(db.Model):
    __tablename__ = 'funcionarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    especialidade = db.Column(db.String(500), nullable=True)
    status = db.Column(db.Enum(StatusFuncionario), default=StatusFuncionario.INATIVO, nullable=False)

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(StatusAgendamento), default=StatusAgendamento.PENDENTE,nullable=False)

    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)

class AtendimentoItem(db.Model):
    __tablename__ = 'atendimento_itens'
    id = db.Column(db.Integer, primary_key=True)
    valor_aplicado = db.Column(db.Numeric(10, 2), nullable=False)
    
    agendamento_id = db.Column(db.Integer, db.ForeignKey('agendamentos.id'), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey('servicos.id'), nullable=False)

class Servico(db.Model):
    __tablename__ = 'servicos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    duracao_estimada = db.Column(db.Integer) 