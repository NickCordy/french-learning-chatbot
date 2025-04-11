from flask import Flask, render_template, request
from utils import get_translation, get_chatbot_response, get_random_lemma, check_translation

app = Flask(__name__)

conversation_history = []
correct_guesses = 0
total_guesses = 0

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template('index.html', conversation_history=conversation_history)
    else:
        user_input = request.form['input']

        if not user_input:
            error_message = "Input cannot be empty. Please enter a valid message."
            return render_template(
                'index.html',
                conversation_history=conversation_history,
                error_message=error_message
            )

        response = get_chatbot_response(user_input, conversation_history)

        translated_input = get_translation(user_input)
        translated_response = get_translation(response)

        conversation_history.append({
            "user": {"eng": user_input, "fra": translated_input},
            "bot": {"eng": response, "fra": translated_response}
        })

        return render_template(
            'index.html',
            conversation_history=conversation_history,
            translation=translated_input,
            input=user_input,
            response=response,
            translated_response=translated_response
        )
    
@app.route('/lemma-guesser', methods=['POST', 'GET'])
def lemma_guesser():
    global total_guesses, correct_guesses

    if request.method == 'GET':
        random_lemma = get_random_lemma()
        return render_template('lemma-guesser.html', random_lemma=random_lemma)
    else:
        user_input = request.form['input']
        random_lemma = request.form['random_lemma']

        if not user_input:
            error_message = "Input cannot be empty. Please enter a valid translation."
            return render_template('lemma-guesser.html', random_lemma=random_lemma, error_message=error_message, guess_history=guess_history)

        is_correct, last_lemma = check_translation(user_input, random_lemma)

        if is_correct:
            correct_guesses += 1

        total_guesses += 1

        random_lemma = get_random_lemma()

        return render_template(
            'lemma-guesser.html',
            random_lemma=random_lemma,
            user_input=user_input,
            is_correct=is_correct,
            last_lemma=last_lemma,
            correct_guesses=correct_guesses,
            total=total_guesses
        )

if __name__ == "__main__":
    app.run(debug=True)