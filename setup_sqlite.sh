#!/usr/bin/env bash

if [ -e mice.db ]; then
  read -p "Overwrite existing mice.db, erasing any existing data? " -n 1 -r
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm mice.db
    echo
    echo
  else
    echo
    echo "No disassemble!"
    exit
  fi
fi

echo "Creating new mice.db, with schema:"
sqlite3 mice.db < schema.sql
sqlite3 mice.db '.schema'
# sqlite3 mice.db '.schema event_types'

echo
echo "Event types:"
sqlite3 mice.db 'SELECT * FROM event_types;'
