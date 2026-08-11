from helpdesk.database import db
from helpdesk.models.usuario import Usuario


def listar_todos():
    return Usuario.query.order_by(Usuario.id).all()


def buscar_por_id(usuario_id):
    return Usuario.query.get(usuario_id)


def buscar_por_email(email):
    return Usuario.query.filter_by(email=email).first()


def contar():
    return Usuario.query.count()


def salvar(usuario):
    db.session.add(usuario)
    db.session.commit()
    return usuario


def atualizar():
    db.session.commit()


def remover(usuario):
    db.session.delete(usuario)
    db.session.commit()
