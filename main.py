"""
Cricbuzz LiveStats - PURE LIVE CRICKET DATA
No demo data - Only real matches from Cricbuzz
"""

import streamlit as st
import pandas as pd
import sqlite3
import requests
import plotly.express as px
import json
import time
from datetime import datetime


st.set_page_config(
    page_title="Cricbuzz LiveStats - Live Cricket Data",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    .main-header {
        background: linear-gradient(135deg, #ff7e5f, #feb47b);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
        transition: 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        background: rgba(255,255,255,0.2);
    }
    .metric-value {
        font-size: 2.8rem;
        font-weight: bold;
        color: #feb47b;
    }
    .match-card {
        background: rgba(0,0,0,0.6);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-left: 5px solid #ff7e5f;
        transition: 0.2s;
    }
    .match-card:hover {
        transform: translateX(5px);
        background: rgba(0,0,0,0.8);
    }
    .team-name {
        font-size: 1.5rem;
        font-weight: bold;
        color: #feb47b;
    }
    .live-score {
        font-size: 1.3rem;
        font-family: monospace;
        background: rgba(0,0,0,0.5);
        padding: 0.3rem 0.8rem;
        border-radius: 8px;
        display: inline-block;
    }
    .live-badge {
        background: #ff4444;
        color: white;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        animation: pulse 1s infinite;
        display: inline-block;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    .status-completed {
        background: #00c853;
        color: white;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        display: inline-block;
    }
    h1, h2, h3, h4, p, label {
        color: white !important;
    }
    .stSidebar {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f23 100%);
    }
    hr {
        border-color: rgba(255,255,255,0.2);
    }
    [data-testid="stMetricLabel"] {
        color: white !important;
    }
    [data-testid="stMetricValue"] {
        color: #feb47b !important;
    }
    .stAlert {
        background-color: rgba(0,0,0,0.5) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)


def init_db():
    conn = sqlite3.connect('cricbuzz_live.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS live_matches (
                    match_id INTEGER PRIMARY KEY,
                    title TEXT,
                    team1 TEXT,
                    team2 TEXT,
                    score1 TEXT,
                    score2 TEXT,
                    venue TEXT,
                    status TEXT,
                    match_type TEXT,
                    timestamp REAL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS players (
                    player_id INTEGER PRIMARY KEY,
                    name TEXT,
                    country TEXT,
                    role TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

RAPIDAPI_KEY = "644d09fd34msh6bcf97c117bc42ep14723fjsne423e70cceb6"


class CricbuzzLiveAPI:
    """Fetches ONLY live cricket data from Cricbuzz"""
    
    def __init__(self):
   
        self.endpoints = [
            {
                "url": "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live",
                "headers": {
                    "X-RapidAPI-Key": RAPIDAPI_KEY,
                    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
                }
            },
            {
                "url": "https://cricbuzz-cricket.p.rapidapi.com/series/v1/live",
                "headers": {
                    "X-RapidAPI-Key": RAPIDAPI_KEY,
                    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
                }
            }
        ]
    
    def get_live_matches(self):
        """Fetch real live matches from Cricbuzz"""
        for endpoint in self.endpoints:
            try:
                response = requests.get(endpoint["url"], headers=endpoint["headers"], timeout=15)
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                continue
        return None
    
    def get_match_scorecard(self, match_id):
        """Fetch detailed scorecard for a specific match"""
        url = f"https://cricbuzz-cricket.p.rapidapi.com/matches/v1/{match_id}"
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
        }
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None


def extract_matches_from_response(data):
    """Extract match data from various API response formats"""
    matches = []
    
    if not data:
        return matches
    
    s
    if isinstance(data, dict):
        
        if 'matchList' in data and data['matchList']:
            for match in data['matchList']:
                matches.append(match)
        
        elif 'seriesMatches' in data:
            for series in data['seriesMatches']:
                if 'seriesAdWrapper' in series:
                    series_data = series['seriesAdWrapper']
                    if 'matches' in series_data:
                        for match in series_data['matches']:
                            matches.append(match)
        
    
        elif 'typeMatches' in data:
            for type_match in data['typeMatches']:
                if 'seriesMatches' in type_match:
                    for series in type_match['seriesMatches']:
                        if 'seriesAdWrapper' in series:
                            if 'matches' in series['seriesAdWrapper']:
                                for match in series['seriesAdWrapper']['matches']:
                                    matches.append(match)
        

        elif 'matches' in data and isinstance(data['matches'], list):
            matches = data['matches']
    
    return matches


if 'api' not in st.session_state:
    st.session_state.api = CricbuzzLiveAPI()
if 'live_matches' not in st.session_state:
    st.session_state.live_matches = []
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = 0
if 'api_working' not in st.session_state:
    st.session_state.api_working = True


with st.sidebar:
    st.markdown("# 🏏 Cricbuzz LiveStats")
    st.markdown("---")
    
    st.markdown("### 📱 Navigation")
    page = st.radio(
        "Go to",
        ["🏠 Home", "🎯 Live Matches", "📊 Player Stats", "💾 SQL Analytics", "✏️ CRUD"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # API Status
    st.markdown("### 🔌 API Status")
    if st.session_state.api_working:
        st.success("🟢 Live API Connected")
    else:
        st.error("🔴 API Connection Failed")
    
    st.markdown("---")
    
    # Stats
    st.markdown("### 📊 Database Stats")
    conn = sqlite3.connect('cricbuzz_live.db')
    try:
        match_count = pd.read_sql("SELECT COUNT(*) as cnt FROM live_matches", conn).iloc[0,0]
        player_count = pd.read_sql("SELECT COUNT(*) as cnt FROM players", conn).iloc[0,0]
        st.metric("Matches Stored", match_count)
        st.metric("Players", player_count)
    except:
        st.metric("Matches Stored", 0)
        st.metric("Players", 0)
    conn.close()
    
    st.markdown("---")
    st.caption("Data Source: Cricbuzz Live API")
    st.caption(f"Last Refresh: {datetime.now().strftime('%H:%M:%S')}")


if page == "🏠 Home":
    st.markdown("""
    <div class="main-header">
        <h1>🏏 Cricbuzz LiveStats</h1>
        <p>Real-Time LIVE Cricket Data from Cricbuzz API</p>
    </div>
    """, unsafe_allow_html=True)
    
  
    with st.spinner("Fetching live cricket data..."):
        data = st.session_state.api.get_live_matches()
        if data:
            st.session_state.api_working = True
            matches = extract_matches_from_response(data)
            live_count = len(matches)
        else:
            st.session_state.api_working = False
            live_count = 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{live_count}</div>
            <div>Live Matches</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">LIVE</div>
            <div>Real-time Data</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">Cricbuzz</div>
            <div>Official Source</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">⚡</div>
            <div>Auto Refresh</div>
        </div>
        """, unsafe_allow_html=True)
    
    if not st.session_state.api_working:
        st.error("""
        ⚠️ **Unable to connect to Cricbuzz API**
        
        Possible reasons:
        - Your RapidAPI subscription may have expired
        - Check your API key at: https://rapidapi.com/cricketapilive/api/cricbuzz-cricket/
        - Free tier may have request limits
        """)
    else:
        st.success("✅ Connected to Cricbuzz API - Fetching LIVE cricket data")


elif page == "🎯 Live Matches":
    st.markdown("## 🔴 LIVE CRICKET MATCHES")
    st.caption("Real-time data from Cricbuzz | Refreshes every 30 seconds")
    
    # Refresh button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    # Auto-refresh logic
    current_time = time.time()
    if current_time - st.session_state.last_refresh > 30:
        st.session_state.last_refresh = current_time
        st.rerun()
    
    # Fetch live data
    with st.spinner("Fetching live cricket matches from Cricbuzz API..."):
        data = st.session_state.api.get_live_matches()
    
    if data:
        st.session_state.api_working = True
        matches = extract_matches_from_response(data)
        
        if matches:
            st.success(f"✅ Found {len(matches)} live match(es)")
            
            # Store in database
            conn = sqlite3.connect('cricbuzz_live.db')
            c = conn.cursor()
            
            for match in matches:
            
                match_info = match.get('matchInfo', match)
                
                match_id = match_info.get('matchId', 0)
                match_desc = match_info.get('matchDesc', 'N/A')
                series_name = match_info.get('seriesName', 'N/A')
                
                # Team information
                team1 = match_info.get('team1', {}).get('teamName', 'Team 1')
                team2 = match_info.get('team2', {}).get('teamName', 'Team 2')
                
                # Scores
                score1 = match.get('matchScore', {}).get('team1Score', {}).get('inngs1', {}).get('runs', '0')
                overs1 = match.get('matchScore', {}).get('team1Score', {}).get('inngs1', {}).get('overs', '0')
                score2 = match.get('matchScore', {}).get('team2Score', {}).get('inngs1', {}).get('runs', '0')
                overs2 = match.get('matchScore', {}).get('team2Score', {}).get('inngs1', {}).get('overs', '0')
                
                # Format scores
                score1_display = f"{score1}/{match.get('matchScore', {}).get('team1Score', {}).get('inngs1', {}).get('wickets', '0')} ({overs1} ov)" if score1 != '0' else "Yet to bat"
                score2_display = f"{score2}/{match.get('matchScore', {}).get('team2Score', {}).get('inngs1', {}).get('wickets', '0')} ({overs2} ov)" if score2 != '0' else "Yet to bat"
                
                # Venue and status
                venue = match_info.get('venueInfo', {}).get('ground', 'Venue TBD')
                status = match_info.get('status', 'Live')
                match_type = match_info.get('matchFormat', 'International')
                
                # Determine badge type
                is_live = 'Live' in status or status == 'In Progress'
                badge_class = 'live-badge' if is_live else 'status-completed'
                badge_text = '🔴 LIVE' if is_live else '✅ COMPLETED'
                
              
                st.markdown(f"""
                <div class="match-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <div style="flex: 2;">
                            <div class="team-name">🏏 {team1}</div>
                            <div class="live-score">{score1_display}</div>
                        </div>
                        <div style="font-size: 1.5rem; padding: 0 15px;">VS</div>
                        <div style="flex: 2; text-align: right;">
                            <div class="team-name">🏏 {team2}</div>
                            <div class="live-score">{score2_display}</div>
                        </div>
                    </div>
                    <hr>
                    <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                        <div>📍 {venue}</div>
                        <div class="{badge_class}">{badge_text}</div>
                        <div>🏆 {match_desc} | {series_name}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Cache to database
                c.execute("""INSERT OR REPLACE INTO live_matches 
                            (match_id, title, team1, team2, score1, score2, venue, status, match_type, timestamp) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                          (match_id, f"{team1} vs {team2}", team1, team2,
                           score1_display, score2_display, venue, status, match_type, time.time()))
                
               
                with st.expander(f"📋 Match Details - {team1} vs {team2}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.json(match_info)
                    with col2:
                        # Fetch detailed scorecard
                        details = st.session_state.api.get_match_scorecard(match_id)
                        if details:
                            st.json(details)
                        else:
                            st.info("Detailed scorecard loading...")
            
            conn.commit()
            conn.close()
            
        else:
            st.warning("No live matches at the moment. Check back during match hours!")
            
           
            conn = sqlite3.connect('cricbuzz_live.db')
            recent = pd.read_sql("SELECT * FROM live_matches ORDER BY timestamp DESC LIMIT 5", conn)
            conn.close()
            if not recent.empty:
                st.info("📦 Recently cached matches:")
                st.dataframe(recent[['title', 'score1', 'score2', 'venue']], use_container_width=True)
    
    else:
        st.session_state.api_working = False
        st.error("""
        ❌ **Failed to fetch live data from Cricbuzz API**
        
        Please check:
        1. Your RapidAPI subscription status
        2. API key validity at https://rapidapi.com/cricketapilive/api/cricbuzz-cricket/
        3. Your internet connection
        
        Press **Refresh** to try again.
        """)


elif page == "📊 Player Stats":
    st.markdown("## 📊 Player Statistics")
    
    conn = sqlite3.connect('cricbuzz_live.db')
    players_df = pd.read_sql("SELECT * FROM players", conn)
    conn.close()
    
    if not players_df.empty:
        fig = px.bar(players_df, x='country', y='player_id', 
                     title='Players by Country', color='country',
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(height=400, plot_bgcolor='rgba(255,255,255,0.1)')
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(players_df, use_container_width=True, hide_index=True)
    else:
        st.info("No players in database. Use CRUD page to add players.")


elif page == "💾 SQL Analytics":
    st.markdown("## 💾 SQL Analytics on Live Data")
    
    conn = sqlite3.connect('cricbuzz_live.db')
    
    # Show available tables
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
    st.write("📂 **Available Tables:**", tables['name'].tolist())
    
    # Predefined queries
    st.subheader("📋 Quick Analytics Queries")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏏 Show All Live Matches", use_container_width=True):
            df = pd.read_sql("SELECT * FROM live_matches ORDER BY timestamp DESC", conn)
            st.dataframe(df, use_container_width=True)
            st.download_button("Download CSV", df.to_csv(index=False), "live_matches.csv")
    
    with col2:
        if st.button("📍 Matches by Venue", use_container_width=True):
            df = pd.read_sql("SELECT venue, COUNT(*) as match_count FROM live_matches GROUP BY venue ORDER BY match_count DESC", conn)
            st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    st.subheader("✏️ Custom SQL Query")
    
    query = st.text_area("Write your SQL query", "SELECT * FROM live_matches LIMIT 10", height=100)
    if st.button("🔍 Execute Query", use_container_width=True):
        try:
            df = pd.read_sql(query, conn)
            st.success(f"Query returned {len(df)} rows")
            st.dataframe(df, use_container_width=True)
            st.download_button("📥 Download Results", df.to_csv(index=False), "query_results.csv")
        except Exception as e:
            st.error(f"SQL Error: {e}")
    
    conn.close()


elif page == "✏️ CRUD":
    st.markdown("## ✏️ Player Management (CRUD)")
    
    conn = sqlite3.connect('cricbuzz_live.db')
    c = conn.cursor()
    
    
    with st.form("add_player"):
        st.subheader("➕ Add New Player")
        col1, col2 = st.columns(2)
        with col1:
            player_id = st.number_input("Player ID", min_value=1, step=1, value=100)
            name = st.text_input("Full Name")
        with col2:
            country = st.text_input("Country")
            role = st.selectbox("Playing Role", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
        
        if st.form_submit_button("💾 Add Player", use_container_width=True):
            if name:
                c.execute("INSERT OR IGNORE INTO players VALUES (?, ?, ?, ?)",
                          (player_id, name, country, role))
                conn.commit()
                st.success(f"✅ Player '{name}' added successfully!")
                st.rerun()
            else:
                st.error("Please enter player name")
    
    
    st.subheader("📋 Current Players")
    players = pd.read_sql("SELECT * FROM players ORDER BY name", conn)
    if not players.empty:
        st.dataframe(players, use_container_width=True, hide_index=True)
        
        
        st.subheader("🗑️ Delete Player")
        del_name = st.selectbox("Select player to delete", players['name'].tolist())
        if st.button("Delete Player", type="primary", use_container_width=True):
            c.execute("DELETE FROM players WHERE name=?", (del_name,))
            conn.commit()
            st.success(f"✅ Deleted player: {del_name}")
            st.rerun()
    else:
        st.info("No players in database. Use the form above to add players.")
    
    conn.close()


st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: rgba(255,255,255,0.7);'>🏏 Cricbuzz LiveStats - Real-time LIVE Cricket Data | Powered by Cricbuzz API</p>",
    unsafe_allow_html=True
)


if page == "🎯 Live Matches" and st.session_state.api_working:
    time.sleep(30)
    st.rerun()