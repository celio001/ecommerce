# E-commerce Flask Application

Este é um sistema de e-commerce desenvolvido com Flask. Ele permite que os usuários se registrem, façam login, adicionem produtos a um carrinho, verifiquem o saldo de suas contas, comprem e vendam produtos.

## Funcionalidades
- Cadastro e login de usuários.
- Sistema de saldo de conta.
- Adicionar e remover produtos do carrinho.
- Compra e venda de produtos.
- Visualização de histórico de compras.

## Pré-requisitos
Certifique-se de ter o seguinte instalado no seu sistema:
- Python 3.8+
- MySQL ou qualquer outro banco de dados compatível com SQLAlchemy
- Pip (gerenciador de pacotes do Python)

## Instalação

1. Clone este repositório:
   
   ```bash
   git clone https://github.com/celio001/ecommerce.git
   cd ecommerce

2. Clone este repositório:
   
   ```bash
   gpython3 -m venv venv
   source venv/bin/activate  # No Windows: venv\\Scripts\\activate

3. Instale as dependências do projeto:
   
   ```bash
   pip install -r requirements.txt

4. Configure o banco de dados:
   No arquivo mercado/__init__.py, configure o URI do banco de dados para se conectar ao seu servidor MySQL (ou outro banco).

5. Instale as dependências do projeto:
   
   ```bash
   flask db upgrade

## Configuração do Banco de Dados:
Este projeto usa SQLAlchemy para gerenciar a comunicação com o banco de dados. No arquivo models.py, as tabelas de Usuários, Produtos e Transações estão definidas.

Para configurar o banco de dados:

- Defina a string de conexão com o banco de dados no arquivo mercado/__init__.py.
- Execute as migrações para criar as tabelas.
  
## Executando a Aplicação:
Após configurar o banco de dados, execute a aplicação com o seguinte comando:

   ```bash
   python run.py
```

A aplicação estará disponível no endereço http://127.0.0.1:5000/

## Estrutura do Projeto
- `run.py`: Arquivo principal para iniciar a aplicação Flask.
- `mercado/`: Diretório com a lógica da aplicação.
  - `__init__.py`: Configurações da aplicação e do banco de dados.
  - `forms.py`: Definições dos formulários (login, cadastro, etc.).
  - `models.py`: Modelos de banco de dados (usuários, produtos, transações).
  - `routes.py`: Definição das rotas (fluxo de navegação, como login, adicionar ao carrinho).
  - `templates/`: Arquivos HTML para a interface do usuário.

## Tecnologias Usadas

- Flask
- SQLAlchemy
- WTForms
- Bootstrap
- MySQL

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para fazer um fork e enviar pull requests.

## Licença
Este projeto é licenciado sob a MIT License.
