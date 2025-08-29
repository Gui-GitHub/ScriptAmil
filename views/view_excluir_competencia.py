import tkinter as tk
from tkinter import messagebox, Listbox, MULTIPLE, Toplevel
from config.config import conectar_db
from .auth_utils import validar_senha_mestra

def view_excluir_competencias(root, nome_empresa):
    """View para listar e excluir códigos de uma empresa específica."""

    # Validação da senha mestra
    if not validar_senha_mestra("Digite a senha mestra para excluir códigos:"):
        return

    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute("SELECT codigos_empresa FROM tabela_empresas WHERE nome_empresa = %s", (nome_empresa,))
    resultado = cursor.fetchone()

    if not resultado or not resultado[0]:
        messagebox.showinfo("Atenção!", f"A empresa '{nome_empresa}' não possui códigos cadastrados.")
        return

    codigos = [c.strip() for c in resultado[0].split(",")]

    # Cria janela
    janela = Toplevel(root)
    janela.title(f"Remover códigos de {nome_empresa}")

    largura = 300
    altura = 300

    # pega largura/altura da tela
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    # calcula posição central
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)

    # aplica geometry centralizada
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    tk.Label(janela, text=f"Códigos da empresa: {nome_empresa}", font=("Arial", 10, "bold")).pack(pady=5)

    listbox_codigos = Listbox(janela, selectmode=MULTIPLE, width=30, height=10)
    listbox_codigos.pack(padx=10, pady=5)

    for codigo in codigos:
        listbox_codigos.insert(tk.END, codigo)

    def confirmar_remocao():
        selecionados = [listbox_codigos.get(i) for i in listbox_codigos.curselection()]
        if not selecionados:
            messagebox.showwarning("Atenção!", "Nenhum código foi selecionado.")
            return

        novos_codigos = [c for c in codigos if c not in selecionados]
        novos_codigos_str = ", ".join(novos_codigos) if novos_codigos else None

        # 🔹 Abre conexão só agora para atualizar
        conexao = conectar_db()
        cursor = conexao.cursor()
        cursor.execute("UPDATE tabela_empresas SET codigos_empresa = %s WHERE nome_empresa = %s",
                       (novos_codigos_str, nome_empresa))
        conexao.commit()
        cursor.close()
        conexao.close()

        messagebox.showinfo("Sucesso!", f"Códigos {', '.join(selecionados)} removidos da empresa '{nome_empresa}'.")
        janela.destroy()

    tk.Button(janela, text="Remover selecionados", command=confirmar_remocao).pack(pady=10)

    janela.transient(root)
    janela.grab_set()
    janela.focus()