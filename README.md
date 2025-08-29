<h1 align="center">SinistrAmil - Portal de Benefícios Automator</h1>

<p align="center">
  <img width="900" height="449" alt="print_princial_amil" src="https://github.com/user-attachments/assets/88a8a1af-7cd8-4d5c-a6be-417142d90b46" alt="sinistramil" />
</p>

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## 📑 Descrição do Projeto

Este projeto é uma **refatoração** de um código existente, que estava desatualizado e sem manutenção por mais de 7 meses.  
O objetivo principal é automatizar o acesso ao **Portal de Benefícios da Amil**, permitindo que usuários extraiam documentos de forma prática e segura, enviando-os automaticamente para o e-mail informado na aplicação.

Durante a refatoração, foram realizadas diversas melhorias:

- Código dividido em módulos para maior organização.
- Atualização da **tela gráfica** amigável (GUI).
- Inclusão de **senha mestre** para segurança em alterações.
- Adição de funções extras como:
  - Adicionar empresas e códigos.
  - Visualizar e editar dados.
  - Excluir competências.
- Implementação de **banco de dados externo (não local)**.
- Correção de falhas do Selenium (projeto antigo não funcionava mais).
- Revisão visual completa da aplicação.

O resultado é um **executável simples** que permite, com poucos cliques, acessar automaticamente o portal da Amil e enviar documentos por e-mail, utilizando login e senha armazenados no banco de dados.

---

## 🛠️ Funcionalidades Principais

- **Automação de Login e Acesso ao Portal Amil**
- **Extração de Documentos** automaticamente
- **Envio de Arquivos por E-mail**
- **Cadastro de Empresas e Códigos**
- **Visualização e Edição de Dados**
- **Senha Mestre** para controle de alterações
- **Banco de Dados Externo** (mais confiável que local)
- **Interface Gráfica** intuitiva e prática

---

## 📥 Como clonar este projeto

Clone via **HTTPS**:
```bash
git clone https://github.com/SEU_USUARIO/SinistrAmil.git
```

Ou via **SSH**:
```bash
git clone git@github.com:SEU_USUARIO/SinistrAmil.git
```

Entre na pasta do projeto:
```bash
cd SinistrAmil
```

---

## 🖥 Como executar

### 1) Pré-requisitos
- **Python 3.8+** instalado  
  Verifique:
  ```bash
  python --version
  ```
  ou
  ```bash
  python3 --version
  ```

- **pip** instalado  
  Atualize (opcional):
  ```bash
  python -m pip install --upgrade pip
  ```

### 2) Criar e ativar ambiente virtual (recomendado)
Crie:
```bash
python -m venv venv
```

Ative:
- **Windows**
  ```bash
  venv\Scripts\activate
  ```
- **Linux/macOS**
  ```bash
  source venv/bin/activate
  ```

### 3) Instalar dependências
```bash
pip install -r requirements.txt
```

### 4) Executar a aplicação
```bash
python app.py
```

Ou, se já tiver o **executável gerado (PyInstaller)**, basta rodar o `.exe` dentro da pasta `dist`.

---

## 📸 Prints da Aplicação

<p align="center">
  <img width="540" height="432" alt="print_senha_amil" src="https://github.com/user-attachments/assets/ab49a56a-75de-41a0-84c4-8d2489a8e07f" />
  <img width="358" height="432" alt="print_editar_amil" src="https://github.com/user-attachments/assets/ffe1f3c8-ee12-4d90-b9df-3c865a22c197" />
</p>

---

## 🧰 Tecnologias Utilizadas

- **Python 3.10+**
- **Selenium** - automação web
- **Tkinter** - interface gráfica
- **SQLite / Banco Externo** - persistência de dados
- **dotenv** - variáveis de ambiente
- **PyInstaller** - geração do executável

---

## 📜 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
