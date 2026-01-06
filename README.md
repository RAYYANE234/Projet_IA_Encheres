Prérequis
-     Python 3.10+
-     Docker + Docker Compose
-     n8n (local ou hébergé)
-     Une clé API Jina AI
-     Une clé API Mistral (ou autre LLM compatible)

 Installation
Cloner le projet

Installer les dépendances Python

Lancer n8n avec Docker

Importer le workflow n8n
Dans l’interface n8n :
-    Workflows → Import
-    Sélectionner 

 Configuration
 

2. Configurer la clé API Jina AI
Dans le nœud Jina AI :
-     Ajouter la clé dans 
 3. Configurer la clé API Mistral
Dans le script Python :
Coller l'URL du Webhook Dans le nœud webhook dans le code python scraper.py (partie WEBHOOK_URL)
 Utilisation
Lancer le script Python

Le script :
- envoie les paramètres au webhook n8n
-  récupère le JSON nettoyé
-  génère les CSV
-  affiche l’estimation final
