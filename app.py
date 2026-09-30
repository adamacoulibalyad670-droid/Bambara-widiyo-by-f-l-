from deep_translator import MyMemoryTranslator
import time

# Texte surun dɔrɔn - 400 lettres max pour éviter blocage
text_short = english_text[:400]

try:
    # MyMemory - gratuit, pas de limite comme Google
    bambara = MyMemoryTranslator(source='en-US', target='bm').translate(text_short)
    time.sleep(1)
except:
    # Si MyMemory ma se, on coupe texte en petits morceaux
    try:
        from deep_translator import GoogleTranslator
        words = text_short.split()
        bambara_parts = []
        for i in range(0, len(words), 20):
            chunk = " ".join(words[i:i+20])
            part = GoogleTranslator(source='en', target='bm').translate(chunk)
            bambara_parts.append(part)
            time.sleep(1)
        bambara = " ".join(bambara_parts)
    except Exception as e2:
        bambara = f"Traduction bloquée, mais Angilɛ ye: {text_short}"
