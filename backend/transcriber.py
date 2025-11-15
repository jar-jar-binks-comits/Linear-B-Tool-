"""
Linear B Transcriber
Converts Linear B syllabograms to Greek transliteration
"""

import json
import os
from typing import List, Dict, Optional

class LinearBTranscriber:
    def __init__(self, data_dir: str = "data"):
        """Initialize transcriber with syllabary data"""
        syllabary_path = os.path.join(data_dir, "syllabary.json")
        
        with open(syllabary_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.syllabary = data['signs']
            self.notes = data.get('notes', {})
        
        self.reverse_syllabary = {
            v['transliteration']: k 
            for k, v in self.syllabary.items()
        }
    
    def transcribe_sign(self, sign: str) -> Optional[Dict[str, str]]:
        """Transcribe a single Linear B sign"""
        if sign in self.syllabary:
            return self.syllabary[sign]
        return None
    
    def transcribe_text(self, text: str, separator: str = "-") -> str:
        """
        Transcribe full Linear B text to transliteration
        
        Args:
            text: Linear B text (Unicode characters)
            separator: Character to use between syllables (default: "-")
            
        Returns:
            Transliterated text
        """
        words = []
        current_word = []
        
        for char in text:
            if char.isspace():
                if current_word:
                    words.append(separator.join(current_word))
                    current_word = []
            else:
                sign_info = self.transcribe_sign(char)
                if sign_info:
                    current_word.append(sign_info['transliteration'])
                else:
                    current_word.append(f"[{char}?]")
        
        if current_word:
            words.append(separator.join(current_word))
        
        return " ".join(words)
    
    def get_phonetic_transcription(self, text: str) -> str:
        """Get phonetic (IPA-like) transcription"""
        result = []
        
        for char in text:
            if char.isspace():
                result.append(" ")
                continue
            
            sign_info = self.transcribe_sign(char)
            if sign_info:
                result.append(sign_info['phonetic'])
            else:
                result.append(f"[{char}?]")
        
        return "".join(result)
    
    def list_all_signs(self) -> Dict[str, Dict]:
        """Return all available signs for reference"""
        return self.syllabary
    
    def search_by_sound(self, sound: str) -> List[str]:
        """Find all signs that represent a given sound"""
        matches = []
        for sign, info in self.syllabary.items():
            if info['transliteration'] == sound.lower():
                matches.append(sign)
        return matches


def main():
    """Test the transcriber with some examples"""
    print("=" * 50)
    print("Linear B Transcriber - Test")
    print("=" * 50)
    
    transcriber = LinearBTranscriber()
    
    test1 = "𐀷𐀙𐀏"
    print(f"\nTest 1: {test1}")
    print(f"Transliteration: {transcriber.transcribe_text(test1)}")
    
    test2 = "𐀡𐀴𐀛𐀊"
    print(f"\nTest 2: {test2}")
    print(f"Transliteration: {transcriber.transcribe_text(test2)}")
    
    print("\n" + "=" * 50)
    print("All signs loaded:", len(transcriber.syllabary))
    print("=" * 50)


if __name__ == "__main__":
    main()