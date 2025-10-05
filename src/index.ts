import express from "express";
import cors from "cors";
import path from "path";
import { fileURLToPath } from "url";
import { googleAI } from "@genkit-ai/googleai";
import { genkit } from "genkit";
import dotenv from "dotenv";
import rateLimit from "express-rate-limit";

// Load environment variables
dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 8080;

// Check if API key is available
if (!process.env.GEMINI_API_KEY) {
  console.error("❌ GEMINI_API_KEY environment variable is not set!");
  console.log("💡 Please set your API key using:");
  console.log("   export GEMINI_API_KEY=your_api_key_here");
  console.log(
    "   or create a .env file with: GEMINI_API_KEY=your_api_key_here"
  );
  process.exit(1);
}

// Mask API key for security (only show first 10 and last 4 characters)
const apiKey = process.env.GEMINI_API_KEY;
const maskedKey = apiKey
  ? `${apiKey.substring(0, 10)}...${apiKey.substring(apiKey.length - 4)}`
  : "NOT_SET";
console.log(`🔑 API Key configured: ${maskedKey}`);

// Initialize AI
const ai = genkit({
  plugins: [googleAI()],
  model: googleAI.model("gemini-2.0-flash")
});

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "../public")));

// Security headers
app.use((req, res, next) => {
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("X-Frame-Options", "DENY");
  res.setHeader("X-XSS-Protection", "1; mode=block");
  res.setHeader("Referrer-Policy", "strict-origin-when-cross-origin");
  next();
});

// Rate limiting to prevent abuse
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 10, // limit each IP to 10 requests per windowMs
  message: {
    error: "Too many requests from this IP, please try again later.",
    details: "Rate limit exceeded. Please wait 15 minutes before trying again."
  },
  standardHeaders: true,
  legacyHeaders: false
});

// Apply rate limiting to API routes
app.use("/api/", limiter);

// Serve the main HTML page
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "../public/index.html"));
});

// API endpoint for video summarization
app.post("/api/summarize", async (req, res) => {
  try {
    const { videoURL, prompt } = req.body;

    if (!videoURL) {
      return res.status(400).json({ error: "Video URL is required" });
    }

    const defaultPrompt = prompt || "Please summarize the following video:";

    console.log(`🎬 Processing video: ${videoURL}`);
    console.log(`📝 Using prompt: ${defaultPrompt}`);

    // Set a timeout for the AI processing (5 minutes)
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(
        () => reject(new Error("Processing timeout after 5 minutes")),
        300000
      );
    });

    // Process video with AI
    const processingPromise = ai.generate({
      prompt: [
        { text: defaultPrompt },
        { media: { url: videoURL, contentType: "video/mp4" } }
      ]
    });

    // Race between processing and timeout
    const { text } = (await Promise.race([
      processingPromise,
      timeoutPromise
    ])) as any;

    console.log(`✅ Video processed successfully`);
    res.json({ summary: text });
  } catch (error) {
    console.error("Error processing video:", error);

    if (error instanceof Error && error.message.includes("timeout")) {
      res.status(408).json({
        error: "Processing timeout",
        details:
          "Video processing took too long. Please try with a shorter video or try again later."
      });
    } else {
      res.status(500).json({
        error: "Failed to process video",
        details: error instanceof Error ? error.message : "Unknown error"
      });
    }
  }
});

// Health check endpoint for Cloud Run
app.get("/health", (req, res) => {
  res.status(200).json({
    status: "healthy",
    timestamp: new Date().toISOString(),
    version: "1.0.0"
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Video Summarizer Web App running on port ${PORT}`);
  console.log(`📝 API endpoint: http://localhost:${PORT}/api/summarize`);
  console.log(`🏥 Health check: http://localhost:${PORT}/health`);
});

export default app;
