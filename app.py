from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movie/<movie_id>')
def movie(movie_id):
    return render_template('movie.html', movie_id=movie_id)

if __name__ == '__main__':
    app.run(debug=True)
    
