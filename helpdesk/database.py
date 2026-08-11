import os

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# o banco fica na raiz do projeto (uma pasta acima deste arquivo)
PASTA_RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CAMINHO_BANCO = os.path.join(PASTA_RAIZ, "helpdesk.db")


def configurar_banco(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + CAMINHO_BANCO
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # os models precisam ser importados antes do create_all, senão o
    # SQLAlchemy não sabe quais tabelas deve criar
    from helpdesk.models import chamado, usuario  # noqa: F401

    with app.app_context():
        db.create_all()
