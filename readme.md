# 🏏 Cricbuzz LiveStats Dashboard

A real-time cricket analytics dashboard built using Streamlit, Python, SQL, and Cricbuzz API integration.

This project provides live cricket match insights, player statistics, database analytics, and interactive visual dashboards for cricket fans and data analysts.

---

# 🚀 Features

- 🔴 Live Match Tracking
- 📊 Interactive KPI Dashboard
- 🧑‍💻 Player Statistics Analysis
- 🏏 Team Performance Insights
- 🗄️ SQLite Database Integration
- 🌐 Cricbuzz API Integration
- 📈 Data Visualization
- ⚡ Real-Time Data Updates

---

# 🛠️ Technologies Used

## Programming Language
- Python

## Frontend
- Streamlit

## Database
- SQLite

## Libraries
- Pandas
- NumPy
- Requests
- Streamlit
- Plotly
- SQLite3

---

# 📂 Project Structure

```bash
cricbuzz_livestats/
│
├── assets/
│   └── style.css
│
├── database/
│   └── schema.sql
│
├── utils/
│   ├── __init__.py
│   ├── api_handler.py
│   ├── db_connection.py
│   └── queries.py
│
├── .env
├── cricbuzz_live.db
├── cricbuzz.db
├── main.py
└── README.md


⚙️ Installation
1️⃣ Clone Repository
git clone https://github.com/YOUR_USERNAME/cricbuzz-livestats.git
2️⃣ Navigate to Project Folder
cd cricbuzz-livestats
3️⃣ Create Virtual Environment
python -m venv .venv
4️⃣ Activate Virtual Environment
Windows
.venv\Scripts\activate
5️⃣ Install Dependencies
pip install -r requirements.txt
▶️ Run Application
streamlit run main.py
📊 Dashboard Output

The dashboard displays:

Live cricket match scores
Team statistics
Match KPIs
Player batting performance
SQL analytics reports
Interactive charts and visuals
Historical match analysis
🗄️ Database Features
Stores cricket match data
Tracks player statistics
SQL query-based analytics
Historical match records
🌐 API Integration

This project fetches live cricket data using:

Cricbuzz API
RapidAPI endpoints
📈 Future Enhancements
AI-based match prediction
Win probability analysis
Fantasy cricket recommendation system
Cloud deployment
User authentication