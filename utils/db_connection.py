import sqlite3
import pandas as pd
from contextlib import contextmanager
import json
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path='cricbuzz.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with schema"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                # Create tables if not exists
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS players (
                        player_id INTEGER PRIMARY KEY,
                        full_name TEXT NOT NULL,
                        country TEXT,
                        playing_role TEXT,
                        batting_style TEXT,
                        bowling_style TEXT,
                        date_of_birth TEXT,
                        profile_url TEXT
                    )
                ''')
                
                cursor.execute('''
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
                    )
                ''')
                
                cursor.execute('''
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
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS live_matches_cache (
                        cache_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        match_id INTEGER,
                        match_data TEXT,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
        except Exception as e:
            print(f"Database initialization error: {e}")
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def execute_query(self, query, params=None):
        """Execute a query and return results as DataFrame"""
        try:
            with self.get_connection() as conn:
                if params:
                    df = pd.read_sql_query(query, conn, params=params)
                else:
                    df = pd.read_sql_query(query, conn)
                return df
        except Exception as e:
            print(f"Query execution error: {e}")
            return pd.DataFrame()
    
    def execute_update(self, query, params=None):
        """Execute an update/insert/delete operation"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                conn.commit()
                return cursor.lastrowid if cursor.lastrowid else True
        except Exception as e:
            print(f"Update execution error: {e}")
            return False
    
    def insert_player(self, player_data):
        """Insert or update player information"""
        query = '''
            INSERT OR REPLACE INTO players 
            (player_id, full_name, country, playing_role, batting_style, bowling_style, date_of_birth, profile_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        return self.execute_update(query, (
            player_data.get('player_id'),
            player_data.get('full_name'),
            player_data.get('country'),
            player_data.get('playing_role'),
            player_data.get('batting_style'),
            player_data.get('bowling_style'),
            player_data.get('date_of_birth'),
            player_data.get('profile_url')
        ))
    
    def insert_player_stats(self, stats_data):
        """Insert player statistics"""
        query = '''
            INSERT OR REPLACE INTO player_stats 
            (player_id, format, matches_played, innings_batted, runs_scored, highest_score,
             batting_average, strike_rate, centuries, half_centuries, wickets_taken,
             bowling_average, economy_rate, best_bowling, catches, stumpings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        return self.execute_update(query, (
            stats_data.get('player_id'),
            stats_data.get('format'),
            stats_data.get('matches_played', 0),
            stats_data.get('innings_batted', 0),
            stats_data.get('runs_scored', 0),
            stats_data.get('highest_score', 0),
            stats_data.get('batting_average', 0.0),
            stats_data.get('strike_rate', 0.0),
            stats_data.get('centuries', 0),
            stats_data.get('half_centuries', 0),
            stats_data.get('wickets_taken', 0),
            stats_data.get('bowling_average', 0.0),
            stats_data.get('economy_rate', 0.0),
            stats_data.get('best_bowling', ''),
            stats_data.get('catches', 0),
            stats_data.get('stumpings', 0)
        ))
    
    def get_top_batsmen(self, format='ODI', limit=10):
        """Get top batsmen by runs"""
        query = '''
            SELECT p.full_name, p.country, ps.runs_scored, ps.batting_average, 
                   ps.strike_rate, ps.centuries, ps.half_centuries
            FROM player_stats ps
            JOIN players p ON ps.player_id = p.player_id
            WHERE ps.format = ? AND ps.runs_scored > 0
            ORDER BY ps.runs_scored DESC
            LIMIT ?
        '''
        return self.execute_query(query, (format, limit))
    
    def get_top_bowlers(self, format='ODI', limit=10):
        """Get top bowlers by wickets"""
        query = '''
            SELECT p.full_name, p.country, ps.wickets_taken, ps.bowling_average,
                   ps.economy_rate, ps.matches_played
            FROM player_stats ps
            JOIN players p ON ps.player_id = p.player_id
            WHERE ps.format = ? AND ps.wickets_taken > 0
            ORDER BY ps.wickets_taken DESC
            LIMIT ?
        '''
        return self.execute_query(query, (format, limit))
    
    def execute_sql_query(self, query):
        """Execute custom SQL query safely"""
        # Basic SQL injection protection
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE']
        query_upper = query.upper()
        for keyword in dangerous_keywords:
            if keyword in query_upper and 'SELECT' not in query_upper:
                return pd.DataFrame({'Error': ['Only SELECT queries are allowed for safety']})
        
        try:
            return self.execute_query(query)
        except Exception as e:
            return pd.DataFrame({'Error': [str(e)]})