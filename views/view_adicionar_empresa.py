import tkinter
from tkinter import ttk, messagebox
from config.config import conectar_db
from .auth_utils import validar_senha_mestra

def abrir_adicionar_empresa(nova):
    """Abre janela para adicionar uma nova empresa, pedindo senha mestra."""

    # Validação da senha mestra
    if not validar_senha_mestra("Digite a senha mestra para adicionar uma empresa:"):
        return

    # Criar nova janela
    add_win = tkinter.Toplevel(nova)
    add_win.title("Adicionar Empresa")
    add_win.configure(bg="#292942")
    add_win.resizable(False, False)

    largura, altura = 450, 300
    largura_tela = add_win.winfo_screenwidth()
    altura_tela = add_win.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    add_win.geometry(f"{largura}x{altura}+{x}+{y}")

    # Labels + Entradas
    frame = tkinter.Frame(add_win, bg="#292942")
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    labels = ["Nome da Empresa", "Login", "Senha", "Códigos (separados por vírgula)"]
    entradas = {}

    for i, texto in enumerate(labels):
        lbl = tkinter.Label(frame, text=texto, fg="white", bg="#292942", anchor="w", font=("Segoe UI", 10, "bold"))
        lbl.grid(row=i, column=0, sticky="w", pady=5)

        ent = ttk.Entry(frame, width=40)
        ent.grid(row=i, column=1, pady=5, padx=5)
        entradas[texto] = ent

    # Função para salvar no banco
    def salvar_empresa():
        nome_empresa = entradas["Nome da Empresa"].get().strip()
        login_empresa = entradas["Login"].get().strip()
        senha_empresa = entradas["Senha"].get().strip()
        codigos_empresa = entradas["Códigos (separados por vírgula)"].get().strip()

        if not nome_empresa or not login_empresa or not senha_empresa:
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
            return

        try:
            conexao = conectar_db()
            cursor = conexao.cursor()
            cursor.execute(
                """
                INSERT INTO `rvwebaut_cotacao`.`tabela_empresas`
                (`nome_empresa`, `login_empresa`, `senha_empresa`, `codigos_empresa`)
                VALUES (%s, %s, %s, %s)
                """,
                (nome_empresa, login_empresa, senha_empresa, codigos_empresa)
            )
            conexao.commit()
            cursor.close()
            conexao.close()

            messagebox.showinfo("Sucesso", f"Empresa '{nome_empresa}' adicionada com sucesso!")
            add_win.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível adicionar a empresa.\n{e}")

    # Botões
    botoes_frame = tkinter.Frame(add_win, bg="#292942")
    botoes_frame.pack(pady=15, fill="x")

    botao_salvar = ttk.Button(botoes_frame, text="Salvar", style="editar_style1.TButton", command=salvar_empresa)
    botao_salvar.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    botao_cancelar = ttk.Button(botoes_frame, text="Cancelar", style="editar_style1.TButton", command=add_win.destroy)
    botao_cancelar.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    botoes_frame.grid_columnconfigure(0, weight=1)
    botoes_frame.grid_columnconfigure(1, weight=1)
