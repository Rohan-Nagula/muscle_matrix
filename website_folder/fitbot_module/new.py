import nltk
import json
import pickle
import random
import numpy as np
import tensorflow as tf
import nltk
nltk.download('punkt')  
nltk.download('wordnet')


from nltk.stem import WordNetLemmatizer
from tensorflow.python.keras.models import load_model

# Reduce words to the base
lemmatizer = WordNetLemmatizer()

# Loading Intents
intents_data = json.loads(open('C:\\Users\\nagula\\Desktop\\MuscleMatrix-main\\website_folder\\fitbot_module\\intents.json').read())

words_list = []
classes_list = []
documents_list = []
ignore_chars = ['?', '!', '.', ',']

# This loop tokenizes each pattern
for intent in intents_data['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words_list.extend(word_list)
        documents_list.append((word_list, intent['tag']))
        # Add a new tag for a new entry
        if intent['tag'] not in classes_list:
            classes_list.append(intent['tag'])

# Removes punctuation characters
words_list = [lemmatizer.lemmatize(word) for word in words_list if word not in ignore_chars]
#words_list = [word for word in words_list if word not in ignore_chars]
words_list = sorted(set(words_list))
classes_list = sorted(set(classes_list))

pickle.dump(words_list, open('C:\\Users\\nagula\\Desktop\\MuscleMatrix-main\\website_folder\\fitbot_module\\words.pkl', 'wb'))
pickle.dump(classes_list, open('C:\\Users\\nagula\\Desktop\\MuscleMatrix-main\\website_folder\\fitbot_module\\classes.pkl', 'wb'))

training_data = []
output_empty = [0] * len(classes_list)

# Creates the training dataset
for document in documents_list:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words_list:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes_list.index(document[1])] = 1
    training_data.append(bag + output_row)

random.shuffle(training_data)
training_data = np.array(training_data)

train_X = training_data[:, :len(words_list)]
train_Y = training_data[:, len(words_list):]

# Creates a sequential neural network model
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(128, input_shape=(len(train_X[0]),), activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(len(train_Y[0]), activation='softmax'))

# Stochastic Gradient Descent
sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist = model.fit(np.array(train_X), np.array(train_Y), epochs=200, batch_size=5, verbose=1)
model.save('C:\\Users\\nagula\\Desktop\\MuscleMatrix-main\\website_folder\\fitbot_module\\chatbot_model.h5', save_format='h5')
print('Done')
