#!/bin/bash

# Database type: mysql or postgres
db_type="postgres"

# Define the MySQL container credentials
mysql_user="root"
mysql_password="DatabasePassword"
mysql_db_name="DatabaseName"
mysql_host="host.docker.internal"
mysql_port="3307"

# Define the PostgreSQL container credentials
postgres_user="DatabaseUser"
postgres_password="DatabasePassword"
postgres_db_name="DatabaseName"
postgres_host="host.docker.internal"
postgres_port="5433"

# Get the current date and time
current_datetime=$(date +'%Y%m%d_%H%M%S')

# Create the backup directory if it doesn't exist
backup_dir="./db/backup"
mkdir -p "$backup_dir"

# Create a subdirectory with the database name
db_backup_dir="$backup_dir/$mysql_db_name"
mkdir -p "$db_backup_dir"

# Create a subdirectory with the database name and current datetime
db_backup_dir="$db_backup_dir/$current_datetime"
mkdir -p "$db_backup_dir"

if [ "$db_type" = "mysql" ]; then
  # Retrieve a list of table names from the database and split it into an array
  IFS=$'\n' read -d '' -r -a table_names <<< $(docker run --rm -e MYSQL_PWD="$mysql_password" mysql:8.0 \
    mysql -h "$mysql_host" -P "$mysql_port" -u "$mysql_user" -N -B -e "USE $mysql_db_name; SHOW TABLES;")

  # Loop through the table names and create individual backups
  for table_name in $table_names; do
    table_backup_file="$db_backup_dir/${table_name}.sql"
    echo "Backing up table $table_name to $table_backup_file"
    docker run --rm -e MYSQL_PWD="$mysql_password" -v "$db_backup_dir:/backups" mysql:8.0 \
      sh -c "exec mysqldump -h $mysql_host -P $mysql_port -u$mysql_user $mysql_db_name $table_name" > "$table_backup_file"
    echo "Backup of table $table_name completed and saved to $table_backup_file"
  done
  echo "All table backups for MySQL database $mysql_db_name completed and saved in $db_backup_dir"

elif [ "$db_type" = "postgres" ]; then
  # Retrieve a list of table names from the database and split it into an array
  IFS=$'\n' read -d '' -r -a table_names <<< $(docker run --rm -e PGPASSWORD="$postgres_password" postgres:16 \
    psql -h "$postgres_host" -p "$postgres_port" -U "$postgres_user" -d "$postgres_db_name" -t -c "SELECT tablename FROM pg_tables WHERE schemaname='public';")

  # Loop through the table names and create individual backups
  for table_name in $table_names; do
    table_backup_file="$db_backup_dir/${table_name}.sql"
    echo "Backing up table $table_name to $table_backup_file"
    docker run --rm -e PGPASSWORD="$postgres_password" -v "$db_backup_dir:/backups" postgres:16 \
      sh -c "exec pg_dump -h $postgres_host -p $postgres_port -U $postgres_user -t $table_name $postgres_db_name" > "$table_backup_file"
    echo "Backup of table $table_name completed and saved to $table_backup_file"
  done
  echo "All table backups for PostgreSQL database $postgres_db_name completed and saved in $db_backup_dir"
else
  echo "Unsupported database type: $db_type"
  exit 1
fi
