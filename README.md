# 🎬 Summarize-A-Video AI

![Summarize-A-Video Hero](docs/images/hero.png)

A high-performance, AI-driven video summarization tool built with **Google Gemini** and **Firebase Genkit**. This tool allows users to transform long videos into concise, actionable summaries in seconds.

## ✨ Key Features

- 📝 **AI Transcription**: Converts speech from video or audio files into accurate text.
- 🤖 **AI-Powered Summarization**: Deeply analyzes content to extract key points, main themes, and recurring topics.
- 📍 **Timestamped Highlights**: Automatically generates a timeline of important moments.
- 🌍 **Multi-Language Support**: Supports summaries in English and Hindi.
- 🔗 **URL & File Support**: Process local uploads (.mp4, .mov, .avi) or remote YouTube links.
- ⚡ **Real-time Processing**: Fast analysis using the latest Gemini models.

## 🛠️ Tech Stack

- **Runtime**: Node.js/TypeScript
- **Framework**: Express.js
- **AI Core**: Google Gemini 1.5 Pro/Flash
- **Orchestration**: Firebase Genkit
- **Storage**: Multer for local handling
- **Styling**: Vanilla CSS (Premium Dark Theme)

## 🚀 Getting Started

### Prerequisites

- Node.js (v18+)
- A Google AI (Gemini) API Key

### Installation

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

## 📈 Daily Progress

We use a [JOURNAL.md](JOURNAL.md) to track daily improvements and small, atomic commits to ensure a high-quality development history.

## 📄 License

This project is licensed under the ISC License.
