from telegram import Update
import requests
from telegram.ext import ContextTypes
from datetime import datetime
from repositories.analyze import analyze_mood
import json

async def message_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Analyze Mood
    mood, score = analyze_mood(user_text)

    # Save Diary
    now = datetime.now()
    date = {"timestamp": now.isoformat()}
    payload = {
        "diary_title": "Test Diary Title",
        "diary_desc": user_text,
        "diary_date": date['timestamp'],
        "diary_mood": round(score * 10),
        "diary_tired": 3 # for now
    }
    response = requests.post(f"http://localhost:8000/api/v1/diary", json=payload)
    data = response.json()

    if response.status_code == 201:
        await update.message.reply_text(f"Your mood seems: {mood}")
    else:
        await update.message.reply_text(f"Something went wrong. Please contact admin {data}")