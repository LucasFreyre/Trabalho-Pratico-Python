class ErroDeNegocio(Exception):
    codigo_http = 400

    def __init__(self, mensagem):
        super().__init__(mensagem)
        self.mensagem = mensagem


class DadosInvalidos(ErroDeNegocio):
    codigo_http = 400


class NaoEncontrado(ErroDeNegocio):
    codigo_http = 404


class Conflito(ErroDeNegocio):
    codigo_http = 409
