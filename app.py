import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load product data
with open('product_data.json', 'r', encoding='utf-8') as f:
    product_data = json.load(f)

@app.route('/')
def index():
    return "Flask API for SHL Assessment Recommendation"

@app.route('/recommend', methods=['GET'])
def recommend():
    # The query text (e.g., job description)
    query = request.args.get('q', '')

    # Very naive approach: 
    #  - If query contains keywords like 'Java', we rank Java test higher
    #  - If query contains 'Python', we could rank something else higher, etc.
    # For demo, we simply filter by approximate duration or do minimal matching.

    # 1) Attempt to parse desired duration from query (e.g., '40 minutes')
    # 2) If found in product data, we shortlist
    # 3) If nothing found, return all

    # This is a simple example. In a real system, you'd use advanced LLM or keyword embedding.
    
    # Extract possible numbers from query - naive approach
    import re
    minutes = re.findall(r'(\d+)\s*minutes?', query.lower())
    desired_minutes = None
    if minutes:
        desired_minutes = int(minutes[0])

    # Filter logic: if desired_minutes is found, pick all tests that have that or less in their duration
    # Then further filter on keywords like 'java', 'python', 'cognitive', 'personality', etc.
    filtered = []
    for item in product_data:
        # GET numeric duration
        item_duration = int(item['duration'].split()[0])

        if desired_minutes:
            if item_duration <= desired_minutes:
                # Optionally check for keywords
                filtered.append(item)
        else:
            filtered.append(item)

    # Additional naive keyword checks
    # If the query includes 'java', prefer Java test at top.
    # If the query includes 'python', prefer Full Stack test at top (just a silly example).
    # For demonstration, let's reorder based on these keywords:
    def score_item(item, q):
        score = 0
        if 'java' in q.lower() and 'java' in item['assessment_name'].lower():
            score += 10
        if 'python' in q.lower() and 'full stack' in item['assessment_name'].lower():
            score += 5
        if 'cognitive' in q.lower() and 'cognitive' in item['assessment_name'].lower():
            score += 5
        if 'personality' in q.lower() and 'personality' in item['assessment_name'].lower():
            score += 5
        return score

    filtered.sort(key=lambda x: score_item(x, query), reverse=True)

    # Return only up to 10 results
    recommended = filtered[:10]

    return jsonify(recommended)

if __name__ == '__main__':
    # Run locally on port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)