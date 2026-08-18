# Task Manager API with SQLite

A simple CRUD REST API for managing tasks, backed by SQLite database for persistent storage.

## Project Structure

```
.
├── app.py              # Main Flask application
├── tasks.db            # SQLite database (auto-created on first run)
├── requirements.txt    # Python dependencies
├── venv/               # Virtual environment
└── README.md          # This file
```

## Why SQLite?

SQLite was chosen for this project because:
- **Lightweight**: Single file database, no separate server needed
- **Simple**: Perfect for learning database fundamentals
- **Portable**: Easy to share and backup (just copy the file)
- **Sufficient**: Handles thousands of records without performance issues

## Database Location

The SQLite database is stored as `tasks.db` in the project root directory. This is a single file that persists all data even after the application restarts.

## Setup & Installation

### Prerequisites
- Python 3.8+

### Steps

1. **Clone the repository**
   ```bash
   cd your-project-directory
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

The server starts at `http://localhost:5000` and automatically creates `tasks.db` with example tasks on first run.

## API Endpoints

### Get All Tasks
```
GET /tasks
```
Returns all tasks from the database.

**Example:**
```bash
curl http://localhost:5000/tasks
```

**Response:**
```json
[
  {"id": 1, "title": "Learn Flask", "done": false},
  {"id": 2, "title": "Build a CRUD API", "done": false},
  {"id": 3, "title": "Connect to SQLite", "done": false}
]
```

### Get Single Task
```
GET /tasks/{id}
```
Returns a specific task by ID. Returns 404 if not found.

**Example:**
```bash
curl http://localhost:5000/tasks/1
```

### Create Task
```
POST /tasks
Content-Type: application/json

{"title": "Task title"}
```
Creates a new task. Title is required. Returns 201 on success, 400 if invalid.

**Example:**
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk"}'
```

### Update Task
```
PUT /tasks/{id}
Content-Type: application/json

{"title": "Updated title", "done": true}
```
Updates task fields. Returns 404 if task not found.

**Example:**
```bash
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
```

### Delete Task
```
DELETE /tasks/{id}
```
Deletes a task. Returns 204 on success, 404 if not found.

**Example:**
```bash
curl -X DELETE http://localhost:5000/tasks/1
```

## Optional Features

### Get Statistics
```
GET /stats
```
Returns task count statistics using SQL COUNT.

### Search Tasks
```
GET /tasks?search=milk
```
Search tasks by title using SQL LIKE.

### Filter by Completion
```
GET /tasks?done=true
```
Filter completed or pending tasks.

## Database Schema

### Tasks Table

```sql
CREATE TABLE task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done BOOLEAN DEFAULT 0
);
```

### Example SQL Queries

**List all tasks:**
```sql
SELECT * FROM task;
```

**Show only completed tasks:**
```sql
SELECT * FROM task WHERE done = 1;
```

**Count all tasks:**
```sql
SELECT COUNT(*) FROM task;
```

**Mark all tasks as completed:**
```sql
UPDATE task SET done = 1;
```

**Delete all completed tasks:**
```sql
DELETE FROM task WHERE done = 1;
```

## Viewing the Database

To inspect the database directly, install **DB Browser for SQLite**:

1. Download from: https://sqlitebrowser.org/
2. Open `tasks.db` with DB Browser
3. Browse tables and run SQL queries manually
4. Changes are immediately reflected in the API

### Database Screenshot

The database file `tasks.db` contains a single table `task` with three columns:
- `id` (INTEGER PRIMARY KEY) - Unique identifier
- `title` (TEXT) - Task description
- `done` (BOOLEAN) - Completion status

## Key Learnings

This project demonstrates a fundamental backend architecture principle:

**APIs describe WHAT the application does. Databases describe WHERE data is stored.**

- The API layer (endpoints) remains unchanged
- The storage layer (in-memory → SQLite) is an implementation detail
- Clients don't care how data is stored, only that it's available

This separation makes it easy to upgrade from SQLite to PostgreSQL, MySQL, or any other database later without changing a single API endpoint.

## Troubleshooting

**Tasks disappear on restart?**
- Verify `tasks.db` file exists in project root
- Check file permissions allow read/write
- Ensure database initialization ran successfully

**Port 5000 already in use?**
- Modify `app.run(port=5001)` in app.py

**Dependencies not installing?**
- Ensure you activated the virtual environment first: `source venv/bin/activate`

## Next Steps

- Add timestamps (created_at, updated_at) to tasks
- Implement user authentication
- Add task categories or tags
- Migrate to PostgreSQL for production
- Add API documentation with Swagger/OpenAPI

## License

MIT License - Feel free to use this project for learning.
# Usage-Metering-Billing-Engine
