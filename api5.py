from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import mysql.connector
import json
from flask_cors import CORS
import cv2

app = Flask(__name__)
# Flask is a Constructor
api = Api(app)
# Api is a Constructor


cors = CORS(app, resources={r"/*": {"origins": "*"}})


##########Function ###################################
def PhotoBoxLoc(file_path, detection_box):
    # Read the Picture File
    im = cv2.imread(file_path)
    # print(type(im))
    # <class 'numpy.ndarray'>

    # print(im.shape)
    # print(list(im.shape))

    photo_size = list(im.shape)
    Photo_Height = photo_size[0]
    Photo_Width = photo_size[1]

    photo_size[0] = float(Photo_Height)
    photo_size[1] = float(Photo_Width)
    photo_size[2] = float(Photo_Height)
    photo_size.append(float(Photo_Width))
    # Photo Size in [Width, Height, Width, Height]

    # photo_matrix =# Photo Size in [Width, Height, Width, Height] [2, 3, 4, 0]
    # detection_box = [[0.238297, 0.446573, 0.765433, 0.880406], [0.331163, 0.120934, 0.478664, 0.339374], [0.322562, 0.187295, 0.690267, 0.488482], [0.230202, 0.766153, 0.381013, 0.875938], [0.302857, 0.117515, 0.36726, 0.332599], [0.736115, 0.113087, 0.926413, 0.254083], [0.797695, 0.115138, 0.910356, 0.212412], [0.290084, 0.310391, 0.691657, 1.0], [0.314701, 0.12257, 0.353346, 0.33], [0.34574, 0.112566, 0.42333, 0.346847], [0.216635, 0.569127, 0.827022, 0.840302], [0.130413, 0.760619, 0.841457, 0.965981], [0.28539, 0.119398, 0.73209, 0.570998], [0.419273, 0.120382, 0.501385, 0.332204], [0.0, 0.515299, 0.727928, 0.87391], [0.145911, 0.778144, 0.381839, 0.86878], [0.0132249, 0.198175, 0.193175, 0.860297], [0.378885, 0.147223, 0.494336, 0.418416], [0.364768, 0.121554, 0.519297, 0.332328], [0.259861, 0.74414, 0.311914, 0.907792], [0.328469, 0.400853, 0.672036, 0.934839], [0.278605, 0.123204, 0.427437, 0.327325], [0.235433, 0.789132, 0.424956, 0.850993], [0.0, 0.955616, 0.109215, 0.995604], [0.216265, 0.747101, 0.252312, 0.905958], [0.0, 0.445165, 0.446449, 0.947666], [0.348877, 0.0807534, 0.490661, 0.393026], [0.00249179, 0.516985, 0.197672, 1.0], [0.0283553, 0.365459, 0.194156, 1.0], [0.00817014, 0.981717, 0.0923114, 0.99742], [0.349314, 0.0541833, 0.521823, 0.511554], [0.366984, 0.108716, 0.457738, 0.353463], [0.245887, 0.71903, 0.420415, 0.87069], [0.0, 0.977547, 0.068404, 0.999763], [0.212994, 0.697949, 0.246994, 0.864202], [0.291925, 0.143807, 0.372145, 0.384878], [0.384879, 0.105576, 0.642985, 0.37286], [0.0, 0.513198, 0.375927, 0.883201], [0.774476, 0.130211, 0.92469, 0.229426], [0.53762, 0.440847, 1.0, 0.955011]]

    new_detection_box = []

    for item1 in detection_box:
        new_photo_size_list = []
        # print("CHECKPOINT: item1:", item1)
        # Zip the Photo Size with the Point Locations in [x,y,x,y]
        zipped_list = zip(photo_size, item1)
        new_photo_size_pair = list(zipped_list)

        for (x, y) in new_photo_size_pair:
            new_photo_size_list.append(x * y)

        # print(new_photo_size_list)
        new_detection_box.append(new_photo_size_list)

    # print("CHECKPOINT:new_detection_box:{}".format(new_detection_box))

    return new_detection_box


