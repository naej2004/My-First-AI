import re

# Compile the regex for removing HTML tags and entities
CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext

# Chemin relatif vers le fichier
file_path = 'd:/TECH TRIBE/ChatBot/KeyboardAI_WithOpenAI/search/prepared_data.txt'

# Lire le fichier texte
with open(file_path, 'r', encoding='utf-8') as file:
    raw_html = file.read()

# Nettoyer le texte
cleaned_text = cleanhtml(raw_html)

# Écrire le texte nettoyé dans un nouveau fichier
with open('prepared_data_fr.txt', 'w', encoding='utf-8') as file:
    file.write(cleaned_text)

print("Le texte a été nettoyé et enregistré dans 'data/prepared_data_nettoye.txt'")
