import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os, sys

# Descobre a pasta onde o .env está (no .exe fica em _MEIPASS)
if getattr(sys, 'frozen', False):  # quando rodar no .exe
    BASE_DIR = sys._MEIPASS
else:  # quando rodar como script Python normal
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Carrega o .env da pasta encontrada
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)

''' Criando conexão de banco de dados '''
def conectar_db():
    try:
        conexao = mysql.connector.connect(
            host = os.getenv("HOST"),
            user = os.getenv("USER"),
            password = os.getenv("PASSWORD"),
            database = os.getenv("DATABASE")    
        )
        return conexao
    except Error as e:
        print("Erro ao estabelecer uma conexão ao banco de dados: {e}")
        return None