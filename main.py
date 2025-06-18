import json
import os
import requests
from openai import OpenAI
import time
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Import configuration
try:
    from config import (
        AZURE_OPENAI_API_KEY as azure_openai_api_key,
        AZURE_OPENAI_BASE_URL as azure_openai_base_url,
        AZURE_BING_SUBSCRIPTION_KEY as azure_bing_subscription_key,
        AZURE_BING_ENDPOINT as azure_bing_endpoint
    )
except ImportError:
    logging.error(
        "config.py not found. Please copy config_template.py to config.py and fill in your API keys.")
    exit(1)

# Load model and tokenizer


def complete(prompt, data_dict, max_tokens=100):
    client = OpenAI(base_url=azure_openai_base_url,
                    api_key=azure_openai_api_key)
    out = []
    for i, p in enumerate(prompt):
        try:
            logging.info(f"Sending completion request for prompt {i}")
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": p},
                    {"role": "user", "content": p}
                ]
            )
            text = completion.choices[0].message.content.strip()
            if '**' in text:
                text = text.replace("**", "")
            j = {
                "id": data_dict[i]['id'],
                "question": data_dict[i]['question'],
                "query": data_dict[i]['query'],
                "answer": text
            }
            out.append(j)
            logging.info(f"Received completion for prompt {i}")
        except Exception as e:
            logging.error(f"Error during completion for prompt {i}: {e}")
    return out


def search_bing(query):
    params = {'q': query, 'mkt': 'en-US'}
    headers = {'Ocp-Apim-Subscription-Key': azure_bing_subscription_key}

    retry_interval_exp = 0
    while True:
        try:
            logging.info(f"Sending Bing search request for query: {query}")
            response = requests.get(
                azure_bing_endpoint, headers=headers, params=params)
            response.raise_for_status()
            logging.info(f"Received Bing search response for query: {query}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            if response.status_code == 403:
                logging.error(
                    "Quota exceeded. Please check your Bing API usage.")
                return {"error": "quota_exceeded"}
            if response.status_code == 404:
                logging.error(
                    "Resource not found. Check the endpoint URL and query parameters.")
                return {}
            if response.status_code == 401:
                logging.error("Check your Bing API key and permissions.")
                return {}
        except requests.exceptions.SSLError as ssl_err:
            logging.error(f"SSL error occurred: {ssl_err}")
            if retry_interval_exp > 6:
                return {}
            time.sleep(2 ** retry_interval_exp)
            retry_interval_exp += 1
        except Exception as ex:
            logging.error(f"Exception: {ex}")
            if retry_interval_exp > 6:
                return {}
            retry_interval_exp += 1


def generate_distractors(question, correct_answer):
    client = OpenAI(base_url=azure_openai_base_url,
                    api_key=azure_openai_api_key)
    prompt = f"Generate three incorrect but plausible answers for the following question:\n\nQuestion: {question}\nCorrect Answer: {correct_answer}\n\nIncorrect Answers:"
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": prompt}
            ]
        )
        text = completion.choices[0].message.content.strip()
        distractors = text.split('\n')
        return distractors[:3]  # Ensure only three distractors are returned
    except Exception as e:
        logging.error(f"Error generating distractors: {e}")
        return ["Distractor 1", "Distractor 2", "Distractor 3"]


def generate_answers_and_options(input_dir, output_file):
    all_data = []
    if not os.path.exists(input_dir):
        logging.error(f"Input directory {input_dir} does not exist.")
        return

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.json'):
                current_file = os.path.join(root, file)
                logging.info(f"Processing file: {current_file}")
                with open(current_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                all_data.extend(data)

    logging.info(f"Total files read: {len(all_data)}")

    if not all_data:
        logging.error("No data found in the input directory.")
        return

    prompts = []
    for line in all_data:
        p = "Answer the question with one entity in the following format, end the answer with '**'.\n\nQuestion: {background} {query}\n\nAnswer: "
        response_json = search_bing(line['query'])
        if "error" in response_json and response_json["error"] == "quota_exceeded":
            logging.error(
                f"Quota exceeded while processing file: {current_file}")
            break
        background = ""
        if 'webPages' in response_json and 'value' in response_json['webPages']:
            background = " ".join([wp['snippet']
                                  for wp in response_json['webPages']['value']])
        prompts.append(p.format(background=background, query=line['query']))

    logging.info(f"Total prompts generated: {len(prompts)}")

    answers = complete(prompts, data_dict=all_data, max_tokens=300)
    logging.info(f"Total answers generated: {len(answers)}")

    for answer in answers:
        distractors = generate_distractors(
            answer['question'], answer['answer'])
        options = [answer['answer']] + distractors
        # Shuffle to randomize the position of the correct answer
        random.shuffle(options)
        answer['options'] = options

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(answers, f, ensure_ascii=False, indent=4)

    logging.info(f"Output written to {output_file}")


if __name__ == "__main__":
    # Use relative path to the answer-query directory in the project
    input_dir = 'answer-query'
    output_file = 'id_question_query_answer_option.json'
    generate_answers_and_options(input_dir, output_file)
