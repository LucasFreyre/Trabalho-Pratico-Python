from flask import Flask, jsonify

from helpdesk.controllers.chamado_controller import chamado_bp
from helpdesk.controllers.usuario_controller import usuario_bp
from helpdesk.database import configurar_banco


def criar_app():
    app = Flask(__name__)
    app.json.ensure_ascii = False  # deixa os acentos legiveis na resposta
    app.json.sort_keys = False

    configurar_banco(app)

    app.register_blueprint(usuario_bp)
    app.register_blueprint(chamado_bp)

    @app.errorhandler(404)
    def rota_nao_encontrada(erro):
        return jsonify({"erro": "Rota não encontrada."}), 404

    @app.errorhandler(405)
    def metodo_nao_permitido(erro):
        return jsonify({"erro": "Método não permitido para esta rota."}), 405

    return app


app = criar_app()


if __name__ == "__main__":
    app.run(debug=True)
