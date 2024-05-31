import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import tensorflow as tf
from tensorflow.python.keras.models import load_model


lemmatizer = WordNetLemmatizer()
intents_data = json.loads(open('C:\\Users\\nagula\\Desktop\\MuscleMatrix-main\\website_folder\\fitbot_module\\intents.json').read())
words_list = pickle.load(open('C:\\Users\\nagula\\Desktop\\MuscleMatrix-main\\website_folder\\fitbot_module\\words.pkl', 'rb'))
classes_list = pickle.load(open('C:\\Users\\nagula\\Desktop\\MuscleMatrix-main\\website_folder\\fitbot_module\\classes.pkl', 'rb'))
# model = load_model('C:\\Users\\nagula\\Desktop\\MuscleMatrix-main\\website_folder\\fitbot_module\\chatbot_model.h5')
model = tf.keras.models.load_model('C:\\Users\\nagula\\Desktop\\MuscleMatrix-main\\website_folder\\fitbot_module\\chatbot_model.h5')
# Tokenizes and lemmatizes the input sentence
def clean_up_sentence(sentence):
    sentence = sentence.lower()
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

# Converts a sentence into a bag of words representation
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words_list)
    for w in sentence_words:
        for i, word in enumerate(words_list):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Predicts the class (intent) of the input sentence
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # Sort by probability values
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    # If the highest probability is below a certain threshold, return a default response
    if len(results) == 0 or results[0][1] < 0.7:
        return_list.append({'intent': 'nointent', 'probability': '1.0'})
        return return_list
    for r in results:
        return_list.append({'intent': classes_list[r[0]], 'probability': str(r[1])})
    return return_list

# Retrieves a random response from the intents JSON file based on the predicted intent
def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result


# while True:
#     message = input("")
#     ints = predict_class(message)
#     res = get_response(ints, intents_data)
#     print(res)
