import { googleAI } from "@genkit-ai/googleai";
import { genkit } from "genkit";
import dotenv from "dotenv";

// Load environment variables
dotenv.config();

// Check if API key is available
if (!process.env.GEMINI_API_KEY) {
  console.error("❌ GEMINI_API_KEY environment variable is not set!");
  console.log("💡 Please set your API key using:");
  console.log("   export GEMINI_API_KEY=your_api_key_here");
  process.exit(1);
}

// Initialize AI
const ai = genkit({
  plugins: [googleAI()],
  model: googleAI.model("gemini-2.0-flash")
});

(async () => {
  try {
    // Step 1: get command line arguments
    const videoURL = process.argv[2];
    if (!videoURL) {
      console.error("Please provide a video URL as a command line argument.");
      process.exit(1);
    }

    // Step 2: construct prompt
    const prompt = process.argv[3] || "Please summarize the following video:";

    console.log(`🎬 Processing video: ${videoURL}`);
    console.log(`📝 Using prompt: ${prompt}`);

    // Step 3: process video
    const { text } = await ai.generate({
      prompt: [
        { text: prompt },
        { media: { url: videoURL, contentType: "video/mp4" } }
      ]
    });

    console.log(`✅ Video processed successfully`);
    console.log("\n📝 Summary:");
    console.log(text);
  } catch (error) {
    console.error("Error processing video:", error);
  }
})();
