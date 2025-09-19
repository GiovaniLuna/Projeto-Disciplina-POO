# main.py
import tkinter as tk
from tkinter import messagebox, ttk

from onibus_convencional import OnibusConvencional
from onibus_executivo import OnibusExecutivo
from passageiro import Passageiro
from viagem import Viagem
from assento import Assento
from sistema_admin import SistemaAdmin
from sistema_vendas import SistemaVendas
from exceptions import ValorInvalidoError,ViagemNaoEncontradaError,AssentoOcupadoError,AssentoInvalidoError,BilheteNaoEncontradoError


class InterfaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Viagens de Ônibus")
        self.root.geometry("920x680")

        self.frame_atual = None
        self.admin = SistemaAdmin()
        self.vendas = SistemaVendas(self.admin.get_todas_as_viagens())

        self.mostrar_menu_principal()

    def limpar_tela(self):
        if self.frame_atual:
            self.frame_atual.destroy()
            self.frame_atual = None

    # -------------------- Menu principal --------------------
    def mostrar_menu_principal(self):
        self.limpar_tela()
        self.frame_atual = tk.Frame(self.root, padx=20, pady=20)
        self.frame_atual.pack(expand=True, fill="both")

        tk.Label(self.frame_atual, text="SISTEMA DE VIAGENS", font=("Helvetica", 22, "bold")).pack(pady=20)
        tk.Button(self.frame_atual, text="Modo Administrador", width=30, height=2, command=self.mostrar_tela_admin).pack(pady=8)
        tk.Button(self.frame_atual, text="Modo de Vendas", width=30, height=2, command=self.mostrar_menu_vendas).pack(pady=8)
        tk.Button(self.frame_atual, text="Sair", width=30, height=2, command=self.root.quit).pack(pady=8)

    # -------------------- Admin --------------------
    def mostrar_tela_admin(self):
        self.limpar_tela()
        self.frame_atual = tk.Frame(self.root, padx=20, pady=20)
        self.frame_atual.pack(expand=True, fill="both")

        tk.Label(self.frame_atual, text="Tela do Administrador", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self.frame_atual, text="Adicionar Viagem", command=self.adicionar_viagem).pack(pady=5, fill="x")
        tk.Button(self.frame_atual, text="Editar Viagem", command=self.editar_viagem).pack(pady=5, fill="x")
        tk.Button(self.frame_atual, text="Remover Viagem", command=self.remover_viagem).pack(pady=5, fill="x")
        tk.Button(self.frame_atual, text="Voltar", command=self.mostrar_menu_principal).pack(pady=20)

    def adicionar_viagem(self):
        self.limpar_tela()
        self.frame_atual = tk.Frame(self.root, padx=20, pady=20)
        self.frame_atual.pack(expand=True, fill="both")

        tk.Label(self.frame_atual, text="Origem:").pack(anchor="w")
        entry_origem = tk.Entry(self.frame_atual); entry_origem.pack(fill="x", pady=5)

        tk.Label(self.frame_atual, text="Destino:").pack(anchor="w")
        entry_destino = tk.Entry(self.frame_atual); entry_destino.pack(fill="x", pady=5)

        tk.Label(self.frame_atual, text="Tipo de Ônibus:").pack(anchor="w")
        tipo_onibus = ttk.Combobox(self.frame_atual, values=["Convencional", "Executivo"], state="readonly")
        tipo_onibus.current(0)
        tipo_onibus.pack(fill="x", pady=5)

        tk.Label(self.frame_atual, text="Dias da semana:").pack(anchor="w")
        dias_vars = {}
        dias = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"]
        dias_frame = tk.Frame(self.frame_atual); dias_frame.pack(anchor="w", pady=5)
        for dia in dias:
            var = tk.BooleanVar()
            tk.Checkbutton(dias_frame, text=dia, variable=var).pack(side="left", padx=5)
            dias_vars[dia] = var

        tk.Label(self.frame_atual, text="Horário (HH:MM):").pack(anchor="w")
        entry_horario = tk.Entry(self.frame_atual); entry_horario.pack(fill="x", pady=5)

        tk.Label(self.frame_atual, text="Preço base:").pack(anchor="w")
        entry_preco = tk.Entry(self.frame_atual); entry_preco.pack(fill="x", pady=5)

        def ok():
            origem = entry_origem.get().strip()
            destino = entry_destino.get().strip()
            horario = entry_horario.get().strip()
            preco = entry_preco.get().strip()
            tipo = tipo_onibus.get()
            dias_escolhidos = [d for d, v in dias_vars.items() if v.get()]

            if not origem or not destino or not horario or not preco or not dias_escolhidos:
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return
            try:
                preco = float(preco)
            except ValueError:
                messagebox.showerror("Erro", "Preço inválido!")
                return

            #Exemplo de try para mostrar
            try:
                viagem: Viagem
                viagem = self.admin.cadastrar_viagem(
                    origem, destino, dias_escolhidos, horario, preco, tipo, 
                    "Modelo Padrão", "Fabricante Padrão"
                )
                
                self.vendas = SistemaVendas(self.admin.get_todas_as_viagens())
                messagebox.showinfo("Sucesso", f"Viagem adicionada: {viagem.get_id_viagem()} - {origem} → {destino}")
                self.mostrar_tela_admin()

            except ValorInvalidoError as e:
                messagebox.showerror("Erro de Cadastro", str(e))
            except Exception as e:
                messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

        tk.Button(self.frame_atual, text="OK", command=ok).pack(pady=10)
        tk.Button(self.frame_atual, text="Voltar", command=self.mostrar_tela_admin).pack(pady=10)

    def editar_viagem(self):
        self.limpar_tela()
        self.frame_atual = tk.Frame(self.root, padx=20, pady=20)
        self.frame_atual.pack(expand=True, fill="both")

        viagens = self.admin.get_todas_as_viagens()
        if not viagens:
            tk.Label(self.frame_atual, text="Não há viagens cadastradas").pack(pady=10)
            tk.Button(self.frame_atual, text="Voltar", command=self.mostrar_tela_admin).pack(pady=10)
            return

        tk.Label(self.frame_atual, text="Clique na viagem que quer editar").pack(pady=10)
        conteudo_frame = tk.Frame(self.frame_atual); conteudo_frame.pack()

        def abrir_edicao(viagem):
            self.limpar_tela()
            self.frame_atual = tk.Frame(self.root, padx=20, pady=20)
            self.frame_atual.pack(expand=True, fill="both")

            tk.Label(self.frame_atual, text=f"Editando viagem {viagem.get_id_viagem()}").pack(pady=5)
            tk.Label(self.frame_atual, text="Origem:").pack(anchor="w")
            e_origem = tk.Entry(self.frame_atual); e_origem.insert(0, viagem.get_origem()); e_origem.pack(fill="x", pady=5)
            tk.Label(self.frame_atual, text="Destino:").pack(anchor="w")
            e_dest = tk.Entry(self.frame_atual); e_dest.insert(0, viagem.get_destino()); e_dest.pack(fill="x", pady=5)
            tk.Label(self.frame_atual, text="Horário:").pack(anchor="w")
            e_hor = tk.Entry(self.frame_atual); e_hor.insert(0, viagem.get_hora()); e_hor.pack(fill="x", pady=5)
            tk.Label(self.frame_atual, text="Preço:").pack(anchor="w")
            e_pre = tk.Entry(self.frame_atual); e_pre.insert(0, viagem.get_preco()); e_pre.pack(fill="x", pady=5)

            def salvar_edicao():
                origem_n = e_origem.get().strip()
                destino_n = e_dest.get().strip()
                horario_n = e_hor.get().strip()
                preco_n = e_pre.get().strip()
                if not origem_n or not destino_n or not horario_n or not preco_n:
                    messagebox.showerror("Erro", "Preencha todos os campos!")
                    return
                try:
                    preco_n = float(preco_n)
                except ValueError:
                    messagebox.showerror("Erro", "Preço inválido!")
                    return
                #Exemplo de try
                try:
                    viagem.set_origem(origem_n)
                    viagem.set_destino(destino_n)
                    viagem.set_hora(horario_n)
                    viagem.set_preco(float(preco_n)) # float() pode lançar ValueError
                    
                    messagebox.showinfo("Sucesso", f"Viagem ID {viagem.get_id_viagem()} editada!")
                    self.editar_viagem() # Recarrega a tela de edição

                except (ValorInvalidoError, ValueError) as e:
                    messagebox.showerror("Erro de Edição", str(e))
                except Exception as e:
                    messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

            tk.Button(self.frame_atual, text="Salvar", command=salvar_edicao).pack(pady=10)
            tk.Button(self.frame_atual, text="Voltar", command=self.editar_viagem).pack(pady=10)

        for v in viagens:
            texto = f"ID {v.get_id_viagem()}: {v.get_origem()} → {v.get_destino()} às {v.get_hora()}"
            tk.Button(conteudo_frame, text=texto, command=lambda vi=v: abrir_edicao(vi)).pack(pady=2, fill="x")

        tk.Button(self.frame_atual, text="Voltar", command=self.mostrar_tela_admin).pack(pady=10)

    def remover_viagem(self):
        self.limpar_tela()
        self.frame_atual = tk.Frame(self.root, padx=20, pady=20)
        self.frame_atual.pack(expand=True, fill="both")

        viagens = self.admin.get_todas_as_viagens()
        if not viagens:
            tk.Label(self.frame_atual, text="Não há viagens cadastradas").pack(pady=10)
        else:
            tk.Label(self.frame_atual, text="Clique na viagem que quer remover").pack(pady=10)
            conteudo_frame = tk.Frame(self.frame_atual); conteudo_frame.pack()

            def remover_viagem_btn(viagem):
                if messagebox.askyesno("Confirma", f"Remover viagem ID {viagem.get_id_viagem()}?"):
                    viagens.remove(viagem)
                    self.vendas = SistemaVendas(viagens)
                    messagebox.showinfo("Sucesso", "Viagem removida!")
                    self.remover_viagem()

            for v in viagens:
                texto = f"ID {v.get_id_viagem()}: {v.get_origem()} → {v.get_destino()} às {v.get_hora()}"
                tk.Button(conteudo_frame, text=texto, command=lambda vi=v: remover_viagem_btn(vi)).pack(pady=2, fill="x")

        tk.Button(self.frame_atual, text="Voltar", command=self.mostrar_tela_admin).pack(pady=10)

    # -------------------- Menu de Vendas --------------------
    def mostrar_menu_vendas(self):
        self.limpar_tela()
        self.frame_atual = tk.Frame(self.root, padx=20, pady=20)
        self.frame_atual.pack(expand=True, fill="both")

        tk.Label(self.frame_atual, text="Menu de Vendas", font=("Helvetica", 18)).pack(pady=10)
        tk.Button(self.frame_atual, text="Listar todas as viagens", width=30, command=self.listar_todas_viagens).pack(pady=6)
        tk.Button(self.frame_atual, text="Vender passagem", width=30, command=self.mostrar_tela_vendas).pack(pady=6)
        tk.Button(self.frame_atual, text="Trocar passagem", width=30, command=self.trocar_passagem_iniciar).pack(pady=6)
        tk.Button(self.frame_atual, text="Voltar", width=30, command=self.mostrar_menu_principal).pack(pady=12)

    def listar_todas_viagens(self):
        self.limpar_tela()
        self.frame_atual = tk.Frame(self.root, padx=20, pady=20)
        self.frame_atual.pack(expand=True, fill="both")

        tk.Label(self.frame_atual, text="Todas as Viagens", font=("Helvetica", 16)).pack(pady=10)
        viagens = self.admin.get_todas_as_viagens()
        if not viagens:
            tk.Label(self.frame_atual, text="Nenhuma viagem cadastrada").pack(pady=5)
        else:
            for v in viagens:
                texto = f"ID {v.get_id_viagem()}: {v.get_origem()} → {v.get_destino()} às {v.get_hora()} (R$ {v.get_preco()})"
                tk.Label(self.frame_atual, text=texto).pack(anchor="w")
        tk.Button(self.frame_atual, text="Voltar", command=self.mostrar_menu_vendas).pack(pady=10)

    # -------------------- Busca e venda --------------------
    def mostrar_tela_vendas(self):
        self.limpar_tela()
        self.frame_atual = tk.Frame(self.root, padx=20, pady=20)
        self.frame_atual.pack(expand=True, fill="both")

        tk.Label(self.frame_atual, text="Buscar Viagens", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self.frame_atual, text="Origem:").pack(anchor="w")
        entry_origem = tk.Entry(self.frame_atual); entry_origem.pack(fill="x", pady=5)
        tk.Label(self.frame_atual, text="Destino:").pack(anchor="w")
        entry_destino = tk.Entry(self.frame_atual); entry_destino.pack(fill="x", pady=5)

        status = tk.Label(self.frame_atual, text=""); status.pack()

        def buscar():
            origem = entry_origem.get().strip()
            destino = entry_destino.get().strip()
            viagens = self.vendas.buscar_viagens_disponiveis(origem, destino)
            if not viagens:
                status.config(text="Nenhuma viagem encontrada!", fg="red")
                return
            self.tela_resultado_vendas(viagens)

        tk.Button(self.frame_atual, text="Buscar", command=buscar).pack(pady=10)
        tk.Button(self.frame_atual, text="Voltar", command=self.mostrar_menu_vendas).pack(pady=10)

    def tela_resultado_vendas(self, viagens):
        self.limpar_tela()
        self.frame_atual = tk.Frame(self.root, padx=20, pady=20)
        self.frame_atual.pack(expand=True, fill="both")

        tk.Label(self.frame_atual, text="Viagens Encontradas", font=("Helvetica", 16)).pack(pady=10)
        for viagem in viagens:
            texto = f"ID {viagem.get_id_viagem()}: {viagem.get_origem()} → {viagem.get_destino()} às {viagem.get_hora()} (R$ {viagem.get_preco()})"
            tk.Button(self.frame_atual, text=texto, command=lambda v=viagem: self.tela_vender_passagem(v)).pack(pady=2, fill="x")
        tk.Button(self.frame_atual, text="Voltar", command=self.mostrar_tela_vendas).pack(pady=10)

    # -------------------- Formulário de venda --------------------
    def tela_vender_passagem(self, viagem):
        self.limpar_tela()
        self.frame_atual = tk.Frame(self.root, padx=20, pady=20)
        self.frame_atual.pack(expand=True, fill="both")

        tk.Label(self.frame_atual, text=f"Vendendo passagem - Viagem {viagem.get_id_viagem()}").pack(pady=5)

        campos = ["nome","idade","cpf","email","telefone"]
        entradas = {}
        for campo in campos:
            tk.Label(self.frame_atual, text=f"{campo.capitalize()}:").pack(anchor="w")
            entry = tk.Entry(self.frame_atual); entry.pack(fill="x", pady=3)
            entradas[campo] = entry

        pcd_var = tk.BooleanVar()
        tk.Checkbutton(self.frame_atual, text="PCD", variable=pcd_var).pack(anchor="w", pady=3)

        status = tk.Label(self.frame_atual, text=""); status.pack()

        def continuar_para_assentos():
            dados_passageiro = {}
            try:
                for campo, entry in entradas.items():
                    valor = entry.get().strip()
                    if campo == "idade":
                        if not valor: 
                            raise ValorInvalidoError("O campo 'idade' é obrigatório.")
                        dados_passageiro[campo] = int(valor)
                    else:
                        dados_passageiro[campo] = valor
                dados_passageiro["pcd"] = pcd_var.get()

                Passageiro(
                    nome=dados_passageiro['nome'],
                    idade=dados_passageiro['idade'],
                    cpf=dados_passageiro['cpf'],
                    email=dados_passageiro.get('email', ''),
                    telefone=dados_passageiro.get('telefone', ''),
                    eh_PCD=dados_passageiro['pcd']
                )
                
                self.mostrar_assentos(viagem, dados_passageiro, modo="venda")
            
            except (ValueError, ValorInvalidoError) as e:
                status.config(text=f"Erro: {e}")
            except Exception as e:
                status.config(text=f"Erro inesperado: {e}")

        tk.Button(self.frame_atual, text="Continuar para assentos", command=continuar_para_assentos).pack(pady=10)
        tk.Button(self.frame_atual, text="Voltar", command=lambda: self.tela_resultado_vendas([viagem])).pack(pady=5)

    # -------------------- Mostrar assentos (venda / troca) --------------------
    def mostrar_assentos(self, viagem, dados_passageiro, modo="venda", passagem_para_troca=None):
        """
        modo: "venda" or "troca"
        passagem_para_troca: Passagem object when modo == "troca"
        """
        self.limpar_tela()
        self.frame_atual = tk.Frame(self.root, padx=12, pady=12)
        self.frame_atual.pack(expand=True, fill="both")

        tk.Label(self.frame_atual, text=f"Escolha o assento - Viagem {viagem.get_id_viagem()}").pack(pady=5)
        onibus = viagem.get_onibus()

        botoes = []
        selected = {'btn': None, 'assento': None, 'tipo': None, 'linha': None, 'coluna': None}
        status = tk.Label(self.frame_atual, text=""); status.pack()

        mapa_assentos = {}  # numero_star -> assento_obj
        frame_grid = tk.Frame(self.frame_atual); frame_grid.pack(pady=10)

        # --- Convencional grid (4x12) ---
        if isinstance(onibus, OnibusConvencional):
            assentos = onibus.get_assentos()  # list of Assento
            for a in assentos:
                mapa_assentos[a.get_numero()] = a

            letras = "ABCDEFGHIJKL"
            for row in range(4):  # 1..4
                for col, letra in enumerate(letras):
                    numero = f"{letra}{row+1}"
                    assento_obj = mapa_assentos.get(numero, None)
                    ocupado = assento_obj.get_ocupado() if assento_obj else False
                    cor = "red" if ocupado else "white"
                    state = "disabled" if ocupado else "normal"

                    def make_cmd(a_obj, num_str, typ, li, co):
                        return lambda: selecionar_assento(a_obj, num_str, typ, li, co)

                    btn = tk.Button(frame_grid, text=numero, width=6, height=2, bg=cor, state=state,
                                    command=make_cmd(assento_obj, numero, "Convencional", row, col))
                    btn.grid(row=row, column=col, padx=2, pady=2)
                    btn.assento_numero = numero
                    botoes.append(btn)

        # --- Executivo grid: semi (em cima) + leito (embaixo) ---
        else:
            semi = onibus.get_assentos_semi_leito()   # matrix 4 x 12
            leito = onibus.get_assentos_leito()      # matrix 3 x 4

            # preencher mapa
            for i, linha in enumerate(semi):
                for j, a in enumerate(linha):
                    mapa_assentos[a.get_numero()] = a
            for i, linha in enumerate(leito):
                for j, a in enumerate(linha):
                    mapa_assentos[a.get_numero()] = a

            # desenhar semi
            for i, linha in enumerate(semi):
                for j, assento_obj in enumerate(linha):
                    numero = assento_obj.get_numero()
                    ocupado = assento_obj.get_ocupado()
                    cor = "red" if ocupado else "white"
                    state = "disabled" if ocupado else "normal"

                    def make_cmd(a_obj, num_str, typ, li, co):
                        return lambda: selecionar_assento(a_obj, num_str, typ, li, co)

                    btn = tk.Button(frame_grid, text=numero, width=10, height=2, bg=cor, state=state,
                                    command=make_cmd(assento_obj, numero, "Semi-Leito", i, j))
                    btn.grid(row=i, column=j, padx=2, pady=2)
                    btn.assento_numero = numero
                    botoes.append(btn)

            # desenhar leito abaixo com offset
            offset = len(semi)
            for i, linha in enumerate(leito):
                for j, assento_obj in enumerate(linha):
                    numero = assento_obj.get_numero()
                    ocupado = assento_obj.get_ocupado()
                    cor = "red" if ocupado else "white"
                    state = "disabled" if ocupado else "normal"

                    def make_cmd(a_obj, num_str, typ, li, co):
                        return lambda: selecionar_assento(a_obj, num_str, typ, li, co)

                    btn = tk.Button(frame_grid, text=numero, width=10, height=2, bg=cor, state=state,
                                    command=make_cmd(assento_obj, numero, "Leito", i, j))
                    btn.grid(row=offset + i, column=j, padx=2, pady=2)
                    btn.assento_numero = numero
                    botoes.append(btn)

        # função para seleção única
        def selecionar_assento(assento_obj, numero_str, tipo, li, co):
            if assento_obj and assento_obj.get_ocupado():
                status.config(text="Assento já ocupado!", fg="red")
                return

            # desmarca anterior
            if selected['btn']:
                prev = selected['btn']
                prev_num = getattr(prev, 'assento_numero', None)
                prev_assento = mapa_assentos.get(prev_num)
                prev_bg = "red" if (prev_assento and prev_assento.get_ocupado()) else "white"
                prev.config(bg=prev_bg)

            # marca novo
            for b in botoes:
                if getattr(b, 'assento_numero', None) == numero_str:
                    b.config(bg="green")
                    selected['btn'] = b
                    break

            selected['assento'] = assento_obj
            selected['tipo'] = tipo
            selected['linha'] = li
            selected['coluna'] = co
            status.config(text=f"Selecionado: {numero_str}", fg="black")

        # confirmar (venda ou troca)
        def confirmar():
            if not selected['btn'] and not selected['assento']:
                status.config(text="Escolha um assento!", fg="red")
                return

            # Venda
            if modo == "venda":
                try:
                    if isinstance(onibus, OnibusConvencional):
                        novo_assento_str = selected['btn'].assento_numero
                        resultado = self.vendas.vender_passagem(
                            viagem, dados_passageiro, novo_assento_str=novo_assento_str
                        )
                    else: # É um OnibusExecutivo
                        resultado = self.vendas.vender_passagem(
                            viagem, dados_passageiro,
                            tipo_assento=selected['tipo'],
                            linha=selected['linha'],
                            coluna=selected['coluna']
                        )

                    messagebox.showinfo("Sucesso", f"Passagem vendida! Bilhete: {resultado.get_bilhete()}")
                    self.mostrar_menu_vendas()

                except (ValorInvalidoError, AssentoInvalidoError, AssentoOcupadoError) as e:
                    status.config(text=f"Erro na venda: {e}", fg="red")
                except NotImplementedError:
                    status.config(text="Erro: Venda para Executivo ainda não implementada no sistema.", fg="red")
                except Exception as e:
                    status.config(text=f"Erro inesperado: {e}", fg="red")
                return

            # Troca
            if modo == "troca":
                try:
                    bilhete = passagem_para_troca.get_bilhete()
        
                    if isinstance(onibus, OnibusConvencional):
                        novo_assento: Assento
                        novo_assento = selected['btn'].assento_numero
                        res = self.vendas.trocar_passagem(bilhete, viagem, novo_assento_str=novo_assento)
                    else: # OnibusExecutivo
                        res = self.vendas.trocar_passagem(
                            bilhete, viagem,
                            tipo_assento=selected['tipo'],
                            linha=selected['linha'],
                            coluna=selected['coluna']
                        )

                    messagebox.showinfo("Sucesso", f"Troca realizada! Bilhete: {res.get_bilhete()}")
                    self.mostrar_menu_vendas()
                
                except (BilheteNaoEncontradoError, ValorInvalidoError, AssentoInvalidoError, AssentoOcupadoError) as e:
                    status.config(text=f"Erro na troca: {e}", fg="red")
                except Exception as e:
                    status.config(text=f"Erro inesperado: {e}", fg="red")
                return

        tk.Button(self.frame_atual, text="Confirmar", command=confirmar).pack(pady=8)
        tk.Button(self.frame_atual, text="Voltar", command=lambda: self.mostrar_menu_vendas()).pack(pady=5)

    # -------------------- Trocar passagem (início) --------------------
    def trocar_passagem_iniciar(self):
        self.limpar_tela()
        self.frame_atual = tk.Frame(self.root, padx=20, pady=20)
        self.frame_atual.pack(expand=True, fill="both")

        tk.Label(self.frame_atual, text="Trocar Passagem - Informe o número do bilhete").pack(pady=10)
        entry_bilhete = tk.Entry(self.frame_atual); entry_bilhete.pack(fill="x", pady=5)
        status = tk.Label(self.frame_atual, text=""); status.pack()

        def buscar_bilhete():
            bilhete = entry_bilhete.get().strip()
            if not bilhete:
                status.config(text="Informe o bilhete!", fg="red")
                return
            try:
                passagem = self.vendas.buscar_passagem_por_bilhete(bilhete)
                self.mostrar_viagens_para_troca(passagem)
            except BilheteNaoEncontradoError as e:
                # Captura o erro se o bilhete não for encontrado
                status.config(text=str(e), fg="red")
            except Exception as e:
                status.config(text=f"Erro inesperado: {e}", fg="red")

        tk.Button(self.frame_atual, text="Buscar", command=buscar_bilhete).pack(pady=8)
        tk.Button(self.frame_atual, text="Voltar", command=self.mostrar_menu_vendas).pack(pady=6)

    def mostrar_viagens_para_troca(self, passagem):
        self.limpar_tela()
        self.frame_atual = tk.Frame(self.root, padx=20, pady=20)
        self.frame_atual.pack(expand=True, fill="both")

        tk.Label(self.frame_atual, text=f"Bilhete: {passagem.get_bilhete()} - Passageiro: {passagem.get_passageiro().get_nome()}").pack(pady=6)
        tk.Label(self.frame_atual, text="Escolha a nova viagem:").pack(pady=6)

        viagens = self.admin.get_todas_as_viagens()
        for v in viagens:
            texto = f"ID {v.get_id_viagem()}: {v.get_origem()} → {v.get_destino()} às {v.get_hora()} (R$ {v.get_preco()})"
            # ao clicar, chamamos mostrar_assentos em modo "troca" com os dados do passageiro preenchidos
            def make_cmd(viagem_obj, passagem_obj):
                def cmd():
                    dados = {
                        'nome': passagem_obj.get_passageiro().get_nome(),
                        'idade': passagem_obj.get_passageiro().get_idade(),
                        'cpf': passagem_obj.get_passageiro().get_cpf(),
                        'email': passagem_obj.get_passageiro().get_email(),
                        'telefone': passagem_obj.get_passageiro().get_telefone(),
                        'pcd': passagem_obj.get_passageiro().get_eh_PCD()
                    }
                    self.mostrar_assentos(viagem_obj, dados, modo="troca", passagem_para_troca=passagem_obj)
                return cmd
            tk.Button(self.frame_atual, text=texto, command=make_cmd(v, passagem)).pack(pady=3, fill="x")

        tk.Button(self.frame_atual, text="Voltar", command=self.mostrar_menu_vendas).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceApp(root)
    root.mainloop()
