from helpdesk.models.chamado import Chamado
from helpdesk.repositories import chamado_repository, usuario_repository
from helpdesk.services import Conflito, DadosInvalidos, NaoEncontrado

STATUS_ABERTO = "Aberto"
STATUS_EM_ATENDIMENTO = "Em atendimento"
STATUS_ENCERRADO = "Encerrado"

PRIORIDADE_ALTA = "Alta"
LIMITE_CHAMADOS_ALTA = 5

# aceita a prioridade digitada com ou sem acento / maiúscula
PRIORIDADES = {
    "baixa": "Baixa",
    "media": "Média",
    "média": "Média",
    "alta": "Alta",
}

TAMANHO_MINIMO_TITULO = 5
TAMANHO_MINIMO_DESCRICAO = 10


def _limpar(valor):
    if valor is None:
        return ""
    return str(valor).strip()


def _validar_titulo(titulo):
    if not titulo:
        raise DadosInvalidos("O título é obrigatório.")
    if len(titulo) < TAMANHO_MINIMO_TITULO:
        raise DadosInvalidos(
            "O título deve ter pelo menos {} caracteres.".format(TAMANHO_MINIMO_TITULO)
        )


def _validar_descricao(descricao):
    if len(descricao) < TAMANHO_MINIMO_DESCRICAO:
        raise DadosInvalidos(
            "A descrição deve ter pelo menos {} caracteres.".format(
                TAMANHO_MINIMO_DESCRICAO
            )
        )


def _converter_prioridade(valor):
    prioridade = PRIORIDADES.get(_limpar(valor).lower())
    if prioridade is None:
        raise DadosInvalidos("A prioridade deve ser Baixa, Média ou Alta.")
    return prioridade


def _validar_limite_de_alta(usuario_id, chamado_ignorado=None):
    """Um usuário não pode ficar com mais de 5 chamados de prioridade Alta em
    aberto ao mesmo tempo (encerrados não entram na conta)."""
    total = chamado_repository.contar_por_prioridade_ignorando_status(
        usuario_id, PRIORIDADE_ALTA, STATUS_ENCERRADO
    )

    # numa alteração o próprio chamado já pode estar somado no total
    if chamado_ignorado is not None:
        if (
            chamado_ignorado.prioridade == PRIORIDADE_ALTA
            and chamado_ignorado.status != STATUS_ENCERRADO
        ):
            total -= 1

    if total >= LIMITE_CHAMADOS_ALTA:
        raise Conflito(
            "O usuário já possui {} chamados de prioridade Alta em aberto.".format(
                LIMITE_CHAMADOS_ALTA
            )
        )


def _buscar_usuario(usuario_id):
    if usuario_id is None:
        raise DadosInvalidos("O chamado deve estar vinculado a um usuário.")

    try:
        usuario_id = int(usuario_id)
    except (TypeError, ValueError):
        raise DadosInvalidos("O campo usuario_id deve ser um número inteiro.")

    usuario = usuario_repository.buscar_por_id(usuario_id)
    if usuario is None:
        raise DadosInvalidos("Usuário {} não existe.".format(usuario_id))
    return usuario


def listar():
    return chamado_repository.listar_todos()


def buscar(chamado_id):
    chamado = chamado_repository.buscar_por_id(chamado_id)
    if chamado is None:
        raise NaoEncontrado("Chamado {} não encontrado.".format(chamado_id))
    return chamado


def listar_abertos():
    return chamado_repository.listar_por_status(STATUS_ABERTO)


def listar_prioridade_alta():
    return chamado_repository.listar_por_prioridade(PRIORIDADE_ALTA)


def criar(dados):
    titulo = _limpar(dados.get("titulo"))
    descricao = _limpar(dados.get("descricao"))

    _validar_titulo(titulo)
    _validar_descricao(descricao)

    prioridade = _converter_prioridade(dados.get("prioridade"))
    usuario = _buscar_usuario(dados.get("usuario_id"))

    if prioridade == PRIORIDADE_ALTA:
        _validar_limite_de_alta(usuario.id)

    chamado = Chamado(
        titulo=titulo,
        descricao=descricao,
        prioridade=prioridade,
        status=STATUS_ABERTO,
        tecnico=_limpar(dados.get("tecnico")) or None,
        usuario_id=usuario.id,
    )
    return chamado_repository.salvar(chamado)


def atualizar(chamado_id, dados):
    chamado = buscar(chamado_id)

    # o status só muda pelos endpoints de iniciar/encerrar, senão as regras
    # de transição seriam furadas por um PUT
    if "status" in dados:
        raise Conflito(
            "O status não pode ser alterado por aqui. "
            "Utilize /chamados/<id>/iniciar ou /chamados/<id>/encerrar."
        )

    if "titulo" in dados:
        titulo = _limpar(dados.get("titulo"))
        _validar_titulo(titulo)
        chamado.titulo = titulo

    if "descricao" in dados:
        descricao = _limpar(dados.get("descricao"))
        _validar_descricao(descricao)
        chamado.descricao = descricao

    if "prioridade" in dados:
        prioridade = _converter_prioridade(dados.get("prioridade"))
        if prioridade == PRIORIDADE_ALTA:
            _validar_limite_de_alta(chamado.usuario_id, chamado_ignorado=chamado)
        chamado.prioridade = prioridade

    if "tecnico" in dados:
        chamado.tecnico = _limpar(dados.get("tecnico")) or None

    chamado_repository.atualizar()
    return chamado


def excluir(chamado_id):
    chamado = buscar(chamado_id)
    chamado_repository.remover(chamado)


def iniciar_atendimento(chamado_id):
    chamado = buscar(chamado_id)

    if chamado.status != STATUS_ABERTO:
        raise Conflito(
            'Apenas chamados com status "Aberto" podem ir para atendimento. '
            "O chamado {} está como {}.".format(chamado.id, chamado.status)
        )

    chamado.status = STATUS_EM_ATENDIMENTO
    chamado_repository.atualizar()
    return chamado


def encerrar(chamado_id):
    chamado = buscar(chamado_id)

    if chamado.status != STATUS_EM_ATENDIMENTO:
        raise Conflito(
            'Apenas chamados com status "Em atendimento" podem ser encerrados. '
            "O chamado {} está como {}.".format(chamado.id, chamado.status)
        )

    chamado.status = STATUS_ENCERRADO
    chamado_repository.atualizar()
    return chamado
