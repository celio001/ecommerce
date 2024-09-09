from mercado import app
from flask import render_template, redirect, url_for, flash
from mercado import db
from mercado.models import Item, User
from mercado.forms import CadastroForm

@app.route('/')
def page_home():
    return render_template('home.html')

@app.route('/produtos')
def page_produto():
    itens = Item.query.all() # Retorna os dados do nosso banco na pagina produto
    return render_template('produtos.html', itens=itens)

@app.route('/cadastro', methods=['GET', 'POST'])
def page_cadastro():
    #Pegar os dados do formulario de cadastro de usuarios
    form = CadastroForm()
    if form.validate_on_submit():
        usuario = User(
            usuario = form.usuario.data,
            email = form.email.data,
            senha = form.senha1.data
        )
        #Guardar os dados no nosso banco de dados
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('page_produto')) # redicionar o usaurio para a pagina de produtos

    #Se o usuario não escrever os dados corretos no campo
    if form.errors != {}: 
        for err in form.errors.values(): #pega os campos que não foi atendido os requisitos exigidos
            flash(f'Erro ao cadastrar usuário {err}') #Retorna uma mensagem do que não foi preenchido corretamente 
    return render_template('cadastro.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)