def readconfigfile(filename):
    myfile = open(filename)
    x = myfile.readlines()

    lfile = []
    dictfile = {}
    num = 0

    for i in x:
        x[num] = i.rstrip("\n")
        z1 = x[num].split("=")
        z2 = tuple(z1)
        lfile.insert(num, z2)
        num += 1

    for x, y in lfile:
        dictfile.update({x: y})

    myfile.close()
    return dictfile


def checkPostedData(postedData, functionName):
    if (functionName == "DateSearch"):
        if "min_datetime" not in postedData or "max_datetime" not in postedData or "filter" not in postedData or "select_cat" not in postedData or "threshold" not in postedData:
            return 301  # Missing parameter
        else:
            return 200
    elif (functionName == "Threshold"):
        if "min_datetime" not in postedData or "max_datetime" not in postedData or "threshold" not in postedData:
            return 301  # Missing parameter
        else:
            return 200
    elif (functionName == "ViewConfig"):
        if "view_data" not in postedData:
            return 301  # Missing parameter
        else:
            return 200
    elif (functionName == "ObjectDetection"):

        ObjectDetectionParam={}

        if "threshold" not in postedData:
            ObjectDetectionParam['threshold'] = 0
        else:
            ObjectDetectionParam['threshold'] = postedData['threshold']

        if "start" not in postedData:
            ObjectDetectionParam['start'] = 'NULL'
        else:
            ObjectDetectionParam['start'] = postedData['start']

        if "end" not in postedData:
            ObjectDetectionParam['end'] = 'NULL'
        else:
            ObjectDetectionParam['end'] = postedData['end']

        if "maxscore" not in postedData:
            ObjectDetectionParam['maxscore'] = 0
        else:
            ObjectDetectionParam['maxscore'] = postedData['maxscore']

        if "limit" not in postedData:
            ObjectDetectionParam['limit'] = 0
        else:
            ObjectDetectionParam['limit'] = postedData['limit']

        if "offset" not in postedData:
            ObjectDetectionParam['offset'] = -1
        else:
            ObjectDetectionParam['offset'] = postedData['offset']

        ObjectDetectionParam['statuscode'] = 200
        print("Completed: Check for Parameter:")
        print("ObjectDetectionParam")
        return ObjectDetectionParam
	
    elif (functionName == "TotalCount"):

        TotalCountParam={}

        if "threshold" not in postedData:
            TotalCountParam['threshold'] = 0
        else:
            TotalCountParam['threshold'] = postedData['threshold']

        if "start" not in postedData:
            TotalCountParam['start'] = 'NULL'
        else:
            TotalCountParam['start'] = postedData['start']

        if "end" not in postedData:
            TotalCountParam['end'] = 'NULL'
        else:
            TotalCountParam['end'] = postedData['end']

        if "maxscore" not in postedData:
            TotalCountParam['maxscore'] = 0
        else:
            TotalCountParam['maxscore'] = postedData['maxscore']

        if "limit" not in postedData:
            TotalCountParam['limit'] = 0
        else:
            TotalCountParam['limit'] = postedData['limit']

        if "offset" not in postedData:
            TotalCountParam['offset'] = -1
        else:
            TotalCountParam['offset'] = postedData['offset']

        TotalCountParam['statuscode'] = 200
        print("Completed: Check for Parameter:")
        print("TotalCountParam")
        return TotalCountParam




