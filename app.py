from flask import Flask, render_template, request, jsonify
from database import get_or_create_user, update_user_score


app = Flask(__name__)

@app.route('/<int:user_id>')
def index(user_id):
    user = get_or_create_user(user_id, "Unknown")
    return render_template('index.html', 
                         user_id=user_id,
                         clicks=user.clicks,
                         max_score=user.max_score)

@app.route('/save_score', methods=['POST'])
def save_score():
    data = request.json
    user_id = data.get('user_id')
    clicks = data.get('clicks')
    max_score = data.get('max_score')
    
    if user_id and clicks is not None and max_score is not None:
        update_user_score(user_id, clicks, max_score)
        return jsonify({'status': 'success'})
    
    return jsonify({'status': 'error'}), 400

@app.errorhandler(400)
def bad_request(e):
    return jsonify({'status': 'error', 'message': 'Bad request'}), 400

if __name__ == '__main__':
    from utils import read_json
    app.run(ssl_context=('cert.pem', 'key.pem'),host=read_json("WEBAPP_HOST"), port=read_json("WEBAPP_PORT"))