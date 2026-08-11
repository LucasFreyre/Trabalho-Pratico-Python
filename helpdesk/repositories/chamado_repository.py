from helpdesk.database import db
from helpdesk.models.chamado import Chamado


def listar_todos():
    return Chamado.query.order_by(Chamado.id).all()


def buscar_por_id(chamado_id):
    return Chamado.query.get(chamado_id)


def listar_por_usuario(usuario_id):
    return Chamado.query.filter_by(usuario_id=usuario_id).order_by(Chamado.id).all()


def listar_por_status(status):
    return Chamado.query.filter_by(status=status).order_by(Chamado.id).all()


def listar_por_prioridade(prioridade):
    return Chamado.query.filter_by(prioridade=prioridade).order_by(Chamado.id).all()


def contar():
    return Chamado.query.count()


def contar_por_status(status):
    return Chamado.query.filter_by(status=status).count()


def contar_por_usuario(usuario_id):
    return Chamado.query.filter_by(usuario_id=usuario_id).count()


def contar_por_prioridade_ignorando_status(usuario_id, prioridade, status_ignorado):
    return (
        Chamado.query.filter(
            Chamado.usuario_id == usuario_id,
            Chamado.prioridade == prioridade,
            Chamado.status != status_ignorado,
        ).count()
    )


def salvar(chamado):
    db.session.add(chamado)
    db.session.commit()
    return chamado


def atualizar():
    db.session.commit()


def remover(chamado):
    db.session.delete(chamado)
    db.session.commit()
