from onibus import Onibus
from assento import Assento
from exceptions import AssentoInvalidoError, AssentoOcupadoError

class OnibusConvencional(Onibus):
    def __init__(self, modelo, fabricante, numrodas, descricao):
        super().__init__(modelo, fabricante, numrodas, descricao, "Convencional")
        self.__assentos = self.gera_assentos()

    def gera_assentos(self):
        lista_assentos = []
        fileiras = "ABCDEFGHIJKL"
        
        for numero in range(1, 5):
            for letra in fileiras:
                numero_do_assento = f"{letra}{numero}"
                novo_assento = Assento(numero_do_assento, False)
                lista_assentos.append(novo_assento)
        return lista_assentos

    def get_assentos(self):
        return self.__assentos

    def ocupar_assento(self, numero_assento, passageiro):
        """
        Ocupa um assento específico. Lança exceções se o assento não existir ou já estiver ocupado.
        """
        assento_alvo = None
        for assento in self.__assentos:
            if assento.get_numero() == numero_assento:
                assento_alvo = assento
                break
        
        if assento_alvo is None:
            raise AssentoInvalidoError(f"O assento '{numero_assento}' não existe neste ônibus.")
        
        if assento_alvo.get_ocupado():
            raise AssentoOcupadoError(f"O assento '{numero_assento}' já está ocupado.")
        
        assento_alvo.set_passageiro(passageiro)

    def libera_assento_por_numero(self, numero_assento):
        assento_alvo = None
        for assento in self.__assentos:
            if assento.get_numero() == numero_assento:
                assento_alvo = assento
                break

        if assento_alvo is None:
            raise AssentoInvalidoError(f"O assento '{numero_assento}' não existe e não pode ser liberado.")

        assento_alvo.set_passageiro(None)
        
    def imprime(self):
        super().imprime()
        livres = sum(1 for a in self.__assentos if not a.get_ocupado())
        print(f"Assentos: {len(self.__assentos)} (Livres: {livres})")