from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        #user_question = request.form['question']

        ai_answer = getAnswer()
        
        return render_template('index.html', answer = ai_answer)

def getAnswer():
    pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-tc-big-en-fr")
    return print(pipe("The Portuguese teacher is very demanding."))


    #result = model(question = user_question, context = earth_context)
    #answer = result["answer"].capitalize() + ". I am " + str(round(result["score"] * 100)) + "% sure."

    #return answer