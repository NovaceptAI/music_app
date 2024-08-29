import os
import requests
import uuid

from app.services.bpm_detection_service import bpm_detection
from app.services.scale_key_detection_service import scale_key_detection
from flask import Blueprint, request, jsonify, render_template
# from app.services import
import redis
from pydub import AudioSegment
# import speech_recognition as sr
from tenacity import retry, wait_exponential, stop_after_attempt
from app.config.db_config import db
from app import config
from app.services.lyrics_service import lyrics_extraction
from app.services.instrument_detection import detect_instruments
# from app.services.read_video import analyze_video
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'docx', 'mp3', 'wav', 'mp4'}

# Create a Blueprint for document-related routes
document_blueprint = Blueprint('documents', __name__)

# Redis client setup
r = redis.Redis(host='localhost', port=6379, db=0)

# Fetch the document that contains the 'gpt_key'
document = db.creds.find_one({"gpt_key": {"$exists": True}})
# Extract the 'gpt_key' value
if document:
    OPENAI_API_KEY = document.get('gpt_key')
else:
    # ChatGPT API configuration
    OPENAI_API_KEY = None


def call_chatgpt_api(prompt, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']


# def convert_audio_to_text(audio_path):
#     try:
#         # Load the audio file and convert it to WAV format
#         audio = AudioSegment.from_file(audio_path)
#         audio.export("temp.wav", format="wav")
#
#         # Use speech recognition to convert audio to text
#         recognizer = sr.Recognizer()
#         with sr.AudioFile("temp.wav") as source:
#             audio_data = recognizer.record(source)
#             text = recognizer.recognize_google(audio_data)
#
#         # Remove the temporary WAV file
#         os.remove("temp.wav")
#
#         return text
#     except FileNotFoundError:
#         return "Audio file not found."
#     except sr.RequestError:
#         return "Could not request results from Google Web Speech API."
#     except sr.UnknownValueError:
#         return "Google Web Speech API could not understand the audio."
#     except Exception as e:
#         return str(e)


# @document_blueprint.route('/upload', methods=['POST'])
# def upload_document():
#     files = request.files.getlist('document')
#     if not files:
#         return jsonify({'error': 'No documents uploaded'}), 400
#
#     document_ids = []
#     for file in files:
#         document_id = str(uuid.uuid4())
#         new_filename = file.filename.replace(" ", "_")
#         filepath = os.path.join('app/tmp', new_filename)
#         file.save(filepath)
#
#         # Enqueue document for processing
#         r.rpush('document_queue', document_id)
#         # Store document metadata in Redis
#         r.hmset(f'document_info:{document_id}', {'file_path': filepath, 'status': 'queued'})
#
#         document_ids.append(document_id)
#
#     return jsonify({'message': 'Documents uploaded successfully', 'document_ids': document_ids}), 200


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@document_blueprint.route('/upload', methods=['POST'])
def upload_files():
    url = request.form.get('url')
    document_files = request.files.getlist('document')
    video_files = request.files.getlist('video')
    audio_files = request.files.getlist('audio')

    document_ids = []

    if url:
        url_id = str(uuid.uuid4())
        # Assuming 'r' is your Redis connection instance
        r.hmset(f'document_info:{url_id}', {
            'url': url,
            'status': 'queued'
        })
        document_ids.append(url_id)

    for file_category, file_type in zip([document_files, video_files, audio_files], ['document', 'video', 'audio']):
        for file in file_category:
            if file and allowed_file(file.filename):
                document_id = str(uuid.uuid4())
                filename = secure_filename(file.filename)
                new_filename = filename.replace(" ", "_")
                filepath = os.path.join(f'app/tmp', new_filename)
                file.save(filepath)

                # Enqueue document for processing
                r.rpush(f'{file_type}_queue', document_id)
                # Store document metadata in Redis with additional 'name' field
                r.hmset(f'document_info:{document_id}', {
                    'file_path': filepath,
                    'status': 'queued',
                    'name': new_filename  # Storing the new filename as 'name'
                })

                document_ids.append(document_id)
            else:
                return jsonify({'error': f'Invalid {file_type} file type'}), 400

    if not document_ids and not url:
        return jsonify({'error': 'No files uploaded or no URL provided'}), 400

    return jsonify({'message': 'Files uploaded successfully', 'document_ids': document_ids})


@document_blueprint.route('/analyze', methods=['POST'])
def analyze_audio():
    document_ids = request.json.get('document_ids', [])  # Expect a list of document IDs
    features = request.json.get('features', [])
    # keywords = request.json.get('keywords', []) if 'Keyword' in features else []

    results = {}

    # Process each document ID
    for document_id in document_ids:
        doc_info_key = f'document_info:{document_id}'
        if not r.exists(doc_info_key):
            results[document_id] = {'error': 'Document ID does not exist'}
            continue

        # Set the document status to processing
        r.hset(doc_info_key, 'status', 'processing')
        r.hset(doc_info_key, 'features', ','.join(features))

        file_path = r.hget(doc_info_key, 'file_path').decode('utf-8')

        # Apply each feature to the document
        document_results = {}
        for feature in features:
            # if feature == "keyword":
            #     document_results[feature] = process_feature(file_path, feature, keywords)
            if feature == "lyrics_extraction":
                document_results[feature] = lyrics_extraction(file_path)
            elif feature == "instrument_detection":
                document_results[feature] = detect_instruments(file_path)
            elif feature == "scale_key_detection":
                document_results[feature] = scale_key_detection(file_path)
            elif feature == "bpm_detection":
                document_results[feature] = bpm_detection(file_path)
            else:
                results = {"No Feature Selected"}

        # Update Redis with the result and status of the document
        r.hmset(doc_info_key, {'status': 'completed', 'results': str(document_results)})

        # Store results for each document
        results[document_id] = document_results

    return jsonify({'message': 'Audio processed', 'results': results}), 200


def process_feature(file_path, feature, keywords=None):
    # Dictionary to map feature names to processing functions
    feature_functions = {}

    func = feature_functions.get(feature)
    if func:
        if feature == "keyword":
            return func(file_path, keywords)
        else:
            return func(file_path)
    return f"No available processing for feature: {feature}"


@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
def get_chatgpt_response(prompt, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    response_json = response.json()
    return response_json['choices'][0]['message']['content']


def process_features_with_chatgpt(text, features, api_key, summarization_type=None, translation_type=None, topic_modelling_type=None,
                                  language=None, keywords=None, filepath=None):
    """
    This Function processes features with the help of chatGPT and in house-trained models

    """

    results = {}
    output_dir = "results"  # Define the directory to save outputs

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if text == "":
        return "No Text Provided"
    for feature in features:

        # Get Sentiment Analysis
        if feature == "sentiment":
            prompt = f"Perform sentiment analysis on the following text:\n{text}"

        # Get Summarization
        elif feature == "summarization":
            if summarization_type == "comprehensive":
                prompt = f"Provide a comprehensive summary of the following text:\n{text}"
            elif summarization_type == "short":
                # prompt = f"Provide a short summary of the following text:\n{text}"
                prompt = f"Provide a short summary of the following text:\n{text}"
            else:
                prompt = f"Summarize the following text:\n{text}"

        # Get Translation
        elif feature == "translation":
            if translation_type == "summarised_translation":
                if language:
                    prompt = f"Summarize the following text in {language}:\n{text}"
                else:
                    prompt = "Error: Language not specified for translation."
            elif translation_type == "full_translation":
                if language:
                    prompt = f"Translate the following text in {language}:\n{text}"
                else:
                    prompt = "Error: Language not specified for translation."

        # Get Segmentation
        elif feature == "segmentation":
            prompt = f"Segment the following text into meaningful sections:\n{text}"
        elif feature == "clustering":
            prompt = f"Cluster the following text into meaningful sections:\n{text}"
        # Get Topic Modelling
        elif feature == "topic_modelling":
            if topic_modelling_type == "concise":
                prompt = f"Identify only the main topics of the following text:\n{text}"
            elif topic_modelling_type == "all_topics":
                # prompt = f"Provide a short summary of the following text:\n{text}"
                prompt = f"Identify all topics of the following text:\n{text}"
            else:
                prompt = f"Summarize the following text:\n{text}"

        # Get Chronology
        elif feature == "chronology":
            prompt = f"Send all dates and associated line or event in a chronological order:\n{text}"

        # Get Similarity
        elif feature == "similarity":
            prompt = f"Please find similar topics and lines from the pdf and mention here:\n{text}"

        # Get Entity Resolution
        elif feature == "entity":
            prompt = f"Perform entity resolution on:\n{text}"

        # Find the keywords
        elif feature == "keyword":
            results[feature] = process_feature(filepath, feature, keywords)
            continue
        try:
            response = get_chatgpt_response(prompt, api_key)
            results[feature] = response
            # Saving the formatted response to a file
            file_name = f"{uuid.uuid4()}_{feature}.txt"  # Unique filename for each feature
            file_path = os.path.join(output_dir, file_name)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(response)
            print(f"Saved {feature} output to {file_path}")

        except requests.exceptions.HTTPError as http_err:
                results[feature] = f"HTTP error occurred: {http_err}"
        except requests.exceptions.ConnectionError as conn_err:
            results[feature] = f"Connection error occurred: {conn_err}"
        except requests.exceptions.Timeout as timeout_err:
            results[feature] = f"Timeout error occurred: {timeout_err}"
        except requests.exceptions.RequestException as req_err:
            results[feature] = f"Request error occurred: {req_err}"

    return results


@document_blueprint.route('/analyze_models', methods=['POST'])
def analyze_with_chatgpt():
    document_ids = request.form.getlist('document_ids')  # This should be adjusted if document_ids is sent differently.
    if document_ids:
        document_ids = document_ids[0].split(',')
    features = request.form.getlist('features')  # Retrieves all 'features' as a list.
    # summarization_type = request.form.get('summary_type')  # Retrieves the summary type if available.
    # translation_type = request.form.get('translation_type')  # Retrieves the summary type if available.
    # topic_modelling_type = request.form.get('topic_modelling_type') # Retrieves the Topic Modelling type if available.
    # language = request.form.get('language')
    # keywords = request.form.get('keywords')
    # if keywords:
    #     keywords = keywords.split(',')
    # api_key = OPENAI_API_KEY
    # if api_key is None:
    #     return jsonify({'message': 'Key Value is Null'}), 200
    #
    # results = {}
    #
    # for document_id in document_ids:
    #     doc_info_key = f'document_info:{document_id}'
    #     if not r.exists(doc_info_key):
    #         results[document_id] = {'error': 'Document ID does not exist'}
    #         continue
    #     file_path = None
    #     if r.hexists(doc_info_key, 'url'):
    #         url = r.hget(doc_info_key, 'url').decode('utf-8')
    #         original_filename = url
    #         try:
    #             document_content = scrape_url.run_search_scraper(url)
    #         except Exception as e:
    #             results[document_id] = {'error': f'Failed to scrape URL: {str(e)}'}
    #             continue
    #     else:
    #         file_path = r.hget(doc_info_key, 'file_path').decode('utf-8')
    #         original_filename = r.hget(doc_info_key, 'name').decode('utf-8')
    #         try:
    #             document_content = get_document_content(file_path)
    #         except Exception as e:
    #             results[document_id] = {'error': f'Failed to read file: {str(e)}'}
    #             continue
    #
    # # Apply features to the document using ChatGPT document_results = process_features_with_chatgpt(
    # document_content, features, api_key, summarization_type, translation_type, topic_modelling_type, language,
    # keywords, file_path)
    #
    #     # Update Redis with the results and status of the document
    #     r.hmset(doc_info_key, {'status': 'completed', 'results': str(document_results)})
    #
    #     # Store results using the original filename as the key instead of document_id
    #     results[original_filename] = document_results

    # return render_template('results.html', results=results)
    return

def get_document_content(file_path):
    # if file_path.endswith('.pdf'):
    #     return summarization.extract_text_from_document(file_path)
    # elif file_path.endswith('.docx'):
    #     return summarization.extract_text_from_docx(file_path)
    # elif file_path.endswith('.txt'):
    #     return summarization.extract_text_from_txt(file_path)
    # elif file_path.endswith(('.wav', '.mp3', '.flac')):
    #     return convert_audio_to_text(file_path)
    # elif file_path.endswith(('.jpg', '.png', '.jpeg')):
    #     return azure_ocr_image(file_path)
    # elif file_path.endswith('.mp4'):
    #     return analyze_video(file_path)
    # elif file_path.endswith(('.txt', '.docx')):
    #     with open(file_path, 'r') as file:
    #         return file.read()
    # else:
    #     raise ValueError("Unsupported file format")
    return

# @document_blueprint.route('/progress/<document_id>', methods=['GET'])
# def get_progress(document_id):
#     doc_info_key = f'document_info:{document_id}'
#     if not r.exists(doc_info_key):
#         return jsonify({'error': 'Invalid document ID'}), 404
#
#     doc_info = r.hgetall(doc_info_key)
#     progress = {
#         'status': doc_info[b'status'].decode('utf-8'),
#         'results': doc_info.get(b'results', b'{}').decode('utf-8')
#     }
#     return jsonify(progress)
