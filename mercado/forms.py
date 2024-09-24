from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from mercado.models import User

class CadastroForm(FlaskForm):

    def validate_username(self, check_user):
        user = User.query.filter_by(usuario=check_user.data).first()
        if user:
            raise ValidationError('Usuário já existe! Cadastre outro nome de usuário')
    
    def validate_email(self, check_email):
        email = User.query.filter_by(email=check_email.data).first()
        if email:
            raise ValidationError('E-mail já existe! Cadastre outro e-mail de usuario')
        
    def validate_senha(self, check_senha):
        senha = User.query.filter_by(senha=check_senha.data).first()
        if senha:
            raise ValidationError('Senha já existe! Cadastre outro e-mail de usuario')
        
    usuario = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()]) #colocamos um tamanho minimo e maximo para ser escrito pelo usuario e que seria obrigatorio
    email = StringField(label='E-mail:', validators=[Email(), DataRequired()]) #validados se o usuario colocou realmente um e-mail e informamos que e um campo obrigatorio
    senha1 = PasswordField(label='Senha:', validators=[Length(min=6), DataRequired()]) #colocamos um tamanho minimo para ser escrito pelo usuario e que seria obrigatorio
    senha2 = PasswordField(label='Confirmação de Senha:', validators=[EqualTo('senha1'), DataRequired()])# validados se a senha1 e igual a senha2 e colocamos que e um campo obrigatorio
    submit = SubmitField(label='Cadastrar')

#Validar Login
class LoginForm(FlaskForm):
    usuario = StringField(label="Usuario:", validators=[DataRequired()]) # Passamos que seria um tipo de dado string e que seria um campo requirido
    senha = PasswordField(label="Senha:", validators=[DataRequired()])
    submit = SubmitField(label='Logar')

class ComprarProdutoForm(FlaskForm):
    submit = SubmitField(label='Comprar produto')

class VenderProdutoForm(FlaskForm):
    submit = SubmitField(label='Vender Produto!')