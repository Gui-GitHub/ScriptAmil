import sys
import os
import re
import tkinter
from tkinter import PhotoImage, messagebox, Menu, ttk
from config.config import conectar_db
from .view_editar_empresas import abrir_editar
from .automacao_amil import iniciar_script
from dotenv import load_dotenv

# Descobre a pasta onde o .env está (no .exe fica em _MEIPASS)
if getattr(sys, 'frozen', False):  # quando rodar no .exe
    BASE_DIR = sys._MEIPASS
else:  # quando rodar como script Python normal
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Carrega o .env da pasta encontrada
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)

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

def fechar_janela(janela):
    """Fecha a janela principal com confirmação do usuário."""
    if messagebox.askokcancel("Fechar", "Você deseja relmente fechar?"):
        janela.destroy()
        sys.exit()
    else:
        janela.deiconify()

def resource_path(relative_path):
    """Retorna o caminho absoluto para recursos, compatível com PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def selecionar_empresa(nome, label_empresa_selecionada):
    """Define a empresa selecionada e atualiza o label na interface."""
    global empresa_selecionada
    empresa_selecionada = nome
    label_empresa_selecionada.config(text=f"Empresa Selecionada: {empresa_selecionada}")

def limitar_competencia(entrada):
    """Limita o campo de competência para até 6 dígitos numéricos."""
    return not entrada or entrada.isdigit() and len(entrada) <= 6

def validar_email(email):
    """Valida o formato do email informado."""
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False

def verificar_campos(empresa_selecionada, entrada_email, entrada_competencia):
    """Verifica se todos os campos obrigatórios estão preenchidos corretamente."""
    email = entrada_email.get()
    competencia = entrada_competencia.get()
    if not empresa_selecionada:
        messagebox.showwarning("Campo obrigatório!", "Por favor, selecione uma empresa.")
        return False
    if not email:
        messagebox.showwarning("Campo obrigatório!", "Por favor, preencha o campo de email corretamente.")
        return False
    if not validar_email(email):
        messagebox.showwarning("Email inválido!", "Por favor, digite um email válido.")
        return False
    if not competencia or len(competencia) != 6:
        messagebox.showwarning("Campo obrigatório!", "Por favor, preencha o campo de competência corretamente.")
        return False
    return True

def iniciar_selenium(janela, empresa_selecionada, entrada_email, entrada_competencia):
    """Executa o script principal de automação para a empresa selecionada."""

    # Verifica se os campos obrigatórios estão preenchidos.
    if verificar_campos(empresa_selecionada, entrada_email, entrada_competencia):
        return iniciar_script(janela, empresa_selecionada, entrada_email, entrada_competencia)

    # Caso contrário, não executa nada
    return None

def iniciar_janela_principal():
    """Inicia a janela principal da aplicação."""
    global empresa_selecionada
    empresa_selecionada = ""

    janela = tkinter.Tk()
    janela.title("SinistrAmil")
    janela.geometry("900x555")
    janela.configure(bg="#292942")
    janela.resizable(False, False)
    centralizar_janela(janela)

    # Ícone
    imagem_caminho = os.getenv('CAMINHO') + '\\imgs\\pngs\\AMIL.png'
    icone = PhotoImage(file=imagem_caminho)
    janela.iconphoto(True, icone)

    # Frame principal (grid centralizado)
    painel = tkinter.Frame(janela, bg="#292942")
    painel.pack(expand=True)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("main_title.TLabel", background="#292942", foreground="#3E14FF",
                    font=("Montserrat", 26, "bold"))
    style.configure("main_label.TLabel", background="#292942", foreground="#E0E0E0",
                    font=("Montserrat", 12))
    style.configure("main_entry.TEntry", foreground="#333333", font=("Montserrat", 12),
                    fieldbackground="#f3f3fa")
    style.configure("main_button.TButton", background="#4f4fa6", foreground="#FFFFFF",
                    font=("Montserrat", 12, "bold"), padding=6)
    style.map("main_button.TButton", background=[("active", "#3E14FF")], foreground=[("active", "#FFFFFF")])
    style.configure("secondary_button.TButton", background="#B1B6B1", foreground="#3E14FF",
                    font=("Montserrat", 11, "bold"), padding=4)
    style.map("secondary_button.TButton", background=[("active", "#3E14FF")], foreground=[("active", "#FFFFFF")])

    # --- Layout centralizado com grid ---
    painel.grid_columnconfigure(0, weight=1)

    ttk.Label(painel, text="SinistrAmil", style="main_title.TLabel").grid(
        row=0, column=0, pady=(30, 20)
    )

    botao_menu = ttk.Button(painel, text="Mostrar Empresas", style="secondary_button.TButton")
    botao_menu.grid(row=1, column=0, pady=(10, 25))

    label_empresa_selecionada = ttk.Label(painel, text="Nenhuma Empresa Selecionada", style="main_label.TLabel")
    label_empresa_selecionada.grid(row=2, column=0, pady=(0, 30))

    # ---- Email ----
    ttk.Label(painel, text="Email:", style="main_label.TLabel").grid(
        row=3, column=0, sticky="w", pady=(0, 5)
    )
    entrada_email = ttk.Entry(painel, style="main_entry.TEntry", width=50)
    entrada_email.grid(row=4, column=0, pady=(0, 20))

    # ---- Competência ----
    ttk.Label(painel, text="Competência: (Ex: 202412)", style="main_label.TLabel").grid(
        row=5, column=0, sticky="w", pady=(0, 5)
    )
    validar = painel.register(limitar_competencia)
    entrada_competencia = ttk.Entry(
        painel, style="main_entry.TEntry", width=50,
        validate="key", validatecommand=(validar, "%P")
    )
    entrada_competencia.grid(row=6, column=0, pady=(0, 30))

    # ---- Botão iniciar ----
    botao_iniciar = ttk.Button(
        painel, text="Iniciar", style="main_button.TButton",
        command=lambda: iniciar_selenium(janela, empresa_selecionada, entrada_email, entrada_competencia)
    )
    botao_iniciar.grid(row=7, column=0, pady=(0, 40))

    # ---- Botão editar ----
    botao_editar = ttk.Button(
        painel, text="Editar Empresas", style="secondary_button.TButton",
        command=lambda: abrir_editar(janela)
    )
    botao_editar.grid(row=8, column=0, pady=(0, 40))

    # --- Menu de empresas ---
    menu = Menu(janela, tearoff=0)
    conexao = conectar_db()
    if conexao is None:
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.\nVerifique a conexão e tente novamente.")
        janela.destroy()
        sys.exit(1)

    cursor = conexao.cursor()
    cursor.execute("SELECT nome_empresa FROM tabela_empresas")
    empresas = cursor.fetchall()
    for empresa in empresas:
        nome_empresa = empresa[0]
        menu.add_command(label=nome_empresa,
                         command=lambda nome=nome_empresa: selecionar_empresa(nome, label_empresa_selecionada))

    def mostrar_menu(evento):
        menu.post(evento.x_root, evento.y_root)

    botao_menu.bind("<Button-1>", mostrar_menu)

    janela.protocol("WM_DELETE_WINDOW", lambda: fechar_janela(janela))
    janela.mainloop()