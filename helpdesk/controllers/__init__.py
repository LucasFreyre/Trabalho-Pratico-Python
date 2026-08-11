from flask import jsonify, request

from helpdesk.services import DadosInvalidos


def ler_corpo_json():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        raise DadosInvalidos("Envie um corpo JSON válido com os dados da requisição.")
    return dados


def resposta_erro(erro):
    return jsonify({"erro": erro.mensagem}), erro.codigo_http
