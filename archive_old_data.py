import datetime
import time
import os, shutil
import pymysql
import pymysql.cursors
from pymysql.constants import CLIENT
from mysqlDb import connectdb
from readconfig import DirOriginalImage,DirCheckedImage,DirBase64JSON,DirPredictionJSON,DirBackupOriginalImage,DirOriginalImageArch,DirCheckedImageArch,DirBase64JSONArch,DirPredictionJSONArch,DirBackupOriginalImageArch,PeriodMoveToArchive,PeriodDeleteFromArchive
import readconfig


def archive_on_db():
  try:
    mydb = connectdb_execmany()

##Moving all rows older than 30 days to archive tables

    mycursor = mydb.cursor()
    sql1 = "start transaction;insert into cctv_archivedb.Folder_A_arc select * from cctv_metadb.Folder_A_meta where file_ts < date_sub(now(),interval "+PeriodMoveToArchive+" day); delete from cctv_metadb.Folder_A_meta where file_ts < date_sub(now(),interval "+PeriodMoveToArchive+" day);commit;"
    sql2 = "start transaction;insert into cctv_archivedb.Folder_B_arc select * from cctv_metadb.Folder_B_meta where file_ts < date_sub(now(),interval "+PeriodMoveToArchive+" day); delete from cctv_metadb.Folder_B_meta where file_ts < date_sub(now(),interval "+PeriodMoveToArchive+" day);commit;"
    sql3 = "start transaction;insert into cctv_archivedb.Folder_C_arc select * from cctv_metadb.Folder_C_meta where file_ts < date_sub(now(),interval "+PeriodMoveToArchive+" day); delete from cctv_metadb.Folder_C_meta where file_ts < date_sub(now(),interval "+PeriodMoveToArchive+" day);commit;"
    sql4 = "start transaction;insert into cctv_archivedb.Folder_D_arc select * from cctv_metadb.Folder_D_meta where file_ts < date_sub(now(),interval "+PeriodMoveToArchive+" day); delete from cctv_metadb.Folder_D_meta where file_ts < date_sub(now(),interval "+PeriodMoveToArchive+" day);commit;"

    mycursor.execute(sql1) 
    mycursor.execute(sql2)
    mycursor.execute(sql3)
    mycursor.execute(sql4)

## Deleting all rows in archive tables older than 2 years


    sql5 = "delete from cctv_archivedb.Folder_A_arc where file_ts < date_sub(now(),interval "+PeriodDeleteFromArchive+" day);commit;"
    sql6 = "delete from cctv_archivedb.Folder_B_arc where file_ts < date_sub(now(),interval "+PeriodDeleteFromArchive+" day);commit;"
    sql7 = "delete from cctv_archivedb.Folder_C_arc where file_ts < date_sub(now(),interval "+PeriodDeleteFromArchive+" day);commit;"
    sql8 = "delete from cctv_archivedb.Folder_D_arc where file_ts < date_sub(now(),interval "+PeriodDeleteFromArchive+" day);commit;"

    mycursor.execute(sql5)
    mycursor.execute(sql6)
    mycursor.execute(sql7)
    mycursor.execute(sql8)

## Moving files older than 30 days to archive directory 

    prod_path_list=[DirBackupOriginalImage+'/',DirCheckedImage+'/',DirBase64JSON+'/',DirPredictionJSON+'/']

    for path in prod_path_list: 
      if os.listdir(path) != []:
        for f in os.listdir(path):
#          if os.path.join(path,f) == true:
#          try:
          full_path = os.path.join(path,f)
          print(f"assigning full_path")
#          except ValueError:
          print(f"directory {path} is empty")
#            break
#          else:
          print(f"full_path is : {full_path}")
#          print(f"from time stamp : {datetime.datetime.fromtimestamp(os.stat(full_path).st_mtime)}")
#          print(f"date today : {datetime.date.today() - datetime.timedelta(days=2)}")
          if datetime.datetime.fromtimestamp(os.stat(full_path).st_mtime).date() < datetime.date.today() - datetime.timedelta(days=int(PeriodMoveToArchive)):
#            print(f"passed if datetime")
            if os.path.isfile(full_path):
#              print (f"passed if isfile")
#              os.rename(full_path,os.path.join(path.replace('Folder_','Folder_arch_'),f))
              shutil.move(full_path,os.path.join(path.replace('Folder_','Folder_arch_'),f))
              print(f"new file : {os.path.join(path.replace('Folder_','Folder_arch_'),f)}")
          
## Deleting files in archive older than 2 years

    arch_path_list=[DirBackupOriginalImageArch+'/',DirCheckedImageArch+'/',DirBase64JSONArch+'/',DirPredictionJSONArch+'/']

    for path in arch_path_list:
      if os.listdir(path) != []:
        for f in os.listdir(path):
          full_path_arch = os.path.join(path,f)
          print(f"full_path_arch is :{full_path_arch}")
          if datetime.datetime.fromtimestamp(os.stat(full_path_arch).st_mtime).date() < datetime.date.today() - datetime.timedelta(days=int(PeriodDeleteFromArchive)):
            if os.path.isfile(full_path_arch):
              os.remove(full_path_arch)
              print(f"deleted {full_path_arch}")

  except Exception as e: 
    print(f"Archiving data failing with error : {e}")


def connectdb_execmany():
  try:
    mydb = pymysql.connect(
    host=readconfig.DBServerIPAddress,
    user=readconfig.DBUsername,
    password=readconfig.DBPassword,
    db=readconfig.DatabaseName,
    cursorclass=pymysql.cursors.DictCursor,
    client_flag=CLIENT.MULTI_STATEMENTS
    )
    return mydb

  except Exception as e:
    print(f"Archiving data failing with error : {e}")  

archive_on_db()
