from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from transformers import logging
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import emoji,os
import warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
warnings.filterwarnings("ignore")
print("Loading models...")
logging.disable_progress_bar()

token_chat = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model_chat = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
with open('ACETH/chatbot/data/token_emoji.pkl','rb') as f:
    token_em = pickle.load(f)
with open('ACETH/chatbot/data/encoder_emoji.pkl','rb') as f:
    encod_em = pickle.load(f)

model_emoji = load_model('ACETH/chatbot/data/emoji_model.h5')
print('Model and tokenizer is loaded')

def addEmoji(text):
    x = pad_sequences(token_em.texts_to_sequences([text]),maxlen=30)
    y_hot = model_emoji.predict([x],verbose=0)[0]
    w_sum = sum(y_hot)
    sort = list(sorted(y_hot))
    dummy = []
    count = 0
    for i in sort:
        count+=i
        dummy.append(count)
    sort = dummy
    r = np.random.uniform(0,1)
    y = np.argmax(y_hot)
    for i,w in enumerate(sort[:-1]):
        if r <= w:
            y = i
            break
    y = encod_em.inverse_transform([y])[0]
    y= y.replace(':','')
    if y == 'male_sign':
        y=''
    text = emoji.emojize(f'{text} :{y}:')
    return text

step = 0
while 1:
    user_text = input('>> User : ')
    if user_text == ':q':
        step = 0
        break
    new_user_input_ids = token_chat.encode(user_text + token_chat.eos_token, return_tensors='pt')
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids
    chat_history_ids = model_chat.generate(bot_input_ids, max_length=1000, pad_token_id=token_chat.eos_token_id)
    text = token_chat.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    text = addEmoji(text)
    step+=1
    print('ACE chatbot : {}'.format(text))
