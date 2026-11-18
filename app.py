from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    # Ana sayfayı render eder (templates klasörü içindeki index.html'i çağırır)
    return render_template('index.html')

@app.route('/api/verify-human', methods=['POST'])
def verify_human():
    data = request.get_json()
    token = data.get('token') if data else None
    
    if token:
        return jsonify({'success': True, 'message': 'Doğrulama başarılı!'})
    return jsonify({'success': False, 'message': 'Doğrulama başarısız.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
    
