from onibus_convencional import OnibusConvencional
from onibus_executivo import OnibusExecutivo
from viagem import Viagem
from exceptions import ValorInvalidoError, ViagemNaoEncontradaError

class SistemaAdmin:
    def __init__(self):
        self.__viagens = []
        self.__proximo_id_viagem = 1

    def cadastrar_viagem(self, origem, destino, dias_da_semana, hora, preco_base, tipo_onibus, modelo, fabricante):
        if not all(isinstance(arg, str) and arg.strip() for arg in [origem, destino, hora, tipo_onibus, modelo, fabricante]):
            raise ValorInvalidoError("Todos os campos de texto (origem, destino, etc.) devem ser preenchidos.")

        if not isinstance(dias_da_semana, list) or not dias_da_semana:
            raise ValorInvalidoError("Pelo menos um dia da semana deve ser selecionado.")

        try:
            preco_valido = float(preco_base)
            if preco_valido <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            raise ValorInvalidoError("O preço base deve ser um número positivo.")

        onibus_obj = None
        tipo_lower = tipo_onibus.lower()
        if tipo_lower == "convencional":
            onibus_obj = OnibusConvencional(modelo, fabricante, 6, "Ônibus convencional com 48 lugares")
        elif tipo_lower == "executivo":
            onibus_obj = OnibusExecutivo(modelo, fabricante, 8, "Ônibus executivo de dois andares")
        else:
            raise ValorInvalidoError(f"Tipo de ônibus desconhecido: '{tipo_onibus}'. Use 'Convencional' ou 'Executivo'.")

        nova_viagem = Viagem(self.__proximo_id_viagem, origem, destino, dias_da_semana, hora, preco_valido, onibus_obj)
        self.__viagens.append(nova_viagem)
        self.__proximo_id_viagem += 1

        return nova_viagem

    def buscar_viagem_por_id(self, id_viagem):
        for viagem in self.__viagens:
            if viagem.get_id_viagem() == id_viagem:
                return viagem
        
        # Lança uma exceção se o loop terminar e nenhuma viagem for encontrada
        raise ViagemNaoEncontradaError(f"Nenhuma viagem foi encontrada com o ID {id_viagem}.")

    def get_todas_as_viagens(self):
        return self.__viagens