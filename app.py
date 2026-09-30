# Dictionnaire pour corriger erreurs courantes de Google en Bambara
CORRECTIONS = {
    "hello": "I ni ce",
    "thank you": "I ni ce",
    "how are you": "I ka kɛnɛ",
    "president": "perésidan",
    "America": "Ameriki",
    # Ajoute tes corrections ici
}

def corriger_bambara(texte):
    texte_lower = texte.lower()
    for en, bm_correct in CORRECTIONS.items():
        if en in texte_lower:
            # On garde traduction Google mais on note correction
            pass
    # Corrections Google -> Bambara correct
    fixes = {
        "I tɛ": "I tɛ", # Google met souvent ça mal
        "ye mun ye": "ye mun ye",
    }
    for mauvais, bon in fixes.items():
        texte = texte.replace(mauvais, bon)
    return texte

# Après traduction:
bambara = corriger_bambara(bambara)
