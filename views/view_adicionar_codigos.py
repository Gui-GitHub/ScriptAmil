import tkinter
from tkinter import ttk, messagebox
from config.config import conectar_db
from .auth_utils import validar_senha_mestra

def abrir_adicionar_codigos(nova, nome_empresa):
    """Abre a janela para adicionar códigos a uma empresa existente."""

    # Validar senha mestra
    if not validar_senha_mestra("Digite a senha mestra para adicionar códigos:"):
        return
    
    # Buscar códigos atuais da empresa
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT codigos_empresa FROM tabela_empresas WHERE nome_empresa = %s",
        (nome_empresa,)
    )
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()

    codigos_existentes = resultado[0] if resultado and resultado[0] else ""

    # Nova janela
    cod_win = tkinter.Toplevel(nova)
    cod_win.title(f"Adicionar Códigos - {nome_empresa}")
    cod_win.configure(bg="#292942")
    cod_win.resizable(False, False)

    largura, altura = 500, 320
    largura_tela = cod_win.winfo_screenwidth()
    altura_tela = cod_win.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    cod_win.geometry(f"{largura}x{altura}+{x}+{y}")

    # Mostrar códigos já existentes
    lbl_existentes = tkinter.Label(
        cod_win, text="Códigos atuais:", fg="white", bg="#292942", anchor="w", font=("Segoe UI", 10, "bold")
    )
    lbl_existentes.pack(pady=(15, 5), padx=10, anchor="w")

    txt_existentes = tkinter.Text(cod_win, wrap="word", height=5, font=("Consolas", 10),
                                  bg="#f3f3fa", fg="#22223b")
    txt_existentes.insert("1.0", codigos_existentes)
    txt_existentes.config(state="disabled")
    txt_existentes.pack(fill="both", padx=10, pady=(0, 10), expand=False)

    # Campo para novos códigos
    lbl_novos = tkinter.Label(
        cod_win, text="Novos códigos (separe por vírgula):",
        fg="white", bg="#292942", anchor="w", font=("Segoe UI", 10, "bold")
    )
    lbl_novos.pack(pady=(5, 5), padx=10, anchor="w")

    entry_novos = ttk.Entry(cod_win, width=60)
    entry_novos.pack(padx=10, pady=(0, 15))

    # Função para salvar no banco
    def salvar_codigos():
        novos_codigos = entry_novos.get().strip()
        if not novos_codigos:
            messagebox.showwarning("Atenção", "Digite pelo menos um código para adicionar.")
            return

        # Concatena com os existentes (se houver)
        codigos_final = codigos_existentes.strip()
        if codigos_final:
            codigos_final += "," + novos_codigos
        else:
            codigos_final = novos_codigos

        try:
            conexao = conectar_db()
            cursor = conexao.cursor()
            cursor.execute(
                "UPDATE tabela_empresas SET codigos_empresa = %s WHERE nome_empresa = %s",
                (codigos_final, nome_empresa)
            )
            conexao.commit()
            cursor.close()
            conexao.close()

            messagebox.showinfo("Sucesso", f"Códigos adicionados à empresa '{nome_empresa}' com sucesso!")
            cod_win.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível atualizar os códigos.\n{e}")

    # Botões
    botoes_frame = tkinter.Frame(cod_win, bg="#292942")
    botoes_frame.pack(pady=10, fill="x")

    botao_salvar = ttk.Button(botoes_frame, text="Salvar", style="editar_style1.TButton", command=salvar_codigos)
    botao_salvar.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    botao_cancelar = ttk.Button(botoes_frame, text="Cancelar", style="editar_style1.TButton", command=cod_win.destroy)
    botao_cancelar.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    botoes_frame.grid_columnconfigure(0, weight=1)
    botoes_frame.grid_columnconfigure(1, weight=1)
