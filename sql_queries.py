#!/usr/bin/env python3
"""
Stage 4: Learn SQL Queries

This script demonstrates SQL queries you can run against the tasks database.
Run this to see how SQL queries work and how they interact with the API.
"""

import sqlite3
from tabulate import tabulate

DATABASE = "tasks.db"

def execute_query(query, description):
    """Execute a SQL query and display results."""
    print(f"\n{'='*60}")
    print(f"Query: {description}")
    print(f"SQL: {query}")
    print(f"{'='*60}")
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            # Convert rows to list of dicts for tabulate
            rows = [dict(row) for row in results]
            print(tabulate(rows, headers="keys", tablefmt="grid"))
        else:
            print("(No results)")
        
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def main():
    print("Stage 4: Learning SQL Queries on Tasks Database")
    print("=" * 60)
    
    # Query 1: List every task
    execute_query(
        "SELECT id, title, done FROM task;",
        "List every task"
    )
    
    # Query 2: Show only completed tasks
    execute_query(
        "SELECT id, title, done FROM task WHERE done = 1;",
        "Show only completed tasks"
    )
    
    # Query 3: Count all tasks
    execute_query(
        "SELECT COUNT(*) as total_tasks FROM task;",
        "Count all tasks"
    )
    
    # Query 4: Count completed vs pending
    execute_query(
        "SELECT done, COUNT(*) as count FROM task GROUP BY done;",
        "Count completed vs pending tasks"
    )
    
    # Query 5: List tasks by title (alphabetical)
    execute_query(
        "SELECT id, title, done FROM task ORDER BY title ASC;",
        "List tasks alphabetically by title"
    )
    
    # Query 6: Find tasks containing a keyword
    execute_query(
        "SELECT id, title, done FROM task WHERE title LIKE '%Flask%';",
        "Find tasks containing 'Flask'"
    )
    
    print("\n" + "=" * 60)
    print("Notes:")
    print("- WHERE filters results (e.g., WHERE done = 1)")
    print("- COUNT(*) counts rows")
    print("- ORDER BY sorts results")
    print("- LIKE searches for text patterns")
    print("- GROUP BY groups results")
    print("=" * 60)

if __name__ == "__main__":
    main()
