from flask import Flask, render_template, request, jsonify
from build_index import PodcastSearchIndex
from groq import Groq
import json
import os

app = Flask(__name__)

# Configure Groq API
API_KEY = os.environ.get('GROQ_API_KEY', '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')
groq_client = Groq(api_key=API_KEY)

# Verify API key works
try:
    test_response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "test"}],
        max_tokens=10
    )
    print("✅ Groq API key verified successfully")
except Exception as e:
    print(f"❌ Groq API key verification failed: {e}")

# Initialize search index
search_index = PodcastSearchIndex()
search_index.load_segments()
search_index.load_index()

VIDEO_ID = "Rni7Fz7208c"

@app.route('/')
def index():
    return render_template('index.html', video_id=VIDEO_ID)

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query', '')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    # Check if it's just a greeting
    greetings = ['hi', 'hello', 'hey', 'yo', 'sup', 'good morning', 'good afternoon', 'good evening']
    if query.lower().strip() in greetings or query.lower().strip().rstrip('!?.') in greetings:
        return jsonify({
            'answer': "Hey there! 👋 I'm excited to chat with you about the Elon Musk × Nikhil Kamath podcast. Feel free to ask me anything - like what Elon thinks about AI, his advice for entrepreneurs, or his views on first-principles thinking. What would you like to know?",
            'timestamp': 0,
            'timestamp_formatted': '0:00',
            'segment_text': '',
            'relevance_score': 1.0
        })
    
    # Search for relevant segments
    results = search_index.search(query, top_k=3)
    
    if not results:
        return jsonify({
            'answer': "Hmm, I couldn't find anything specific about that in the podcast. Could you try rephrasing your question? I'm pretty good at finding stuff about Elon's views on technology, business, AI, and his philosophy. What aspect are you curious about?",
            'timestamp': 0,
            'timestamp_formatted': '0:00',
            'segment_text': '',
            'relevance_score': 0.0
        })
    
    # Build context from the best matching segments
    context = ""
    for i, segment in enumerate(results[:3]):
        context += f"\n[Segment {i+1} - Timestamp {segment['start_formatted']}]:\n{segment['text']}\n"
    
    best_match = results[0]
    
    try:
        answer = generate_ai_answer(query, context, best_match)
    except Exception as e:
        print(f"AI generation failed: {e}")
        answer = generate_simple_answer(query, best_match)
    
    return jsonify({
        'answer': answer,
        'timestamp': int(best_match['start']),
        'timestamp_formatted': best_match['start_formatted'],
        'segment_text': best_match['text'][:200] + '...',
        'relevance_score': best_match['relevance_score']
    })

def generate_ai_answer(query, context, best_match):
    """Generate natural, conversational answer using Groq API"""
    
    system_prompt = """You are a friendly, enthusiastic podcast companion bot. You help people understand what was discussed in the Elon Musk x Nikhil Kamath podcast (People by WTF Ep. 16).

YOUR PERSONALITY:
- You're casual and warm, like talking to a friend who watched the podcast
- You use natural language with occasional emojis 
- You're genuinely excited about the interesting insights from the podcast
- You speak in first person ("I think...", "From what I gathered...")
- You never sound like you're reading from a transcript
- You give context and explain WHY something is interesting, not just WHAT was said

CRITICAL RULES:
1. NEVER mention "segments", "transcript", or "according to the podcast" in a robotic way
2. NEVER start with "Based on the podcast transcript..." or similar phrases
3. NEVER format your answer like you're citing sources
4. ALWAYS weave the timestamp naturally into the conversation
5. If the query is about a person's views, explain it as if YOU understood it from watching
6. Keep responses between 100-200 words
7. If someone says just "hi" or "hello", greet them warmly and ask what they'd like to know

EXAMPLE BAD RESPONSE (never do this):
"Based on the podcast transcript segments, Elon Musk discusses AI at timestamp 1:30:32..."

EXAMPLE GOOD RESPONSE:
"Elon had some really fascinating thoughts on AI! 🤖 Around 1 hour 30 minutes in, he talked about how AI is actually getting pretty good at humor - he even mentioned this model called Grok that can do these hilarious vulgar roasts. But here's the interesting part: he thinks comedy might actually be one of the LAST things AI truly masters. Pretty mind-bending when you think about it!"

Remember: Sound like a human who watched the podcast and is excited to share what they learned!"""

    user_prompt = f"""The user asked: "{query}"

Here's what was actually said in the podcast (use this info but present it naturally):
{context}

The key moment is at {best_match['start_formatted']}

Give a natural, conversational response. Sound like a real person, not a bot reading transcripts."""

    try:
        print("\n🤖 Generating AI response...")
        
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=350,
            temperature=0.85  # Slightly higher for more natural variation
        )
        
        answer = response.choices[0].message.content
        print("✅ AI response generated")
        
        # Clean up any remaining robotic phrases
        answer = answer.replace("Based on the podcast transcript", "")
        answer = answer.replace("According to the transcript", "")
        answer = answer.replace("The transcript shows", "")
        answer = answer.replace("the given transcript segments", "the conversation")
        
        # Add timestamp naturally if not already included
        if best_match['start_formatted'] not in answer:
            timestamp_minutes = best_match['start_formatted']
            answer += f"\n\n🎧 They got into this around {timestamp_minutes} in the conversation."
        
        return answer.strip()
        
    except Exception as e:
        print(f"❌ Groq API error: {e}")
        raise e

def generate_simple_answer(query, segment):
    """Fallback answer - also made more natural"""
    timestamp = segment['start_formatted']
    
    # More natural fallback responses
    templates = [
        f"Ah, interesting question! So around {timestamp} in the podcast, they touched on this. {segment['text'][:300]}... \n\nWant me to find more specific details about this?",
        
        f"I caught that part! 🎯 Near {timestamp}, there was a discussion about this. Here's the gist: {segment['text'][:300]}... \n\nFascinating stuff, right?",
        
        f"Great question! The conversation around {timestamp} covers this. Basically, {segment['text'][:300]}... \n\nLet me know if you want to explore this topic more!"
    ]
    
    import random
    return random.choice(templates)

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🎙️  Podcast Q&A Bot with Natural AI")
    print("="*50)
    print("\n✅ Search index loaded")
    print("🤖 Groq AI (Llama 3.1) ready")
    print("\n📺 Open: http://localhost:5000")
    print("\nTry asking:")
    print('  • "What does Elon think about AI?"')
    print('  • "How should entrepreneurs deal with government?"')
    print('  • "What is first-principles thinking?"')
    print('  • Just say "Hi" to start a conversation!')
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)