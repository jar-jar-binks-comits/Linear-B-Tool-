document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('linearb-input');
    const transcribeBtn = document.getElementById('transcribe-btn');
    const clearBtn = document.getElementById('clear-btn');
    const addSpaceBtn = document.getElementById('add-space-btn');
    const resultsSection = document.getElementById('results');
    const transliterationOutput = document.getElementById('transliteration-output');
    const phoneticOutput = document.getElementById('phonetic-output');
    const analysisSection = document.getElementById('analysis-section');
    const analysisOutput = document.getElementById('analysis-output');
    const examplesContainer = document.getElementById('examples-container');
    const syllabaryContainer = document.getElementById('syllabary-container');

    // Load syllabary and examples immediately
    loadSyllabary();
    loadExamples();

    // Transcribe button
    transcribeBtn.addEventListener('click', async () => {
        const text = input.value.trim();
        
        if (!text) {
            alert('Please enter some Linear B text');
            return;
        }

        try {
            const response = await fetch('/api/transcribe', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });

            const data = await response.json();

            if (data.success) {
                transliterationOutput.textContent = data.transliteration;
                phoneticOutput.textContent = data.phonetic;
                resultsSection.style.display = 'block';

                const words = data.transliteration.split(' ');
                if (words.length === 1) {
                    analyzeWord(words[0]);
                } else {
                    analysisSection.style.display = 'none';
                }
                
                // Scroll to results
                resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                alert('Error: ' + (data.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to transcribe text');
        }
    });

    // Clear button
    clearBtn.addEventListener('click', () => {
        input.value = '';
        resultsSection.style.display = 'none';
        analysisSection.style.display = 'none';
        input.focus();
    });

    // Add space button
    addSpaceBtn.addEventListener('click', () => {
        input.value += ' ';
        input.focus();
    });

    // Allow Enter key to transcribe
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && e.ctrlKey) {
            transcribeBtn.click();
        }
    });

    // Analyze word
    async function analyzeWord(word) {
        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ word })
            });

            const data = await response.json();

            if (data.success && data.analysis) {
                let html = `
                    <div class="analysis-item">
                        <strong>Meaning:</strong> ${data.analysis.meaning || 'Unknown'}
                    </div>
                `;

                if (data.analysis.classical_greek) {
                    html += `
                        <div class="analysis-item">
                            <strong>Classical Greek:</strong> ${data.analysis.classical_greek}
                        </div>
                    `;
                }

                if (data.analysis.reconstruction) {
                    html += `
                        <div class="analysis-item">
                            <strong>Reconstruction:</strong> ${data.analysis.reconstruction}
                        </div>
                    `;
                }

                if (data.comparison && data.comparison.changes && data.comparison.changes.length > 0) {
                    html += `<div class="analysis-item"><strong>Sound Changes:</strong><ul style="margin-left: 20px; margin-top: 5px;">`;
                    data.comparison.changes.forEach(change => {
                        html += `<li style="margin: 5px 0;">${change.type}: ${change.description}</li>`;
                    });
                    html += `</ul></div>`;
                }

                analysisOutput.innerHTML = html;
                analysisSection.style.display = 'block';
            } else {
                analysisSection.style.display = 'none';
            }
        } catch (error) {
            console.error('Error analyzing word:', error);
        }
    }

    // Load examples
    async function loadExamples() {
        try {
            const response = await fetch('/api/examples');
            const examples = await response.json();

            examples.forEach(example => {
                const card = document.createElement('div');
                card.className = 'example-card';
                card.innerHTML = `
                    <h4>${example.name}</h4>
                    <div class="example-linear-b">${example.linear_b}</div>
                    <p class="example-description">${example.description}</p>
                `;
                card.addEventListener('click', () => {
                    input.value = example.linear_b;
                    input.focus();
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                });
                examplesContainer.appendChild(card);
            });
        } catch (error) {
            console.error('Error loading examples:', error);
        }
    }

    // Load syllabary into sidebar
    async function loadSyllabary() {
        try {
            const response = await fetch('/api/syllabary');
            const signs = await response.json();

            // Sort alphabetically by transliteration
            signs.sort((a, b) => a.transliteration.localeCompare(b.transliteration));

            signs.forEach(sign => {
                const card = document.createElement('div');
                card.className = 'syllable-card';
                card.innerHTML = `
                    <span class="syllable-sign">${sign.sign}</span>
                    <span class="syllable-trans">${sign.transliteration}</span>
                `;
                card.addEventListener('click', () => {
                    input.value += sign.sign;
                    input.focus();
                    // Visual feedback
                    card.style.background = 'rgba(240, 165, 0, 0.5)';
                    setTimeout(() => {
                        card.style.background = 'rgba(240, 165, 0, 0.1)';
                    }, 200);
                });
                card.title = `Add "${sign.transliteration}" to input`;
                syllabaryContainer.appendChild(card);
            });
        } catch (error) {
            console.error('Error loading syllabary:', error);
            syllabaryContainer.innerHTML = '<p style="color: #ff6b6b; padding: 20px;">Error loading syllabary</p>';
        }
    }
});