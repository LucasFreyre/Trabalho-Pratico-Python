from flask import Blueprint, jsonify

from helpdesk.controllers import ler_corpo_json, resposta_erro
from helpdesk.services import ErroDeNegocio, chamado_service

chamado_bp = Blueprint("chamados", __name__, url_prefix="/chamados")


def serializar_chamado(chamado):
    return {
        "id": chamado.id,
        "titulo": chamado.titulo,
        "descricao": chamado.descricao,
        "prioridade": chamado.prioridade,
        "status": chamado.status,
        "tecnico": chamado.tecnico,
        "data_abertura": chamado.data_abertura.strftime("%Y-%m-%d %H:%M:%S"),
        "usuario_id": chamado.usuario_id,
    }


@chamado_bp.get("")
def listar():
    chamados = chamado_service.listar()
    return jsonify([serializar_chamado(c) for c in chamados]), 200


@chamado_bp.get("/abertos")
def listar_abertos():
    chamados = chamado_service.listar_abertos()
    return jsonify([serializar_chamado(c) for c in chamados]), 200


@chamado_bp.get("/prioridade/alta")
def listar_prioridade_alta():
    chamados = chamado_service.listar_prioridade_alta()
    return jsonify([serializar_chamado(c) for c in chamados]), 200


@chamado_bp.get("/<int:chamado_id>")
def buscar(chamado_id):
    try:
        chamado = chamado_service.buscar(chamado_id)
    except ErroDeNegocio as erro:
        return resposta_erro(erro)
    return jsonify(serializar_chamado(chamado)), 200


@chamado_bp.post("")
def criar():
    try:
        dados = ler_corpo_json()
        chamado = chamado_service.criar(dados)
    except ErroDeNegocio as erro:
        return resposta_erro(erro)
    return jsonify(serializar_chamado(chamado)), 201


@chamado_bp.put("/<int:chamado_id>")
def atualizar(chamado_id):
    try:
        dados = ler_corpo_json()
        chamado = chamado_service.atualizar(chamado_id, dados)
    except ErroDeNegocio as erro:
        return resposta_erro(erro)
    return jsonify(serializar_chamado(chamado)), 200


@chamado_bp.delete("/<int:chamado_id>")
def excluir(chamado_id):
    try:
        chamado_service.excluir(chamado_id)
    except ErroDeNegocio as erro:
        return resposta_erro(erro)
    return "", 204


@chamado_bp.patch("/<int:chamado_id>/iniciar")
def iniciar(chamado_id):
    try:
        chamado = chamado_service.iniciar_atendimento(chamado_id)
    except ErroDeNegocio as erro:
        return resposta_erro(erro)
    return jsonify(serializar_chamado(chamado)), 200


@chamado_bp.patch("/<int:chamado_id>/encerrar")
def encerrar(chamado_id):
    try:
        chamado = chamado_service.encerrar(chamado_id)
    except ErroDeNegocio as erro:
        return resposta_erro(erro)
    return jsonify(serializar_chamado(chamado)), 200
