from exceptions import ValorInvalidoError

class Onibus:
    def __init__(self, modelo, fabricante, num_rodas, descricao, tipo_onibus):
        if not isinstance(modelo, str) or not modelo.strip():
            raise ValorInvalidoError("O modelo do ônibus deve ser um texto não vazio.")
        if not isinstance(fabricante, str) or not fabricante.strip():
            raise ValorInvalidoError("O fabricante do ônibus deve ser um texto não vazio.")
        if not isinstance(num_rodas, int) or num_rodas <= 0:
            raise ValorInvalidoError("O número de rodas deve ser um inteiro positivo.")

        self.__modelo = modelo
        self.__fabricante = fabricante
        self.__num_rodas = num_rodas
        self.__descricao = descricao
        self.__tipo_onibus = tipo_onibus

    def get_modelo(self):
        return self.__modelo

    def set_modelo(self, modelo):
        if not isinstance(modelo, str) or not modelo.strip():
            raise ValorInvalidoError("O modelo do ônibus deve ser um texto não vazio.")
        self.__modelo = modelo

    def get_fabricante(self):
        return self.__fabricante

    def set_fabricante(self, fabricante):
        if not isinstance(fabricante, str) or not fabricante.strip():
            raise ValorInvalidoError("O fabricante do ônibus deve ser um texto não vazio.")
        self.__fabricante = fabricante

    def get_num_rodas(self):
        return self.__num_rodas

    def set_num_rodas(self, num_rodas):
        if not isinstance(num_rodas, int) or num_rodas <= 0:
            raise ValorInvalidoError("O número de rodas deve ser um inteiro positivo.")
        self.__num_rodas = num_rodas

    def get_descricao(self):
        return self.__descricao

    def set_descricao(self, descricao):
        self.__descricao = descricao

    def get_tipo_onibus(self):
        return self.__tipo_onibus

    def set_tipo_onibus(self, tipo_onibus):
        self.__tipo_onibus = tipo_onibus


    def ocupar_assento(self, *args, **kwargs):
        raise NotImplementedError("Este método deve ser implementado na subclasse")

    def get_assentos(self):
        raise NotImplementedError("Este método deve ser implementado na subclasse")

    def get_assentos(self):
        pass

    def ocupar_assento(self):
        pass

    
    def imprime(self):
        print("Modelo:", self.__modelo)
        print("Fabricante:", self.__fabricante)
        print("Número de rodas:", self.__num_rodas)
        print("Descrição:", self.__descricao)
        print("Tipo de ônibus:", self.__tipo_onibus)