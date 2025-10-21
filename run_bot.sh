#!/bin/bash
# Script to run asvz-bot with proper environment setup
# IMPROVED VERSION: Now checks WITHOUT logging in first!

# Configuration
BOT_DIR="$HOME/asvz-bot/src"
LESSON_ID="196346"  # Change this to your lesson ID
LOG_FILE="$HOME/asvz-bot/bot.log"

# Set display for headless browser
export DISPLAY=:99

# Ensure Xvfb is running
if ! pgrep -x "Xvfb" > /dev/null; then
    Xvfb :99 -screen 0 1280x1024x16 > /dev/null 2>&1 &
    sleep 2
fi

# Change to bot directory
cd "$BOT_DIR" || exit 1

# Activate virtual environment
source .venv/bin/activate

# Run the bot and log output
echo "=== Bot run started at $(date) ===" >> "$LOG_FILE"
python3 asvz_bot.py lesson "$LESSON_ID" >> "$LOG_FILE" 2>&1
echo "=== Bot run finished at $(date) ===" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
