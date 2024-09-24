# Importações necessárias para a integração com o banco de dados, criptografia de senhas e autenticação de usuários.
from mercado import db, login_manager
from mercado import bcrypt
from flask_login import UserMixin

# Função decoradora usada pelo Flask-Login para carregar o usuário com base no user_id armazenado na sessão.
@login_manager.user_loader
def load_user(user_id):
    # Busca o usuário no banco de dados com base no user_id.
    return User.query.get(int(user_id))

# Classe que representa os usuários no banco de dados. Herda de db.Model para criar a tabela no SQLAlchemy e de UserMixin para integração com o Flask-Login.
class User(db.Model, UserMixin):
    # Define as colunas da tabela de usuários.
    id = db.Column(db.Integer, primary_key=True)  # Chave primária única para cada usuário.
    usuario = db.Column(db.String(length=30), nullable=False, unique=True)  # Nome de usuário único.
    email = db.Column(db.String(length=50), nullable=False, unique=True)  # Email único do usuário.
    senha = db.Column(db.String(length=60), nullable=False, unique=True)  # Senha criptografada do usuário.
    valor = db.Column(db.Integer, nullable=False, default=5000)  # Saldo inicial padrão do usuário.
    
    # Relacionamento com a tabela 'Item', indicando que um usuário pode ter vários itens.
    itens = db.relationship('Item', backref='dono_user', lazy=True)
    
    # Propriedade que formata o saldo do usuário para exibição com o formato de moeda brasileira.
    @property
    def formataValor(self):
        if len(str(self.valor)) >= 4:
            return f'R$ {str(self.valor)[:-3]},{str(self.valor)[-3:]}'
        else:
            return f'R$ {self.valor}'

    # Propriedade que retorna a senha criptografada.
    @property
    def senhacrip(self):
        return self.senha
    
    # Setter para criptografar a senha em texto claro antes de salvar no banco de dados.
    @senhacrip.setter
    def senhacrip(self, senha_text):
        self.senha = bcrypt.generate_password_hash(senha_text).decode('utf-8')

    # Método que verifica se a senha fornecida pelo usuário corresponde à senha armazenada.
    def converte_senha(self, senha_texto_claro):
        return bcrypt.check_password_hash(self.senha, senha_texto_claro)

    # Verifica se o usuário tem saldo suficiente para comprar um determinado produto.
    def compra_disponivel(self, produto_obj):
        return self.valor >= produto_obj.preco

    # Verifica se o usuário possui o produto que deseja vender.
    def venda_disponivel(self, produto_obj):
        return produto_obj in self.itens

# Classe que representa os itens disponíveis para compra e venda.
class Item(db.Model):
    # Define as colunas da tabela de itens.
    id = db.Column(db.Integer, primary_key=True)  # Chave primária única para cada item.
    nome = db.Column(db.String(length=30), nullable=False, unique=True)  # Nome do item, deve ser único.
    preco = db.Column(db.Integer, nullable=False)  # Preço do item.
    cod_barra = db.Column(db.String(length=12), nullable=False, unique=True)  # Código de barras único do item.
    descricao = db.Column(db.String(length=1024), nullable=False, unique=True)  # Descrição do item.
    
    # Chave estrangeira que relaciona o item com o dono (usuário).
    dono = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Retorna uma representação em string do item.
    def __repr__(self):
        return f"Item{self.nome}"
    
    # Método que realiza a compra do item, transferindo-o para o usuário e deduzindo o saldo do usuário.
    def compra(self, usuario):
        self.dono = usuario.id
        usuario.valor -= self.preco
        db.session.commit()

    # Método que realiza a venda do item, removendo o dono e acrescentando o valor da venda ao saldo do usuário.
    def venda(self, usuario):
        self.dono = None
        usuario.valor += self.preco
        db.session.commit()
