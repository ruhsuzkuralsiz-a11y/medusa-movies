from flask import Flask, render_template

app = Flask(__name__)

# 1. Ana Sayfa (Tüm filmlerin, kategorilerin ve alt menünün olduğu ilk ekran)
@app.route('/')
def index():
    return render_template('index.html')

# 2. Film İzleme Sayfası (Server 1, Server 2, Multiembed ve Fragman butonlarının olduğu ekran)
@app.route('/movie/<movie_id>')
def movie(movie_id):
    return render_template('movie.html', movie_id=movie_id)

if __name__ == '__main__':
    app.run(debug=True)
    
