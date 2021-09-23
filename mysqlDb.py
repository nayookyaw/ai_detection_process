#import mysql.connector
#import mysql
import pymysql.cursors
import os
import datetime
import misc
#import uuid
import readconfig

from __main__ import * 


def mysql_data_input_folderA(uuid_value,filepath):
    try:
        '''
        mydb = pymysql.connect(
            host=readconfig.DBServerIPAddress,
            user=readconfig.DBUsername,
            password=readconfig.DBPassword,
            db=readconfig.DatabaseName,
            cursorclass=pymysql.cursors.DictCursor
        )
        '''
        mydb = connectdb()

        mycursor = mydb.cursor()

        sql = "insert into Folder_A_meta(uuid_meta,filepath,file_ts) values (%s,%s,convert(%s,datetime(3)))"
        val = (uuid_value,filepath,datetime.datetime.fromtimestamp(os.path.getctime(filepath)))
        mycursor.execute(sql, val)
        mydb.commit()

        print("Folder_A_meta: ", mycursor.rowcount," record inserted.")

    except Exception as e:
        misc.printerr("mysql_data_input_folderA", e)


def mysql_data_input_folderB(uuid_value,filepath):
    try:
        '''
        mydb = mysql.connector.connect(
            host=readconfig.DBServerIPAddress,
            user=readconfig.DBUsername,
            passwd=readconfig.DBPassword,
            database=readconfig.DatabaseName
        )
        '''
        mydb = connectdb()

        mycursor = mydb.cursor()

        sql = "insert into Folder_B_meta(uuid_meta,filepath,file_ts) values (%s,%s,convert(%s,datetime(3)))"
        val = (uuid_value,filepath,datetime.datetime.fromtimestamp(os.path.getctime(filepath)))
        mycursor.execute(sql, val)
        mydb.commit()

        print("Folder_B_meta: ", mycursor.rowcount," record inserted.")

    except Exception as e:
        misc.printerr("mysql_data_input_folderB", e)


def mysql_data_input_folderC(uuid_value,filepath):
    try:
        '''
        mydb = mysql.connector.connect(
            host=readconfig.DBServerIPAddress,
            user=readconfig.DBUsername,
            passwd=readconfig.DBPassword,
            database=readconfig.DatabaseName
        )
        '''
        mydb = connectdb()

        mycursor = mydb.cursor()

        sql = "insert into Folder_C_meta(uuid_meta,filepath,file_ts) values (%s,%s,convert(%s,datetime(3)))"
        val = (uuid_value,filepath,datetime.datetime.fromtimestamp(os.path.getctime(filepath)))
        mycursor.execute(sql, val)
        mydb.commit()

        print("Folder_C_meta: ", mycursor.rowcount," record inserted.")

    except Exception as e:
        misc.printerr("mysql_data_input_folderC", e)


def mysql_data_input_folderD(uuid_value,filepath,json_predict):
    try:
        '''
        mydb = mysql.connector.connect(
            host=readconfig.DBServerIPAddress,
            user=readconfig.DBUsername,
            passwd=readconfig.DBPassword,
            database=readconfig.DatabaseName
        )
        '''
        mydb = connectdb()

        mycursor = mydb.cursor()

        sql = "insert into Folder_D_meta(uuid_meta,filepath,file_ts,predict_json) values (%s,%s,convert(%s,datetime(3)),%s)"
        val = (uuid_value,filepath,datetime.datetime.fromtimestamp(os.path.getctime(filepath)),json_predict)
        mycursor.execute(sql, val)

        mydb.commit()

        print("Folder_D_meta: ", mycursor.rowcount," record inserted.")

    except Exception as e:
        misc.printerr("mysql_data_input_folderD", e)


def connectdb():
    try:
        mydb = pymysql.connect(
            host=readconfig.DBServerIPAddress,
            user=readconfig.DBUsername,
            password=readconfig.DBPassword,
            db=readconfig.DatabaseName,
            cursorclass=pymysql.cursors.DictCursor
        )
        return mydb

    except Exception as e:
        misc.printerr("connectdb", e)



