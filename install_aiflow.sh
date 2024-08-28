sudo apt install nginx -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update -y
sudo apt install python3.11 -y
sudo apt install python3.11-distutils  -y
sudo apt install python3.11-dev -y
sudo apt install git wget zip -y
apt-get install pkg-config build-essential libmysqlclient-dev -y
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11
sudo apt install mariadb-server
sudo mysql_secure_installation

mysql

# SELECT user, host FROM mysql.user;
# CREATE DATABASE aiflow;
# CREATE DATABASE docsbot;
# CREATE DATABASE support;
# CREATE USER 'aiflow'@'%' IDENTIFIED BY 'Lakshmanan@2003';
# GRANT ALL PRIVILEGES ON aiflow.* TO 'aiflow'@'%';
# GRANT ALL PRIVILEGES ON docsbot.* TO 'aiflow'@'%';
# GRANT ALL PRIVILEGES ON support.* TO 'aiflow'@'%';

cd /var/www/
apt install tree nmap -y
wget https://files.phpmyadmin.net/phpMyAdmin/5.2.1/phpMyAdmin-5.2.1-all-languages.zip
unzip phpMyAdmin-5.2.1-all-languages.zip
rm phpMyAdmin-5.2.1-all-languages.zip
mv phpMyAdmin-5.2.1-all-languages/ phpmyadmin
git clone -b aiflow_flask https://gitlab.com/sragavan/projects aiflow_flask
git clone -b aiflow_flask git@gitlab.com:sragavan/projects.git aiflow_flask
git clone -b aiflow_nextjs git@gitlab.com:sragavan/projects.git aiflow_nextjs
git clone -b aiflow_nodejs git@gitlab.com:sragavan/projects.git aiflow_nodejs
git clone -b docsbot_flask git@gitlab.com:sragavan/projects.git docsbot_flask
git clone -b docsbot_nextjs git@gitlab.com:sragavan/projects.git docsbot_nextjs
git clone -b support_nextjs git@gitlab.com:sragavan/projects.git support_nextjs
git clone -b support_flask git@gitlab.com:sragavan/projects.git support_flask
git clone -b openinterpreter_react git@gitlab.com:sragavan/projects.git openinterpreter_react
git clone -b openinterpreter_flask git@gitlab.com:sragavan/projects.git openinterpreter_flask

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install 20.4
export NVM_DIR="$HOME/.nvm"
nvm install 20.4

node -v
npm -v

npm install flowise -g
npm install pm2 -g

cd /var/www/aiflow_nextjs/
npm i  --legacy-peer-deps

cd /var/www/aiflow_nodejs/
npm i  --legacy-peer-deps

cd /var/www/docsbot_nextjs/
npm i  --legacy-peer-deps

cd /var/www/support_nextjs
npm i  --legacy-peer-deps

cd /var/www/openinterpreter_react
npm i  --legacy-peer-deps

curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11
sudo apt install python3.11-venv -y

cd /var/www/docsbot_flask/
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd /var/www/aiflow_flask/
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd /var/www/support_flask
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd /var/www/openinterpreter_flask
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

service nginx restart
sudo apt install ca-certificates apt-transport-https software-properties-common -y
sudo add-apt-repository ppa:ondrej/php -y
sudo apt install --no-install-recommends php8.1 php8.1-fpm -y
sudo apt-get install -y php8.1-cli php8.1-common php8.1-mysql php8.1-zip php8.1-gd php8.1-mbstring php8.1-curl php8.1-xml php8.1-bcmath -y
sudo python3.11 -m venv /opt/certbot/
sudo /opt/certbot/bin/pip install --upgrade pip
sudo /opt/certbot/bin/pip install certbot certbot-nginx
sudo ln -s /opt/certbot/bin/certbot /usr/bin/certbot
sudo certbot --nginx
