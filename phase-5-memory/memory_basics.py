import sqlite3 #inbuilt library, file based database

# Connect database — if file is not there is will be created automatically
conn = sqlite3.connect("memory.db")
cursor = conn.cursor()  #cursor is tool, it runs command on database

# Create table — if table does not exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT NOT NULL UNIQUE,
        value TEXT NOT NULL
    )
""")
conn.commit()

# function to save memory
def save_memory(key, value):
    cursor.execute(
        "INSERT OR REPLACE INTO user_memory (key, value) VALUES (?, ?)",
        (key, value)
    )
    conn.commit()
    print(f"Saved: {key} = {value}")

# to retrieve the memory
def get_memory(key):
    cursor.execute(
        "SELECT value FROM user_memory WHERE key = ?",
        (key,)
    )
    result = cursor.fetchone()
    if result:
        return result[0]
    return None

save_memory("user_name", "Chelsi")
save_memory("user_language", "Hinglish")

print(get_memory("user_name"))
print(get_memory("user_language"))
print(get_memory("user_age"))  