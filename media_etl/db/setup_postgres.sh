#!/bin/bash
## requirement: postgres  port: /data/postgresql.conf # (change requires restart) ~line: 63
printf "%s starting...\n" "${BASH_SOURCE[0]}"
START=$(date +%s.%N)

# ROLE WITH LOGIN can be used as a USER (alias)
psql -c "DROP DATABASE IF EXISTS media_db;" -U postgres
psql -c "DROP USER IF EXISTS run_admin_run;" -U postgres
psql -c "DROP ROLE IF EXISTS run_admin_run;" -U postgres

psql -c "CREATE ROLE run_admin_run WITH SUPERUSER CREATEDB LOGIN ENCRYPTED PASSWORD 'run_pass_run';" -U postgres
psql -c "CREATE DATABASE media_db WITH ENCODING='UTF8' OWNER=run_admin_run CONNECTION LIMIT=24;" -U postgres
psql -c "GRANT ALL PRIVILEGES ON DATABASE media_db to run_admin_run;" -U postgres

# list users withi attributes
psql -c "\du" -U postgres

# list databases
psql -c "\l" -U postgres

# connect to database
psql -c "\c media_db;" -U postgres

# list tables
psql -c "\dt" -U postgres

#psql media_db run_admin_run;
#quit

END=$(date +%s.%N)
RUNTIME=$(echo "$END - $START" | bc)
printf "runtime: %0.3f seconds" "$RUNTIME"
printf "%s complete...\n" "${BASH_SOURCE[0]}"
