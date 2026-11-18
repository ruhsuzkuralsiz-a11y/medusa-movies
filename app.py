from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Ana sayfa
@app.route('/')
def index():
    return render_template('index.html')

# Dinamik Film Sayfası (Örn: /movie/1263337)
@app.route('/movie/<movie_id>')
def movie_detail(movie_id):
    # Burada gelen movie_id değerini template'e gönderiyoruz ki hangi film olduğu bilinsin
    return render_template('index.html', movie_id=movie_id)

# Robot olmadığını doğrulama API'si
@app.route('/api/verify-human', methods=['POST'])
def verify_human():
    data = request.get_json()
    token = data.get('token') if data else None
    
    if token:
        return jsonify({'success': True, 'message': 'Doğrulama başarılı!'})
    return jsonify({'success': False, 'message': 'Doğrulama başarısız.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
    
