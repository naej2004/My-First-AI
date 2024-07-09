import torch
from transformers import (GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, TextDataset,
                          DataCollatorForLanguageModeling)
import os

# Charger le tokenizer et le modèle pré-entraîné GPT-2
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")


# Préparer le dataset
def load_dataset(file_path, tokenize):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    except UnicodeDecodeError:
        print("Erreur de décodage UTF-8, tentative avec ISO-8859-1...")
        with open(file_path, "r", encoding="ISO-8859-1") as f:
            text = f.read()

    # Écrire le contenu dans un fichier temporaire
    temp_file_path = "temp_prepared_data.txt"
    with open(temp_file_path, "w", encoding="utf-8") as f:
        f.write(text)

    dataset = TextDataset(
        tokenizer=tokenize,
        file_path=temp_file_path,
        block_size=128
    )

    # Supprimer le fichier temporaire après utilisation
    os.remove(temp_file_path)

    return dataset


# Coller les données pour l'entraînement
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)

# Charger les données d'entraînement
train_dataset = load_dataset("prepared_data_fr.txt", tokenizer)

# Définir les arguments d'entraînement
training_args = TrainingArguments(
    output_dir="./results",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    save_steps=10_000,
    save_total_limit=2,
)

# Créer l'entraîneur
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
)

# Lancer l'entraînement
for epoch in range(training_args.num_train_epochs):
    # Entraînement pour une époque
    trainer.train()

    # Sauvegarder le modèle et le tokenizer à la fin de chaque époque
    model.save_pretrained(f"./fine_tuned_gpt2_epoch_{epoch+1}")
    tokenizer.save_pretrained(f"./fine_tuned_gpt2_epoch_{epoch+1}")

# Sauvegarder le modèle fine-tuné et le tokenizer après l'entraînement complet
model.save_pretrained("./KeyboardAI")
tokenizer.save_pretrained("./KeyboardAI")
