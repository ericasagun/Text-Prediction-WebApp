from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.http import JsonResponse

import tensorflow as tf 
from tensorflow.keras.preprocessing.sequence import pad_sequences

from .forms import InputForm

import pickle
import os
import json
import numpy as np



# Load model
model = tf.keras.models.load_model(os.path.join(os.getcwd(), 'tweetApp', 'static', 'model', 'tweet_model'))
tokenizer_file = os.path.join(os.getcwd(), 'tweetApp', 'static', 'model', 'tokenizer.pickle')
with open(tokenizer_file, 'rb') as file:
    tokenizer = pickle.load(file)

# Main function, listens to the user activity on the text field.
def home(request):
    if request.method == 'POST' and request.is_ajax():
        text = request.POST.get('text')
        
        top_words = predictWord(text, 3, 1)
        predicted_twt = predictSentence(text)

        context = {'top1': top_words[0], 'top2': top_words[1], 'top3': top_words[2], 'tweet': predicted_twt}
        return JsonResponse(context)

    else:
        return render(request, 'home.html')

# Predicts the next word given the seed text
# returns top k words (based on probability) predicted by the model
def predictWord(seed_text, k=1):
    max_sequence_len = model.get_layer('embedding').output_shape[1]

    token_list = tokenizer.texts_to_sequences([seed_text])[0]
    token_list = pad_sequences([token_list], maxlen=max_sequence_len, padding='pre')

    predicted = model.predict(token_list, verbose=0)
    top_k_values, top_k_indices = tf.nn.top_k(predicted, k=k)

    indices = list(np.array(top_k_indices)[0])
    suggested_words = []
    for predicted in indices:
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                suggested_words.append(output_word)
                break
            
    return suggested_words

# Returns phrase predicted with n_seed+1 words (+1 for the seed_text)
def predictSentence(seed_text, n_seed=10):
    max_sequence_len = model.get_layer('embedding').output_shape[1]
    for _ in range(n_seed):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len, padding='pre')
        predicted = np.argmax(model.predict(token_list), axis=-1)
        
        output_word = ""
        
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
    return seed_text