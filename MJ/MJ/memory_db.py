import sqlite3
import os
from typing import List, Optional, Dict
from contextlib import contextmanager
from datetime import datetime
from memory_models import Conversation, Preference

class MemoryDatabase:
    def __init__(self, db_path: str = "nova_memory.db"):
        self.db_path = os.path.abspath(db_path)
        print(f"Initializing database at: {self.db_path}")
        self._init_db()

    @contextmanager
    def _get_connection(self):
        """Get a database connection with automatic cleanup"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        """Initialize database schema"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    session_id TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    created TEXT NOT NULL,
                    updated TEXT NOT NULL
                )
            """)
            
            conn.commit()

    def remember_conversation(self, role: str, content: str, 
                            session_id: Optional[str] = None) -> Conversation:
        """Store a conversation entry"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            timestamp = datetime.now().isoformat()
            cursor.execute(
                """INSERT INTO conversations 
                (role, content, timestamp, session_id) 
                VALUES (?, ?, ?, ?)""",
                (role, content, timestamp, session_id)
            )
            conn.commit()
            return Conversation(
                id=cursor.lastrowid,
                role=role,
                content=content,
                timestamp=timestamp,
                session_id=session_id
            )

    def get_conversation_history(self, limit: int = 10) -> List[Conversation]:
        """Retrieve recent conversation history"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM conversations 
                ORDER BY timestamp DESC 
                LIMIT ?""",
                (limit,)
            )
            return [
                Conversation(
                    id=row['id'],
                    role=row['role'],
                    content=row['content'],
                    timestamp=row['timestamp'],
                    session_id=row['session_id']
                ) for row in cursor.fetchall()
            ]

    def remember_preference(self, key: str, value: str) -> Preference:
        """Store or update a preference"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            
            cursor.execute(
                "SELECT created FROM preferences WHERE key = ?",
                (key,)
            )
            existing = cursor.fetchone()
            created = existing['created'] if existing else now
            
            cursor.execute(
                """INSERT OR REPLACE INTO preferences 
                (key, value, created, updated) 
                VALUES (?, ?, ?, ?)""",
                (key, value, created, now)
            )
            conn.commit()
            return Preference(key=key, value=value, created=created, updated=now)

    def get_preferences(self) -> Dict[str, str]:
        """Get all preferences"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT key, value FROM preferences")
            return {row['key']: row['value'] for row in cursor.fetchall()}

    def summarize_conversations(self) -> str:
        """Generate a readable conversation summary"""
        history = self.get_conversation_history()
        if not history:
            return "No conversation history"
        
        return "\n".join(
            f"[{conv.timestamp}] {conv.role}: {conv.content}" 
            for conv in reversed(history))