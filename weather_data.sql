-- Create the table for storing daily weather summaries
CREATE TABLE IF NOT EXISTS daily_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    city TEXT NOT NULL,
    avg_temp REAL NOT NULL,
    max_temp REAL NOT NULL,
    min_temp REAL NOT NULL,
    dominant_condition TEXT NOT NULL,
    UNIQUE(date, city) -- Prevent duplicate entries for the same day and city
);
