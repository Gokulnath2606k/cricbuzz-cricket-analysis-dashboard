

SQL_QUERIES = {
   
    "q1_indian_players": """
        SELECT full_name, playing_role, batting_style, bowling_style
        FROM players
        WHERE country = 'India'
        ORDER BY full_name
    """,
    
    "q2_recent_matches": """
        SELECT match_desc, team1_name || ' vs ' || team2_name AS teams,
               venue_name || ', ' || venue_city AS venue,
               match_date, status
        FROM matches
        WHERE date(match_date) >= date('now', '-30 days')
        ORDER BY match_date DESC
    """,
    
    "q3_top_run_scorers_odi": """
        SELECT p.full_name, ps.runs_scored, ps.batting_average, ps.centuries
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        WHERE ps.format = 'ODI' AND ps.runs_scored > 0
        ORDER BY ps.runs_scored DESC
        LIMIT 10
    """,
    
    "q4_large_venues": """
        SELECT venue_name, venue_city, venue_country
        FROM matches
        GROUP BY venue_name, venue_city, venue_country
        HAVING COUNT(match_id) > 5
        ORDER BY COUNT(match_id) DESC
    """,
    
    "q5_team_wins": """
        SELECT winning_team AS team_name, COUNT(*) AS total_wins
        FROM matches
        WHERE winning_team IS NOT NULL
        GROUP BY winning_team
        ORDER BY total_wins DESC
    """,
    
    "q6_players_by_role": """
        SELECT playing_role, COUNT(*) AS player_count
        FROM players
        WHERE playing_role IS NOT NULL
        GROUP BY playing_role
        ORDER BY player_count DESC
    """,
    
    "q7_highest_scores_by_format": """
        SELECT format, MAX(highest_score) AS highest_score
        FROM player_stats
        GROUP BY format
    """,
    
    "q8_series_2024": """
        SELECT DISTINCT series_name, match_type, match_date
        FROM matches
        WHERE strftime('%Y', match_date) = '2024'
        ORDER BY match_date DESC
    """,
    
    
    "q9_allrounders": """
        SELECT p.full_name, ps.runs_scored, ps.wickets_taken, ps.format
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        WHERE ps.runs_scored > 1000 AND ps.wickets_taken > 50
        ORDER BY (ps.runs_scored + ps.wickets_taken * 20) DESC
    """,
    
    "q10_recent_completed_matches": """
        SELECT match_desc, team1_name || ' vs ' || team2_name AS teams,
               winning_team, victory_margin, victory_type, venue_name
        FROM matches
        WHERE status = 'Completed'
        ORDER BY match_date DESC
        LIMIT 20
    """,
    
    "q11_player_format_comparison": """
        SELECT p.full_name,
               MAX(CASE WHEN ps.format = 'Test' THEN ps.runs_scored ELSE 0 END) AS test_runs,
               MAX(CASE WHEN ps.format = 'ODI' THEN ps.runs_scored ELSE 0 END) AS odi_runs,
               MAX(CASE WHEN ps.format = 'T20I' THEN ps.runs_scored ELSE 0 END) AS t20_runs,
               AVG(ps.batting_average) AS overall_avg
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        GROUP BY p.player_id
        HAVING COUNT(DISTINCT ps.format) >= 2
        ORDER BY overall_avg DESC
    """,
    
    "q16_performance_by_year": """
        WITH yearly_stats AS (
            SELECT p.full_name, 
                   strftime('%Y', ps.updated_at) AS year,
                   AVG(ps.runs_scored) AS avg_runs,
                   AVG(ps.strike_rate) AS avg_strike_rate,
                   COUNT(*) AS matches_played
            FROM player_stats ps
            JOIN players p ON ps.player_id = p.player_id
            WHERE strftime('%Y', ps.updated_at) >= '2020'
            GROUP BY p.player_id, year
            HAVING matches_played >= 5
        )
        SELECT * FROM yearly_stats
        ORDER BY full_name, year DESC
    """,
    
    
    "q17_toss_advantage": """
        SELECT 
            CASE WHEN winning_team IS NOT NULL THEN 'Known' ELSE 'Unknown' END AS result_status,
            COUNT(*) AS match_count
        FROM matches
        GROUP BY result_status
    """,
    
    "q18_most_economical_bowlers": """
        SELECT p.full_name, ps.economy_rate, ps.wickets_taken, ps.matches_played
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        WHERE ps.format IN ('ODI', 'T20I')
          AND ps.economy_rate > 0
          AND ps.matches_played >= 10
          AND ps.wickets_taken > 0
        ORDER BY ps.economy_rate ASC
        LIMIT 10
    """,
    
    "q20_matches_by_format": """
        SELECT p.full_name,
               SUM(CASE WHEN ps.format = 'Test' THEN ps.matches_played ELSE 0 END) AS test_matches,
               SUM(CASE WHEN ps.format = 'ODI' THEN ps.matches_played ELSE 0 END) AS odi_matches,
               SUM(CASE WHEN ps.format = 'T20I' THEN ps.matches_played ELSE 0 END) AS t20_matches,
               AVG(ps.batting_average) AS batting_avg
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        GROUP BY p.player_id
        HAVING SUM(ps.matches_played) >= 20
        ORDER BY total_matches DESC
    """,
}

def get_all_queries():
    """Returns dictionary of all SQL queries"""
    return SQL_QUERIES

def get_query_by_name(query_name):
    """Get specific query by name"""
    return SQL_QUERIES.get(query_name, "SELECT 'Query not found' AS message")