import os
import time

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")


app = Flask(__name__)

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# Primary model
PRIMARY_MODEL = "gemini-3.6-flash"

# Fallback model
FALLBACK_MODEL = "gemini-3.1-flash-lite"


# ============================================================
# GEMINI REQUEST WITH RETRY
# ============================================================

def generate_with_gemini(prompt):

    models_to_try = [
        PRIMARY_MODEL,
        FALLBACK_MODEL
    ]

    last_error = None

    for model in models_to_try:

        for attempt in range(3):

            try:

                print(
                    f"Trying {model} "
                    f"(attempt {attempt + 1}/3)..."
                )

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                if response.text:
                    return response.text

            except Exception as e:

                last_error = e

                print(
                    f"{model} failed: {str(e)}"
                )

                # Wait before retrying
                if attempt < 2:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)

        print(
            f"{model} unavailable. "
            f"Trying next model..."
        )

    raise Exception(
        f"Gemini service is currently unavailable. "
        f"Please try again in a few moments. "
        f"Details: {last_error}"
    )


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# RESEARCH GENERATOR
# ============================================================

@app.route("/generate-research", methods=["POST"])
def generate_research():

    try:

        data = request.get_json()

        topic = data.get("topic", "").strip()
        field = data.get(
            "field",
            "Computer Science"
        ).strip()

        if not topic:

            return jsonify({
                "success": False,
                "error": "Please enter a research topic."
            }), 400


        prompt = f"""
You are an academic research assistant.

A university student wants to conduct research on:

Research Topic:
{topic}

Research Field:
{field}

Prepare a structured academic research analysis.

Use these sections:

1. RESEARCH SUMMARY

Explain the research topic clearly.

2. RESEARCH OBJECTIVES

Provide 3 to 5 specific objectives.

3. RESEARCH QUESTIONS

Provide 3 to 5 research questions.

4. SUGGESTED METHODOLOGY

Explain a practical research methodology.

5. SUGGESTED AI/ML MODELS

Suggest appropriate AI or machine learning models
and briefly explain their suitability.

6. KEYWORDS

Provide 5 to 8 important keywords.

Important:
- Use clear academic English.
- Do not invent experimental results.
- Do not create fake citations.
- Do not claim that experiments have already been performed.
- Use headings and bullet points.
"""


        result = generate_with_gemini(prompt)


        return jsonify({
            "success": True,
            "result": result
        })


    except Exception as e:

        print(
            "Research generation error:",
            str(e)
        )

        return jsonify({
            "success": False,
            "error": str(e)
        }), 503


# ============================================================
# TITLE GENERATOR
# ============================================================

@app.route("/generate-title", methods=["POST"])
def generate_title():

    try:

        data = request.get_json()

        topic = data.get("topic", "").strip()

        if not topic:

            return jsonify({
                "success": False,
                "error": "Please enter a research idea."
            }), 400


        prompt = f"""
You are an academic research title generator.

Research idea:

{topic}

Generate 5 professional academic research titles.

Requirements:

- Suitable for a university research project.
- Clear and specific.
- Concise.
- Professional academic language.
- Use AI/ML terminology when relevant.
- Do not claim experimental results.

Return only a numbered list of 5 titles.
"""


        result = generate_with_gemini(prompt)


        return jsonify({
            "success": True,
            "result": result
        })


    except Exception as e:

        print(
            "Title generation error:",
            str(e)
        )

        return jsonify({
            "success": False,
            "error": str(e)
        }), 503


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "running",
        "application": "ResearchAI",
        "ai_provider": "Google Gemini",
        "primary_model": PRIMARY_MODEL
    })


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )