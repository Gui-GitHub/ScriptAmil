import os, sys
import tkinter
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import re
import mysql.connector
from config.config import conectar_db
from dotenv import load_dotenv

# Descobre a pasta onde o .env está (no .exe fica em _MEIPASS)
if getattr(sys, 'frozen', False):  # quando rodar no .exe
    BASE_DIR = sys._MEIPASS
else:  # quando rodar como script Python normal
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Carrega o .env da pasta encontrada
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)

def abrir_editar_senha(janela_pai, empresa_selecionada):
    """Abre a janela para alteração de senha da empresa selecionada."""
    janela_pai.withdraw()
    nova_alterar = tkinter.Toplevel()
    nova_alterar.attributes('-fullscreen', False)
    nova_alterar.title("Alterar senha")
    nova_alterar.geometry('854x480')
    nova_alterar.configure(bg='#292942')
    nova_alterar.grab_set()
    nova_alterar.resizable(False, False)
    nova_alterar.protocol("WM_DELETE_WINDOW", lambda: ao_fechar(nova_alterar, janela_pai))
    centralizar_janela(nova_alterar)

    def listar_senha_empresas(nome_empresa):
        """Retorna a senha atual da empresa informada."""
        conexao = conectar_db()
        cursor = conexao.cursor()
        cursor.execute("SELECT senha_empresa FROM tabela_empresas WHERE nome_empresa = %s", (nome_empresa,))
        senha = cursor.fetchone()[0]
        cursor.close()
        conexao.close()
        return senha

    def voltar_janela():
        """Fecha a janela de alteração de senha e retorna para a anterior."""
        nova_alterar.destroy()
        janela_pai.deiconify()

    def verificar_senha():
        """Valida os campos e executa a troca de senha se estiver tudo correto."""
        senha_atual = entry_senha_atual.get().strip()
        senha_nova = entry_senha_nova.get().strip()
        confirmar_senha = entry_confirmar_senha.get().strip()

        if not senha_atual or not senha_nova or not confirmar_senha:
            messagebox.showerror("Atenção!", "Todos os campos devem ser preenchidos.")
            return
        senha_banco = listar_senha_empresas(empresa_selecionada)

        if senha_atual == senha_banco:
            if senha_nova == confirmar_senha:
                if validar_senhas(senha_atual, senha_nova, confirmar_senha):
                    atualizar_senha(empresa_selecionada, senha_nova)
                else:
                    messagebox.showerror("Erro!", "A nova senha não atende os critérios.")
            else:
                messagebox.showerror("Erro!", "A nova senha e a confirmação não coincidem.")
        else:
            messagebox.showerror("Erro!", "A senha atual está incorreta.")

    def atualizar_senha(nome_empresa, nova_senha):
        """Atualiza a senha da empresa no banco de dados."""
        conexao = conectar_db()
        if conexao is None:
            return
        try:
            cursor = conexao.cursor()
            cursor.execute("UPDATE tabela_empresas SET senha_empresa = %s WHERE nome_empresa = %s", (nova_senha, nome_empresa))
            conexao.commit()
            messagebox.showinfo("Sucesso!", "Senha atualizada com sucesso!")
            voltar_janela()
        except mysql.connector.Error as e:
            print(f"Erro ao atualizar a senha: {e}")
            messagebox.showerror("Erro", "Não foi possível atualizar a senha.")
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

    def validar_senhas(senha_atual, senha_nova, confirmar_senha):
        """Valida se a nova senha atende aos critérios de segurança."""
        if senha_nova == senha_atual or confirmar_senha == senha_atual:
            messagebox.showerror("Erro!", "A nova senha não pode ser igual a anterior.")
            return False
        # if len(senha_nova) < 6 or len(confirmar_senha) < 6:
        #     messagebox.showerror("Erro!", "As senhas devem conter no mínimo 6 caracteres.")
        #     return False
        # if len(senha_nova) > 10 or len(confirmar_senha) > 10:
        #     messagebox.showerror("Erro!", "As senhas devem conter no máximo 10 caracteres.")
        #     return False
        if not re.search(r"[a-z]", senha_nova) or not re.search(r"[a-z]", confirmar_senha):
            messagebox.showerror("Erro!", "As senhas devem conter pelo menos uma letra minúscula.")
            return False
        if not re.search(r"[A-Z]", senha_nova) or not re.search(r"[A-Z]", confirmar_senha):
            messagebox.showerror("Erro!", "As senhas devem conter pelo menos uma letra maiúscula.")
            return False
        if not re.search(r"[0-9]", senha_nova) or not re.search(r"[0-9]", confirmar_senha):
            messagebox.showerror("Erro!", "As senhas devem conter pelo menos um número.")
            return False
        # if not re.search(r"[\W_]", senha_nova) or not re.search(r"[\W_]", confirmar_senha):
        #     messagebox.showerror("Erro!", "As senhas devem conter pelo menos um caractere especial.")
        #     return False
        return True

    style2 = ttk.Style()
    style2.theme_use('clam')
    style2.configure("alterar_style2.TLabel", background="#292942", foreground="#3E14FF", font=("Montserrat", 25, "bold"))
    style2.configure("alterar_style2-1.TLabel", background="#292942", foreground="#E0E0E0", font=("Montserrat", 12))
    style2.configure("alterar_style2-2.TLabel", background="#292942", foreground="#E0E0E0", font=("Montserrat", 8))
    style2.configure("alterar_style2-3.TLabel", background="#292942", foreground="#E0E0E0", font=("Montserrat", 10))
    style2.configure("alterar_style2.TEntry", background="#292942", foreground="#22223b", fieldbackground="#f3f3fa", font=("Montserrat", 12))
    style2.configure("alterar_style2.TButton", background="#4f4fa6", foreground="#FFFFFF", font=("Montserrat", 12, "bold"))
    style2.map("alterar_style2.TButton",
        background=[("active", "#3E14FF")],
        foreground=[("active", "#FFFFFF")])
    style2.configure("alterar_style2-voltar.TButton", background="#292942", foreground="#969696", font=("Montserrat", 12), width=5)
    style2.configure("alterar_style2-alternar.TButton", relief="flat", background="#292942", foreground="#969696", padding=(10, 5), borderwidth=0, highlightthickness=0, focusthickness=0, font=("Montserrat", 10))
    style2.map("alterar_style2-alternar.TButton", relief=[("active", "flat")], borderwidth=[("active", 0)], highlightthickness=[("active", 0)], background=[("active", "#555555")], foreground=[("active", "#FFFFFF")])

    botao_voltar = ttk.Button(nova_alterar, text="Voltar", style="alterar_style2-voltar.TButton", command=voltar_janela)
    botao_voltar.place(x=30, y=40)

    label_alterar_senha = ttk.Label(nova_alterar, text="Alterar Senha", style="alterar_style2.TLabel")
    label_alterar_senha.place(x=315, y=50)

    label_empresa_selecionado = ttk.Label(nova_alterar, text=f"Empresa Selecionada: {empresa_selecionada}", style="alterar_style2-1.TLabel")
    label_empresa_selecionado.place(x=290, y=100)

    label_senha_atual = ttk.Label(nova_alterar, text="Senha atual:", style="alterar_style2-1.TLabel")
    label_senha_atual.place(x=333, y=150)
    entry_senha_atual = ttk.Entry(nova_alterar, style="alterar_style2.TEntry", width=30)
    entry_senha_atual.place(x=333, y=180)

    label_senha_nova = ttk.Label(nova_alterar, text="Nova senha:", style="alterar_style2-1.TLabel")
    label_senha_nova.place(x=333, y=210)
    entry_senha_nova = ttk.Entry(nova_alterar, style="alterar_style2.TEntry", width=30)
    entry_senha_nova.place(x=333, y=240)

    label_regras = ttk.Label(nova_alterar, text="As senhas devem conter:", style="alterar_style2-3.TLabel")
    label_regras.place(x=162, y=230)
    label_regras1 = ttk.Label(nova_alterar, text="(1) - Letra Maíuscula;\n(1) - Letra Minúscula;\n(1) - Número;", style="alterar_style2-2.TLabel")
    label_regras1.place(x=162, y=250)
    label_regras = ttk.Label(nova_alterar, text="Recomendado:", style="alterar_style2-3.TLabel")
    label_regras.place(x=550, y=230)
    label_regras1 = ttk.Label(nova_alterar, text="No mínimo 6 caracteres;\nNo máximo 10 caracteres;\n(1) - Caractere Especial.", style="alterar_style2-2.TLabel")
    label_regras1.place(x=550, y=250)

    label_confirmar_senha = ttk.Label(nova_alterar, text="Confirmar senha:", style="alterar_style2-1.TLabel")
    label_confirmar_senha.place(x=333, y=270)
    entry_confirmar_senha = ttk.Entry(nova_alterar, style="alterar_style2.TEntry", width=30)
    entry_confirmar_senha.place(x=333, y=300)

    botao_confirmar = ttk.Button(nova_alterar, text="Confirmar", style="alterar_style2.TButton", command=verificar_senha)
    botao_confirmar.place(x=358, y=365)

    icone_mostrar_img = Image.open(os.getenv('CAMINHO') + '\\imgs\\pngs\\eye.png')
    icone_mostrar_img = icone_mostrar_img.resize((12, 12), Image.LANCZOS)
    icone_mostrar = ImageTk.PhotoImage(icone_mostrar_img)

    icone_esconder_img = Image.open(os.getenv('CAMINHO') + '\\imgs\\pngs\\closed-eye.png')
    icone_esconder_img = icone_esconder_img.resize((12, 12), Image.LANCZOS)
    icone_esconder = ImageTk.PhotoImage(icone_esconder_img)

    def alternar_visao():
        """Alterna a visualização dos campos de senha entre visível e oculto."""
        if entry_senha_atual.cget('show') == '':
            entry_senha_atual.config(show='*')
            entry_senha_nova.config(show='*')
            entry_confirmar_senha.config(show='*')
            botao_alternar_visao.config(image=icone_mostrar)
        else:
            entry_senha_atual.config(show='')
            entry_senha_nova.config(show='')
            entry_confirmar_senha.config(show='')
            botao_alternar_visao.config(image=icone_esconder)

    botao_alternar_visao = ttk.Button(nova_alterar, image=icone_esconder, style="alterar_style2-alternar.TButton", command=alternar_visao)
    botao_alternar_visao.place(x=300, y=180)

    def focus_out(event):
        """Remove o foco do botão de alternar visão após o clique."""
        event.widget.master.focus()

    botao_alternar_visao.bind("<ButtonRelease-1>", focus_out)

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
