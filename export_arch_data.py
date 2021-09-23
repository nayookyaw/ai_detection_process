import datetime
import os,pwd,grp
import pymysql.cursors
from mysqlDb import connectdb
import shutil
import sys,stat
from readconfig import DirOriginalImage,DirCheckedImage,DirBase64JSON,DirPredictionJSON,DirBackupOriginalImage,DirOriginalImageArch,DirCheckedImageArch,DirBase64JSONArch,DirPredictionJSONArch,DirBackupOriginalImageArch,DirExportData

def validate(date_text):
  datetime.datetime.strptime(date_text, '%d-%m-%Y')


def print_menu():
  os.system('clear')
  print (30 * "-" , "EXPORT ARCHIVE DATA" , 30 * "-")
  print ("This tool exports data out of database & encrypted folder")
  print ("Data from database will be in the csv format ")
  print ("Both files will be stored in subdirectories under /home/sambauser/NAS/Export_Out/")
  print ("main directory /home/sambauser/NAS/Export_Out/")
  print ("TAKE NOTE THAT BOTH DATE ARE INCLUSIVE OF DATA TO BE EXPORTED")
#    print ("5. Exit")
#    print 67 * "-"


#    loop=True

#    while loop:          ## While loop which will keep going until loop = False
print_menu()    ## Displays menu

while True:
  try:
    fromdate = input("Export from date  [DD-MM-YYYY]: ")
    validate(fromdate)
  except ValueError:
    print(f"Sorry please enter value in right format")
    continue
  else:
    break

while True:
  try:
    untildate = input("Export until date  [DD-MM-YYYY]: ")
    validate(untildate)
  except ValueError:
    print(f"Sorry please enter value in right format")
    continue
  else:
    break

export_file = "Export_dump_"+datetime.datetime.now().strftime("%d%m%Y_%H%M%S")+".csv"
print(f"Exported file name will be /home/sambauser/NAS/Export_Out/{export_file}")


try: 

  ExportTempDir="/tmp/Datadump_"+datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
  FinalExportDir=DirExportData+ExportTempDir[4:]
  os.makedirs(ExportTempDir)
  os.makedirs(FinalExportDir)
  os.chmod(ExportTempDir,stat.S_IRWXU|stat.S_IROTH|stat.S_IWOTH|stat.S_IXOTH)
#  os.chmod(FinalExportDir,stat.S_IRWXU|stat.S_IROTH|stat.S_IWOTH|stat.S_IXOTH)

  mydb = connectdb()

  ##Moving all rows older than 30 days to archive tables

  mycursor = mydb.cursor()


  sql1 = "select * from cctv_archivedb.Folder_A_arc where file_ts between str_to_date('"+fromdate+"','%d-%m-%Y') and str_to_date('"+untildate+"','%d-%m-%Y') into outfile '"+ExportTempDir+"/Folder_A_arc_"+export_file+"' FIELDS TERMINATED BY '|' ENCLOSED BY '\"';"

#  print (sql1)

  sql2="select * from cctv_archivedb.Folder_B_arc where file_ts between str_to_date('"+fromdate+"','%d-%m-%Y') and str_to_date('"+untildate+"','%d-%m-%Y') into outfile '"+ExportTempDir+"/Folder_B_arc_"+export_file+"' FIELDS TERMINATED BY '|' ENCLOSED BY '\"';"

#  print(sql2)

  sql3="select * from cctv_archivedb.Folder_C_arc where file_ts between str_to_date('"+fromdate+"','%d-%m-%Y') and str_to_date('"+untildate+"','%d-%m-%Y') into outfile '"+ExportTempDir+"/Folder_C_arc_"+export_file+"' FIELDS TERMINATED BY '|' ENCLOSED BY '\"';"

  sql4="select * from cctv_archivedb.Folder_D_arc where file_ts between str_to_date('"+fromdate+"','%d-%m-%Y') and str_to_date('"+untildate+"','%d-%m-%Y') into outfile '"+ExportTempDir+"/Folder_D_arc_"+export_file+"' FIELDS TERMINATED BY '|' ENCLOSED BY '\"';"


  mycursor.execute(sql1)
  mycursor.execute(sql2)
  mycursor.execute(sql3)
  mycursor.execute(sql4)

  mycursor.close


except Exception as e:
  print(f"Export data from archive database failing with error : {e}")


try:
  ## Copy archived data out from archived folders to Export_Out folder

  arch_path_list=[DirBackupOriginalImageArch+'/',DirCheckedImageArch+'/',DirBase64JSONArch+'/',DirPredictionJSONArch+'/']

  for path in arch_path_list:
    if os.listdir(path) != []:
      for f in os.listdir(path):
        full_path_arch = os.path.join(path,f)
#        print(f"full_path_arch is :{full_path_arch}")
        if datetime.datetime.strptime(fromdate,'%d-%m-%Y') < datetime.datetime.fromtimestamp(os.stat(full_path_arch).st_mtime) < datetime.datetime.strptime(untildate,'%d-%m-%Y'):
          if os.path.isfile(full_path_arch):
#            print(f"path now is : {path}")
            if path == DirBackupOriginalImageArch+'/':
              if os.path.exists(FinalExportDir+"/Folder_arch_0"):
                pass
              else:
                os.makedirs(FinalExportDir+"/Folder_arch_0")
              shutil.copyfile(DirBackupOriginalImageArch+'/'+f,FinalExportDir+"/Folder_arch_0/"+f)
            
            elif path == DirCheckedImageArch+'/':
              if os.path.exists(FinalExportDir+"/Folder_arch_B"):
                pass
              else:
                os.makedirs(FinalExportDir+"/Folder_arch_B")
              shutil.copyfile(DirCheckedImageArch+'/'+f,FinalExportDir+"/Folder_arch_B/"+f)

            elif path == DirBase64JSONArch+'/':
              if os.path.exists(FinalExportDir+"/Folder_arch_C"):
                pass
              else:
                os.makedirs(FinalExportDir+"/Folder_arch_C")
              shutil.copyfile(DirBase64JSONArch+'/'+f,FinalExportDir+"/Folder_arch_C/"+f)

            elif path == DirPredictionJSONArch+'/':
              if os.path.exists(FinalExportDir+"/Folder_arch_D"):
                pass
              else:
                os.makedirs(FinalExportDir+"/Folder_arch_D")
              shutil.copyfile(DirPredictionJSONArch+'/'+f,FinalExportDir+"/Folder_arch_D/"+f)

            else:
              continue

#            os.remove(full_path_arch)

except Exception as e:
  print(f"Copy archived data from archived folder to Export_Out folder failing with error : {e}")

try:
  for s in os.listdir(ExportTempDir): 
    file_path = os.path.join(ExportTempDir,s)
    if os.path.isfile(file_path): 
      final_path=FinalExportDir+"/"+s
#      print(final_path)
      print(f"Final export dir : {final_path}")
      shutil.copyfile(file_path,final_path)

  shutil.rmtree(ExportTempDir)

except Exception as e:
  print(f"Copy archived data from temporary directory to Export_Out folder failing with error : {e}")


print(f"Exported data can be found in : {FinalExportDir}")

