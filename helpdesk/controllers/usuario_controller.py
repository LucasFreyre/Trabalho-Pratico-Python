from flask import Blueprint, jsonify

from helpdesk.controllers import ler_corpo_json, resposta_erro
from helpdesk.controllers.chamado_controller import serializar_chamado
from helpdesk.services import ErroDeNegocio, usuario_service

usuario_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


def serializar_usuario(usuario):
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "setor": usuario.setor,
    }


@usuario_bp.get("")
def listar():
    usuarios = usuario_service.listar()
    return jsonify([serializar_usuario(u) for u in usuarios]), 200


@usuario_bp.get("/<int:usuario_id>")
def buscar(usuario_id):
    try:
        usuario = usuario_service.buscar(usuario_id)
    except ErroDeNegocio as erro:
        return resposta_erro(erro)
    return jsonify(serializar_usuario(usuario)), 200


@usuario_bp.post("")
def criar():
    try:
        dados = ler_corpo_json()
        usuario = usuario_service.criar(dados)
    except ErroDeNegocio as erro:
        return resposta_erro(erro)
    return jsonify(serializar_usuario(usuario)), 201


@usuario_bp.put("/<int:usuario_id>")
def atualizar(usuario_id):
    try:
        dados = ler_corpo_json()
        usuario = usuario_service.atualizar(usuario_id, dados)
    except ErroDeNegocio as erro:
        return resposta_erro(erro)
    return jsonify(serializar_usuario(usuario)), 200


@usuario_bp.delete("/<int:usuario_id>")
def excluir(usuario_id):
    try:
        usuario_service.excluir(usuario_id)
    except ErroDeNegocio as erro:
        return resposta_erro(erro)
    return "", 204


@usuario_bp.get("/<int:usuario_id>/chamados")
def listar_chamados(usuario_id):
    try:
        chamados = usuario_service.listar_chamados(usuario_id)
    except ErroDeNegocio as erro:
        return resposta_erro(erro)
    return jsonify([serializar_chamado(c) for c in chamados]), 200
