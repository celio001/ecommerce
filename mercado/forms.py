from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired

class CadastroForm(FlaskForm):
    usuario = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()]) #colocamos um tamanho minimo e maximo para ser escrito pelo usuario e que seria obrigatorio
    email = StringField(label='E-mail:', validators=[Email(), DataRequired()]) #validados se o usuario colocou realmente um e-mail e informamos que e um campo obrigatorio
    senha1 = PasswordField(label='Senha:', validators=[Length(min=6), DataRequired()]) #colocamos um tamanho minimo para ser escrito pelo usuario e que seria obrigatorio
    senha2 = PasswordField(label='Confirmação de Senha:', validators=[EqualTo('senha1'), DataRequired()])# validados se a senha1 e igual a senha2 e colocamos que e um campo obrigatorio
    submit = SubmitField(label='Cadastrar')
