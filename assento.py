from exceptions import ValorInvalidoError, AssentoOcupadoError
from passageiro import Passageiro

class Assento:
    def __init__(self, numero, ocupado):
        if not isinstance(numero, str) or not numero.strip():
            raise ValorInvalidoError("O número do assento deve ser um texto não vazio.")
        if not isinstance(ocupado, bool):
            raise ValorInvalidoError("O status 'ocupado' deve ser um valor booleano (True ou False).")

        self.__numero = numero
        self.__ocupado = ocupado
        self.__passageiro = None

    def get_numero(self):
        return self.__numero
    
    def set_numero(self, numero):
        if not isinstance(numero, str) or not numero.strip():
            raise ValorInvalidoError("O número do assento deve ser um texto não vazio.")
        self.__numero = numero
    
    def get_ocupado(self):
        return self.__ocupado

    def set_ocupado(self, ocupado):
        if not isinstance(ocupado, bool):
            raise ValorInvalidoError("O status 'ocupado' deve ser um valor booleano (True ou False).")
        self.__ocupado = ocupado
    
    def get_passageiro(self):
        return self.__passageiro

    def set_passageiro(self, passageiro):
        if passageiro is not None and not isinstance(passageiro, Passageiro):
            raise ValorInvalidoError("O passageiro deve ser um objeto da classe Passageiro ou None.")

        if self.get_ocupado() and passageiro is not None and self.__passageiro is not None:
            raise AssentoOcupadoError(f"Assento {self.get_numero()} já está ocupado por {self.__passageiro.get_nome()}.")

        if passageiro is not None:
            self.__passageiro = passageiro
            self.set_ocupado(True)
        else: 
            self.__passageiro = None
            self.set_ocupado(False)  