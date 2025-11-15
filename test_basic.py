"""
Basic test script to verify everything is working
Run this after setup to check your installation
"""

import sys
import os

from backend.transcriber import LinearBTranscriber
from backend.analyzer import MycenaeanAnalyzer

def test_setup():
    """Test that files are loaded correctly"""
    print("Testing setup...")
    try:
        transcriber = LinearBTranscriber(data_dir="backend/data")
        analyzer = MycenaeanAnalyzer(data_dir="backend/data")
        print("✓ Files loaded successfully")
        print(f"✓ Syllabary signs loaded: {len(transcriber.syllabary)}")
        print(f"✓ Lexicon words loaded: {len(analyzer.lexicon)}")
        return transcriber, analyzer
    except Exception as e:
        print(f"✗ Error loading files: {e}")
        sys.exit(1)

def test_transcription(transcriber):
    """Test basic transcription"""
    print("\nTesting transcription...")
    
    tests = [
        ("𐀷𐀙𐀏", "wa-na-ka", "king"),
        ("𐀡𐀴𐀛𐀊", "po-ti-ni-ja", "lady/mistress"),
        ("𐀴𐀀", "te-o", "god")
    ]
    
    for linear_b, expected, meaning in tests:
        result = transcriber.transcribe_text(linear_b)
        status = "✓" if expected in result else "✗"
        print(f"{status} {linear_b} → {result} ({meaning})")

def test_analysis(analyzer):
    """Test morphological analysis"""
    print("\nTesting analysis...")
    
    tests = [
        ("wa-na-ka", "king"),
        ("po-ti-ni-ja", "mistress"),
        ("te-o", "god")
    ]
    
    for word, expected_meaning in tests:
        result = analyzer.analyze_word(word)
        if result and expected_meaning.lower() in result.get('meaning', '').lower():
            print(f"✓ {word}: {result['meaning']}")
        else:
            print(f"✗ {word}: Analysis failed or meaning mismatch")

def test_classical_comparison(analyzer):
    """Test Classical Greek comparison"""
    print("\nTesting Classical Greek comparison...")
    
    comparison = analyzer.compare_to_classical("wa-na-ka")
    if 'mycenaean' in comparison:
        print(f"✓ Mycenaean: {comparison['mycenaean']}")
        print(f"  Classical: {comparison['classical']}")
        print(f"  Meaning: {comparison['meaning']}")
        if comparison['changes']:
            print("  Changes detected:")
            for change in comparison['changes']:
                print(f"    - {change['type']}")
    else:
        print("✗ Comparison failed")

def main():
    print("=" * 60)
    print("LINEAR B TOOL - BASIC TESTS")
    print("=" * 60)
    
    transcriber, analyzer = test_setup()
    test_transcription(transcriber)
    test_analysis(analyzer)
    test_classical_comparison(analyzer)
    
    print("\n" + "=" * 60)
    print("If you see mostly ✓ marks, everything is working!")
    print("If you see ✗ marks, check the error messages above.")
    print("=" * 60)

if __name__ == "__main__":
    main()