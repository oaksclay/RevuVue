
# 🌟RevuVue: AI-powered Review Summarizer🌟

Leverage OpenAI's API to distill customer reviews into a concise summary. With the UI powered by Streamlit and review management via sqlite3, RevuVue demonstrates how to tie multiple technologies together to provide a seamless experience. Perfect demonstration for leveraging LLM for quickly deploying a custom solution.

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- OpenAI API key

### Installation & Setup

1. **Clone the Repository**

```bash
git clone https://github.com/oaksclay/RevuVue.git
cd RevuVue
```

2. **Install Required Python Libraries**

```bash
pip install -r requirements.txt
```

3. **Set Up OpenAI API Key**

You'll need to set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

4. **Run the Application**

```bash
streamlit run main.py
```

## 📖 Usage

Upon launching, the Streamlit dashboard will guide you through:

1. Adding new reviews to the database.
2. Analyzing and summarizing existing reviews from the included `.db` file. The sample reviews provided are about a bedding set.

## 📝 Feedback and Contributions

I welcome feedback, bug reports, and pull requests!

For major changes, please open an issue first to discuss what you would like to change.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