def QuerySQL_new(x, y, threshold_val, maxscore, limit, offset):
    config_param = readconfigfile('/home/osboxes/script/config.txt')

    NAS_IP=str(config_param["NASServerIPAddress"])
    NAS_FTP_Folder=str(config_param["FTP_Folder"])
    NAS_Path="ftp://"+NAS_IP+NAS_FTP_Folder+"/"
    # print("CheckPoint:  NAS_Path:{}".format(NAS_Path))

    mydb = mysql.connector.connect(
        host=str(config_param["DBServerIPAddress"]),
        user=str(config_param["DBUsername"]),
        passwd='P@ssw0rd',
        database=str(config_param["DatabaseName"])
    )

    print("/n/nThe Values Return:/n/nx:{},y:{},threshold:{},maxscore:{}".format(x,y,threshold_val,maxscore))

    #Build the String
    Str_Start = "Folder_A_meta.file_ts >= \"{}\"".format(x)
    Str_End = "Folder_A_meta.file_ts <= \"{}\"".format(y)
    Str_Select = "SELECT Folder_A_meta.uuid_meta,Folder_A_meta.file_ts,Folder_B_meta.filepath, Folder_D_meta.predict_json FROM Folder_A_meta RIGHT JOIN Folder_D_meta ON Folder_A_meta.uuid_meta=Folder_D_meta.uuid_meta RIGHT JOIN Folder_B_meta ON Folder_A_meta.uuid_meta=Folder_B_meta.uuid_meta "
    Str_Order = "ORDER BY Folder_A_meta.file_ts DESC"

    # ADJUST THE SQLString based on the Requirements of x, y
    if x == "NULL":
        if y == "NULL":
            print("case 1")
            Str_Where = " "
            SQLString = Str_Select + Str_Where + Str_Order

        else:
            print("case 2")
            Str_Where = " WHERE "+ Str_End + " "
            SQLString = Str_Select + Str_Where + Str_Order

    else:
        if y == "NULL":
            print("case 3")
            Str_Where = " WHERE "+ Str_Start + " "
            SQLString = Str_Select + Str_Where + Str_Order
        else:
            print("case 4")
            Str_Where = " WHERE "+ Str_Start + " AND " + Str_End + " "
            SQLString = Str_Select + Str_Where + Str_Order

    if limit > 0 and offset > -1:
        Str_Pagination = " LIMIT "+ str(limit) + " OFFSET " + str(offset) + " "
        SQLString = SQLString + Str_Pagination


    print(SQLString)

    mycursor = mydb.cursor()
    mycursor.execute(SQLString)

    data = mycursor.fetchall()

    print("Checkpoint: SQL DATA Fetched")
    #print("TYPE of DATA:\n\n{}".format(type(data)))

    """
    # Create Statement
    SQLString = (
        "SELECT Folder_A_meta.uuid_meta,Folder_A_meta.file_ts,Folder_B_meta.filepath, Folder_D_meta.predict_json FROM Folder_A_meta RIGHT JOIN Folder_D_meta ON Folder_A_meta.uuid_meta=Folder_D_meta.uuid_meta RIGHT JOIN Folder_B_meta ON Folder_A_meta.uuid_meta=Folder_B_meta.uuid_meta WHERE Folder_A_meta.file_ts >= \"{}\" AND Folder_A_meta.file_ts <= \"{}\" ORDER BY Folder_A_meta.file_ts ASC".format(
            x, y))
    """



    # When No Data Returned,

    if len(data) == 0:
        print("There is no detection meet within defined situation.")
        data_notfound = {
            "Message": "There is no detection meet within defined situation."
        }

        return json.dumps(data_notfound, indent=4, sort_keys=False)

    i = 0
    ListDictOfWord = []

    # When Got Data Returned,
    # Check Data Based on Threshold
    for retData in data:
        field = ["uuid_meta", "file_ts", "filepath", "predict_json"]
        # Convert the DateTimetoString
        retData1 = list(retData)
        retData1[1] = str(retData1[1])

        #Keep Original Filepath for Manipulation later
        Original_filepath= retData1[2]

        # Change_File Path
        List_filepath = str(retData1[2]).split("/")
        retData1[2] = NAS_Path + List_filepath[-1]
        # print("CheckPoint:Changed File Path{}".format(retData1[2]))

        #predict_json
        # print("TYPE:".format(type(retData1[3])))
        retData1[3] = json.loads(retData1[3])
        # ZIP the Field and Data

        zipObj = zip(field, retData1)
        # Convert the zipObj to Dictionary
        dictOfWord = dict(zipObj)
        # print("Dict of Word: {}".format(dictOfWord))

        a = dictOfWord["predict_json"]

        if "predictions" in a:
            # filtered score is a Dictionary
            num_detect_status = check_num_detect(dictOfWord)

            if num_detect_status == 0:
                print("CheckPoint: NO DETECTION")
                Threshold_dictofWord = {
                    "uuid_meta": dictOfWord["uuid_meta"],
                    "file_ts": dictOfWord["file_ts"],
                    "filepath": dictOfWord["filepath"],
                    "label_score": "[]",
                    "detection_boxes": "[]",
                    "label_name": "[]",
                    "num_of_detection": 0,
                    "Message": "NO DETECTION"
                }

            else:
                filtered_score = filter_threshold(dictOfWord, threshold_val, Original_filepath)

                # [(Detection Box, Scoring , Detection Class as Text)]

                #When the Filtered Threshold NOT 0
                if len(filtered_score) != 0:
                    # print("Checkpoint: Filtered Score NOT = 0")
                    Label_Score = [j for i,j,k in filtered_score]
                    detection_boxes= [i for i,j,k in filtered_score]
                    Label_Name =  [k for i,j,k in filtered_score]

                    #Max Score
                    if maxscore == 1:
                        print("Checkpoint: Max Score= 1")
                        Max_Label_Score = max(Label_Score)
                        Max_detection_boxes = detection_boxes[Label_Score.index(Max_Label_Score)]
                        Max_Label_Name = Label_Name[Label_Score.index(Max_Label_Score)]
                        print("CHECKPOINT: Max_Label_Name")
                        print(Max_Label_Name)

                        Threshold_dictofWord = {
                            "uuid_meta": dictOfWord["uuid_meta"],
                            "file_ts": dictOfWord["file_ts"],
                            "filepath": dictOfWord["filepath"],
                            "label_score": Max_Label_Score,
                            "detection_boxes": detection_boxes,
                            "label_name": Label_Name[0],
                            "num_of_detection": (len(filtered_score)),
                            "Message": "OK"
                             }
                    else:
                        print("Checkpoint: Max Score= 0")
                        Threshold_dictofWord = {
                            "uuid_meta": dictOfWord["uuid_meta"],
                            "file_ts": dictOfWord["file_ts"],
                            "filepath": dictOfWord["filepath"],
                            "label_score": Label_Score,
                            "detection_boxes": detection_boxes,
                            "label_name": Label_Name[0],
                            "num_of_detection": (len(filtered_score)),
                            "Message": "OK"
                            }
                else:
                    # When the Filtered Threshold IS 0
                    print("Checkpoint: Filtered Score = 0")
                    Threshold_dictofWord = {
                        "uuid_meta": dictOfWord["uuid_meta"],
                        "file_ts": dictOfWord["file_ts"],
                        "filepath": dictOfWord["filepath"],
                        "label_score": "[]",
                        "detection_boxes": "[]",
                        "label_name": "[]",
                        "num_of_detection": 0,
                        "Message": "There is no detection meet within defined situation."

                        }
                ListDictOfWord.append(Threshold_dictofWord)

        else:
            break

    # Convert the Final Result to JSON
    # print("--------------------json_item")
    # print(ListDictOfWord)
    json_item = json.dumps(ListDictOfWord, indent=4)
    # print(json_item)

    # print("FALSE")
    # print(json_item)
    print("Checkpoint: List Dict of Word Done")

    return json_item
    # return jsonify(json_item)
    # cursor.close()
    # connection.close()

