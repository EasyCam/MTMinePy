# mtminepy/services/nlp_service.py
import jieba
import jieba.posseg as pseg
import nltk
from nltk.tokenize import word_tokenize
from langdetect import detect
import re
import importlib.util

# NLTK Setup - download required data
def _ensure_nltk_data():
    """Download required NLTK data packages."""
    packages = [
        'punkt',
        'punkt_tab',
        'averaged_perceptron_tagger',
        'averaged_perceptron_tagger_eng',
    ]
    for pkg in packages:
        try:
            nltk.data.find(f'tokenizers/{pkg}' if 'punkt' in pkg else f'taggers/{pkg}')
        except LookupError:
            try:
                nltk.download(pkg, quiet=True)
            except:
                pass

_ensure_nltk_data()

class NLPEngine:
    def __init__(self):
        self.spacy_models = {}
        self.hanlp_pipeline = None
        self.ltp_pipeline = None
        self.janome_tokenizer = None
        
        # Check for presence of optional libs without importing
        self.has_hanlp = importlib.util.find_spec("hanlp") is not None
        self.has_ltp = importlib.util.find_spec("ltp") is not None
        self.has_spacy = importlib.util.find_spec("spacy") is not None
        self.has_janome = importlib.util.find_spec("janome") is not None

    def detect_lang_safe(self, text):
        try:
            lang = detect(text)
            # Map langdetect codes to standard codes
            LANG_MAP = {
                'zh-cn': 'cn', 'zh-tw': 'cn', 'zh': 'cn',
                'ja': 'ja', 'en': 'en', 'ko': 'ko', 'ru': 'ru', 
                'de': 'de', 'fr': 'fr', 'it': 'it', 'es': 'es', 'pt': 'pt'
            }
            return LANG_MAP.get(lang.lower(), 'other')
        except:
            return 'unknown'

    def tokenize(self, text, lang, engine="default", stopwords=set(), pos_filter=None):
        """
        pos_filter: list of POS tags to keep (e.g. ['noun', 'verb', 'adj'])
        """
        tokens = []
        if not isinstance(text, str): return []

        # --- CHINESE ---
        if lang == 'cn':
            # Use Jieba POS tagging by default as it's lightweight
            words = pseg.cut(text)
            for w, flag in words:
                if not pos_filter:
                    tokens.append(w)
                else:
                    # Jieba tags: n=noun, v=verb, a=adj, d=adv
                    is_match = False
                    if 'noun' in pos_filter and flag.startswith('n'): is_match = True
                    if 'verb' in pos_filter and flag.startswith('v'): is_match = True
                    if 'adj' in pos_filter and flag.startswith('a'): is_match = True
                    if is_match: tokens.append(w)

        # --- JAPANESE ---
        elif lang == 'ja':
            if self.has_janome:
                if not self.janome_tokenizer:
                    try:
                        from janome.tokenizer import Tokenizer as JanomeTokenizer
                        self.janome_tokenizer = JanomeTokenizer()
                    except: pass
                
                if self.janome_tokenizer:
                    for t in self.janome_tokenizer.tokenize(text):
                        part_of_speech = t.part_of_speech.split(',')[0]
                        if not pos_filter:
                            tokens.append(t.surface)
                        else:
                            is_match = False
                            if 'noun' in pos_filter and '\u540d\u8a5e' in part_of_speech: is_match = True
                            if 'verb' in pos_filter and '\u52d5\u8a5e' in part_of_speech: is_match = True
                            if 'adj' in pos_filter and '\u5f62\u5bb9\u8a5e' in part_of_speech: is_match = True
                            if is_match: tokens.append(t.surface)
                else:
                    tokens = list(text)
            else:
                tokens = list(text)

        # --- ENGLISH & OTHERS ---
        else:
            if engine == 'spacy' and self.has_spacy:
                model = f"{lang}_core_news_sm" if lang != 'en' else "en_core_web_sm"
                if model not in self.spacy_models:
                    try:
                        import spacy
                        self.spacy_models[model] = spacy.load(model)
                    except: pass
                
                if model in self.spacy_models:
                    doc = self.spacy_models[model](text)
                    for token in doc:
                        if not pos_filter:
                            tokens.append(token.text)
                        else:
                            is_match = False
                            if 'noun' in pos_filter and token.pos_ == 'NOUN': is_match = True
                            if 'verb' in pos_filter and token.pos_ == 'VERB': is_match = True
                            if 'adj' in pos_filter and token.pos_ == 'ADJ': is_match = True
                            if is_match: tokens.append(token.text)
                else:
                    tokens = word_tokenize(text)
            else:
                # NLTK
                words = word_tokenize(text)
                if not pos_filter:
                    tokens = words
                else:
                    try:
                        tagged = nltk.pos_tag(words)
                        for w, tag in tagged:
                            is_match = False
                            if 'noun' in pos_filter and tag.startswith('NN'): is_match = True
                            if 'verb' in pos_filter and tag.startswith('VB'): is_match = True
                            if 'adj' in pos_filter and tag.startswith('JJ'): is_match = True
                            if is_match: tokens.append(w)
                    except LookupError:
                        # Fallback: return all words if POS tagger unavailable
                        tokens = words

        return [t for t in tokens if t.strip() and t.lower() not in stopwords]

nlp_engine = NLPEngine()
