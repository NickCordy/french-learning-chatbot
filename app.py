from flask import Flask, render_template, request
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)

# Citation for model below
translate_model = pipeline("translation", model="Helsinki-NLP/opus-mt-tc-big-en-fr")

# Citation for model below
chatbot_model_name = "facebook/blenderbot-400M-distill"
chatbot_model = AutoModelForSeq2SeqLM.from_pretrained(chatbot_model_name)
chatbot_tokenizer = AutoTokenizer.from_pretrained(chatbot_model_name)

conversation_history_eng = []
conversation_history_fra = []

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':

         # Pair the conversations for the GET request 
        paired_conversations = zip(conversation_history_fra, conversation_history_eng)
        return render_template('index.html', paired_conversations = paired_conversations,)
    else:
        # Translates user's input and get responses both in French and English
        # Adds responses to conversation history

        user_input = request.form['input']

        response = get_chatbot_response(user_input)

        conversation_history_eng.append(user_input)
        conversation_history_eng.append(response)

        translated_input = get_translation(user_input)
        translated_response = get_translation(response)

        conversation_history_fra.append(translated_input)
        conversation_history_fra.append("Bot: " + translated_response)

        # Pair the conversations for rendering and return render_template with conversations
        paired_conversations = zip(conversation_history_fra, conversation_history_eng)
        return render_template('index.html',
                           paired_conversations = paired_conversations,
                           translation = translated_input,
                           input = user_input,
                           response = response,
                           translated_response = translated_response)

def get_translation(text):
    # Translates the text using the model

    result = translate_model(text)
    translated_text = result[0]['translation_text'].capitalize()
    return translated_text

def get_chatbot_response(user_input):
    # Generates a response from the chatbot based on the conversation history

    history_string = "\n".join(conversation_history_eng)
    inputs = chatbot_tokenizer.encode_plus(history_string, user_input, return_tensors="pt")
    outputs = chatbot_model.generate(**inputs, max_length=60)

    return chatbot_tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

if __name__ == "__main__":
    app.run()

# Translation Model: Helsinki-NLP/opus-mt-tc-big-en-fr
# @inproceedings{tiedemann-thottingal-2020-opus,
#     title = "{OPUS}-{MT} {--} Building open translation services for the World",
#     author = {Tiedemann, J{\"o}rg  and Thottingal, Santhosh},
#     booktitle = "Proceedings of the 22nd Annual Conference of the European Association for Machine Translation",
#     month = nov,
#     year = "2020",
#     address = "Lisboa, Portugal",
#     publisher = "European Association for Machine Translation",
#     url = "https://aclanthology.org/2020.eamt-1.61",
#     pages = "479--480",
# }

# @inproceedings{tiedemann-2020-tatoeba,
#     title = "The Tatoeba Translation Challenge {--} Realistic Data Sets for Low Resource and Multilingual {MT}",
#     author = {Tiedemann, J{\"o}rg},
#     booktitle = "Proceedings of the Fifth Conference on Machine Translation",
#     month = nov,
#     year = "2020",
#     address = "Online",
#     publisher = "Association for Computational Linguistics",
#     url = "https://aclanthology.org/2020.wmt-1.139",
#     pages = "1174--1182",
# }

# Conversational Model: facebook/blenderbot-400M-distill 
# @inproceedings{roller2020recipes,
#   author={Stephen Roller, Emily Dinan, Naman Goyal, Da Ju, Mary Williamson, Yinhan Liu, Jing Xu, Myle Ott, Kurt Shuster, Eric M. Smith, Y-Lan Boureau, Jason Weston},
#   title={Recipes for building an open-domain chatbot},
#   journal={arXiv preprint arXiv:2004.13637},
#   year={2020},
# }