def QuerySQL_totalcount_new(x, y, threshold_val, maxscore):
    config_param = readconfigfile('/home/osboxes/script/config.txt')

    NAS_IP=str(config_param["NASServerIPAddress"])
    NAS_FTP_Folder=str(config_param["FTP_Folder"])
    NAS_Path="ftp://"+NAS_IP+NAS_FTP_Folder+"/"
    # print("CheckPoint:  NAS_Path:{}".format(NAS_Path))

    mydb = mysql.connector.connect(
        host=str(config_param["DBServerIPAddress"]),
        user=str(config_param["DBUsername"]),
        passwd='P@ssw0rd',
        database=str(config_param["DatabaseName"])
    )

    print("/n/nThe Values Return:/n/nx:{},y:{},threshold:{},maxscore:{}".format(x,y,threshold_val,maxscore))

    #Build the String
    Str_Start = "Folder_A_meta.file_ts >= \"{}\"".format(x)
    Str_End = "Folder_A_meta.file_ts <= \"{}\"".format(y)
    Str_Select = "SELECT Folder_A_meta.uuid_meta,Folder_A_meta.file_ts,Folder_B_meta.filepath, Folder_D_meta.predict_json FROM Folder_A_meta RIGHT JOIN Folder_D_meta ON Folder_A_meta.uuid_meta=Folder_D_meta.uuid_meta RIGHT JOIN Folder_B_meta ON Folder_A_meta.uuid_meta=Folder_B_meta.uuid_meta "
    Str_Order = "ORDER BY Folder_A_meta.file_ts DESC"

    # ADJUST THE SQLString based on the Requirements of x, y
    if x == "NULL":
        if y == "NULL":
            print("case 1")
            Str_Where = " "
            SQLString = Str_Select + Str_Where + Str_Order

        else:
            print("case 2")
            Str_Where = " WHERE "+ Str_End + " "
            SQLString = Str_Select + Str_Where + Str_Order

    else:
        if y == "NULL":
            print("case 3")
            Str_Where = " WHERE "+ Str_Start + " "
            SQLString = Str_Select + Str_Where + Str_Order
        else:
            print("case 4")
            Str_Where = " WHERE "+ Str_Start + " AND " + Str_End + " "
            SQLString = Str_Select + Str_Where + Str_Order

    print(SQLString)

    mycursor = mydb.cursor()
    mycursor.execute(SQLString)

    data = mycursor.fetchall()

    print("Checkpoint: SQL DATA Fetched")
    #print("TYPE of DATA:\n\n{}".format(type(data)))

    """
    # Create Statement
    SQLString = (
        "SELECT Folder_A_meta.uuid_meta,Folder_A_meta.file_ts,Folder_B_meta.filepath, Folder_D_meta.predict_json FROM Folder_A_meta RIGHT JOIN Folder_D_meta ON Folder_A_meta.uuid_meta=Folder_D_meta.uuid_meta RIGHT JOIN Folder_B_meta ON Folder_A_meta.uuid_meta=Folder_B_meta.uuid_meta WHERE Folder_A_meta.file_ts >= \"{}\" AND Folder_A_meta.file_ts <= \"{}\" ORDER BY Folder_A_meta.file_ts ASC".format(
            x, y))
    """



    # When No Data Returned,

    if len(data) == 0:
        print("There is no detection meet within defined situation.")
        data_notfound = {
            "Message": "There is no detection meet within defined situation."
        }

        return json.dumps(data_notfound, indent=4, sort_keys=False)

    # Convert the Final Result to JSON
    json_item = json.dumps({"total_count":len(data)}, indent=4, sort_keys=False)
    # print(json_item)

    # print("FALSE")
    # print(json_item)
    print("Checkpoint: List Dict of Word Done")

    return json_item
    # return jsonify(json_item)
    # cursor.close()
    # connection.close()



