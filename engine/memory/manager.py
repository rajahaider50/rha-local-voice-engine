from engine.memory.database import MemoryDatabase
import datetime

class MemoryManager:
    def __init__(self, db_path: str = "rha_memory.db"):
        """
        Phase 14: Memory System.
        Manages storing and retrieving user facts and preferences.
        """
        self.db = MemoryDatabase(db_path)

    def save_fact(self, content: str, memory_type: str = "fact") -> bool:
        """Saves a conversational fact (e.g. 'My name is Ali')."""
        try:
            import sqlite3
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO memories (memory_type, content) VALUES (?, ?)', 
                (memory_type, content)
            )
            conn.commit()
            conn.close()
            print(f"[Memory] Saved {memory_type}: {content}")
            return True
        except Exception as e:
            print(f"[Memory] Error saving: {e}")
            return False

    def save_interaction(self, user_text: str, assistant_text: str) -> bool:
        """Persist a compact conversation pair for later local context."""
        return self.save_fact(
            f"User: {user_text}\nAssistant: {assistant_text}",
            memory_type="conversation",
        )

    def retrieve_relevant_context(self, query: str) -> str:
        """
        Retrieves recent memories to inject into the LLM prompt.
        For a production system, this would use vector embeddings.
        For Phase 14, we retrieve the last 5 facts.
        """
        try:
            import sqlite3
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            cursor.execute(
                'SELECT content FROM memories ORDER BY timestamp DESC LIMIT 5'
            )
            rows = cursor.fetchall()
            conn.close()
            
            if rows:
                facts = "\n".join([f"- {row[0]}" for row in rows])
                return f"Relevant memories about the user:\n{facts}"
            return ""
        except Exception:
            return ""
