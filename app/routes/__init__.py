from .clientes import clientes_bp
from .servicos import servicos_bp
from .funcionarios import funcionarios_bp
from .agendamentos import agendamentos_bp
# objeto + prefixo na url 
ALL_BLUEPRINTS = [
    (clientes_bp, '/clientes'),
    (servicos_bp, '/servicos'),
    (funcionarios_bp, '/funcionarios'),
    (agendamentos_bp, '/agendamentos'),
]