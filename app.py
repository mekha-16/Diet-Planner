from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# 🔑 Gemini API key
genai.configure(api_key="GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-2.5-flash")

@app.route("/generate", methods=["POST"])
def generate_plan():
    data = request.json

    prompt = f"""
    Create a BRIEF and PRECISE personalized workout plan and diet plan for a student.

    User Details:
    - Age: {data['age']}
    - Height: {data['height']} cm
    - Weight: {data['weight']} kg
    - Fitness Goal: {data['goal']}
    - Diet Preference: {data['diet']}

    Format your response EXACTLY as follows:

    WORKOUT PLAN:
    - [Bullet point 1: Day/Type - Exercise 1 (sets x reps)]
    - [Bullet point 2: Day/Type - Exercise 2 (sets x reps)]
    - [Continue with 5-8 bullet points total]
    - Keep each bullet point to ONE sentence maximum
    - Focus on key exercises only, no explanations

    DIET PLAN:
    - [Bullet point 1: Meal time - Food item with portion]
    - [Bullet point 2: Meal time - Food item with portion]
    - [Continue with 8-12 bullet points total]
    - Keep each bullet point to ONE sentence maximum
    - Include breakfast, lunch, dinner, and snacks only
    - No lengthy explanations or disclaimers

    IMPORTANT RULES:
    1. Be VERY BRIEF - maximum 15 bullet points total for both sections
    2. Use ONLY bullet points (format: - Text here)
    3. No paragraphs, no explanations, no disclaimers
    4. Separate sections clearly with "WORKOUT PLAN:" and "DIET PLAN:" headers
    5. Keep response under 300 words total
    """

    response = model.generate_content(prompt)

    text = response.text

     # Split response into workout and diet
    parts = text.split("DIET PLAN:")
    if len(parts) < 2:
        parts = text.split("Diet Plan:")
    
    workout = parts[0].replace("WORKOUT PLAN:", "").replace("Workout Plan:", "").strip()
    diet = parts[1].strip() if len(parts) > 1 else ""

    return jsonify({
        "workout": workout,
        "diet": diet
    })

if __name__ == "__main__":
    app.run(debug=True)