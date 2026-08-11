from helpdesk.database import db


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    setor = db.Column(db.String(80))

    chamados = db.relationship("Chamado", back_populates="usuario")

    def __repr__(self):
        return "<Usuario {} - {}>".format(self.id, self.email)
