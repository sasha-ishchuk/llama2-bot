import random

from flask import Flask, request, jsonify, render_template
import requests
from textblob import TextBlob

app = Flask(__name__)

OLLAMA_URL = 'http://localhost:11434/api/generate'

openings = [
    "Hi there! How can I assist you today?",
    "Hello! What can I help you with?",
    "Greetings! How may I be of service today?",
    "Hey! Looking for some information? I'm here to help!",
    "Good day! What would you like to talk about?"
]

closings = [
    "Thanks for chatting with me! Have a wonderful day!",
    "Glad I could help! Feel free to reach out if you have more questions.",
    "It was nice talking to you. Take care!",
    "Thanks for stopping by! Have a great day ahead!",
    "I'm here whenever you need me. Goodbye for now!"
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    hi_keywords = [
        "hello", "hi", "greetings", "hey", "good day", "howdy", "morning", "afternoon", "evening", "what's up"
    ]

    bye_keywords = [
        "goodbye", "bye", "farewell", "see you", "take care", "later", "thanks", "thank you", "have a great day",
        "cheers"
    ]

    shopping_keywords = [
        "buy", "purchase", "shop", "order", "checkout", "cart", "wishlist",
        "sale", "discount", "deal", "offer", "coupon", "promo", "promotion",
        "return", "exchange", "refund", "shipping", "delivery", "tracking",
        "product", "item", "stock", "availability", "brand", "size", "color",
        "price", "payment", "credit card", "debit card", "cash on delivery",
        "customer service", "support", "review", "rating", "feedback", "recommendation",
        "membership", "subscription", "gift card", "voucher", "store", "boutique",
        "checkout", "billing", "address", "invoice", "shopping bag", "ecommerce",
        "marketplace", "retailer", "merchandise", "fashion", "apparel", "electronics",
        "furniture", "home decor", "jewelry", "accessories", "gadget", "grocery"
    ]

    if any(keyword in user_input.lower() for keyword in hi_keywords):
        return jsonify({"response": random.choice(openings)})

    if any(keyword in user_input.lower() for keyword in bye_keywords):
        return jsonify({"response": random.choice(closings)})

    if not any(keyword in user_input.lower() for keyword in shopping_keywords):
        return jsonify({"response": "Sorry, I can only assist you with shopping ;(\n Try another question."})

    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "model": "llama2",
        "prompt": user_input,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, headers=headers, json=data)
        if response.status_code != 200:
            return jsonify({"error": "Failed to connect to Ollama"}), 500

        try:
            response_data = response.json()
            generated_text = response_data['response']

            blob = TextBlob(generated_text)
            if blob.sentiment.polarity >= 0:
                return jsonify({"response": generated_text})
            else:
                return jsonify({"response": "The response generated had a negative sentiment. Please try again."})

        except ValueError:
            return jsonify({"error": "Invalid JSON response from Ollama", "details": response.text}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
