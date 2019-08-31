import pusher
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/www/app.local/tmp/messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

pusher_client = pusher.Pusher(
  app_id='853579',
  key='6d0fa50e973e9e012e4b',
  secret='7ae6d0aef0a13258e811',
  cluster='eu',
  ssl=True
)

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    message = db.Column(db.String(500))

@app.route('/')
def index():

    messages = Message.query.all()

    return render_template('index.html', messages=messages)


@app.route('/message', methods=['POST'])
def message():

    try:

        username = request.form.get('username')
        message = request.form.get('message')
        
        new_message = Message(username=username, message=message)
        db.session.add(new_message)
        db.session.commit()
        
        pusher_client.trigger('chat-channel', 'new-message', {'username' : username, 'message': message})
        return jsonify({'result' : 'success'})

    except:
    
        return jsonify({'result' : 'failure'})

@app.route('/client', methods=['POST'])
def ret_client():
    return (request.form.get('username'))

if __name__ == '__main__':
    app.run(debug=True)
