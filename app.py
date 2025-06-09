import os
import secrets
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import escape

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@"
    f"{os.getenv('MYSQL_HOST', 'localhost')}/{os.getenv('MYSQL_DATABASE')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize the database tables when the application starts
with app.app_context():
    db.create_all()

class Checklist(db.Model):
    __tablename__ = 'checklists'
    id = db.Column(db.String(32), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    items = db.relationship('ChecklistItem', backref='checklist', lazy=True, cascade='all, delete-orphan')

class ChecklistItem(db.Model):
    __tablename__ = 'checklist_items'
    id = db.Column(db.Integer, primary_key=True)
    checklist_id = db.Column(db.String(32), db.ForeignKey('checklists.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def generate_checklist_id():
    return secrets.token_urlsafe(16)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    try:
        # Execute a lightweight query to confirm database connectivity
        db.session.execute('SELECT 1')
        return jsonify({'status': 'ok'})
    except Exception:
        return jsonify({'status': 'error'}), 500

@app.route('/checklist/new', methods=['POST'])
def create_checklist():
    title = escape(request.form.get('title', '').strip())
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    checklist_id = generate_checklist_id()
    checklist = Checklist(id=checklist_id, title=title)
    db.session.add(checklist)
    db.session.commit()

    return redirect(url_for('view_checklist', checklist_id=checklist_id))

@app.route('/checklist/<checklist_id>')
def view_checklist(checklist_id):
    checklist = Checklist.query.get_or_404(checklist_id)
    return render_template('checklist.html', checklist=checklist)

@app.route('/checklist/<checklist_id>/title', methods=['PUT'])
def update_title(checklist_id):
    checklist = Checklist.query.get_or_404(checklist_id)
    title = escape(request.json.get('title', '').strip())
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    checklist.title = title
    db.session.commit()
    return jsonify({'title': checklist.title})

@app.route('/checklist/<checklist_id>/items', methods=['POST'])
def add_item(checklist_id):
    checklist = Checklist.query.get_or_404(checklist_id)
    content = escape(request.json.get('content', '').strip())
    if not content:
        return jsonify({'error': 'Content is required'}), 400

    item = ChecklistItem(checklist_id=checklist_id, content=content)
    db.session.add(item)
    db.session.commit()

    return jsonify({
        'id': item.id,
        'content': item.content,
        'completed': item.completed
    })

@app.route('/checklist/<checklist_id>/items/<int:item_id>', methods=['DELETE'])
def delete_item(checklist_id, item_id):
    item = ChecklistItem.query.filter_by(
        checklist_id=checklist_id,
        id=item_id
    ).first_or_404()
    
    db.session.delete(item)
    db.session.commit()
    return '', 204

@app.route('/checklist/<checklist_id>/items/<int:item_id>/toggle', methods=['PUT'])
def toggle_item(checklist_id, item_id):
    item = ChecklistItem.query.filter_by(
        checklist_id=checklist_id,
        id=item_id
    ).first_or_404()
    
    item.completed = not item.completed
    db.session.commit()
    return jsonify({'completed': item.completed})

@app.route('/checklist/<checklist_id>/reset', methods=['POST'])
def reset_checklist(checklist_id):
    checklist = Checklist.query.get_or_404(checklist_id)
    
    # Update all items to not completed
    ChecklistItem.query.filter_by(checklist_id=checklist_id).update({ChecklistItem.completed: False})
    db.session.commit()
    
    return jsonify({'message': 'Checklist reset successfully'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
