
class Error(Exception):
    """Classe base para as exceções do módulo requisition_pool_olt"""
    pass




class TimeOutError(Error):
    """Exceção lançada quando excede o tempo de espera pela resposta da olt."""

    def __init__(self):
        self.message = "Switch excedeu o tempo máximo de resposta"

    def __str__(self):
        return self.message


class ConnectionError(Error):
    """Exceção lançada quando o script não consegue se conectar com a olt."""

    def __init__(self):
        self.message = "Não foi possível estabelecer conexão com a olt"

    def __str__(self):
        return self.message


class CommandError(Error):
    """Exceção lançada quando um error é gerado durante a execução de um dos scripts da OLT."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
