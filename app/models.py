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
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(320), nullable=False, unique=True)
    senha = db.Column(db.String(128), nullable=False)
    data_cadastro = db.Column(db.Date, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Um cliente tem vários agendamentos
    agendamentos = db.relationship('Agendamento', back_populates='cliente', lazy=True)

class Funcionario(db.Model):
    __tablename__ = 'funcionarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    especialidade = db.Column(db.String(500), nullable=True)
    status = db.Column(db.Enum(StatusFuncionario), default=StatusFuncionario.INATIVO, nullable=False)

    # Um funcionário tem vários agendamentos
    agendamentos = db.relationship('Agendamento', back_populates='funcionario', lazy=True)

class Servico(db.Model):
    __tablename__ = 'servicos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    duracao_estimada = db.Column(db.Integer)

    # Relação com os itens de atendimento
    itens_atendimento = db.relationship('AtendimentoItem', back_populates='servico')

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(StatusAgendamento), default=StatusAgendamento.PENDENTE, nullable=False)

    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    # relação cliente e funcionario para atendimento
    cliente = db.relationship('Cliente', backref='agendamentos')
    funcionario = db.relationship('Funcionario', backref='agendamentos')
    # relação dos Itens
    itens_atendimento = db.relationship('AtendimentoItem', backref='agendamento', cascade="all, delete-orphan")

    # O agendamento pertence a um cliente e a um funcionário
    cliente = db.relationship('Cliente', back_populates='agendamentos')
    funcionario = db.relationship('Funcionario', back_populates='agendamentos')

    # Relação com os itens
    itens_atendimento = db.relationship('AtendimentoItem', back_populates='agendamento', cascade="all, delete-orphan")

class AtendimentoItem(db.Model):
    __tablename__ = 'atendimento_itens'
    id = db.Column(db.Integer, primary_key=True)
    valor_aplicado = db.Column(db.Numeric(10, 2), nullable=False)
    agendamento_id = db.Column(db.Integer, db.ForeignKey('agendamentos.id'), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey('servicos.id'), nullable=False)
    
    agendamento = db.relationship('Agendamento', back_populates='itens_atendimento')
    servico = db.relationship('Servico', back_populates='itens_atendimento')
