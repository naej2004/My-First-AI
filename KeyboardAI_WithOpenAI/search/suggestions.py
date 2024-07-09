from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline
import torch

# Charger le tokenizer et le modèle fine-tuné
model_path = "D:/TECH TRIBE/ChatBot/KeyboardAI_WithOpenAI/search/KeyboardAI"

tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

# Spécifier explicitement le pad_token_id pour éviter l'avertissement
model.config.pad_token_id = model.config.eos_token_id

# Créer un pipeline pour la génération de texte avec ton modèle fine-tuné
generator = pipeline('text-generation', model=model, tokenizer=tokenizer)


def suggerer_mots(contexte, num_suggestions=4):
    # Générer un grand nombre de suggestions brutes pour maximiser les chances d'obtenir des suggestions valides
    raw_suggestions = generator(contexte, max_new_tokens=1, num_return_sequences=num_suggestions * 10)
    unique_suggestions = []
    seen_texts = set()

    for suggestion in raw_suggestions:
        generated_text = suggestion['generated_text'][len(contexte):].strip()
        # Vérifier que la suggestion est un seul mot et non vide
        if ' ' not in generated_text and generated_text not in seen_texts and generated_text != '':
            seen_texts.add(generated_text)
            unique_suggestions.append(generated_text)
        if len(unique_suggestions) >= num_suggestions:
            break

    # Si pas assez de suggestions valides ont été trouvées
    if len(unique_suggestions) < num_suggestions:
        print(f"Seulement {len(unique_suggestions)} suggestions uniques trouvées.")

    return unique_suggestions


# Exemple d'utilisation
contexte = "Hello, my"
suggestions = suggerer_mots(contexte)
print(suggestions)
