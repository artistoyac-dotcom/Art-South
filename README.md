# ArtSite

Génère le site vitrine à partir des œuvres enregistrées.

## Utilisation

1. Ajoute une œuvre dans `data/oeuvres.json` (copie le format de l'œuvre existante), et place son image dans `site/images/`.
2. Lance :
   ```
   python artsite.py
   ```
3. Le fichier `site/index.html` est régénéré avec toutes les œuvres.
4. Pour prévisualiser : double-clique sur `site/index.html`, il s'ouvre dans ton navigateur.
5. Pour publier : fais un commit + push du dossier `site/` (via GitHub Desktop) — si GitHub Pages est activé sur le repo, le site en ligne se met à jour automatiquement.

## Champs d'une œuvre (data/oeuvres.json)

| Champ | Exemple |
|---|---|
| id | "ART00002" |
| titre | "Palmeraie au crépuscule" |
| annee | "2026" |
| technique | "Aquarelle" |
| dimensions | "40 x 50 cm" |
| style | "Orientaliste" |
| description | Texte libre |
| prix | 350 |
| statut | "disponible" ou "vendu" |
| image | "images/nom-du-fichier.jpg" |
