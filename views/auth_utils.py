# auth_utils.py
import os, sys
from tkinter import simpledialog, messagebox
from dotenv import load_dotenv

# Descobre a pasta onde o .env está (no .exe fica em _MEIPASS)
if getattr(sys, 'frozen', False):  # quando rodar no .exe
    BASE_DIR = sys._MEIPASS
else:  # quando rodar como script Python normal
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho para o .env
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)

def validar_senha_mestra(mensagem="Digite a senha mestra:"):
    """
    Exibe um prompt pedindo a senha mestra e valida contra o .env.
    Retorna True se a senha for válida, False caso contrário.
    """
    SENHA_MESTRA = os.getenv("SENHA_MESTRA")
    senha_digitada = simpledialog.askstring("Senha Mestra", mensagem, show="*")

    if senha_digitada is None:
        return False  # usuário cancelou
    if senha_digitada != SENHA_MESTRA:
        messagebox.showerror("Erro", "Senha mestra incorreta.")
        return False

    return True
