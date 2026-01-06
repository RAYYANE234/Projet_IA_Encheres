import json
from mistralai import Mistral

# 🔑 Mets ta clé API Mistral ici
MISTRAL_API_KEY = "gHeHiGm5VjXbfLn00zy6p0eDhjFHQdlN"

client = Mistral(api_key=MISTRAL_API_KEY)

def main():
    print("=== Chargement des données ===")

    # Charger le produit
    with open("produit.json", "r", encoding="utf-8") as f:
        product = json.load(f)

    # Charger les résultats du scraping
    with open("resultats.json", "r", encoding="utf-8") as f:
        resultats = json.load(f)

    # n8n renvoie une liste → on prend le premier élément
    listings = resultats[0]

    print("Produit chargé :", product)
    print("Annonces chargées :", list(listings.keys()))

    # Construire le prompt IA
    prompt = f"""
Tu es un expert en estimation de prix de vêtements d'occasion.

Voici le produit :
{json.dumps(product, ensure_ascii=False, indent=2)}

Voici les annonces trouvées :
{json.dumps(listings, ensure_ascii=False, indent=2)}

Analyse les annonces similaires et retourne :
- un prix estimé
- un prix minimum
- un prix maximum
- une justification courte
- les annonces les plus proches
"""

    print("\n=== Envoi à Mistral AI ===")

    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {"role": "system", "content": "Tu es un expert en estimation de prix."},
            {"role": "user", "content": prompt}
        ]
    )

    result = response.choices[0].message.content

    print("\n=== Résultat IA ===")
    print(result)

    # Sauvegarde dans un fichier
    with open("estimation_mistral.txt", "w", encoding="utf-8") as f:
        f.write(result)

    print("\n→ Résultat sauvegardé dans estimation_mistral.txt")

if __name__ == "__main__":
    main()