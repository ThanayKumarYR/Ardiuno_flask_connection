from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your secret key
db = SQLAlchemy(app)
socketio = SocketIO(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key1 = db.Column(db.String(50))
    key2 = db.Column(db.String(50))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        key1 = request.form.get('key1')
        key2 = request.form.get('key2')

        # Store data in the database (replace the old record if it exists)
        existing_data = Data.query.first()
        if existing_data:
            existing_data.key1 = key1
            existing_data.key2 = key2
        else:
            new_data = Data(key1=key1, key2=key2)
            db.session.add(new_data)

        db.session.commit()

        print(f"Received key1: {key1}, key2: {key2}")  # Debugging print
        socketio.emit('update', {'key1': key1, 'key2': key2})
        return render_template('index.html', key1=key1, key2=key2)
    
    # Fetch the latest data from the database
    latest_data = Data.query.first()
    if latest_data:
        key1 = latest_data.key1
        key2 = latest_data.key2
    else:
        key1 = ""
        key2 = ""
    
    return render_template('index.html', key1=key1, key2=key2)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True, host="0.0.0.0", port=5001)
