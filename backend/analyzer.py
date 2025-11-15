"""
Mycenaean Greek Morphological Analyzer
Analyzes transcribed Linear B words for linguistic features
"""

import json
import os
from typing import Dict, Optional, List

class MycenaeanAnalyzer:
    def __init__(self, data_dir: str = "data"):
        """Initialize analyzer with lexicon data"""
        lexicon_path = os.path.join(data_dir, "lexicon.json")
        
        with open(lexicon_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.lexicon = data['words']
            self.common_endings = data.get('common_endings', {})
    
    def analyze_word(self, transliteration: str) -> Optional[Dict]:
        """Analyze a transliterated word"""
        normalized = transliteration.lower().strip()
        
        if normalized in self.lexicon:
            word_data = self.lexicon[normalized].copy()
            word_data['transliteration'] = normalized
            return word_data
        
        return self._analyze_unknown_word(normalized)
    
    def _analyze_unknown_word(self, word: str) -> Optional[Dict]:
        """Attempt analysis of word not in lexicon"""
        result = {
            'transliteration': word,
            'status': 'unknown',
            'possible_analysis': []
        }
        
        for ending, description in self.common_endings.items():
            if word.endswith(ending.replace('-', '')):
                result['possible_analysis'].append({
                    'ending': ending,
                    'function': description
                })
        
        if result['possible_analysis']:
            result['status'] = 'partial'
            return result
        
        return None
    
    def get_classical_equivalent(self, transliteration: str) -> Optional[str]:
        """Get the Classical Greek form of a Mycenaean word"""
        word_data = self.analyze_word(transliteration)
        if word_data and 'classical_greek' in word_data:
            return word_data['classical_greek']
        return None
    
    def compare_to_classical(self, transliteration: str) -> Dict:
        """Compare Mycenaean form to Classical Greek"""
        word_data = self.analyze_word(transliteration)
        if not word_data or 'classical_greek' not in word_data:
            return {'error': 'Word not found or no Classical equivalent'}
        
        mycenaean = word_data.get('reconstruction', transliteration)
        classical = word_data['classical_greek']
        
        changes = []
        
        if mycenaean.startswith('w') and not classical.startswith('ϝ'):
            changes.append({
                'type': 'Loss of digamma',
                'description': f'Initial w- lost: {mycenaean} → {classical}'
            })
        
        if 'kʷ' in word_data.get('etymology', '') or 'labiovelar' in word_data.get('notes', '').lower():
            changes.append({
                'type': 'Labiovelar change',
                'description': 'Labiovelar *kʷ became π (p) or τ (t)'
            })
        
        return {
            'mycenaean': mycenaean,
            'classical': classical,
            'meaning': word_data.get('meaning', 'unknown'),
            'changes': changes,
            'etymology': word_data.get('etymology', '')
        }
    
    def search_by_meaning(self, meaning: str) -> List[Dict]:
        """Search lexicon by English meaning"""
        results = []
        meaning_lower = meaning.lower()
        
        for trans, data in self.lexicon.items():
            if meaning_lower in data.get('meaning', '').lower():
                results.append({
                    'transliteration': trans,
                    'meaning': data['meaning'],
                    'classical': data.get('classical_greek', ''),
                    'reconstruction': data.get('reconstruction', trans)
                })
        
        return results
    
    def list_all_words(self) -> List[str]:
        """Return list of all words in lexicon"""
        return list(self.lexicon.keys())


def main():
    """Test the analyzer"""
    print("=" * 50)
    print("Mycenaean Greek Analyzer - Test")
    print("=" * 50)
    
    analyzer = MycenaeanAnalyzer()
    
    print("\nTest 1: Analyzing 'wa-na-ka'")
    result = analyzer.analyze_word("wa-na-ka")
    if result:
        print(f"  Meaning: {result['meaning']}")
        print(f"  Classical Greek: {result['classical_greek']}")
    
    print("\n" + "=" * 50)
    print(f"Total words in lexicon: {len(analyzer.lexicon)}")
    print("=" * 50)


if __name__ == "__main__":
    main()