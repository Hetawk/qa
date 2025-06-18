#!/usr/bin/env python3
"""
Sample usage script for the Question & Answer Game Data Generator

This script demonstrates how to use the main functionality to generate
quiz data from your question files.
"""

import os
import logging
from main import generate_answers_and_options


def main():
    # Setup logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Configuration
    input_directory = "answer-query"  # Directory containing your question JSON files
    output_file = "generated_quiz_data.json"  # Output file for the generated data

    # Check if input directory exists
    if not os.path.exists(input_directory):
        logging.error(f"Input directory '{input_directory}' not found!")
        logging.info(
            "Please make sure you have question files in the 'answer-query' directory")
        return

    # Check if config file exists
    if not os.path.exists("config.py"):
        logging.error("config.py not found!")
        logging.info(
            "Please copy config_template.py to config.py and fill in your API keys")
        return

    logging.info("Starting question and answer generation...")
    logging.info(f"Input directory: {input_directory}")
    logging.info(f"Output file: {output_file}")

    # Generate the data
    try:
        generate_answers_and_options(input_directory, output_file)
        logging.info("Generation completed successfully!")
        logging.info(f"Check '{output_file}' for your generated quiz data")
    except Exception as e:
        logging.error(f"Error during generation: {e}")


if __name__ == "__main__":
    main()
