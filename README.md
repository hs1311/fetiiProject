# 🚗 FetiiPro LangChain SQL Chatbot

A powerful natural language to SQL chatbot built with LangChain and OpenAI GPT-4 for analyzing FetiiPro ride-sharing data.

## ✨ Features

- **🧠 Natural Language Processing**: Ask questions in plain English
- **🔍 SQL Generation**: Automatically converts questions to SQL queries
- **📊 Data Analysis**: Analyze demographics, riders, and trip data
- **🌐 Web Interface**: Beautiful, responsive web UI
- **📈 Analytics**: Track query performance and statistics
- **💾 Memory**: Remembers conversation context
- **🚀 GPT-4 Powered**: Advanced AI for accurate query understanding

## 🏗️ Project Structure

```
fetiipro/
├── src/
│   ├── langchain_chatbot.py    # Core chatbot logic
│   ├── langchain_web_app.py    # Web interface
│   └── simple_setup.py          # Database setup
├── data/
│   ├── csv_xlsx/               # Clean CSV files
│   └── database/               # SQLite database
├── requirements.txt            # Python dependencies
├── demo.html                   # Standalone demo
└── README.md                   # This file
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
set OPENAI_API_KEY=your_api_key_here
```

### 2. Setup Database
```bash
python src/simple_setup.py
```

### 3. Run Chatbot
```bash
# Web interface
python src/langchain_web_app.py

# Or use the batch file
START_CHATBOT.bat
```

### 4. Access Chatbot
- **Local**: http://localhost:8082
- **External**: http://[YOUR_IP]:8082

## 📊 Sample Questions

- "How many total trips are there?"
- "What is the average passenger count?"
- "How many trips happened on weekends?"
- "What are the busiest hours for trips?"
- "How many large group trips are there?"

## 🎯 Complex Queries Supported

- **Location-based**: "How many groups went to Moody Center last month?"
- **Demographic**: "What are the top drop-off spots for 18-24 year-olds?"
- **Time-based**: "When do large groups typically ride downtown?"
- **Multi-table joins**: Combines demographics, riders, and trips data

## 🛠️ Technical Stack

- **LangChain**: Framework for LLM applications
- **OpenAI GPT-4**: Advanced language model
- **SQLite**: Local database
- **Python HTTP Server**: Web interface
- **HTML/CSS/JavaScript**: Frontend

## 📈 Database Schema

### Tables
- **demographics**: user_id, age
- **riders**: trip_id, user_id, age
- **trips**: trip_id, booking_user_id, pick_up_address, drop_off_address, passenger_count, date, hour, day_of_week, is_weekend, time_of_day

### Relationships
- demographics.user_id ↔ riders.user_id
- riders.trip_id ↔ trips.trip_id
- trips.booking_user_id ↔ demographics.user_id

## 🔧 Configuration

The chatbot uses environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `PORT`: Server port (default: 8082)

## 📱 Demo Options

1. **Live Demo**: Run the web interface
2. **Standalone Demo**: Open `demo.html` in browser (no setup required)
3. **Interview Demo**: Use `INTERVIEW_DEMO.html` for presentations

## 🚀 Deployment

Ready for cloud deployment with:
- `Procfile`: Railway deployment configuration
- `app.json`: App metadata
- `runtime.txt`: Python version specification

## ✅ Verification

Use `verify_answers.py` to check chatbot accuracy:
```bash
python verify_answers.py
```

## 🎉 Success Metrics

- ✅ 2000 total trips in database
- ✅ Complex query support
- ✅ Real-time web interface
- ✅ GPT-4 powered responses
- ✅ Clean, professional UI

---

**Built with ❤️ using LangChain + OpenAI GPT-4**