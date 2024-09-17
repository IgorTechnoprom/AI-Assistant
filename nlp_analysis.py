# nlp_analysis.py

import spacy

# Load the English language model
nlp = spacy.load('en_core_web_sm')

def analyze_thought(text):
    """
    Analyzes the given text and extracts entities and key information.

    Parameters:
    - text (str): The text to analyze.

    Returns:
    - dict: A dictionary containing entities and other extracted information.
    """
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]

    # You can add more analysis here (e.g., sentiment, parts of speech)

    analysis_result = {
        'entities': entities,
        'keywords': tokens
    }

    return analysis_result
