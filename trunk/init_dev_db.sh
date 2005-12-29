#!/bin/sh
#
# $Id$
#
# Initialize the development database.
#

DBFILE="grocerific.db"

#
# Make sure the database is empty by removing it.
#
rm -f $DBFILE

#
# Initialize the database with the table structure.
#
#sqlite3 $DBFILE < schema.sql || exit 1
tg-admin sql create || exit 1

#
# Load some test data.
#
sqlite3 -echo $DBFILE < dev_data.sql || exit 1
