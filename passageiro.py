from exceptions import ValorInvalidoError

class Passageiro:
    def __init__(self, nome, idade, cpf, email, telefone, eh_PCD):
        if not isinstance(nome, str) or not nome.strip():
            raise ValorInvalidoError("O nome do passageiro não pode ser vazio.")
        
        if not isinstance(idade, int) or idade < 0:
            raise ValorInvalidoError("A idade deve ser um número inteiro igual ou maior que zero.")
       
        if email and (not isinstance(email, str) or "@" not in email):
            raise ValorInvalidoError("O formato do e-mail é inválido.")
        
        if telefone and not isinstance(telefone, str):
            raise ValorInvalidoError("O telefone deve ser uma string.")
        
        if telefone and len(''.join(filter(str.isdigit, telefone))) < 8:
            raise ValorInvalidoError("Telefone deve ter pelo menos 8 dígitos.")
        
        if not isinstance(cpf, str):
            raise ValorInvalidoError("O CPF deve ser uma string.")
        
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        
        if len(cpf_limpo) != 11:
            raise ValorInvalidoError("O CPF deve conter exatamente 11 dígitos.")
        
        if not isinstance(eh_PCD, bool):
            raise ValorInvalidoError("A informação sobre PCD deve ser um valor booleano (True/False).")
        
        self.__nome = nome
        self.__idade = idade
        self.__cpf = cpf
        self.__email = email
        self.__telefone = telefone
        self.__PCD = eh_PCD

    def get_nome(self):
        return self.__nome

    def set_nome(self, nome):
        if not isinstance(nome, str) or not nome.strip():
            raise ValorInvalidoError("O nome do passageiro não pode ser vazio.")
        self.__nome = nome.strip()

    def get_idade(self):
        return self.__idade

    def set_idade(self, idade):
        if not isinstance(idade, int) or idade < 0:
            raise ValorInvalidoError("A idade deve ser um número inteiro igual ou maior que zero.")
        self.__idade = idade

    def get_cpf(self):
        return self.__cpf

    def set_cpf(self, cpf):
        if not isinstance(cpf, str):
            raise ValorInvalidoError("O CPF deve ser uma string.")
        
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        
        if len(cpf_limpo) != 11:
            raise ValorInvalidoError("O CPF deve conter exatamente 11 dígitos.")
        self.__cpf = cpf_limpo

    def get_email(self):
        return self.__email

    def set_email(self, email):
        if email and (not isinstance(email, str) or "@" not in email):
            raise ValorInvalidoError("O formato do e-mail é inválido.")
        self.__email = email

    def get_telefone(self):
        return self.__telefone

    def set_telefone(self, telefone):
        if telefone and not isinstance(telefone, str):
            raise ValorInvalidoError("O telefone deve ser uma string.")
        self.__telefone = telefone

    def get_eh_PCD(self):
        return self.__PCD

    def set_eh_PCD(self, valor):
        if not isinstance(valor, bool):
            raise ValorInvalidoError("A informação sobre PCD deve ser um valor booleano (True/False).")
        self.__PCD = valor

    def eh_isento_de_pagamento(self):
        return self.__PCD or self.__idade < 6 or self.__idade > 60

    def __str__(self):
        return f"{self.__nome} ({self.__idade} anos) - CPF: {self.__cpf}"

