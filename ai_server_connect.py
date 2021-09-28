import requests
import json
import misc
import logging
import threading

def send_data_to_ai_server(ai_server_predictions_data, ai_server_image_encode_string) :
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
                        "detection_scores" : [],
                        "detection_boxes" : [],
                        "label" : "",
                        "image" : "",
                    }
                    if detection_scores_original :
                        config_json = read_config_json()
                        max_thread = float(config_json['max_score'])

                        ai_server_data["detection_scores"] = [i for i in detection_scores_original if i >= max_thread] 
                    if ai_server_data["detection_scores"] :
                        if detection_boxes_original :
                            for i in ai_server_data["detection_scores"] :
                                index = detection_scores_original.index(i)
                                if index == 0 or index :
                                    ai_server_data["detection_boxes"].append(detection_boxes_original[index])
                        if label_original :
                            ai_server_data["label"] = list(set(label_original))[0]
                    if ai_server_image_encode_string :
                        ai_server_data["image"] = ai_server_image_encode_string
                    
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
# send_data_to_ai_server("hello","hey")