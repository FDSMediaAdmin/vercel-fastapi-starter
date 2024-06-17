#!/bin/bash
# Define the MySQL container credentials
db_user="root"
db_password="DatabasePassword"
db_name="DatabaseName"
mysql_host="host.docker.internal"
mysql_port="3307"

# Get the current date and time
current_datetime=$(date +'%Y%m%d_%H%M%S')

# Create the backup directory if it doesn't exist
backup_dir="./db/backup"
mkdir -p "$backup_dir"

# Create a subdirectory with the database name
db_backup_dir="$backup_dir/$db_name"
mkdir -p "$db_backup_dir"

# Create a subdirectory with the database name
db_backup_dir="$db_backup_dir/$current_datetime"
mkdir -p "$db_backup_dir"
# Retrieve a list of table names from the database and split it into an array
IFS=$'\n' read -d '' -r -a table_names <<< $(docker run --rm -e MYSQL_PWD="$db_password" mysql:8.0 \
  mysql -h "$mysql_host" -P "$mysql_port" -u "$db_user" -N -B -e "USE $db_name; SHOW TABLES;")


# Loop through the table names and create individual backups
for table_name in $table_names; do
  table_backup_file="$db_backup_dir/${table_name}.sql"
  echo "table_backup_file $table_backup_file"
  echo "after table_backup_file"
  #touch $table_backup_file
  docker run --rm -e MYSQL_PWD="$db_password" -v "$db_backup_dir:/backups" mysql:8.0 \
    sh -c "exec mysqldump -h "$mysql_host" -P "$mysql_port" -u$db_user $db_name $table_name" > "$table_backup_file"
  echo "Backup of table $table_name completed and saved to $table_backup_file"
done

echo "All table backups for database $db_name completed and saved in $db_backup_dir"