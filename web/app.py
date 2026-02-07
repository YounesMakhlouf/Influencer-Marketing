import logging
import os
import pickle

import httpx

from flask import Flask, request, jsonify

from web.cleaning import clean_and_process_content
from dataScraper.dataParser import parse_user
from dataScraper.scraper import scrape_user

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

_HERE = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(_HERE, 'bert_9.pkl')

with open(input_file, 'rb') as f_in:
    topic_model = pickle.load(f_in)

# Load the BERTopic model
_topic_label_map: dict[int, str] = {
    topic_id: label
    for topic_id, label in zip(
        topic_model.topic_labels_.keys(),
        topic_model.generate_topic_labels(),
    )
}

app = Flask(__name__)


def get_topic_details(topic_id):
    label = _topic_label_map.get(topic_id, f"Unknown_{topic_id}")
    return {'id': int(topic_id), 'label': label}


def scrape_user_data(name):
    """Scrape and parse an Instagram user's bio and category.

    Raises:
        httpx.HTTPStatusError: If the Instagram API returns an error.
        ValueError: If the response doesn't contain valid user data.
    """
    scraped_data = scrape_user(name)
    if 'data' not in scraped_data or 'user' not in scraped_data['data']:
        raise ValueError(f"Invalid user data received for '{name}'")

    user_data = parse_user(scraped_data['data']['user'])
    return {'bio': user_data['bio'], 'category': user_data['category']}


def predict_topics(text):
    topics, probs = topic_model.transform([text])
    topic_details = get_topic_details(topics[0])
    return topic_details, probs.tolist()


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text input'}), 400

        text = data['text']

        # Get topic predictions
        topic_details, probs = predict_topics(text)
        topic_label = topic_details['label']
        return jsonify({'label': topic_label, 'probs': probs})
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.json
        if not data or 'name' not in data:
            return jsonify({'error': 'Missing username input'}), 400

        name = data['name']
        result = scrape_user_data(name)
        return jsonify(result)
    except httpx.HTTPStatusError as e:
        logging.error("Instagram API error for user '%s': %s", name, e)
        return jsonify({'error': f'Instagram API error: {e.response.status_code}'}), 502
    except Exception as e:
        logging.error("Scrape error: %s", e)
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/predict_user', methods=['POST'])
def full_process():
    try:
        data = request.json
        if not data or 'name' not in data:
            return jsonify({'error': 'Missing username input'}), 400

        name = data['name']
        user_data = scrape_user_data(name)
        bio = user_data['bio']
        category = user_data['category']
        if category is not None:
            bio += ' ' + category

        cleaned_bio = clean_and_process_content(bio)
        topic_details, probs = predict_topics(cleaned_bio)

        result = {'bio': cleaned_bio, 'topics': topic_details, 'probs': probs}
        return jsonify(result)
    except httpx.HTTPStatusError as e:
        logging.error("Instagram API error for user '%s': %s", name, e)
        return jsonify({'error': f'Instagram API error: {e.response.status_code}'}), 502
    except Exception as e:
        logging.error("Prediction error: %s", e)
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
