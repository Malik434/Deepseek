import re
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

def clean_text(text):
    text = text.strip()  
    text = re.sub(r"[^\w\s.,!?'-]", "", text)  
    text = re.sub(r"\s+", " ", text)  
    return text

def analyze_sentiment(text):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="Your-API-Key",
    )

    cleaned_text = clean_text(text)  # Clean text before sending

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {"role": "system", "content": "You are a sentiment analysis tool. Classify the text strictly as Positive, Negative, or Neutral. Respond with only one word: Positive, Negative, or Neutral. Do NOT provide explanations."},
                {"role": "user", "content": cleaned_text}
            ]
        )
        
        print("API Response:", response)
        
        if response and hasattr(response, "choices") and response.choices:
            sentiment = response.choices[0].message.content.strip()
            
            valid_sentiments = {"Positive", "Negative", "Neutral"}
            if sentiment not in valid_sentiments:
                return "Error: Unexpected response format"
            
            return sentiment
    
    except Exception as e:
        print("Error occurred:", e)
        return f"API Error: {str(e)}"

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'GET':
        text = request.args.get("text", "")
    else:  
        data = request.json
        text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    result = analyze_sentiment(text)
    return jsonify({"sentiment": result})

if __name__ == "__main__":
    app.run(debug=True)
