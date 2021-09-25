import requests
import json
import misc

def send_data_to_ai_server(ai_server_predictions_data, ai_server_image_encode_string) :
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
                        ai_server_data["detection_scores"] = [i for i in detection_scores_original if i >= 0.4] 
                    if detection_boxes_original and ai_server_data["detection_scores"] :
                        for i in ai_server_data["detection_scores"] :
                            index = detection_scores_original.index(i)
                            if index == 0 or index :
                                ai_server_data["detection_boxes"].append(detection_boxes_original[index])
                    if ai_server_image_encode_string :
                        ai_server_data["image"] = ai_server_image_encode_string
                    if label_original :
                        ai_server_data["label"] = list(set(label_original))[0]

                    response = requests.post("http://192.168.99.193:3001/post/req", json.dumps(ai_server_data))
                    logging.info(response)

    except Exception as e:
        misc.printerr("sendDataToAiServer", e)

# send_data_to_ai_server("hello","hey")