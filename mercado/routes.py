from mercado import app
from flask import render_template, redirect, url_for, flash, request
from mercado import db
from mercado.models import Item, User
from mercado.forms import CadastroForm, LoginForm, ComprarProdutoForm, VenderProdutoForm
from flask_login import login_user, logout_user, login_required, current_user

# Rota para a página inicial
@app.route('/')
def page_home():
    return render_template('home.html')

# Rota para a página de produtos, com métodos GET e POST para comprar e vender produtos.
@app.route('/produtos', methods=['GET', 'POST'])
@login_required  # Exige que o usuário esteja logado para acessar essa rota.
def page_produto():
    compra_form = ComprarProdutoForm()  # Formulário de compra de produtos.
    venda_form = VenderProdutoForm()  # Formulário de venda de produtos.
    
    if request.method == "POST":
        # Lógica de compra de produto.
        compra_produto = request.form.get('compra_produto')
        produto_obj = Item.query.filter_by(nome=compra_produto).first()
        if produto_obj:
            if current_user.compra_disponivel(produto_obj):
                produto_obj.compra(current_user)
                flash(f'Parabéns! Você comprou o produto {produto_obj.nome}', category="success")
            else:
                flash(f'Você não possui saldo suficiente para comprar o produto {produto_obj.nome}', category='danger')
        
        # Lógica de venda de produto.
        venda_produto = request.form.get('venda_produto')
        produto_obj_venda = Item.query.filter_by(nome=venda_produto).first()
        if produto_obj_venda:
            if current_user.venda_disponivel(produto_obj_venda):
                produto_obj_venda.venda(current_user)
                flash(f'Parabéns! Você vendeu o produto {produto_obj_venda.nome}', category="success")
            else:
                flash(f'Algo deu errado com a venda do produto {produto_obj_venda.nome}', category="danger")
        
        # Redireciona para a página de produtos após a compra ou venda.
        return redirect(url_for('page_produto')) 
    
    # Método GET para listar os produtos disponíveis e os itens do usuário.
    if request.method == 'GET':
        itens = Item.query.filter_by(dono=None)  # Busca os itens disponíveis para compra.
        donos_itens = Item.query.filter_by(dono=current_user.id)  # Busca os itens que pertencem ao usuário.
        return render_template('produtos.html', itens=itens, compra_form=compra_form, dono_itens=donos_itens, venda_form=venda_form)

# Rota para a página de cadastro de novos usuários.
@app.route('/cadastro', methods=['GET', 'POST'])
def page_cadastro():
    form = CadastroForm()  # Formulário de cadastro de usuário.
    if form.validate_on_submit():
        # Cria um novo usuário com base nos dados fornecidos no formulário.
        usuario = User(
            usuario=form.usuario.data,
            email=form.email.data,
            senhacrip=form.senha1.data
        )
        # Adiciona o usuário ao banco de dados.
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('page_produto'))  # Redireciona para a página de produtos.
    
    # Exibe mensagens de erro caso o formulário tenha sido preenchido incorretamente.
    if form.errors != {}:
        for err in form.errors.values():
            flash(f'Erro ao cadastrar usuário: {err}', category="danger")
    return render_template('cadastro.html', form=form)

# Rota para a página de login.
@app.route('/login', methods=['GET', 'POST'])
def page_login():
    form = LoginForm()  # Formulário de login.
    if form.validate_on_submit():
        # Autentica o usuário com base no nome de usuário e senha fornecidos.
        usuario_logado = User.query.filter_by(usuario=form.usuario.data).first()
        if usuario_logado and usuario_logado.converte_senha(senha_texto_claro=form.senha.data):
            login_user(usuario_logado)  # Loga o usuário.
            flash(f'Login realizado com sucesso! {usuario_logado.usuario}', category='success')
            return redirect(url_for('page_produto'))
        else:
            flash(f'Usuário ou senha incorretos! Tente novamente.', category='danger')
    return render_template('login.html', form=form)

# Rota para realizar o logout do usuário.
@app.route('/logout')
def page_logout():
    logout_user()  # Desloga o usuário.
    flash('Você fez o logout', category='info')
    return redirect(url_for('page_home'))  # Redireciona para a página inicial.

# Inicia o servidor Flask em modo de depuração.
if __name__ == '__main__':
    app.run(debug=True)
