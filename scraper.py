import requests
import json
import csv
import subprocess


WEBHOOK_URL = "VOTRE_WEBHOOK_URL"

def ask(prompt, example):
    print(f"{prompt} (ex: {example})")
    return input("> ").strip()

def write_csv(filename, items):
    """Crée un CSV propre à partir d'une liste de dictionnaires."""
    if not items:
        print(f"Aucun item pour {filename}, CSV vide.")
        with open(filename, "w", newline="", encoding="utf-8") as f:
            f.write("")  # fichier vide
        return

    # Récupérer toutes les clés présentes dans les items
    fieldnames = set()
    for item in items:
        fieldnames.update(item.keys())
    fieldnames = list(fieldnames)

    # Écriture du CSV
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(items)

    print(f"→ CSV généré : {filename}")

def main():
    print("=== Création du JSON produit ===")

    brand = ask("Marque", "Zara")
    type_ = ask("Type de vêtement", "veste")
    material = ask("Matière", "laine mélangée")
    size = ask("Taille", "M")
    color = ask("Couleur", "beige")
    condition = ask("État", "très bon")

    product_json = {
        "brand": brand,
        "type": type_,
        "material": material,
        "size": size,
        "color": color,
        "condition": condition
    }

    print("\nJSON généré :")
    print(product_json)

    #  Sauvegarde du JSON produit localement
    with open("produit.json", "w", encoding="utf-8") as f:
        json.dump(product_json, f, ensure_ascii=False, indent=4)
    print("→ JSON produit sauvegardé dans produit.json")

    print("\nEnvoi au workflow n8n...")
    response = requests.post(WEBHOOK_URL, json=product_json)

    # Sauvegarde du JSON reçu depuis n8n
    try:
        data = response.json()

        with open("resultats.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("→ Réponse sauvegardée dans resultats.json")

        # n8n renvoie une liste → on prend le premier élément
        payload = data[0]

        ebay = payload.get("ebay", [])
        vinted = payload.get("vinted", [])
        leboncoin = payload.get("leboncoin", [])

        #  Création des CSV
        write_csv("ebay.csv", ebay)
        write_csv("vinted.csv", vinted)
        write_csv("leboncoin.csv", leboncoin)
        print("\n=== Exécution du script Mistral ===")
        subprocess.run(["python", "mistral.py"])

    except Exception as e:
        print(" Impossible de convertir la réponse en JSON :", e)

if __name__ == "__main__":
    main()