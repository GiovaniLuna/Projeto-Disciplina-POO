from passageiro import Passageiro
from viagem import Viagem
from exceptions import ValorInvalidoError
import random

class Passagem:
    def __init__(self, viagem: Viagem, passageiro: Passageiro, assento: str):
        if not isinstance(viagem, Viagem):
            raise ValorInvalidoError("Uma passagem deve estar associada a um objeto Viagem válido.")
        
        if not isinstance(passageiro, Passageiro):
            raise ValorInvalidoError("Uma passagem deve estar associada a um objeto Passageiro válido.")

        if not isinstance(assento, str) or not assento.strip():
            raise ValorInvalidoError("O assento da passagem deve ser uma string não vazia.")

        self.__viagem = viagem
        self.__passageiro = passageiro
        self.__assento = assento
        self.__preco = self.gera_preco()
        self.__bilhete = str(random.randint(100000, 999999))

    def get_viagem(self):
        return self.__viagem

    def set_viagem(self, viagem):
        if not isinstance(viagem, Viagem):
            raise ValorInvalidoError("Uma passagem deve estar associada a um objeto Viagem válido.")
        self.__viagem = viagem

    def get_passageiro(self):
        return self.__passageiro

    def set_passageiro(self, passageiro):
        if not isinstance(passageiro, Passageiro):
            raise ValorInvalidoError("Uma passagem deve estar associada a um objeto Passageiro válido.")
        self.__passageiro = passageiro

    def get_assento(self):
        return self.__assento

    def set_assento(self, assento):
        if not isinstance(assento, str) or not assento.strip():
            raise ValorInvalidoError("O assento da passagem deve ser uma string não vazia.")
        self.__assento = assento

    def get_preco(self):
        return self.__preco

    def get_bilhete(self):
        return self.__bilhete

    def gera_preco(self):
        preco_base = self.__viagem.get_preco()
        if self.__passageiro.eh_isento_de_pagamento():
            return 0.0
        return preco_base