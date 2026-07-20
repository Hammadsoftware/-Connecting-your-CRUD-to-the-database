import sqlite3
import json
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
DATABASE = 'tasks.db'

def get_db_connection():
    """Get database connection with row factory."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with schema and example data."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN DEFAULT 0
        )
    ''')
    
    # Insert example tasks only if table is empty
    cursor.execute('SELECT COUNT(*) FROM task')
    if cursor.fetchone()[0] == 0:
        example_tasks = [
            ('Learn Flask', 0),
            ('Build a CRUD API', 0),
            ('Connect to SQLite', 0),
        ]
        cursor.executemany('INSERT INTO task (title, done) VALUES (?, ?)', example_tasks)
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """GET /tasks - Retrieve all tasks with optional search/filter."""
    search_query = request.args.get('search', '').strip()
    done_filter = request.args.get('done', None)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = 'SELECT id, title, done FROM task WHERE 1=1'
    params = []
    
    if search_query:
        query += ' AND title LIKE ?'
        params.append(f'%{search_query}%')
    
    if done_filter is not None:
        done_value = 1 if done_filter.lower() in ['true', '1', 'yes'] else 0
        query += ' AND done = ?'
        params.append(done_value)
    
    cursor.execute(query, params)
    tasks = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(task) for task in tasks])

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """GET /tasks/{id} - Retrieve a single task by id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, done FROM task WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    conn.close()
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    return jsonify(dict(task))

@app.route('/tasks', methods=['POST'])
def create_task():
    """POST /tasks - Create a new task."""
    data = request.get_json() or {}
    
    # Validation
    if 'title' not in data:
        return jsonify({"error": "Missing title"}), 400
    
    title = data['title'].strip() if isinstance(data['title'], str) else ''
    if not title:
        return jsonify({"error": "Title cannot be empty"}), 400
    
    # Insert into database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO task (title, done) VALUES (?, ?)', (title, 0))
    conn.commit()
    
    task_id = cursor.lastrowid
    conn.close()
    
    return jsonify({"id": task_id, "title": title, "done": False}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """PUT /tasks/{id} - Update a task."""
    data = request.get_json() or {}
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if task exists
    cursor.execute('SELECT id, title, done FROM task WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    
    if not task:
        conn.close()
        return jsonify({"error": "Task not found"}), 404
    
    # Prepare update
    title = task['title']
    done = task['done']
    
    if 'title' in data:
        title = data['title'].strip() if isinstance(data['title'], str) else ''
        if not title:
            conn.close()
            return jsonify({"error": "Title cannot be empty"}), 400
    
    if 'done' in data:
        done = 1 if data['done'] else 0
    
    # Update database
    cursor.execute('UPDATE task SET title = ?, done = ? WHERE id = ?', (title, done, task_id))
    conn.commit()
    conn.close()
    
    return jsonify({"id": task_id, "title": title, "done": bool(done)})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """DELETE /tasks/{id} - Delete a task."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if exists
    cursor.execute('SELECT id FROM task WHERE id = ?', (task_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "Task not found"}), 404
    
    # Delete
    cursor.execute('DELETE FROM task WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    
    return '', 204

@app.route('/stats', methods=['GET'])
def get_stats():
    """GET /stats - Get task statistics."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as total FROM task')
    total = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as completed FROM task WHERE done = 1')
    completed = cursor.fetchone()['completed']
    
    pending = total - completed
    conn.close()
    
    return jsonify({
        "total": total,
        "completed": completed,
        "pending": pending
    })

if __name__ == '__main__':
    app.run(debug=False, port=5000, threaded=False)
