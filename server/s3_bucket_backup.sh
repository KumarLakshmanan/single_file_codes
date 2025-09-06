#!/bin/bash
dates=$(date +"%Y-%m-%d")

zip -r "$dates.zip" /var/www/api/json
mv "$dates.zip" /root/filezip

find . -name "*.zip" -type f -mtime +7 -exec rm {} \;

aws s3 cp "/root/filezip/$dates.zip" s3://{AWS-S2-BUCKET}/json/

rm -rf "/root/filezip/$dates.zip"

# Database credentials
DB_HOST="{AWS-RDS-HOST}"
DB_USER=""
DB_PASSWORD=""
DB_NAME=""

# Backup filename
BACKUP_FILE="/root/dbzip/$dates.sql"

mysqldump -h $DB_HOST -P 3306 -u $DB_USER -p$DB_PASSWORD $DB_NAME --ignore-table={$DB_NAME.matrix_downline,$DB_NAME.food_suggestion} > $BACKUP_FILE

find . -name "*.sql" -type f -mtime +7 -exec rm {} \;

# aws s3 rm s3://{AWS-S2-BUCKET}/database/ --recursive

aws s3 cp "/root/dbzip/$dates.sql" s3://{AWS-S2-BUCKET}/database/

rm -rf "/root/dbzip/$dates.sql"
