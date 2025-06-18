# QA Data Generator

A powerful Python application that generates structured question and answer datasets with multiple choice options for quiz games, educational applications, and trivia systems. The system leverages AI models to create accurate answers and plausible distractors (incorrect options) for questions.

> **Perfect for**: Quiz games, educational apps, trivia applications, and Q&A systems

## 🚀 Features

- **🤖 AI-Powered Answers**: Leverages OpenAI/Azure OpenAI for generating accurate, contextual answers
- **🔍 Web Search Integration**: Uses Bing Search API to gather background context for better responses
- **🎯 Smart Distractor Generation**: Creates plausible incorrect answers for multiple choice questions
- **⚡ Multiple AI Backends**: Supports OpenAI, Azure OpenAI, and local Ollama models
- **📊 Batch Processing**: Efficiently handles large datasets with progress tracking and backup
- **🎮 Game-Ready Format**: Outputs data in formats perfect for quiz and trivia applications
- **🔧 Flexible Configuration**: Easy setup with template-based configuration

## 📁 Project Structure

```
qa/
├── 📄 main.py                    # Main application entry point
├── 🧠 distractors_generator.py   # Distractor generation logic
├── 🤖 gpt.py                     # GPT model utilities
├── 🖥️  ollama_server.py          # Local Ollama server integration
├── ⚙️  config_template.py        # Configuration template
├── 📋 requirements.txt          # Python dependencies
├── 📂 answer-query/             # Input data directory
├── 📝 ekd_prompt.json          # Prompt templates
└── 📖 README.md                # This file
```

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Hetawk/qa.git
   cd qa
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys**
   ```bash
   cp config_template.py config.py
   ```
   Edit `config.py` with your actual API keys:
   - Azure OpenAI API key
   - Bing Search API key
   - Or configure for local Ollama usage

## 🚀 Quick Start

### Basic Usage

1. **Prepare your question data**

   - Place JSON files with questions in the `answer-query/` directory
   - Each file should contain questions in the expected format

2. **Run the generator**

   ```bash
   python main.py
   ```

3. **Check output**
   - Generated data will be saved to `id_question_query_answer_option.json`
   - Each entry includes: question, answer, and multiple choice options

## 📋 Data Format

**Input Format** (questions):

```json
[
  {
    "id": 14000,
    "question": "Which great lake is the highest above sea level?",
    "query": "highest elevation great lake"
  }
]
```

**Output Format** (with answers and options):

```json
[
  {
    "id": 14000,
    "question": "Which great lake is the highest above sea level?",
    "query": "highest elevation great lake",
    "answer": "Lake Superior",
    "options": ["Lake Superior", "Lake Michigan", "Lake Huron", "Lake Erie"]
  }
]
```

## ⚙️ Configuration Options

### AI Models

- **Azure OpenAI**: For cloud-based processing with enterprise features
- **OpenAI**: Direct OpenAI API usage
- **Ollama**: For local model inference (privacy-focused)

### Search Integration

- **Bing Search**: Provides contextual background for questions
- Configurable search parameters and result processing

## 🎯 Use Cases

- **🎮 Quiz Applications**: Generate trivia questions with multiple choice answers
- **📚 Educational Games**: Create learning materials with varying difficulty levels
- **🤖 Training Data**: Prepare datasets for question-answering AI systems
- **🎲 Game Development**: Populate quiz games with structured, high-quality content
- **📖 Study Materials**: Generate practice questions for educational content

## 🔑 API Requirements

To use this application, you'll need one or more of the following:

- **🔷 Azure OpenAI**: For enterprise-grade AI-powered answer generation
- **🔍 Bing Search API**: For contextual web search (optional but recommended)
- **🤖 OpenAI API**: Alternative to Azure OpenAI
- **🖥️ Local Ollama**: For offline AI model usage (privacy-focused option)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. 🍴 Fork the repository
2. 🌟 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. ✨ Make your changes
4. 🧪 Add tests if applicable
5. 📤 Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

Need help? Here's how to get support:

- 🐛 **Bug Reports**: [Create an issue](https://github.com/Hetawk/qa/issues)
- 💡 **Feature Requests**: [Create an issue](https://github.com/Hetawk/qa/issues)
- 📖 **Documentation**: Check this README and code comments
- ⚙️ **Configuration Help**: Review `config_template.py`

---

<div align="center">

**⭐ Star this repo if you find it helpful! ⭐**

Made with ❤️ for the developer community

</div>
