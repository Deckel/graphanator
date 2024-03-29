from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prod.db'

db = SQLAlchemy(app)

class ConversationTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String, nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Messsage %r>' % self.id

with app.app_context():
        db.create_all()

@app.route('/', methods=['POST', 'GET'])

def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,  port=5001)
