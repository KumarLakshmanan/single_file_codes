#!/bin/bash

# Usage ./server.sh aiflow
# Usage ./server.sh docsbot
# Usage ./server.sh

# $1 is the first argument
 
# if $1 is not empty
if [ -n "$1" ]; then
    # print the value of $1
    echo "Server: $1"
    if [ "$1" = "docsbot" ]; then
        cd /var/www/docsbot_flask
        source /var/www/docsbot_flask/venv/bin/activate
        git pull
        pm2 delete "docsbot_flask"
        pm2 start "python3.11 /var/www/docsbot_flask/app.py" --name "docsbot_flask"

        cd /var/www/docsbot_nextjs
        git pull
        pm2 delete "docsbot_nextjs"
        npm run build
        pm2 start "npm run start" --name "docsbot_nextjs"

    elif [ "$1" = "support" ]; then
        cd /var/www/support_flask
        source /var/www/support_flask/venv/bin/activate
        git pull
        pm2 delete "support_flask"
        pm2 start "python3.11 /var/www/support_flask/app.py" --name "support_flask"

        cd /var/www/support_nextjs
        git pull
        pm2 delete "support_nextjs"
        npm run build
        pm2 start "npm run start" --name "support_nextjs"

    elif [ "$1" = "aiflow" ]; then

        cd /var/www/aiflow_flask
        source /var/www/aiflow_flask/venv/bin/activate
        git pull
        pm2 delete "aiflow_flask"
        pm2 start "python3.11 /var/www/aiflow_flask/app.py" --name "aiflow_flask"

        cd /var/www/aiflow_nextjs
        git pull
        pm2 delete "aiflow_nextjs"
        pm2 start "npm run dev" --name "aiflow_nextjs"

        cd /var/www/aiflow_nodejs
        git pull
        pm2 delete "aiflow_nodejs"
        pm2 start "npm run production" --name "aiflow_nodejs"

        pm2 delete "flowise"
        pm2 start "npx flowise start" --name "flowise"
    else
        echo "Invalid server name"
    fi
else
    echo "Sorry please input the server name"
fi
