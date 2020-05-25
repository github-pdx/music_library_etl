#!/bin/bash
## requirement: postgres
printf "%s starting...\n" "${BASH_SOURCE[0]}"
START=$(date +%s.%N)

psql -c "CREATE DATABASE media_db;" -U postgres
psql -c "CREATE USER run_admin_run WITH PASSWORD 'run_pass_run';" -U postgres

END=$(date +%s.%N)
RUNTIME=$(echo "$END - $START" | bc)
printf "runtime: %0.3f seconds" "$RUNTIME"

printf "%s complete...\n" "${BASH_SOURCE[0]}"


#  sudo -u postgres createuser run_admin_run
#  sudo -u postgres createdb media_db
# grant all privileges on database <dbname> to <username>
