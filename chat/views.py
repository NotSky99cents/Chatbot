from django.shortcuts import render

from django.http import HttpResponse

from .models import Intent, Pattern

import tensorflow as tf

from keras.models import Sequential, load_model

from keras.layers import Dense, Dropout

import nltk

from nltk.corpus import stopwords

from nltk.stem import WordNetLemmatizer

import numpy as np

import random

nltk.download("punkt")
nltk.download("wordnet")


intents = Intent.objects.all()
patterns = Pattern.objects.all()


words = []
classes = []
data_X = []
data_Y = []

lemmatizer = WordNetLemmatizer()
model = Sequential()


def train_model():
  global lemmatizer, model, intents, patterns, words, classes, data_X, data_Y
  for intent in intents:
    for pattern in Pattern.objects.filter(intents=intent):
      tokens = nltk.word_tokenize(pattern.question)
      words.extend(tokens)
      data_X.append(tokens)
      data_Y.append(intent.tags)

    if intent.tags not in classes:
      classes.append(intent.tags)





  words = [lemmatizer.lemmatize(word.lower()) for word in words if word != "?"]

  words = sorted(list(set(words)))

  classes = sorted(list(set(classes)))




  training = []

  output_empty = [0] * len(classes)




  for x, doc in enumerate(data_X):

      bag = []

      tokens = [lemmatizer.lemmatize(word.lower()) for word in doc]

      for word in words:

          bag.append(1) if word in tokens else bag.append(0)



      output_row = list(output_empty)

      output_row[classes.index(data_Y[x])] = 1

      training.append([bag, output_row])




  random.shuffle(training)

  training = np.array(training)




  train_X = list(training[:, 0])

  train_Y = list(training[:, 1])





  model.add(Dense(128, input_shape=(len(train_X[0]),), activation="relu"))

  model.add(Dropout(0.5))

  model.add(Dense(64, activation="relu"))

  model.add(Dropout(0.5))

  model.add(Dense(len(train_Y[0]), activation = "softmax"))

  adam = tf.keras.optimizers.legacy.Adam(learning_rate=0.01, decay=1e-6)

  model.compile(loss='categorical_crossentropy',

                optimizer=adam,

                metrics=["accuracy"])

  print(model.summary())

  model.fit(x=train_X, y=train_Y, epochs=100, verbose=1)




  model.save("chatbot_model.h5")

train_model()



def clean_text(text):

  tokens = nltk.word_tokenize(text)

  tokens = [lemmatizer.lemmatize(word) for word in tokens]

  return tokens




def bag_of_words(text, vocab):

  tokens = clean_text(text)

  bow = [0] * len(vocab)

  for w in tokens:

    for idx, word in enumerate(vocab):

      if word == w:

        bow[idx] = 1

  return np.array(bow)




def pred_class(text, vocab, labels):

  bow = bag_of_words(text, vocab)

  result = model.predict(np.array([bow]))[0] #Extracting probabilities

  thresh = 0.5

  y_pred = [[indx, res] for indx, res in enumerate(result) if res > thresh]

  y_pred.sort(key=lambda x: x[1], reverse=True) #Sorting by values of probability in decreasing order

  return_list = []

  for r in y_pred:

    return_list.append(labels[r[0]]) #Contains labels(tags) for highest probability

  return return_list


def get_Response(intents, data):
  if len(intents) == 0:
    result = "Sorry! I don't understand, but no worries I'm a quick learner, you can simply train me by adding this intent via admin panel"
  else:
    tag = intents[0]
    for i in data:
      if i.tags == tag:
        result = i.response
        break
  return result



def index(request):
  return render(request, 'index.html')


def get_output(request):
  user_input = request.GET.get('userMessage')
  global intents
  message = user_input.lower()
  Intent_list = pred_class(message, words, classes)
  result = get_Response(Intent_list, intents)
  return HttpResponse(result)