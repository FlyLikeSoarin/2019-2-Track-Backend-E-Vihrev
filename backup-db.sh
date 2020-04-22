#! /bin/bash

if [ ! -d ".db-backup" ]; then
  # Setup
  mkdir ./.db-backup
  touch ./.db-backup/.congig

  echo "# Database backup configuration" >> ./.db-backup/.congig

  echo "ROTATIONS='5'" >> ./.db-backup/.congig
  echo "HOST='127.0.0.1'" >> ./.db-backup/.congig
  echo "PORT='5432'" >> ./.db-backup/.congig
  echo "USER='chat_db_admin'" >> ./.db-backup/.congig
  echo "PASS='5971'" >> ./.db-backup/.congig
  echo "DB='chat_db'" >> ./.db-backup/.congig
else
  # Backing up
  source ./.db-backup/.congig

  CURRENT_BACKUPS=$(ls ./.db-backup/ | wc -l)
  if (($CURRENT_BACKUPS >= $ROTATIONS)); then
    # Deleting oldest file
    echo "You reached limit of backups, oldest backup is going to be deleted."
    OLDEST=$(ls -tU ./.db-backup/ | tail -1)
    echo "Are you sure you want to delete [$OLDEST]? (y/n)"
    read answer
    if [ $answer == 'y' ]; then
      rm "./.db-backup/$OLDEST"
    else
      echo "Backup interrupted!"
      exit
    fi
  fi
  echo "Backing up..."
  DTTM=$(date)
  pg_dump -h $HOST -p $PORT -U $USER -d $DB -f "./.db-backup/backup $DTTM"
  echo "Finished!"
fi
