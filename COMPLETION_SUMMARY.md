## Assignment Completion Summary: W3·A1 — Connecting CRUD to Database

### ✅ Project Status: COMPLETE

All 6 stages and requirements have been successfully implemented and tested.

---

## What Was Built

A complete **Task Manager REST API** using:
- **Framework**: Flask (Python)
- **Database**: SQLite (`tasks.db`)
- **ORM**: SQLModel (SQLAlchemy-based)
- **Runtime**: Python 3.8+

### Project Files

```
project/
├── app.py                 # Main Flask application (CRUD endpoints)
├── sql_queries.py         # SQL learning demonstrations
├── tasks.db              # SQLite database (auto-created)
├── requirements.txt      # Python dependencies
├── README.md            # Full project documentation
├── .gitignore           # Git ignore rules
└── venv/                # Virtual environment
```

---

## Requirement Verification

### ✅ API Requirements

- [x] **Same CRUD endpoints as Assignment 1**
  - `GET /tasks` - List all tasks (with optional search/filter)
  - `GET /tasks/{id}` - Get single task
  - `POST /tasks` - Create task (returns 201)
  - `PUT /tasks/{id}` - Update task
  - `DELETE /tasks/{id}` - Delete task (returns 204)

- [x] **Data persists across server restarts**
  - Tasks are stored in SQLite, survive application restarts
  - 3 example tasks inserted only on first run

- [x] **Proper error handling**
  - Invalid requests return `400 Bad Request`
  - Unknown IDs return `404 Not Found` with error JSON
  - Missing title returns `400`

- [x] **Database automatically created**
  - First run creates `tasks.db` if missing
  - Schema created automatically on startup
  - Transactions handled properly

### ✅ Database Requirements

- [x] **SQLite database with proper schema**
  ```sql
  CREATE TABLE task (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN DEFAULT 0
  )
  ```

- [x] **All CRUD operations use SQL**
  - CREATE: `INSERT INTO task (title, done) VALUES (?, ?)`
  - READ: `SELECT * FROM task` / `SELECT * FROM task WHERE id = ?`
  - UPDATE: `UPDATE task SET ... WHERE id = ?`
  - DELETE: `DELETE FROM task WHERE id = ?`

- [x] **Three example tasks on first run**
  - "Learn Flask"
  - "Build a CRUD API"
  - "Connect to SQLite"

### ✅ Optional Features Implemented

- [x] **Search using SQL LIKE**
  - `GET /tasks?search=milk` → filters by title

- [x] **Filter by completion status**
  - `GET /tasks?done=true` → completed tasks only

- [x] **Statistics endpoint**
  - `GET /stats` → returns total, completed, pending counts

- [x] **SQL learning demonstrations**
  - `sql_queries.py` demonstrates 6 SQL queries
  - Shows SELECT, WHERE, COUNT, ORDER BY, LIKE, GROUP BY

---

## Testing Results

### Stage 0: Database Creation ✅
```
✓ Database created on first run
✓ 3 example tasks inserted
✓ Only once on first run (idempotent)
✓ Persists across application restarts
```

### Stage 1: Read Endpoints ✅
```
✓ GET /tasks returns all tasks
✓ GET /tasks/1 returns single task
✓ GET /tasks/999 returns 404 with error message
✓ All responses are valid JSON
```

### Stage 2: Create Endpoint ✅
```
✓ POST /tasks creates new task
✓ Returns 201 Created status
✓ Task persists after server restart
✓ Tasks survive application restarts
```

### Stage 3: Update & Delete ✅
```
✓ PUT /tasks/{id} updates task fields
✓ Mark tasks as complete
✓ DELETE /tasks/{id} removes task
✓ Returns 204 No Content on success
✓ All operations reflected in database immediately
```

### Stage 4: SQL Learning ✅
```
✓ List every task: SELECT * FROM task
✓ Filter: SELECT * FROM task WHERE done = 1
✓ Count: SELECT COUNT(*) FROM task
✓ Sort: SELECT * FROM task ORDER BY title
✓ Search: SELECT * FROM task WHERE title LIKE '%Flask%'
✓ Group: SELECT done, COUNT(*) FROM task GROUP BY done
✓ All queries executable via sql_queries.py
```

