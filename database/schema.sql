-- Players Table
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    country TEXT,
    playing_role TEXT,
    batting_style TEXT,
    bowling_style TEXT,
    date_of_birth TEXT,
    profile_url TEXT
);

-- Player Statistics Table
CREATE TABLE IF NOT EXISTS player_stats (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    format TEXT CHECK(format IN ('Test', 'ODI', 'T20I')),
    matches_played INTEGER DEFAULT 0,
    innings_batted INTEGER DEFAULT 0,
    runs_scored INTEGER DEFAULT 0,
    highest_score INTEGER DEFAULT 0,
    batting_average REAL DEFAULT 0.0,
    strike_rate REAL DEFAULT 0.0,
    centuries INTEGER DEFAULT 0,
    half_centuries INTEGER DEFAULT 0,
    wickets_taken INTEGER DEFAULT 0,
    bowling_average REAL DEFAULT 0.0,
    economy_rate REAL DEFAULT 0.0,
    best_bowling TEXT,
    catches INTEGER DEFAULT 0,
    stumpings INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

-- Matches Table
CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY,
    match_desc TEXT,
    series_name TEXT,
    match_type TEXT,
    team1_name TEXT,
    team2_name TEXT,
    venue_name TEXT,
    venue_city TEXT,
    venue_country TEXT,
    match_date TEXT,
    status TEXT,
    winning_team TEXT,
    victory_margin TEXT,
    victory_type TEXT
);

-- Live Match Data Cache
CREATE TABLE IF NOT EXISTS live_matches_cache (
    cache_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER,
    match_data TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better performance
CREATE INDEX idx_player_country ON players(country);
CREATE INDEX idx_player_role ON players(playing_role);
CREATE INDEX idx_stats_player ON player_stats(player_id);
CREATE INDEX idx_stats_format ON player_stats(format);
CREATE INDEX idx_matches_date ON matches(match_date);