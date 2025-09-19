from onibus import Onibus
from assento import Assento
from exceptions import AssentoInvalidoError, AssentoOcupadoError,ValorInvalidoError


class OnibusExecutivo(Onibus):
    def __init__(self, modelo, fabricante, numrodas, descricao):
        super().__init__(modelo, fabricante, numrodas, descricao, "Executivo")
        self.__assentos_semi_leito = self.gera_assentos_semi_leito()
        self.__assentos_leito = self.gera_assentos_leito()

    def gera_assentos_semi_leito(self):
        fileiras = "ABCDEFGHIJKL"
        matriz = []
        for numero in range(1, 5):  # 1..4
            linha = []
            for letra in fileiras:
                numero_do_assento = f"S - {letra}{numero}"
                linha.append(Assento(numero_do_assento, False))
            matriz.append(linha)
        return matriz

    def gera_assentos_leito(self):
        fileiras = "ABCD"
        matriz = []
        for numero in range(1, 4):  # 1..3
            linha = []
            for letra in fileiras:
                numero_do_assento = f"L - {letra}{numero}"
                linha.append(Assento(numero_do_assento, False))
            matriz.append(linha)
        return matriz

    def get_assentos_semi_leito(self):
        return self.__assentos_semi_leito

    def get_assentos_leito(self):
        return self.__assentos_leito

    def _localiza_assento(self, numero_assento_procurado):
        """
        Método auxiliar simplificado. Busca em ambas as listas e retorna 
        apenas o objeto Assento se encontrar, ou None caso contrário.
        """
        for linha in self.__assentos_semi_leito:
            for assento in linha:
                if assento.get_numero() == numero_assento_procurado:
                    return assento
        
        for linha in self.__assentos_leito:
            for assento in linha:
                if assento.get_numero() == numero_assento_procurado:
                    return assento
        
        return None

    def ocupar_assento(self, numero_assento, passageiro):
        """
        Lógica de ocupação agora é limpa e direta, sem retornos True/False.
        Foi renomeado de 'set_assento' para 'ocupar_assento' para consistência.
        """
        assento_alvo = self._localiza_assento(numero_assento)
        
        if assento_alvo is None:
            raise AssentoInvalidoError(f"O assento '{numero_assento}' não existe neste ônibus.")
        
        if assento_alvo.get_ocupado():
            raise AssentoOcupadoError(f"O assento '{numero_assento}' já está ocupado.")
        
        assento_alvo.set_passageiro(passageiro)

    def libera_assento_por_numero(self, numero_assento):
        """
        Lógica de liberação corrigida, seguindo o mesmo padrão.
        """
        assento_alvo = self._localiza_assento(numero_assento)

        if assento_alvo is None:
            raise AssentoInvalidoError(f"O assento '{numero_assento}' não existe e não pode ser liberado.")
        
        assento_alvo.set_passageiro(None)

    def ocupar_assento_por_posicao(self, tipo_assento, linha_idx, coluna_idx, passageiro):
        """
        Método antigo ('set_assento_por_posicao') refatorado para usar exceções.
        """
        matriz = None
        if tipo_assento.lower() == "semi-leito":
            matriz = self.__assentos_semi_leito
        elif tipo_assento.lower() == "leito":
            matriz = self.__assentos_leito
        else:
            raise ValorInvalidoError(f"Tipo de assento desconhecido: '{tipo_assento}'")
        
        try:
            assento = matriz[linha_idx][coluna_idx]
        except IndexError:
            raise AssentoInvalidoError("Posição de assento (linha ou coluna) inválida.")

        if assento.get_ocupado():
            raise AssentoOcupadoError(f"O assento na posição especificada já está ocupado.")
        
        assento.set_passageiro(passageiro)


    def imprime(self):
        super().imprime()
        livres_sl = sum(1 for l in self.__assentos_semi_leito for a in l if not a.get_ocupado())
        total_sl = sum(len(l) for l in self.__assentos_semi_leito)
        livres_l = sum(1 for l in self.__assentos_leito for a in l if not a.get_ocupado())
        total_l = sum(len(l) for l in self.__assentos_leito)
        print(f"Assentos Semi-Leito: {total_sl} (Livres: {livres_sl})")
        print(f"Assentos Leito: {total_l} (Livres: {livres_l})")