### Stage 5: Documentation ✅
```
✓ README.md explains:
  - Why SQLite was chosen
  - Where database is stored (/project/tasks.db)
  - How to start the project (python3 app.py)
  - Database schema details
  - Example SQL queries
✓ Ready to clone and run
```

---

## API Test Summary

### Create Test (POST)
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Complete Assignment"}'

→ Status: 201 Created
→ Response: {"id": 4, "title": "Complete Assignment", "done": false}
```

### Read Tests (GET)
```bash
curl http://localhost:5000/tasks
→ Status: 200 OK
→ Returns: [{"id": 1, "title": "Learn Flask", "done": false}, ...]

curl http://localhost:5000/tasks/1
→ Status: 200 OK
→ Returns: {"id": 1, "title": "Learn Flask", "done": false}

curl http://localhost:5000/tasks/999
→ Status: 404 Not Found
→ Returns: {"error": "Task not found"}
```

### Update Test (PUT)
```bash
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

→ Status: 200 OK
→ Returns: {"id": 1, "title": "Learn Flask", "done": true}
```

### Delete Test (DELETE)
```bash
curl -X DELETE http://localhost:5000/tasks/1

→ Status: 204 No Content
```

### Stats Test (Bonus)
```bash
curl http://localhost:5000/stats

→ Status: 200 OK
→ Returns: {"total": 3, "completed": 0, "pending": 3}
```

---

## Key Architecture Insights

### API vs Storage Separation

This project demonstrates the **fundamental backend principle**:

```
The API layer describes WHAT the application does.
The storage layer describes WHERE data is stored.
```

**Before (In-Memory):**
```
Client → API → Python Array → Lost on restart
```

**After (SQLite):**
```
Client → API → SQL Database → Persistent
```

**The API endpoints are 100% identical.** Only the implementation behind them changed.

### Benefits Demonstrated

1. **Persistence**: Data survives application restarts
2. **Scalability**: Can easily switch to PostgreSQL/MySQL later
3. **Consistency**: Multiple requests see same data
4. **Reliability**: ACID transactions ensure data integrity

---

## How to Run

### Setup (one time)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Start Server
```bash
source venv/bin/activate
python3 app.py
```

Server runs on `http://localhost:5000`

### Make Requests
```bash
# Get all tasks
curl http://localhost:5000/tasks

# Create task
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk"}'

# Update task
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

# Delete task
curl -X DELETE http://localhost:5000/tasks/1

# View stats
curl http://localhost:5000/stats

# Search by title
curl "http://localhost:5000/tasks?search=milk"

# Filter by completion
curl "http://localhost:5000/tasks?done=true"
```

### Learn SQL
```bash
source venv/bin/activate
python3 sql_queries.py
```

---

## Database File

- **Location**: `tasks.db` (project root)
- **Size**: ~8 KB
- **Type**: SQLite 3.x database
- **Format**: Single binary file (easy to backup, commit to git)

### View with DB Browser
1. Download: https://sqlitebrowser.org/
2. Open: `tasks.db` file
3. Browse: Tables and execute custom queries
4. Changes immediately reflected in API

---

## Validation Checklist

- [x] Database file exists and is valid SQLite
- [x] Tasks table created with correct schema
- [x] Three example tasks inserted on first run
- [x] All CRUD operations working
- [x] Validation working (400 errors)
- [x] Not found errors working (404)
- [x] Data persists across restarts
- [x] SQL queries demonstrated
- [x] Documentation complete
- [x] Code is clean and commented
- [x] Requirements file accurate
- [x] Virtual environment set up
- [x] .gitignore configured

---

## Next Steps (Optional)

The architecture now supports:
- Migrate to PostgreSQL (0 API changes needed)
- Add user authentication
- Add timestamps (created_at, updated_at)
- Add task categories/tags
- Add pagination for large datasets
- Deploy to production (with WSGI server like Gunicorn)

---

**Assignment Complete** ✓

The API is identical to Assignment 1, but the data now persists!
