from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

DB_NAME = '312project'

TABLES = {}

TABLES['user'] = (
    "CREATE TABLE `user` ("
        "`username` VARCHAR(99) NOT NULL,"
        "`password` VARCHAR(99) NOT NULL,"
        "`is_online` BOOLEAN,"
        "`username_color` VARCHAR(99) ,"
        "`bio` VARCHAR(99) NOT NULL,"
        "PRIMARY KEY (`username`)"
    ") ENGINE=InnoDB")

TABLES['voting'] = (
    "CREATE TABLE `voting` ("
    "   `vote_ID` INT NOT NULL,"
    "   `creator_username` VARCHAR(99) NOT NULL,"
    "   `vote_name` VARCHAR(99) NOT NULL,"
    "   `vote_description` VARCHAR(99) NOT NULL,"
    "   `photo` BLOB,"
    "   `option_one_name` VARCHAR(99) NOT NULL,"
    "   `option_one_votes` INT NOT NULL,"
    "   `option_two_name` VARCHAR(99) NOT NULL,"
    "   `option_two_votes` INT NOT NULL,"
    "   `option_three_name` VARCHAR(99),"
    "   `option_three_votes` INT,"
    "   `option_four_name` VARCHAR(99),"
    "   ` option_four_votes` INT,"
    "   `option_five_name` VARCHAR(99),"
    "   `option_five_votes` INT,"
    "   PRIMARY KEY (`vote_ID`),"
    "   FOREIGN KEY (`creator_username`) REFERENCES `user`(`username`)"
    ") ENGINE=InnoDB")

TABLES['message'] = (
    "CREATE TABLE `message`  ("
        "`message_ID` INT NOT NULL,"
        "`sender_username` VARCHAR(99) NOT NULL,"
        "`receiver_username` VARCHAR(99) NOT NULL,"
        "`content` VARCHAR(999) NOT NULL,"
        "`message_time` DATETIME NOT NULL,"
        "PRIMARY KEY (`message_ID`),"
        "FOREIGN KEY (`sender_username`) REFERENCES `user`(`username`),"
        "FOREIGN KEY (`receiver_username`) REFERENCES `user`(`username`)"
    ") ENGINE=InnoDB")


cnx = mysql.connector.connect(user='root', password='sammy_liu',
                              host='127.0.0.1')
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()