def check_num_detect(dictOfWord):
    a = dictOfWord["predict_json"]
    num_detection = a["predictions"][0]["num_detections"]
    if num_detection == 0:
        num_detect_result = 0

    else:
        num_detect_result = num_detection

    return num_detect_result



def filter_threshold(dictOfWord, threshold_val, Original_FilePath):
    # Decide the Category

    a = dictOfWord["predict_json"]
    num_detection= a["predictions"][0]["num_detections"]
    detection_boxes= a["predictions"][0]["detection_boxes"]
    scoring = a["predictions"][0]["detection_scores"]
    detection_classes_as_text=a["predictions"][0]["detection_classes_as_text"]

    #Convert the DetectionBox to new Picture Location
    new_detection_boxes = PhotoBoxLoc(Original_FilePath, detection_boxes)
    detection_boxes = new_detection_boxes

    #Combine all the results together
    #[(Detection Box, Scoring , Detection Class as Text)]
    zipped = zip(detection_boxes, scoring,detection_classes_as_text)
    predicted_zipped_result= list(zipped)

    #scoring = a["predictions"][0]["scores"]
    #i = 0

    # Check the Threshold Versus Scorings
    for x in scoring:
        # compare with threshold
        if float(x) <= float(threshold_val):
            predicted_zipped_result[scoring.index(x)] = 888

            #p = a["predictions"][0]["scores"]
            #q = a["predictions"][0]["labels"]
            #predicted [i] = 888
            # print("Scoring<Threshold")
        else:
            pass

            #p = a["predictions"][0]["scores"]
            #q = a["predictions"][0]["labels"]
            # print("Passed_Threshold")
        #i += 1

