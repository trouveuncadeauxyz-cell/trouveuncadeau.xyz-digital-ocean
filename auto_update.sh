#!/bin/bash
# Auto-update script: Checks GitHub for new version and installs automatically

LOG_FILE="/var/www/trouveuncadeau/trouveuncadeau/auto_update.log"
REPO_DIR="/var/www/trouveuncadeau/trouveuncadeau"

echo "========================================" | tee -a $LOG_FILE
echo "$(date): 🔍 Checking GitHub for new version..." | tee -a $LOG_FILE

cd $REPO_DIR

# Fetch latest from GitHub
git fetch origin main 2>&1 | tee -a $LOG_FILE

# Compare local version with GitHub version
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" = "$REMOTE" ]; then
    echo "$(date): ✅ Already running latest version" | tee -a $LOG_FILE
    exit 0
fi

# NEW VERSION FOUND!
echo "$(date): 🆕 NEW VERSION FOUND ON GITHUB!" | tee -a $LOG_FILE
echo "$(date): 📥 Downloading and installing..." | tee -a $LOG_FILE

# Stop running services
echo "$(date): 🛑 Stopping services..." | tee -a $LOG_FILE
./stop_all.sh >> $LOG_FILE 2>&1
sleep 3

# Download new version from GitHub
echo "$(date): 📦 Pulling new version from GitHub..." | tee -a $LOG_FILE
git pull origin main 2>&1 | tee -a $LOG_FILE

# Install dependencies
source venv/bin/activate

echo "$(date): 📚 Installing updated dependencies..." | tee -a $LOG_FILE
pip install -r requirements.txt --break-system-packages >> $LOG_FILE 2>&1
pip install -r frontend/requirements-frontend.txt --break-system-packages >> $LOG_FILE 2>&1

# Clean cache
find backend frontend -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Restart with new version
echo "$(date): 🚀 Starting new version..." | tee -a $LOG_FILE
./start_all.sh >> $LOG_FILE 2>&1

echo "$(date): ✅ NEW VERSION INSTALLED AND RUNNING!" | tee -a $LOG_FILE
echo "========================================" | tee -a $LOG_FILE
