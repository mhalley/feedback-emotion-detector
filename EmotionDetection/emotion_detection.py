"""
Module Name: emotion_detection

Description:
    This module provides functions for performing emotion analysis on text data.
    It uses an external emotion analysis service to analyze the emotions of given text.

Functions:
    emotion_detector(text_to_analyze):
        Analyze the emotions of the given text and return the results. 
        Identify the dominant emotion within the text.

Usage:
    import emotion_detection

    emotion_result = emotion_detection.emotion_detector("I love this new technology!")
    print(emotion_result)
"""
import json
import requests

def emotion_detector(text_to_analyze):
    """
    Analyze the given text and detect emotions.

    Args:
        text_to_analyze (str): The text to be analyzed.

    Returns:
        dict: A dictionary containing emotion scores and the dominant emotion.
    """
    # URL of the emotion detector service
    url = ('https://sn-watson-emotion.labs.skills.network/v1/'
        'watson.runtime.nlp.v1/NlpService/EmotionPredict')

    # Create a dictionary with the text to be analyzed
    myobj = { "raw_document": { "text": text_to_analyze } }

    # Set the headers required for the API request
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    # Send a POST request to the API with the text and headers
    response = requests.post(url, json = myobj, headers=header, timeout=10)

    # Parse the JSON response from the API
    formatted_response = json.loads(response.text)

    # Check if 'emotionPredictions' key exists in the response
    # or if the response status code is 400
    if ('emotionPredictions' not in formatted_response or
        response.status_code == 400):
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    # Extract emotions from the response
    anger_score = formatted_response['emotionPredictions'][0]['emotion']['anger']
    disgust_score = formatted_response['emotionPredictions'][0]['emotion']['disgust']
    fear_score = formatted_response['emotionPredictions'][0]['emotion']['fear']
    joy_score = formatted_response['emotionPredictions'][0]['emotion']['joy']
    sadness_score = formatted_response['emotionPredictions'][0]['emotion']['sadness']

    dominant_emotion_score = max([anger_score, disgust_score, fear_score, joy_score, sadness_score])
    emotions = ['anger', 'disgust', 'fear', 'joy', 'sadness']
    dominant_emotion = [
        emotion for emotion in emotions
        if formatted_response['emotionPredictions'][0]['emotion'][emotion] == dominant_emotion_score
        ][0]

    # Return a dictionary containing emotional detector results
    return {
        'anger': anger_score, 
        'disgust': disgust_score, 
        'fear': fear_score, 
        'joy': joy_score, 
        'sadness': sadness_score, 
        'dominant_emotion': dominant_emotion
    }