#    zip_a = zip(q, p)
#    dict_a = dict(zip_a)
    #dict_a_nz = {x: y for x, y in dict_a.items() if y != 888}
    clean_predicted_zipped_result=[item for item in predicted_zipped_result if item != 888 ]

    #json_retCat = dict_a_nz

    # Return as ()
    print("Checkpoint: Clean Predicted Zipped Result Done")
    return clean_predicted_zipped_result


##########Classes ###################################
class ObjectDetection(Resource):
    def post(self):
        # Basic Setting
        #config_param = readconfigfile('/home/osboxes/script/config.txt')

        # Check and Get the Status Code of Get
        postedData = request.get_json()
        print("Checkpoint: POSTED DATA DONE")
        print(postedData)

        # Check if Assign value=0 if no Value Return, Return as Dictionary
        ParamDict = checkPostedData(postedData, "ObjectDetection")

        # Call SQL
        x=ParamDict['start']
        y=ParamDict['end']
        threshold_val=ParamDict['threshold']
        maxscore=ParamDict['maxscore']
        print(x, y, threshold_val, maxscore)

        limit=ParamDict['limit']
        offset=ParamDict['offset']
        print("limit" , limit)
        print("offset" , offset)


        # Return Data from SQL Query
        Ret_Result = json.loads(QuerySQL_new(x, y, threshold_val, maxscore, limit, offset))

        #print(Ret_Result)


        #IP address of Server
        #serverIP = config_param["server_IP"]

        return jsonify(Ret_Result)

class TotalCount(Resource):
    def post(self):
        # Basic Setting
        #config_param = readconfigfile('/home/osboxes/script/config.txt')

        # Check and Get the Status Code of Get
        postedData = request.get_json()
        print("Checkpoint: POSTED DATA DONE")
        print(postedData)

        # Check if Assign value=0 if no Value Return, Return as Dictionary
        ParamDict = checkPostedData(postedData, "TotalCount")

	# Call SQL
        x=ParamDict['start']
        y=ParamDict['end']
        threshold_val=ParamDict['threshold']
        maxscore=ParamDict['maxscore']
        print(x, y, threshold_val, maxscore)

        # Return Data from SQL Query
        Ret_Result = json.loads(QuerySQL_totalcount_new(x, y, threshold_val, maxscore))

        #print(Ret_Result)


        #IP address of Server
        #serverIP = config_param["server_IP"]

        return jsonify(Ret_Result)


class GetTest(Resource):
    def post(self):
        postedData = request.get_json()
        print("Get Test OK")
        return ("GetTest OK"+postedData)

##########Add Resources ###################################

api.add_resource(ObjectDetection,"/objectdetection")
api.add_resource(TotalCount,"/totalcount")
api.add_resource(GetTest,"/gettest")

if __name__ == "__main__":
    app.run(host='0.0.0.0' , port=5000, debug=True)







