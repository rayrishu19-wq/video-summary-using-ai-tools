# 🎬 Summarize-A-Video AI

![Summarize-A-Video Hero](docs/images/hero.png)

A high-performance, AI-driven video summarization tool built with **Google Gemini** and **Firebase Genkit**. This tool allows users to transform long videos into concise, actionable summaries in seconds.

## 🌟 Why This Project?

In an era of information overload, watching lengthy videos to find specific information is time-consuming. **Summarize-A-Video AI** leverages state-of-the-art Generative AI to provide users with immediate value by condensing hours of content into minutes of reading.

## ✨ Key Features

- 📝 **AI Transcription**: Converts speech from video or audio files into accurate text.
- 🤖 **AI-Powered Summarization**: Deeply analyzes content to extract key points, main themes, and recurring topics.
- 📍 **Timestamped Highlights**: Automatically generates a timeline of important moments.
- 🌍 **Multi-Language Support**: Supports summaries in English and Hindi.
- 🔗 **URL & File Support**: Process local uploads (.mp4, .mov, .avi) or remote YouTube links.
- ⚡ **Real-time Processing**: Fast analysis using the latest Gemini models.

## 🛠️ Tech Stack

- **Frontend**: Vanilla HTML5, CSS3 (Premium Dark Mode), JavaScript
- **Backend**: Node.js, TypeScript, Express.js
- **AI Core**: Google Gemini 1.5 Pro / Flash
- **Framework**: Firebase Genkit
- **Deployment**: Optimized for Docker & Google Cloud Run

## 🚀 Getting Started

### 📋 Prerequisites

- **Node.js**: Version 18.x or higher
- **API Key**: A valid [Google AI Studio (Gemini) API Key](https://aistudio.google.com/)

### 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/video-summary-using-ai-tools.git
   cd video-summary-using-ai-tools
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure Environment:**
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_GENAI_API_KEY=your_api_key_here
   ```

4. **Run Development Server:**
   ```bash
   npm run dev
   ```

## 📈 Project Status

We track daily improvements in our [JOURNAL.md](JOURNAL.md). This project follows a philosophy of atomic, meaningful commits to ensure long-term maintainability.

## 📄 License

This project is licensed under the ISC License - see the [LICENSE](LICENSE) file for details.
