#!/bin/bash

# MySQL credentials
db_user=""
db_password=""
mysql_host="host.docker.internal"
mysql_port="3306"

# Database information
new_db_name=""
new_user=""
new_user_password=""

# Connect to MySQL container and create the database
docker run --rm -e MYSQL_PWD="$db_password" mysql:8.0 \
  mysql -h "$mysql_host" -P "$mysql_port" -u "$db_user" -e "CREATE DATABASE IF NOT EXISTS $new_db_name;" 2>/dev/null
if [ $? -eq 0 ]; then
  echo "Database '$new_db_name' created successfully."
else
  echo "Error: Unable to create database '$new_db_name'. Exiting."
  exit 1
fi

# Create a new MySQL user with necessary privileges
docker run --rm -e MYSQL_PWD="$db_password" mysql:8.0 \
  mysql -h "$mysql_host" -P "$mysql_port" -u "$db_user" -e "CREATE USER '$new_user'@'%' IDENTIFIED BY '$new_user_password';" 2>/dev/null
docker run --rm -e MYSQL_PWD="$db_password" mysql:8.0 \
  mysql -h "$mysql_host" -P "$mysql_port" -u "$db_user" -e "GRANT ALL PRIVILEGES ON $new_db_name.* TO '$new_user'@'%';" 2>/dev/null
docker run --rm -e MYSQL_PWD="$db_password" mysql:8.0 \
  mysql -h "$mysql_host" -P "$mysql_port" -u "$db_user" -e "FLUSH PRIVILEGES;" 2>/dev/null
docker run --rm -e MYSQL_PWD="$db_password" mysql:8.0 \
  mysql -h "$mysql_host" -P "$mysql_port" -u "$db_user" -e "GRANT PROCESS ON *.* TO '$new_user'@'%';FLUSH PRIVILEGES;" 2>/dev/null
if [ $? -eq 0 ]; then
  echo "User '$new_user' created with privileges for database '$new_db_name'."
else
  echo "Error: Unable to create user or grant privileges. Exiting."
  exit 1
fi

echo "Script executed successfully."