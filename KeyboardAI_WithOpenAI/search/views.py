from django.shortcuts import render
from django.http import JsonResponse
from transformers import AutoModelForCausalLM, AutoTokenizer, GPT2LMHeadModel, GPT2Tokenizer, pipeline
import torch

# Modèle et tokenizer pour le chat
tokenizer_chat = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model_chat = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Chemin vers le modèle fine-tuné pour les suggestions

model_path = "D:/TECH Projects/MyFirstAI/KeyboardAI_WithOpenAI/search/KeyboardAI"

# Modèle et tokenizer pour les suggestions
tokenizer_suggestion = GPT2Tokenizer.from_pretrained(model_path)
model_suggestion = GPT2LMHeadModel.from_pretrained(model_path)

# Fix: Explicitly set the pad_token to eos_token
model_suggestion.config.pad_token_id = model_suggestion.config.eos_token_id

# Create a pipeline for text generation with your fine-tuned model
generator = pipeline('text-generation', model=model_suggestion, tokenizer=tokenizer_suggestion)

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

def get_chat_response(text):
    chat_history_ids = None
    for step in range(5):
        new_user_input_ids = tokenizer_chat.encode(str(text) + tokenizer_chat.eos_token, return_tensors='pt')
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if chat_history_ids is not None else new_user_input_ids
        chat_history_ids = model_chat.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer_chat.eos_token_id)
        response = tokenizer_chat.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response

def get_response(request):
    if request.method == "POST":
        msg = request.POST.get('msg')
        response = get_chat_response(msg)
        return JsonResponse({'response': response})
    return JsonResponse({'response': 'Only POST method is allowed.'})

def get_suggestions(request):
    if request.method == "POST":
        context = request.POST.get('context')
        # Vérification si le tokenizer a un token de padding
        suggestions = suggerer_mots(context)
        print(suggestions)
        return JsonResponse({'suggestions': suggestions})
    return JsonResponse({'suggestions': []})

def home_page(request):
    return render(request, template_name="chat.html")


