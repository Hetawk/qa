# Setup Guide

## Quick Start

1. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API keys**

   ```bash
   cp config_template.py config.py
   ```

   Edit `config.py` and add your API keys:

   - Get Azure OpenAI API key from Azure Portal
   - Get Bing Search API key from Azure Cognitive Services
   - Or set up local Ollama for offline usage

3. **Prepare your data**

   - Place your question JSON files in the `answer-query/` directory
   - Each file should contain an array of question objects

4. **Run the generator**
   ```bash
   python main.py
   ```
   or
   ```bash
   python example_usage.py
   ```

## API Key Setup

### Azure OpenAI

1. Create an Azure OpenAI resource
2. Get your API key and endpoint
3. Update `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_BASE_URL` in config.py

### Bing Search (Optional)

1. Create a Bing Search v7 resource in Azure
2. Get your subscription key
3. Update `AZURE_BING_SUBSCRIPTION_KEY` in config.py

### Local Ollama (Alternative)

1. Install Ollama: https://ollama.ai/
2. Run: `ollama run llama3.1`
3. Use `ollama_server.py` for local inference

## Data Format

Your input JSON files should follow this format:

```json
[
  {
    "id": 1,
    "question": "What is the capital of France?",
    "query": "capital of France"
  }
]
```

## Troubleshooting

- **Import errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
- **API errors**: Check your API keys and network connection
- **No data generated**: Verify your input JSON files are properly formatted
- **Rate limiting**: The system includes retry logic, but you may need to wait for rate limits to reset
