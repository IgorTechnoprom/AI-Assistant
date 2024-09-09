-- SQL schema for AI Assistant mind mapping
CREATE TABLE IF NOT EXISTS thoughts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    thought TEXT NOT NULL,
    sender TEXT NOT NULL CHECK(sender IN ('user', 'ai')),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_thought_id INTEGER,
    child_thought_id INTEGER,
    relationship_type TEXT CHECK(relationship_type IN ('child', 'parent', 'jump')),
    FOREIGN KEY (parent_thought_id) REFERENCES thoughts(id),
    FOREIGN KEY (child_thought_id) REFERENCES thoughts(id)
);
