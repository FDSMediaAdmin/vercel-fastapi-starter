#!/bin/bash

# Define the PostgreSQL container credentials
db_user="DatabaseUser"
db_password="DatabasePassword"
db_name="DatabaseName"
postgres_host="docker.for.mac.localhost"
postgres_port="5433"
schema_name="public"
image="postgres:16"


backup_dir="./db/backup/$db_name"
force_restore="false"

# Check if the database already exists
db_exists() {
  local dbname=$1
  echo "checking if db $dbname exists"
  if docker run --rm -e PGPASSWORD="$db_password" "$image" \
    psql -h "$postgres_host" -p "$postgres_port" -U "$db_user" -d "$dbname" -c "SELECT 1" 2>/dev/null; then
    return 0  # Database exists
  else
    return 1  # Database does not exist
  fi
}

# Check if we can continue (based on database existence and newdbname)
can_continue() {
  local db_exists_result=$1
  local newdbname="$2"

  if [ "$db_exists_result" -eq 0 ] && [ -n "$newdbname" ] && [ "$newdbname" != "$db_name" ]; then
    return 0  # We can continue
  else
    return 1  # We cannot continue
  fi
}

# Determine target Database name
get_database_name() {
  local db_exists_result=$1
  local can_continue_result=$2
  local newdbname="$3"
  local force_restore="$4"

  if [ "$force_restore" == "true" ]; then
    echo "$db_name"
  else
    if [ "$db_exists_result" -eq 0 ] && [ "$can_continue_result" -eq 0 ]; then
       echo "$newdbname"
    else
      echo "$db_name"
    fi
  fi
}

# Create the new database (if applicable) and return the database name
create_database() {
  local newdbname="$1"

  if [ "$db_exists_result" -eq 0 ] && [ "$can_continue_result" -eq 0 ]; then
    docker run --rm -e PGPASSWORD="$db_password" "$image" \
      psql -h "$postgres_host" -p "$postgres_port" -U "$db_user" -c "CREATE DATABASE $newdbname;"
    if [ $? -eq 0 ]; then
      echo 0
    else
      echo 1
    fi
  else
    echo 1
  fi
}

# Import SQL files from the specified subfolder
import_sql_files2() {
  local subfolder="$1"
  local dbname="$2"

  echo "import_sql_files:subfolder:$subfolder"
  echo "import_sql_files:dbname: $dbname"

  if [ -n "$subfolder" ]; then
    docker run --rm -v "$backup_dir/$subfolder:/backup" -e PGPASSWORD="$db_password" "$image" \
      psql -h "$postgres_host" -p "$postgres_port" -U "$db_user" -d "$dbname" -f /backup/*.sql
    echo "importing from folder $subfolder into db $dbname"
  else
    echo "No valid backup folders found in $backup_dir."
  fi
}

import_sql_files() {
  local subfolder="$1"
  local dbname="$2"

  if [ -n "$subfolder" ]; then
    sql_files=( "$subfolder"/*.sql )

    if [ ${#sql_files[@]} -eq 0 ]; then
      echo "No SQL files found in $backup_dir/$subfolder."
    else
      echo "sql_files: $sql_files"
      for sql_file in "${sql_files[@]}"; do
        echo "sql_file: $sql_file"
        cat "$sql_file" | docker run --rm -i -e PGPASSWORD="$db_password" "$image" \
          psql -h "$postgres_host" -p "$postgres_port" -U "$db_user" -d "$dbname"
        echo "Imported $sql_file into $dbname."
      done
    fi
  else
    echo "No valid backup folders found in $backup_dir."
  fi
}

# Process command-line arguments using getopts
while getopts ":n:f" opt; do
  case $opt in
    n)
      newdbname="$OPTARG"
      ;;
    f)
      force_restore="true"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# Find the newest subfolder in the backup directory by sorting, not by created or modified date
latest_backup_subfolder=$(ls -1 "$backup_dir" | grep -E '^[0-9]{8}_[0-9]{6}$' | sort -n | tail -n 1)

# Check if there are subfolders with backup files
if [ -z "$latest_backup_subfolder" ]; then
  echo "No backup folders found in $backup_dir."
  exit 1
fi

if [ "$force_restore" == "false" ]; then
  # Check if the source database exists
  db_exists $db_name
  db_exists_result=$?
else
  db_exists_result=0
fi

echo "force_restore value: $force_restore"
if [ "$force_restore" == "false" ]; then
  # Check if we can continue
  can_continue "$db_exists_result" "$newdbname"
  can_continue_result=$?
else
  can_continue_result=0
fi
echo "can_continue_result: $can_continue_result db_exists_result: $db_exists_result"
# Check if we can continue
if [ "$can_continue_result" -eq 1 ] &&  [ "$db_exists_result" -eq 0 ]; then
  echo "Error: Cannot continue. The database already exists, and no new database name is provided."
  exit 1
fi

# Get the database name
final_db_name=$(get_database_name "$db_exists_result" "$can_continue_result" "$newdbname" "$force_restore")
echo "finale db name: $final_db_name"
echo "newdbname $newdbname final_db_name $final_db_name"
# If new target database, check if it exists and exit if yes
if [ "$force_restore" == "false" ]; then
  if [ "$newdbname" != "$final_db_name" ]; then
    db_exists $final_db_name
    final_db_exists_result=$?
    if [ "$final_db_exists_result" -eq 0 ]; then
      echo "Error: Target Database exists, exiting"
      exit 1
    else
      echo "Target Database does not yet exist, continuing"
    fi
  fi
fi

if [ "$force_restore" == "false" ]; then
  # Create new database, we know already it doesn't exist
  create_database_result=$(create_database "$final_db_name")

  # Check if database creation succeeded and if not exit
  if [ $create_database_result -eq 0 ]; then
    echo "Database creation successful."
  else
    echo "Error: Database creation failed. Exiting."
    exit 1
  fi

else
   echo "Database reused."
   docker run --rm -e PGPASSWORD="$db_password" "$image" \
  psql -h "$postgres_host" -p "$postgres_port" -U "$db_user" -d "$db_name" -c "DO
  \$\$
  DECLARE
      r RECORD;
  BEGIN
      -- if the schema is different than the current one, add schema to table name as well
      FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = '$schema_name') LOOP
          EXECUTE 'DROP TABLE IF EXISTS $schema_name.' || quote_ident(r.tablename) || ' CASCADE';
      END LOOP;
  END
  \$\$;"


echo "All tables in schema '$schema_name' have been dropped."
fi

# Import SQL files into the final database
import_sql_files "$backup_dir/$latest_backup_subfolder" "$final_db_name"

echo "Data imported into $final_db_name from $latest_backup_subfolder"
