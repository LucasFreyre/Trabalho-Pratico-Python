from helpdesk.models.usuario import Usuario
from helpdesk.repositories import chamado_repository, usuario_repository
from helpdesk.services import Conflito, DadosInvalidos, NaoEncontrado


def _limpar(valor):
    if valor is None:
        return ""
    return str(valor).strip()


def listar():
    return usuario_repository.listar_todos()


def buscar(usuario_id):
    usuario = usuario_repository.buscar_por_id(usuario_id)
    if usuario is None:
        raise NaoEncontrado("Usuário {} não encontrado.".format(usuario_id))
    return usuario


def criar(dados):
    nome = _limpar(dados.get("nome"))
    email = _limpar(dados.get("email"))
    setor = _limpar(dados.get("setor"))

    if not nome:
        raise DadosInvalidos("O nome é obrigatório.")
    if not email:
        raise DadosInvalidos("O e-mail é obrigatório.")

    if usuario_repository.buscar_por_email(email) is not None:
        raise Conflito("Já existe um usuário cadastrado com o e-mail {}.".format(email))

    usuario = Usuario(nome=nome, email=email, setor=setor or None)
    return usuario_repository.salvar(usuario)


def atualizar(usuario_id, dados):
    usuario = buscar(usuario_id)

    # só altera os campos que vieram no corpo da requisição
    if "nome" in dados:
        nome = _limpar(dados.get("nome"))
        if not nome:
            raise DadosInvalidos("O nome é obrigatório.")
        usuario.nome = nome

    if "email" in dados:
        email = _limpar(dados.get("email"))
        if not email:
            raise DadosInvalidos("O e-mail é obrigatório.")

        existente = usuario_repository.buscar_por_email(email)
        if existente is not None and existente.id != usuario.id:
            raise Conflito("O e-mail {} já está em uso por outro usuário.".format(email))
        usuario.email = email

    if "setor" in dados:
        usuario.setor = _limpar(dados.get("setor")) or None

    usuario_repository.atualizar()
    return usuario


def excluir(usuario_id):
    usuario = buscar(usuario_id)

    if chamado_repository.contar_por_usuario(usuario.id) > 0:
        raise Conflito(
            "Não é possível excluir o usuário porque ele possui chamados cadastrados."
        )

    usuario_repository.remover(usuario)


def listar_chamados(usuario_id):
    usuario = buscar(usuario_id)
    return chamado_repository.listar_por_usuario(usuario.id)
