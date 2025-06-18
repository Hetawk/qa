# ollama_server.py

import json
import os
import random
import requests
import logging
import signal
import sys

from distractors_generator import DistractorGenerator




class OllamaServer:
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def __init__(self, base_url, model_name="llama3.1", max_tokens=100):
        self.base_url = base_url
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.progress_data = []
        self.completed_data = []

        # Register signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, sig, frame):
        logging.info("Interrupt received, saving progress and output...")
        self.save_progress()
        self.save_output('partial_output.json')  # Save the partially completed output
        sys.exit(0)



    def save_output(self, output_file):
        if self.completed_data:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.completed_data, f, ensure_ascii=False, indent=4)
            logging.info(f"Output saved to {output_file}.")

    def complete(self, prompts, data_dict):
        out = []
        endpoint = "/v1/chat/completions"
        url = self.base_url + endpoint

        for i, p in enumerate(prompts):
            try:
                logging.info(f"Sending completion request for prompt {i}")
                logging.info(f"Request: {p}")
                payload = {
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": p}
                    ],
                    "max_tokens": self.max_tokens
                }
                headers = {"Content-Type": "application/json"}
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()

                text = response.json()['choices'][0]['message']['content'].strip()
                if '**' in text:
                    text = text.replace("**", "")
                j = {
                    "id": data_dict[i]['id'],
                    "question": data_dict[i]['question'],
                    "query": data_dict[i]['query'],
                    "answer": text
                }
                out.append(j)
                logging.info(f"Received completion for prompt {i}: {j}")
            except requests.exceptions.HTTPError as http_err:
                logging.error(f"HTTP error occurred for prompt {i}: {http_err}")
            except Exception as e:
                logging.error(f"Error during completion for prompt {i}: {e}")
        return out

    def generate_answers_and_options(self, input_dir, output_file, distractor_generator):
        self.progress_data = []  # Reset progress data at the start
        self.completed_data = []  # Reset completed data at the start

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
            background = ""  # Since Bing search is removed, background is empty
            prompts.append(p.format(background=background, query=line['query']))

        logging.info(f"Total prompts generated: {len(prompts)}")

        answers = self.complete(prompts, data_dict=all_data)
        logging.info(f"Total answers generated: {len(answers)}")

        for answer in answers:
            distractors = distractor_generator.generate_distractors(answer['question'], answer['answer'])
            options = [answer['answer']] + distractors
            random.shuffle(options)  # Shuffle to randomize the position of the correct answer
            answer['options'] = options

            # Append options and then save progress
            self.progress_data.append(answer)  # Append to progress data with options
            self.completed_data.append(answer)  # Append to completed data

            logging.info(f"Options for question ID {answer['id']}: {options}")
            logging.info(f"Final JSON for question ID {answer['id']}: {answer}")  # Log the final JSON structure

            self.save_progress()  # Save progress after each distractor generation
            self.save_output('partial_output.json')  # Save the partially completed output

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.completed_data, f, ensure_ascii=False, indent=4)

        logging.info(f"Output written to {output_file}")

    def save_progress(self):
        if self.progress_data:
            with open('progress_backup.json', 'w', encoding='utf-8') as f:
                json.dump(self.progress_data, f, ensure_ascii=False, indent=4)
            logging.info("Progress saved successfully.")

if __name__ == "__main__":
    ollama_base_url = "http://127.0.0.1:11434"

    ollama_server = OllamaServer(base_url=ollama_base_url)
    distractor_generator = DistractorGenerator(base_url=ollama_base_url)

    input_dir = 'D:/coding_env/py/generate_json/answer-query/3'
    output_file = 'id_question_query_answer_option.json'

    ollama_server.generate_answers_and_options(input_dir, output_file, distractor_generator)
    ollama_server.save_progress()
    ollama_server.save_output(output_file)
