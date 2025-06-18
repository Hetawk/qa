# distractors_generator.py

import logging

import requests


class DistractorGenerator:
    def __init__(self, base_url, model_name="llama3.1"):
        self.base_url = base_url
        self.model_name = model_name

    def generate_distractors(self, question, correct_answer):
        endpoint = "/v1/chat/completions"
        url = self.base_url + endpoint

        prompt = f"Generate three incorrect but plausible answers for the following question:\n\nQuestion: {question}\nCorrect Answer: {correct_answer}\n\nIncorrect Answers:"
        try:
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 150  # Adjust the token limit as needed
            }
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()

            text = response.json()['choices'][0]['message']['content'].strip()
            distractors = [d.strip() for d in text.split('\n') if d.strip()]

            logging.info(f"Distractors generated: {distractors}")  # Log the generated distractors

            if len(distractors) < 3:
                distractors += ["Distractor"] * (3 - len(distractors))
            return distractors[:3]  # Ensure only three distractors are returned
        except Exception as e:
            logging.error(f"Error generating distractors: {e}")
            return ["Distractor 1", "Distractor 2", "Distractor 3"]

