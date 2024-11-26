from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalogo.db'
db = SQLAlchemy(app)
 
class Genero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
 
class Artista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    genero_id = db.Column(db.Integer, db.ForeignKey('genero.id'), nullable=False)
    genero = db.relationship('Genero', backref=db.backref('artistas', lazy=True))
 
class Disco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    capa = db.Column(db.String(200))
    artista_id = db.Column(db.Integer, db.ForeignKey('artista.id'), nullable=False)
    artista = db.relationship('Artista', backref=db.backref('discos', lazy=True))
 
class Faixa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    disco_id = db.Column(db.Integer, db.ForeignKey('disco.id'), nullable=False)
    disco = db.relationship('Disco', backref=db.backref('faixas', lazy=True))
 
db.create_all()
 
@app.route('/')
def index():
    discos = Disco.query.all()
    return render_template('index.html', discos=discos)
 
@app.route('/novo_disco', methods=['GET', 'POST'])
def novo_disco():
    if request.method == 'POST':
        titulo = request.form['titulo']
        ano = request.form['ano']
        capa = request.form['capa']
        artista_id = request.form['artista']
        disco = Disco(titulo=titulo, ano=ano, capa=capa, artista_id=artista_id)
        db.session.add(disco)
        db.session.commit()
        return redirect(url_for('index'))
    artistas = Artista.query.all()
    return render_template('novo_disco.html', artistas=artistas)
 
@app.route('/editar_disco/<int:id>', methods=['GET', 'POST'])
def editar_disco(id):
    disco = Disco.query.get_or_404(id)
    if request.method == 'POST':
        disco.titulo = request.form['titulo']
        disco.ano = request.form['ano']
        disco.capa = request.form['capa']
        disco.artista_id = request.form['artista']
        db.session.commit()
        return redirect(url_for('index'))
    artistas = Artista.query.all()
    return render_template('editar_disco.html', disco=disco, artistas=artistas)
 
@app.route('/deletar_disco/<int:id>')
def deletar_disco(id):
    disco = Disco.query.get_or_404(id)
    db.session.delete(disco)
    db.session.commit()
    return redirect(url_for('index'))
 
@app.route('/novo_artista', methods=['GET', 'POST'])
def novo_artista():
    if request.method == 'POST':
        nome = request.form['nome']
        genero_id = request.form['genero']
        artista = Artista(nome=nome, genero_id=genero_id)
        db.session.add(artista)
        db.session.commit()
        return redirect(url_for('index'))
    generos = Genero.query.all()
    return render_template('novo_artista.html', generos=generos)
 
@app.route('/novo_genero', methods=['GET', 'POST'])
def novo_genero():
    if request.method == 'POST':
        nome = request.form['nome']
        genero = Genero(nome=nome)
        db.session.add(genero)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('novo_genero.html')
 
if __name__ == '__main__':
    app.run(debug=True)