-- Table principale des jeux
CREATE TABLE IF NOT EXISTS games (
    appid         INTEGER PRIMARY KEY,
    name          VARCHAR(255) NOT NULL,
    developer     VARCHAR(255),
    publisher     VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS snapshots(
id SERIAL PRIMARY KEY,
appid INTEGER NOT NULL REFERENCES games(appid) ON DELETE CASCADE,
created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
owners_lower INTEGER NOT NULL,
price_eur NUMERIC(10, 2) NOT NULL,  --10 chiffres dont 2 après la virgule
discount INTEGER,
positive INTEGER,
negative INTEGER, 
review_ratio NUMERIC(5, 4),
score_rank      INTEGER,
average_forever INTEGER,
average_2weeks  INTEGER,
median_forever  INTEGER,
ccu             INTEGER
);

-- creation d'index
CREATE INDEX IF NOT EXISTS idx_snapshots_appid ON snapshots(appid);
CREATE INDEX IF NOT EXISTS idx_snapshots_created_at ON snapshots(created_at);
CREATE INDEX IF NOT EXISTS idx_games_name ON games(name);