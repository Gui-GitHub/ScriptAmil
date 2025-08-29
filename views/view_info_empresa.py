import tkinter
from tkinter import ttk, messagebox
from config.config import conectar_db
from .auth_utils import validar_senha_mestra

def abrir_informacao_empresa(nova, nome_empresa):
    """Abre a janela com informações da empresa, pedindo senha mestra."""

    # Validar senha mestra
    if not validar_senha_mestra("Digite a senha mestra para informações da empresa:"):
        return

    # Busca informações da empresa
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT nome_empresa, login_empresa, senha_empresa, codigos_empresa FROM tabela_empresas WHERE nome_empresa = %s",
        (nome_empresa,)
    )
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()

    if resultado:
        nome, login, senha, codigos = resultado
        codigos = codigos if codigos else ""
        info = (
            f"Nome: {nome}\n"
            f"Login: {login}\n"
            f"Senha: {senha}\n"
            f"Códigos: {codigos}"
        )

        # Nova janela para exibir informações copiáveis
        info_win = tkinter.Toplevel(nova)
        info_win.title("Informações da Empresa")
        info_win.configure(bg="#292942")
        info_win.resizable(True, True)

        # Define tamanho fixo
        largura, altura = 500, 300
        largura_tela = info_win.winfo_screenwidth()
        altura_tela = info_win.winfo_screenheight()
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
        info_win.geometry(f"{largura}x{altura}+{x}+{y}")

        # Texto copiável
        text = tkinter.Text(info_win, wrap="word", font=("Consolas", 11), bg="#f3f3fa", fg="#22223b")
        text.insert("1.0", info)
        text.config(state="normal")
        text.pack(expand=True, fill="both", padx=10, pady=10)
        text.focus_set()

        # Botão fechar
        ttk.Button(info_win, text="Fechar", command=info_win.destroy).pack(pady=5)

    else:
        messagebox.showerror("Erro", "Empresa não encontrada.")