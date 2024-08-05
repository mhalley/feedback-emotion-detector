import json
import requests

def emotion_detector(text_to_analyze):  # Define a function named emotion_detector that takes a string input (text_to_analyze)
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'  # URL of the emotion detector service
    myobj = { "raw_document": { "text": text_to_analyze } }  # Create a dictionary with the text to be analyzed
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}  # Set the headers required for the API request
    response = requests.post(url, json = myobj, headers=header, timeout=10)  # Send a POST request to the API with the text and headers

    # Parsing the JSON response from the API
    formatted_response = json.loads(response.text)
    # Extracting emotions from the response
    anger_score = formatted_response['emotionPredictions'][0]['emotion']['anger']
    disgust_score = formatted_response['emotionPredictions'][0]['emotion']['disgust']
    fear_score = formatted_response['emotionPredictions'][0]['emotion']['fear']
    joy_score = formatted_response['emotionPredictions'][0]['emotion']['joy']
    sadness_score = formatted_response['emotionPredictions'][0]['emotion']['sadness']
    
    dominant_emotion_score = max([anger_score, disgust_score, fear_score, joy_score, sadness_score])
    emotions = ['anger', 'disgust', 'fear', 'joy', 'sadness']
    dominant_emotion = [emotion for emotion in emotions if formatted_response['emotionPredictions'][0]['emotion'][emotion] == dominant_emotion_score][0]

    # If the response status code is 400, give value 'None' for all scores
    if response.status_code == 400:
        # Extracting sentiment label and score from the response
        anger_score = None
        disgust_score = None
        fear_score = None
        joy_score = None
        sadness_score = None
        dominant_emotion = None
        

    # Returning a dictionary containing emotional detector results
    return {'anger': anger_score, 'disgust': disgust_score, 'fear': fear_score, 'joy': joy_score, 'sadness': sadness_score, 'dominant_emotion': dominant_emotion}

