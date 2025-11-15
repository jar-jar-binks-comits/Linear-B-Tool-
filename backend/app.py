"""
Flask web application for Linear B Transcription Tool
"""

from flask import Flask, render_template, request, jsonify
from transcriber import LinearBTranscriber
from analyzer import MycenaeanAnalyzer
import os

app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

# Initialize tools
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
transcriber = LinearBTranscriber(data_dir=DATA_DIR)
analyzer = MycenaeanAnalyzer(data_dir=DATA_DIR)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    """API endpoint for transcription"""
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        transliteration = transcriber.transcribe_text(text)
        phonetic = transcriber.get_phonetic_transcription(text)
        
        return jsonify({
            'success': True,
            'transliteration': transliteration,
            'phonetic': phonetic
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint for word analysis"""
    data = request.json
    word = data.get('word', '')
    
    if not word:
        return jsonify({'error': 'No word provided'}), 400
    
    try:
        analysis = analyzer.analyze_word(word)
        
        if not analysis:
            return jsonify({
                'success': False,
                'message': 'Word not found in lexicon'
            })
        
        # Get classical comparison if available
        comparison = None
        if 'classical_greek' in analysis:
            comparison = analyzer.compare_to_classical(word)
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'comparison': comparison
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Return example tablets/phrases"""
    examples = [
        {
            'name': 'wa-na-ka (King)',
            'linear_b': '𐀷𐀙𐀏',
            'description': 'The word for "king" or "lord" in Mycenaean Greek'
        },
        {
            'name': 'po-ti-ni-ja (Lady/Goddess)',
            'linear_b': '𐀡𐀴𐀛𐀊',
            'description': 'Important religious title meaning "mistress" or "lady"'
        },
        {
            'name': 'te-o (God)',
            'linear_b': '𐀳𐀀',
            'description': 'The word for "god" (theos)'
        },
        {
            'name': 'i-qo (Horse)',
            'linear_b': '𐀂𐀦',
            'description': 'Shows labiovelar sound change: *hikkʷos → hippos'
        }
    ]
    return jsonify(examples)

@app.route('/api/syllabary', methods=['GET'])
def get_syllabary():
    """Return all syllabary signs"""
    signs = []
    for sign, info in transcriber.syllabary.items():
        signs.append({
            'sign': sign,
            'transliteration': info['transliteration'],
            'phonetic': info['phonetic'],
            'unicode': info['unicode']
        })
    return jsonify(signs)

if __name__ == '__main__':
    app.run(debug=True, port=5000)