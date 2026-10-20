import sqlite3
import json
from typing import List, Dict, Any

DB_PATH = "chat_history.db"

def init_db():
    """Initialize the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def store_message(role: str, content: str, message_id: str = None, timestamp: float = None) -> None:
    """Store a message in the database"""
    import time
    import uuid
    
    if not message_id:
        message_id = str(uuid.uuid4())
    
    if not timestamp:
        timestamp = time.time()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO messages (id, role, content, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (message_id, role, content, timestamp))
    conn.commit()
    conn.close()

def get_chat_history(limit: int = 100) -> List[Dict[str, Any]]:
    """Get chat history from database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, role, content, timestamp
        FROM messages
        ORDER BY timestamp ASC
        LIMIT ?
    ''', (limit,))
    
    messages = []
    for row in cursor.fetchall():
        messages.append({
            'id': row[0],
            'role': row[1],
            'content': row[2],
            'timestamp': row[3]
        })
    
    conn.close()
    
    return messages

def get_last_n_messages(n=4):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content, timestamp FROM messages ORDER BY id DESC LIMIT ?",
        (n,)
    )
    messages = cursor.fetchall()
    conn.close()
    return list(reversed(messages))  # To return in oldest-to-latest order
