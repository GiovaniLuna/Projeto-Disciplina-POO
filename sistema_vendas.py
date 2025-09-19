from passageiro import Passageiro
from passagem import Passagem
from onibus_convencional import OnibusConvencional
from onibus_executivo import OnibusExecutivo
from exceptions import BilheteNaoEncontradoError, ValorInvalidoError
 
class SistemaVendas:
    def __init__(self, lista_de_viagens):
        self.__lista_viagens = lista_de_viagens
        self.__passagens = []

    def buscar_viagens_disponiveis(self, origem, destino):
        encontradas = []
        for viagem in self.__lista_viagens:
            if viagem.get_origem().lower() == origem.lower() and viagem.get_destino().lower() == destino.lower():
                encontradas.append(viagem)
        return encontradas

    def vender_passagem(self, viagem, dados_passageiro, tipo_assento=None, linha=None, coluna=None, novo_assento_str=None):        
        passageiro = Passageiro(
            dados_passageiro['nome'],
            dados_passageiro['idade'],
            dados_passageiro['cpf'],
            dados_passageiro.get('email', ''),
            dados_passageiro.get('telefone', ''),
            dados_passageiro.get('pcd', False)
        )

        onibus = viagem.get_onibus()
        if novo_assento_str: # Venda para Convencional
            onibus.ocupar_assento(novo_assento_str, passageiro)
            assento_ocupado_str = novo_assento_str
        elif tipo_assento is not None: # Venda para Executivo
            onibus.ocupar_assento_por_posicao(tipo_assento, linha, coluna, passageiro)
            # Precisamos obter o número do assento a partir da posição
            if tipo_assento.lower() == "semi-leito":
                assento_ocupado_str = onibus.get_assentos_semi_leito()[linha][coluna].get_numero()
            else:
                assento_ocupado_str = onibus.get_assentos_leito()[linha][coluna].get_numero()
        else:
            raise ValorInvalidoError("Informações do assento insuficientes para a venda.")
        

        preco_final = viagem.get_preco()
        if isinstance(onibus, OnibusExecutivo) and tipo_assento and tipo_assento.lower() == "leito":
            preco_final *= 1.5
        if passageiro.eh_isento_de_pagamento():
            preco_final = 0.0

        passagem = Passagem(viagem, passageiro, assento_ocupado_str)
        passagem._Passagem__preco = preco_final
        self.__passagens.append(passagem)
        return passagem

    def buscar_passagem_por_bilhete(self, bilhete_numero):
        for p in self.__passagens:
            if p.get_bilhete() == bilhete_numero:
                return p
        raise BilheteNaoEncontradoError(f"O bilhete com número '{bilhete_numero}' não foi encontrado.")

    def liberar_assento_da_passagem(self, passagem):
        onibus = passagem.get_viagem().get_onibus()
        numero_assento = passagem.get_assento()

        onibus.libera_assento_por_numero(numero_assento)

    def trocar_passagem(self, bilhete_numero, nova_viagem, tipo_assento=None, linha=None, coluna=None, novo_assento_str=None):
        passagem_atual = self.buscar_passagem_por_bilhete(bilhete_numero)
        passageiro = passagem_atual.get_passageiro()
        onibus_novo = nova_viagem.get_onibus()
        assento_novo_final_str = ""

        if isinstance(onibus_novo, OnibusConvencional):
            if not novo_assento_str:
                raise ValorInvalidoError("Para ônibus Convencional, o número do novo assento é obrigatório.")
            onibus_novo.ocupar_assento(novo_assento_str, passageiro)
            assento_novo_final_str = novo_assento_str
        else:  # OnibusExecutivo
            if tipo_assento is None or linha is None or coluna is None:
                raise ValorInvalidoError("Para ônibus Executivo, tipo, linha e coluna do novo assento são obrigatórios.")
            onibus_novo.ocupar_assento_por_posicao(tipo_assento, linha, coluna, passageiro)
            
            if tipo_assento.lower() == "semi-leito":
                assento_novo_final_str = onibus_novo.get_assentos_semi_leito()[linha][coluna].get_numero()
            else:
                assento_novo_final_str = onibus_novo.get_assentos_leito()[linha][coluna].get_numero()

        try:
            self.liberar_assento_da_passagem(passagem_atual)
        except Exception as e:
            onibus_novo.libera_assento_por_numero(assento_novo_final_str)
            raise RuntimeError(f"Erro crítico ao liberar o assento antigo. A troca foi revertida. Detalhe: {e}")

        passagem_atual.set_viagem(nova_viagem)
        passagem_atual.set_assento(assento_novo_final_str)
    
        return passagem_atual