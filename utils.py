import torch
import random
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# Initialize models
translate_model = pipeline("translation", model="Helsinki-NLP/opus-mt-tc-big-en-fr")
model_name = "facebook/blenderbot_small-90M"
chatbot_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
chatbot_tokenizer = AutoTokenizer.from_pretrained(model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
chatbot_model = chatbot_model.to(device)

pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en", framework='pt')

def get_translation(text):
    """Translates the text using the translation model."""
    result = translate_model(text)
    translated_text = result[0]['translation_text'].capitalize()
    return translated_text

def get_chatbot_response(user_input, conversation_history):
    """Generates a response from the chatbot based on the conversation history."""
    # Limit conversation history to the last 5 exchanges
    history_string = "\n".join(
        f"User: {entry['user']['eng']}\nBot: {entry['bot']['eng']}" for entry in conversation_history[-5:]
    )
    history_string += f"\nUser: {user_input}"

    # Tokenize and generate response
    inputs = chatbot_tokenizer.encode_plus(history_string, return_tensors="pt", truncation=True, max_length=512).to(device)
    outputs = chatbot_model.generate(
        **inputs,
        max_length=60,
        num_beams=5,
        no_repeat_ngram_size=2,
        early_stopping=True
    )
    return chatbot_tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

def get_random_lemma():
    """Fetch a random lemma from the CSV file."""
    random_int = random.randint(0, 10000)
    with open('10000-most-common-lemmas-fr.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines[random_int].strip()

def check_translation(user_translation, random_lemma):
    """Check if the user's translation matches the correct translation."""
    translation = pipe(random_lemma)
    correct_translation = translation[0]['translation_text']
    is_correct = user_translation.strip().lower() == correct_translation.strip().lower()
    return is_correct, correct_translation