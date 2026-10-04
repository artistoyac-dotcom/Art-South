"""
ArtSite — Générateur du site vitrine
=====================================

Fonctionnement :
- Les œuvres sont stockées dans data/oeuvres.json
- Lance `python artsite.py` : il régénère site/index.html avec toutes les œuvres
- Le site final est dans le dossier site/ — c'est lui qui est publié (GitHub Pages)

Pour ajouter une œuvre : ajoute-la à la main dans data/oeuvres.json (ou utilise
plus tard le script d'ajout automatique), puis relance artsite.py.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "oeuvres.json"
SITE_DIR = BASE_DIR / "site"
OUTPUT_FILE = SITE_DIR / "index.html"

NOM_ARTISTE = "Rayane Yacine"
TAGLINE = "Peintures et aquarelles du Sahara algérien"


def charger_oeuvres():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def carte_oeuvre(o):
    statut_classe = "statut-disponible" if o["statut"] == "disponible" else "statut-vendu"
    statut_texte = "Disponible" if o["statut"] == "disponible" else "Vendu"
    return f"""
    <div class="oeuvre" data-style="{o.get('style','')}" data-statut="{o['statut']}" data-prix="{o.get('prix', 0)}"
         onclick='ouvrirModale({json.dumps(o, ensure_ascii=False)})'>
      <div class="oeuvre-image-wrap">
        <img src="{o['image']}" alt="{o['titre']}" loading="lazy">
        <div class="prix-flottant">{o.get('prix', '')} €</div>
      </div>
      <div class="oeuvre-legende">
        <div>
          <div class="titre-oeuvre">{o['titre']}</div>
          <div class="meta-oeuvre">{o.get('annee','')} · {o.get('technique','')}</div>
        </div>
        <div class="meta-oeuvre"><span class="statut-point {statut_classe}"></span>{statut_texte}</div>
      </div>
    </div>"""


def styles_disponibles(oeuvres):
    return sorted({o.get("style", "") for o in oeuvres if o.get("style")})


def generer_html(oeuvres):
    cartes = "\n".join(carte_oeuvre(o) for o in oeuvres)
    options_styles = "\n".join(
        f'<option value="{s}">{s}</option>' for s in styles_disponibles(oeuvres)
    )

    oeuvre_hero = oeuvres[0] if oeuvres else None
    hero_img = oeuvre_hero["image"] if oeuvre_hero else ""
    hero_caption = oeuvre_hero["titre"] if oeuvre_hero else ""

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{NOM_ARTISTE} — {TAGLINE}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>

<nav class="nav">
  <div class="nav-logo">{NOM_ARTISTE}</div>
  <div class="nav-liens">
    <a href="#galerie">Galerie</a>
    <a href="#contact">Contact</a>
  </div>
</nav>

<section class="hero">
  <div class="hero-texte">
    <div class="hero-eyebrow">Laghouat, Algérie</div>
    <h1>Peindre la lumière du Sahara</h1>
    <p>Huiles et aquarelles inspirées des oasis, des palmeraies et de la vie quotidienne
       du Sud algérien, dans la tradition orientaliste d'Étienne Dinet.</p>
  </div>
  <figure class="hero-image">
    <img src="{hero_img}" alt="{hero_caption}">
    <figcaption>{hero_caption}</figcaption>
  </figure>
</section>

<div class="filtres" id="galerie">
  <label>Style</label>
  <select id="filtre-style" onchange="filtrer()">
    <option value="">Tous</option>
    {options_styles}
  </select>

  <label>Disponibilité</label>
  <select id="filtre-statut" onchange="filtrer()">
    <option value="">Toutes</option>
    <option value="disponible">Disponible</option>
    <option value="vendu">Vendu</option>
  </select>

  <label>Prix</label>
  <select id="filtre-prix" onchange="filtrer()">
    <option value="">Tous</option>
    <option value="0-300">Jusqu'à 300 €</option>
    <option value="300-600">300 € – 600 €</option>
    <option value="600-9999">600 € et plus</option>
  </select>
</div>

<div class="galerie" id="grille-galerie">
{cartes}
</div>

<div class="modale-fond" id="modale-fond" onclick="if(event.target===this) fermerModale()">
  <div class="modale">
    <img id="modale-img" src="" alt="">
    <div class="modale-texte">
      <button class="modale-fermer" onclick="fermerModale()">✕</button>
      <h2 id="modale-titre"></h2>
      <div class="modale-meta" id="modale-meta"></div>
      <p class="modale-description" id="modale-description"></p>
      <div class="modale-prix" id="modale-prix"></div>
      <div class="modale-actions">
        <a class="bouton bouton-principal" id="modale-contact" href="#contact">Me contacter</a>
        <a class="bouton bouton-secondaire" href="https://instagram.com" target="_blank" rel="noopener">Voir sur Instagram</a>
      </div>
    </div>
  </div>
</div>

<footer class="pied" id="contact">
  <div>{NOM_ARTISTE} — {TAGLINE}</div>
  <div><a href="mailto:contact@example.com">contact@example.com</a> · <a href="https://instagram.com" target="_blank" rel="noopener">Instagram</a></div>
</footer>

<script>
function ouvrirModale(o) {{
  document.getElementById('modale-img').src = o.image;
  document.getElementById('modale-titre').textContent = o.titre;
  document.getElementById('modale-meta').textContent = (o.annee || '') + ' · ' + (o.technique || '') + ' · ' + (o.dimensions || '');
  document.getElementById('modale-description').textContent = o.description || '';
  document.getElementById('modale-prix').textContent = o.statut === 'disponible' ? (o.prix + ' €') : 'Vendu';
  document.getElementById('modale-fond').classList.add('ouverte');
}}
function fermerModale() {{
  document.getElementById('modale-fond').classList.remove('ouverte');
}}
document.addEventListener('keydown', e => {{ if (e.key === 'Escape') fermerModale(); }});

function filtrer() {{
  const style = document.getElementById('filtre-style').value;
  const statut = document.getElementById('filtre-statut').value;
  const prixRange = document.getElementById('filtre-prix').value;
  document.querySelectorAll('.oeuvre').forEach(el => {{
    let visible = true;
    if (style && el.dataset.style !== style) visible = false;
    if (statut && el.dataset.statut !== statut) visible = false;
    if (prixRange) {{
      const [min, max] = prixRange.split('-').map(Number);
      const prix = Number(el.dataset.prix);
      if (prix < min || prix > max) visible = false;
    }}
    el.style.display = visible ? '' : 'none';
  }});
}}
</script>

</body>
</html>
"""


def main():
    oeuvres = charger_oeuvres()
    if not oeuvres:
        print("Aucune œuvre dans data/oeuvres.json — le site sera généré vide.")

    html = generer_html(oeuvres)
    SITE_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Site généré : {OUTPUT_FILE} ({len(oeuvres)} œuvre(s))")


if __name__ == "__main__":
    main()
