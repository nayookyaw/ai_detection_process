import requests
import json
import misc
import logging
import threading
import cv2

def send_data_to_ai_server(ai_server_predictions_data, ai_server_image_encode_string, ai_server_file_name) :
    logging.basicConfig(level=logging.DEBUG ,filename='/home/osboxes/AI_Connect_log.txt', filemode='w', format=' %(asctime)s- %(message)s')

    try:
        if ai_server_predictions_data :
            ai_server_predictions_data_dict = ai_server_predictions_data.json()
            if ai_server_predictions_data_dict : 
                predictions_data_arr = ai_server_predictions_data_dict['predictions']
                if len(predictions_data_arr) > 0 :
                    predictions_data_arr = predictions_data_arr[0]
                    detection_scores_original = predictions_data_arr["detection_scores"]
                    detection_boxes_original = predictions_data_arr["detection_boxes"]
                    label_original = predictions_data_arr["detection_classes_as_text"]
                    ai_server_data = {
                        "label_score" : [],
                        "detection_boxes" : [],
                        "label_name" : "",
                        "image_data" : "",
                        "file_name" : "",
                    }
                    if detection_scores_original :
                        config_json = read_config_json()
                        max_thread = float(config_json['max_score'])

                        ai_server_data["label_score"] = [i for i in detection_scores_original if i >= max_thread] 
                    if ai_server_data["label_score"] :
                        if detection_boxes_original :
                            for i in ai_server_data["label_score"] :
                                index = detection_scores_original.index(i)
                                if index == 0 or index :
                                    ai_server_data["detection_boxes"].append(detection_boxes_original[index])
                            ai_server_data["detection_boxes"] = PhotoBoxLoc(ai_server_file_name, ai_server_data["detection_boxes"])
                        if label_original :
                            ai_server_data["label_name"] = list(set(label_original))[0]
                    if ai_server_image_encode_string :
                        ai_server_data["image_data"] = ai_server_image_encode_string
                    if ai_server_file_name :
                        ai_server_data["file_name"] = ai_server_file_name
                    
                    logging.info("send data to AI server")
                    # logging.info(ai_server_data)

                    # send data to AI Server
                    communicate_server_thred = threading.Thread(target=communicate_with_server, args=(ai_server_data,))
                    communicate_server_thred.start()

    except Exception as e:
        logging.error (str(e))
        misc.printerr("sendDataToAiServer", e)

def communicate_with_server(result_data):
    try:
        config_json = read_config_json()
        server_url = config_json['ai_sever_url']

        response = requests.post(server_url , json.dumps(result_data))
        logging.info(response)

    except Exception as err:
        logging.error(str(e))

def read_config_json():
    with open ('/home/osboxes/script/config.json', 'r') as config_data:
        data = config_data.read()
    
    return json.loads(data)

def PhotoBoxLoc(file_name, detection_box):
    file_path = "/home/sambauser/NAS/Folder_B/" + file_name
    im = cv2.imread(file_path)

    photo_size = list(im.shape)
    Photo_Height = photo_size[0]
    Photo_Width = photo_size[1]

    photo_size[0] = float(Photo_Height)
    photo_size[1] = float(Photo_Width)
    photo_size[2] = float(Photo_Height)
    photo_size.append(float(Photo_Width))
    
    new_detection_box = []
    if len(detection_box) > 0 :
        for item1 in detection_box:
            new_photo_size_list = []
            zipped_list = zip(photo_size, item1)
            new_photo_size_pair = list(zipped_list)

            for (x, y) in new_photo_size_pair:
                new_photo_size_list.append(x * y)
            new_detection_box.append(new_photo_size_list)
    return new_detection_box
    

# send_data_to_ai_server("hello","hey")