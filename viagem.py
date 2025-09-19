from onibus import Onibus
from exceptions import ValorInvalidoError

class Viagem:
    def __init__(self, id_viagem, origem, destino, dias_da_semana, hora, preco, onibus: Onibus):
        if not isinstance(id_viagem, int) or id_viagem <= 0:
            raise ValorInvalidoError("O ID da viagem deve ser um número inteiro positivo.")
        
        if not isinstance(origem, str) or not origem.strip():
            raise ValorInvalidoError("A origem da viagem não pode ser vazia.")
        
        if not isinstance(destino, str) or not destino.strip():
            raise ValorInvalidoError("O destino da viagem não pode ser vazio.")
        
        if origem.strip().lower() == destino.strip().lower():
            raise ValorInvalidoError("A origem e o destino da viagem não podem ser iguais.")

        if not isinstance(dias_da_semana, list) or not dias_da_semana:
            raise ValorInvalidoError("A viagem deve ocorrer em pelo menos um dia da semana.")

        if not isinstance(hora, str) or len(hora) != 5 or hora[2] != ':':
            raise ValorInvalidoError("O formato da hora deve ser 'HH:MM'.")
        try:
            h, m = map(int, hora.split(':'))
            if not (0 <= h <= 23 and 0 <= m <= 59):
                raise ValueError()
        except ValueError:
            raise ValorInvalidoError("Os valores de hora (0-23) e/ou minuto (0-59) são inválidos.")

        if not isinstance(preco, (int, float)) or preco <= 0:
            raise ValorInvalidoError("O preço da viagem deve ser um número positivo.")

        if not isinstance(onibus, Onibus):
            raise ValorInvalidoError("A viagem deve ter um objeto Ônibus associado.")
        
        self.__id_viagem = id_viagem
        self.__origem = origem
        self.__destino = destino
        self.__dias_da_semana = dias_da_semana
        self.__hora = hora
        self.__preco = preco
        self.__onibus = onibus

    def get_id_viagem(self):
        return self.__id_viagem

    def set_id_viagem(self, id_viagem):
        if not isinstance(id_viagem, int) or id_viagem <= 0:
            raise ValorInvalidoError("O ID da viagem deve ser um número inteiro positivo.")
        self.__id_viagem = id_viagem

    def get_origem(self):
        return self.__origem

    def set_origem(self, origem):
        if not isinstance(origem, str) or not origem.strip():
            raise ValorInvalidoError("A origem da viagem não pode ser vazia.")
        if hasattr(self, '_Viagem__destino') and origem.lower() == self.__destino.lower():
            raise ValorInvalidoError("A origem não pode ser igual ao destino.")
        self.__origem = origem.strip()

    def get_destino(self):
        return self.__destino

    def set_destino(self, destino):
        if not isinstance(destino, str) or not destino.strip():
            raise ValorInvalidoError("O destino da viagem não pode ser vazio.")
        if hasattr(self, '_Viagem__origem') and destino.lower() == self.__origem.lower():
            raise ValorInvalidoError("O destino não pode ser igual à origem.")
        self.__destino = destino.strip()

    def get_dias_da_semana(self):
        return self.__dias_da_semana

    def set_dias_da_semana(self, dias):
        if not isinstance(dias, list) or not dias:
            raise ValorInvalidoError("A viagem deve ocorrer em pelo menos um dia da semana.")
        self.__dias_da_semana = dias

    def get_hora(self):
        return self.__hora

    def set_hora(self, hora):
        if not isinstance(hora, str) or len(hora) != 5 or hora[2] != ':':
            raise ValorInvalidoError("O formato da hora deve ser 'HH:MM'.")
        try:
            h, m = map(int, hora.split(':'))
            if not (0 <= h <= 23 and 0 <= m <= 59):
                raise ValueError()
        except ValueError:
            raise ValorInvalidoError("Os valores de hora (0-23) e/ou minuto (0-59) são inválidos.")
        self.__hora = hora

    def get_preco(self):
        return self.__preco

    def set_preco(self, preco):
        if not isinstance(preco, (int, float)) or preco <= 0:
            raise ValorInvalidoError("O preço da viagem deve ser um número positivo.")
        self.__preco = preco

    def get_onibus(self):
        return self.__onibus

    def set_onibus(self, onibus):
        if not isinstance(onibus, Onibus):
            raise ValorInvalidoError("A viagem deve ter um objeto Ônibus associado.")
        self.__onibus = onibus

    def imprime(self):
        print(f"ID: {self.__id_viagem}")
        print(f"Origem: {self.__origem}")
        print(f"Destino: {self.__destino}")
        print(f"Dias da semana: {self.__dias_da_semana}")
        print(f"Hora: {self.__hora}")
        print(f"Preço: {self.__preco}")
        print(f"Tipo de ônibus: {self.__onibus.get_tipo_onibus()}")
        print(f"Assentos disponíveis:", {self.__onibus.get_assentos()})
