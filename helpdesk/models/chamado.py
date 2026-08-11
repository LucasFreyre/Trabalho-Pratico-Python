from datetime import datetime

from helpdesk.database import db


class Chamado(db.Model):
    __tablename__ = "chamados"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    prioridade = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    tecnico = db.Column(db.String(120))
    data_abertura = db.Column(db.DateTime, nullable=False, default=datetime.now)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    usuario = db.relationship("Usuario", back_populates="chamados")

    def __repr__(self):
        return "<Chamado {} - {}>".format(self.id, self.status)
