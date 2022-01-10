import pymysql.cursors
import readconfig

import schedule
import time 

import os

from constants import Constants

class Manage_Data :

    connection = ""
    cursor = ""

    def remove_dbtable_data ():
        print("start dbtable data deleting ...")

        try :
            
            if Manage_Data.connection and Manage_Data.cursor :

                for dbtable in Constants.DB_TABLES :
                    sql = "delete from " + dbtable
                    Manage_Data.cursor.execute(sql)

                Manage_Data.connection.commit()

                print("DBTable data has been deleted successfully!")

        except Exception as e :
            print("Error while deleting dbtable data from MySQL", str(e))

    def remove_folder_b_c_d_data ():
        print("start folder_b_c_d data deleting ...")

        try :

            for folder in Constants.FOLDERS :
                remove_filepath = Constants.FOLDER_PATH + folder

                # remove files 
                items = os.listdir(remove_filepath)
                for item in items :
                    os.remove(os.path.join(remove_filepath, item))

            print("Folder B,C,D data has been deleted successfully!")

        except Exception as e :
            print("Error while deleting folder b,c,d data from MySQL", str(e))

    def connet_db () :
        try :
            Manage_Data.connection = pymysql.connect(
                    host=readconfig.DBServerIPAddress,
                    user=readconfig.DBUsername,
                    password=readconfig.DBPassword,
                    db=readconfig.DatabaseName,
                    cursorclass=pymysql.cursors.DictCursor
                )
            if Manage_Data.connection:
                Manage_Data.cursor = Manage_Data.connection.cursor()
        except Exception as e :
            print("Error while connecting to MySQL", str(e))

# connet_db
Manage_Data.connet_db()

# schedule tasks
schedule.every(Constants.INTERVAL_SECONDS).seconds.do(Manage_Data.remove_dbtable_data)
schedule.every(Constants.INTERVAL_SECONDS).seconds.do(Manage_Data.remove_folder_b_c_d_data)
while True:
    schedule.run_pending()
    time.sleep(1)