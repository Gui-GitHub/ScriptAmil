import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import messagebox
from config.config import conectar_db

def iniciar_script(janela, empresa_selecionada, entrada_email, entrada_competencia):

    """Executa o script principal de automação para a empresa selecionada."""
    max_retries = 3
    attempt = 0
    while attempt < max_retries:
        attempt += 1
        navegador = None
        try:
            # Dados do usuário
            email_usuario = entrada_email.get()
            competencia_usuario = entrada_competencia.get()

            # Dados da empresa
            conexao = conectar_db()
            cursor = conexao.cursor()
            cursor.execute("SELECT login_empresa, senha_empresa, codigos_empresa FROM tabela_empresas WHERE nome_empresa = %s", (empresa_selecionada,))
            resultado = cursor.fetchone()
            login_empresa, senha_empresa, codigos = resultado
            numeros = [num.strip() for num in codigos.split(',')]

            # Configuração do Chrome
            chrome_options = Options()
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option("useAutomationExtension", False)
            chrome_options.add_experimental_option("detach", True)
            servico = Service(ChromeDriverManager().install())
            navegador = webdriver.Chrome(service=servico, options=chrome_options)

            # Remover barra de aviso
            navegador.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            })
            guias = navegador.window_handles
            navegador.set_page_load_timeout(60)

            # Login
            navegador.maximize_window()
            navegador.get("https://www.amil.com.br/empresa/#/login")
            WebDriverWait(navegador, 15).until(EC.presence_of_element_located((By.XPATH, '//input[@type="text" or @type="email"]'))).send_keys(login_empresa)
            WebDriverWait(navegador, 15).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(senha_empresa)
            navegador.find_element(By.CSS_SELECTOR, '.test_button_login').click()
            WebDriverWait(navegador, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))).click()

            # Acessando BI
            try:
                WebDriverWait(navegador, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="app"]/div[2]/div[2]/div/div/div[3]/div/div[1]/div/div[2]/div/div/a[5]'))).click()
            except (TimeoutException, NoSuchElementException):
                navegador.quit()
                messagebox.showerror("Erro de Login", "Usuário ou senha inválidos, tente modificar a senha.")
                if hasattr(janela, 'deiconify'):
                    janela.deiconify()
                break

            time.sleep(6)

            # Acessando página de solicitações
            navegador.get("https://www.amil.com.br/bioperadora/ContaCorrente/SolicitacaoExterno.aspx?Origem=S")
            navegador.switch_to.window(guias[-1])
            time.sleep(4)

            for numero in numeros:
                preencher_formulario(navegador, numero, email_usuario, competencia_usuario)

            # Finalizando
            navegador.execute_script("alert('O script foi executado com sucesso e se encerrará em 5 segundos.')")
            time.sleep(5)
            navegador.quit()
            break

        except (NoSuchElementException, TimeoutException) as e:
            if navegador:
                navegador.quit()
            if attempt >= max_retries:
                messagebox.showerror("Erro", f"Falha ao executar o script após {max_retries} tentativas.\nErro: {e}")
                break
        except Exception as e:
            if navegador:
                navegador.quit()
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")
            break

def preencher_formulario(navegador, numero, email_usuario, competencia_usuario):
    """Preenche os formulários CAD e Útil para cada código da empresa."""
    for tipo in ['CAD', 'Útil']:
        # Campo Email
        campo_email = WebDriverWait(navegador, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_EmailTextBox"]'))
        )
        campo_email.clear()
        campo_email.send_keys(email_usuario)

        # Campo Competência
        campo_comp = WebDriverWait(navegador, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_CompetenciaTextBox"]'))
        )
        campo_comp.clear()
        campo_comp.send_keys(competencia_usuario)

        # Selecionar tipo
        navegador.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_TipoSolicitacaoDropDownList"]').click()
        if tipo == 'CAD':
            navegador.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_TipoSolicitacaoDropDownList"]/option[2]').click()
        else:
            navegador.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_TipoSolicitacaoDropDownList"]/option[3]').click()

        # Campo Empresa
        campo_empresa = navegador.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_EmpresaFiltroTextBox"]')
        campo_empresa.clear()
        campo_empresa.send_keys(numero.strip("'"))

        time.sleep(1)
        navegador.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_FiltrarButton"]').click()
        time.sleep(3)

        WebDriverWait(navegador, 60).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_SalvarSolicitacaoButton"]'))
        ).click()
        time.sleep(2)
