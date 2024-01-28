from flask import Flask, render_template, request
from transformers import MarianMTModel, MarianTokenizer

app = Flask(__name__)

src_text = [
    "The Portuguese teacher is very demanding.",
    "When was your last hearing test?"
]

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        model_name = "pytorch-models/opus-mt-tc-big-en-fr"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        translated = model.generate(**tokenizer(src_text, return_tensors="pt", padding=True))
        for t in translated:
            print( tokenizer.decode(t, skip_special_tokens=True) )
        return render_template('index.html')
    #else:
        #user_question = request.form['question']

       # ai_answer = getAnswer(user_question)
        
        #return render_template('index.html', answer = ai_answer, question = user_question)

def getAnswer(user_question):
    model_name = "pytorch-models/opus-mt-tc-big-en-fr"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    translated = model.generate(**tokenizer(src_text, return_tensors="pt", padding=True))
    for t in translated:
        print( tokenizer.decode(t, skip_special_tokens=True) )

    f = open("earth.txt", "r")
    earth_context = f.read()

    result = model(question = user_question, context = earth_context)
    answer = result["answer"].capitalize() + ". I am " + str(round(result["score"] * 100)) + "% sure."

    return answer