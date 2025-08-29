import tkinter
from tkinter import ttk, messagebox
from config.config import conectar_db
from .auth_utils import validar_senha_mestra
from .view_alterar_senha import abrir_editar_senha
from .view_excluir_competencia import view_excluir_competencias
from .view_info_empresa import abrir_informacao_empresa
from .view_adicionar_empresa import abrir_adicionar_empresa
from .view_adicionar_codigos import abrir_adicionar_codigos

def abrir_editar(janela):
    """Abre a janela principal de edição de empresas."""
    janela.withdraw()
    nova = tkinter.Toplevel()
    nova.attributes('-fullscreen', False)
    nova.title("Editar")
    nova.geometry('900x555')
    nova.configure(bg='#292942')
    nova.grab_set()
    nova.resizable(False, False)
    nova.protocol("WM_DELETE_WINDOW", lambda: ao_fechar(nova, janela))
    centralizar_janela(nova)

    ''' Estilizações Janela Editar Empresas '''
    style1 = ttk.Style() 
    style1.theme_use('clam')
    style1.configure("editar_style1.TLabel", background="#292942", foreground="#3E14FF", font=("Montserrat", 25, "bold"))
    style1.configure("editar_style1-2.TLabel", background="#292942", foreground="#E0E0E0", font=("Montserrat", 16))
    style1.configure("editar_style1.TButton", background="#4f4fa6", foreground="#FFFFFF", font=("Montserrat", 12, "bold"), width=13, borderwidth=0)
    style1.map("editar_style1.TButton",
        background=[("active", "#3E14FF")],
        foreground=[("active", "#FFFFFF")])
    style1.configure("editar_style1_voltar.TButton", background="#292942", foreground="#969696", font=("Montserrat", 12), width=5)

    def carregar_empresas(listbox):
        """Carrega os nomes das empresas no listbox."""
        conexao = conectar_db()
        cursor = conexao.cursor()
        cursor.execute("SELECT nome_empresa FROM tabela_empresas")
        empresas = cursor.fetchall()
        for empresa in empresas: 
             
            listbox.insert(tkinter.END, empresa[0])
        cursor.close()
        conexao.close()
    
    def alterar_senha():
        """Verifica se uma empresa foi selecionada para alterar a SENHA."""
        empresa_selecionada = listbox_empresas.curselection()
        if not empresa_selecionada:
            messagebox.showwarning("Atenção", "Selecione uma empresa para prosseguir.")
            return
        nome_empresa = listbox_empresas.get(empresa_selecionada)
        abrir_editar_senha(nova, nome_empresa)  # Chama a função da view

    def mostrar_info_empresa():
        """Exibe informações da empresa selecionada após senha mestra, chamando a nova view."""
        empresa_selecionada = listbox_empresas.curselection()
        if not empresa_selecionada:
            messagebox.showwarning("Atenção", "Selecione uma empresa para ver informações.")
            return

        nome_empresa = listbox_empresas.get(empresa_selecionada)
        abrir_informacao_empresa(nova, nome_empresa)  # Chama a função da view

    def remover_codigos_empresa():
        """Abre a view para excluir códigos da empresa selecionada."""
        empresa_selecionada = listbox_empresas.curselection()
        if not empresa_selecionada:
            messagebox.showwarning("Atenção", "Selecione uma empresa para prosseguir.")
            return
        
        nome_empresa = listbox_empresas.get(empresa_selecionada)
        view_excluir_competencias(nova, nome_empresa)  # Chama a view
            
    def voltar_janela():
        """Fecha a janela atual e retorna para a anterior."""
        nova.destroy()
        janela.deiconify()
    
    def excluir_empresa():    
        """Exclui a empresa selecionada do banco de dados."""
        empresa_selecionada = listbox_empresas.curselection()
        if not empresa_selecionada:
            messagebox.showwarning("Atenção!", "Selecione uma empresa para prosseguir.")
            return

        nome_empresa = listbox_empresas.get(empresa_selecionada)

        # Validar senha mestra
        if not validar_senha_mestra("Digite a senha mestra para excluir a empresa:"):
            return

        # Confirmar exclusão
        resposta = messagebox.askquestion("Atenção!", f"Você realmente deseja excluir a empresa '{nome_empresa}'?")
        if resposta != 'yes':
            messagebox.showinfo("Ação cancelada!", f"A empresa '{nome_empresa}' não foi excluída.")
            return

        # Excluir do banco
        conexao = conectar_db()
        cursor = conexao.cursor()
        try:
            cursor.execute("DELETE FROM tabela_empresas WHERE nome_empresa = %s", (nome_empresa,))
            conexao.commit()
            messagebox.showinfo("Sucesso!", f"A empresa '{nome_empresa}' foi excluída com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro!", f"Não foi possível excluir a empresa.\n{e}")
        finally:
            cursor.close()
            conexao.close()

    def adicionar_empresa():
        """Chama a view para adicionar uma nova empresa."""
        abrir_adicionar_empresa(nova)  # Chama a função da view

    def adicionar_codigos():
        """Chama a view para adicionar códigos a uma empresa já existente."""
        empresa_selecionada = listbox_empresas.curselection()
        if not empresa_selecionada:
            messagebox.showwarning("Atenção", "Selecione uma empresa para adicionar códigos.")
            return

        nome_empresa = listbox_empresas.get(empresa_selecionada)
        abrir_adicionar_codigos(nova, nome_empresa)  # Chama a view

    ''' Bloco de Lista de Empresas '''
    lista_frame = tkinter.LabelFrame(nova, text="Empresas", bg="#292942", fg="#FFFFFF",
                                     font=("Montserrat", 12, "bold"), bd=2, relief="groove", labelanchor="n")
    lista_frame.place(x=280, y=100, width=350, height=200)

    listbox_empresas = tkinter.Listbox(
        lista_frame,
        bg="#f3f3fa",
        fg="#22223b",
        font=("Montserrat", 11),
        highlightbackground="#3E14FF",
        selectbackground="#3E14FF",
        selectforeground="#FFFFFF"
    )
    scrollbar = tkinter.Scrollbar(lista_frame, orient="vertical", command=listbox_empresas.yview)
    listbox_empresas.config(yscrollcommand=scrollbar.set)

    listbox_empresas.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
    scrollbar.pack(side="right", fill="y", pady=10)

    carregar_empresas(listbox_empresas)

    ''' Botões acima da lista (em grid lado a lado) '''
    botoes_frame = tkinter.Frame(nova, bg="#292942")
    botoes_frame.place(x=280, y=310, width=350)

    botao_alterar_senha = ttk.Button(
        botoes_frame, text="Alterar senha", style="editar_style1.TButton", command=alterar_senha
    )
    botao_alterar_senha.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    botao_ver_info = ttk.Button(
        botoes_frame, text="Ver informações", style="editar_style1.TButton", command=mostrar_info_empresa
    )
    botao_ver_info.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    botoes_frame.grid_columnconfigure(0, weight=1)
    botoes_frame.grid_columnconfigure(1, weight=1)

    botao_voltar = ttk.Button(nova, text="Voltar", style="editar_style1_voltar.TButton", command=voltar_janela)
    botao_voltar.place(x=30, y=40)

    ''' Botões de baixo (adicionar/remover) continuam como grid lado a lado) '''
    botoes_codigos_frame = tkinter.Frame(nova, bg="#292942")
    botoes_codigos_frame.place(x=280, y=380, width=350)

    botao_add_codigo = ttk.Button(botoes_codigos_frame, text="Adicionar códigos",
                                  style="editar_style1.TButton", command=adicionar_codigos)
    botao_add_codigo.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    botao_remover_codigo = ttk.Button(botoes_codigos_frame, text="Remover códigos",
                                      style="editar_style1.TButton", command=remover_codigos_empresa)
    botao_remover_codigo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    botoes_empresas_frame = tkinter.Frame(nova, bg="#292942")
    botoes_empresas_frame.place(x=280, y=450, width=350)

    botao_add_empresa = ttk.Button(botoes_empresas_frame, text="Adicionar empresa",
                                   style="editar_style1.TButton", command=adicionar_empresa)
    botao_add_empresa.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    botao_remover_empresa = ttk.Button(botoes_empresas_frame, text="Excluir empresa",
                                       style="editar_style1.TButton", command=excluir_empresa)
    botao_remover_empresa.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    botoes_codigos_frame.grid_columnconfigure(0, weight=1)
    botoes_codigos_frame.grid_columnconfigure(1, weight=1)
    botoes_empresas_frame.grid_columnconfigure(0, weight=1)
    botoes_empresas_frame.grid_columnconfigure(1, weight=1)

def centralizar_janela(janela):
    """Centraliza a janela na tela."""
    janela.update_idletasks()
    largura_janela = janela.winfo_width()
    altura_janela = janela.winfo_height()
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela // 2) - (largura_janela // 2)
    y = (altura_tela // 2) - (altura_janela // 2)
    janela.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')

def ao_fechar(nova, janela):
    """Fecha a janela atual e libera o foco para a anterior."""
    nova.grab_release()
    nova.destroy()
    janela.deiconify()