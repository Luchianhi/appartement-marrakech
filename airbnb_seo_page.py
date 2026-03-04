"""
=============================================================
  Générateur de page SEO pour votre annonce Airbnb
  Visible sur Google grâce aux données structurées (Schema.org)
=============================================================
  Instructions :
  1. Remplissez la section CONFIGURATION ci-dessous
  2. Ajoutez vos photos dans le dossier 'photos/'
  3. Lancez : python airbnb_seo_page.py
  4. Ouvrez le fichier 'index.html' généré
  5. Hébergez-le sur GitHub Pages, Netlify ou votre serveur
=============================================================
"""

import json
import os
from datetime import datetime

# ============================================================
#  CONFIGURATION — REMPLISSEZ CES INFORMATIONS
# ============================================================

CONFIG = {
    # Infos générales
    "titre": "Appartement Lumineux au Cœur de Marrakech",
    "sous_titre": "Appartement Beldi Marrakech",
    "description_courte": """
    Séjournez dans ce magnifique appartement confortable, situé à Socoma, dans un quartier calme et proche de toutes commodités.
    Vous profitez d’un logement privé, bien agencé et adapté aux séjours courts ou longs.
    Le centre-ville reste accessible en quelques minutes. Idéal pour couples, familles ou déplacements professionnels,
    l’appartement offre un cadre pratique et reposant pour découvrir Marrakech en toute tranquillité.""",
    
    "description_longue": """
        Bienvenue dans notre appartement d'exception, entièrement ensoleillé.
        Situé au cœur de Marrakech, à quelques pas des souks et des meilleurs restaurants,
        cet espace lumineux allie confort moderne et charme marocain authentique.
        
        Idéal pour les couples, familles ou groupes d'amis souhaitant découvrir la Perle du Sud.
        
        Équipements : WiFi, Climatisation, Cuisine équipée,
        Linge de maison fourni, Parking disponible.
    """,

    # Localisation
    "ville": "Marrakech",
    "pays": "Maroc",
    "adresse_affichee": "Socoma, Marrakech",  # Pas l'adresse exacte pour la sécurité
    "latitude": 31.616632,
    "longitude": -8.062899,

    # Capacité & Prix
    "voyageurs_max": 4,
    "chambres": 1,
    "lits": 1,
    "salles_de_bain": 1,
    "prix_par_nuit": 350,  # en DH
    "devise": "DH",
    "lien_airbnb": "https://www.airbnb.fr/rooms/1629117532108126066?source_impression_id=p3_1772653938_P3y781jiIJR264ZE",  # ← Mettez votre vrai lien

    # Photos (URLs ou chemins locaux)
    "photos": [
        {"url": "D:\09_PICTURES\0903_APPART\APPART MARRAKECH\APPART SOCOMA\20260227_125812", "alt": "Salon lumineux"},
        {"url": "D:\09_PICTURES\0903_APPART\APPART MARRAKECH\APPART SOCOMA\20260227_125855", "alt": "Chambre principale"},
        {"url": "D:\09_PICTURES\0903_APPART\APPART MARRAKECH\APPART SOCOMA\20260227_125924", "alt": "Salle de bain"},
        {"url": "D:\09_PICTURES\0903_APPART\APPART MARRAKECH\APPART SOCOMA\20260227_125956", "alt": "Cuisine"},
        {"url": "D:\09_PICTURES\0903_APPART\APPART MARRAKECH\APPART SOCOMA\20260225_ 225729", "alt": "Petit salon"},
    ],

    # Équipements (icônes emoji ou texte)
    "equipements": [
        {"icone": "📶", "nom": "WiFi"},
        {"icone": "❄️", "nom": "Climatisation"},
        {"icone": "🍳", "nom": "Cuisine"},
        {"icone": "🅿️", "nom": "Parking"},
        {"icone": "📺", "nom": "Smart TV"},
        {"icone": "🔑", "nom": "Entrée autonome"},
    ],

    # Avis clients
    "note_globale": 4.92,
    "nombre_avis": 87,
    "avis": [
        {
            "auteur": "Sophie M.",
            "pays": "France",
            "note": 5,
            "date": "Novembre 2024",
            "texte": "Appartement absolument magnifique ! Hôte très réactif et accueillant. On reviendra !"
        },
        {
            "auteur": "Carlos R.",
            "pays": "Espagne",
            "note": 5,
            "date": "Octobre 2025",
            "texte": "Increíble apartamento, muy bien ubicado, limpio y con todos los servicios. Muy recomendable."
        },
        {
            "auteur": "Emma K.",
            "pays": "Allemagne",
            "note": 5,
            "date": "Septembre 2024",
            "texte": "Perfect stay in Marrakech! The apartment is stylish, clean and the location is ideal. The host was very helpful with local tips."
        },
    ],

    # SEO
    "mots_cles": "appartement Marrakech, location Marrakech, Airbnb Marrakech, vacances Maroc, location courte durée Marrakech",
    "hote_nom": "Luchianhi",
    "hote_photo": "https://i.pravatar.cc/150?img=11",
    "annee_hote": 2021,

    # Couleurs du site (personnalisables)
    "couleur_principale": "#FF385C",  # Rouge Airbnb
    "couleur_secondaire": "#222222",
}

# ============================================================
#  GÉNÉRATION HTML — Ne modifiez pas cette partie
# ============================================================

def generer_etoiles(note):
    plein = int(note)
    demi = 1 if (note - plein) >= 0.5 else 0
    vide = 5 - plein - demi
    return "★" * plein + ("½" if demi else "") + "☆" * vide

def generer_schema_org(c):
    """Données structurées Schema.org pour Google Rich Results"""
    schema = {
        "@context": "https://schema.org",
        "@type": "LodgingBusiness",
        "name": c["titre"],
        "description": c["description_courte"],
        "url": c["lien_airbnb"],
        "image": [p["url"] for p in c["photos"][:3]],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": c["ville"],
            "addressCountry": c["pays"]
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": c["latitude"],
            "longitude": c["longitude"]
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": c["note_globale"],
            "reviewCount": c["nombre_avis"],
            "bestRating": 5
        },
        "priceRange": f"€{c['prix_par_nuit']}/nuit",
        "numberOfRooms": c["chambres"],
        "occupancy": {
            "@type": "QuantitativeValue",
            "maxValue": c["voyageurs_max"]
        },
        "review": [
            {
                "@type": "Review",
                "author": {"@type": "Person", "name": r["auteur"]},
                "reviewRating": {"@type": "Rating", "ratingValue": r["note"]},
                "reviewBody": r["texte"],
                "datePublished": r["date"]
            }
            for r in c["avis"]
        ]
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)

def generer_html(c):
    photos_html = ""
    for i, photo in enumerate(c["photos"]):
        cls = "photo-main" if i == 0 else "photo-thumb"
        photos_html += f'<img src="{photo["url"]}" alt="{photo["alt"]}" class="{cls}" loading="lazy">\n'

    equip_html = ""
    for eq in c["equipements"]:
        equip_html += f"""
        <div class="equip-item">
            <span class="equip-icone">{eq["icone"]}</span>
            <span>{eq["nom"]}</span>
        </div>"""

    avis_html = ""
    for avis in c["avis"]:
        etoiles = "★" * avis["note"] + "☆" * (5 - avis["note"])
        avis_html += f"""
        <div class="avis-card">
            <div class="avis-header">
                <div class="avis-avatar">{avis["auteur"][0]}</div>
                <div>
                    <div class="avis-auteur">{avis["auteur"]} <span class="avis-pays">— {avis["pays"]}</span></div>
                    <div class="avis-date">{avis["date"]}</div>
                </div>
                <div class="avis-etoiles">{etoiles}</div>
            </div>
            <p class="avis-texte">"{avis["texte"]}"</p>
        </div>"""

    annees_exp = datetime.now().year - c["annee_hote"]

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- SEO META TAGS -->
    <title>{c["titre"]} — Location {c["ville"]} | Airbnb</title>
    <meta name="description" content="{c["description_courte"]} À partir de {c["prix_par_nuit"]}€/nuit. Note {c["note_globale"]}/5 ({c["nombre_avis"]} avis).">
    <meta name="keywords" content="{c["mots_cles"]}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{c["lien_airbnb"]}">

    <!-- OPEN GRAPH (Facebook, WhatsApp, LinkedIn) -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{c["titre"]}">
    <meta property="og:description" content="{c["description_courte"]}">
    <meta property="og:image" content="{c["photos"][0]["url"]}">
    <meta property="og:url" content="{c["lien_airbnb"]}">
    <meta property="og:locale" content="fr_FR">

    <!-- TWITTER CARD -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{c["titre"]}">
    <meta name="twitter:description" content="{c["description_courte"]}">
    <meta name="twitter:image" content="{c["photos"][0]["url"]}">

    <!-- SCHEMA.ORG (Google Rich Results) -->
    <script type="application/ld+json">
{generer_schema_org(c)}
    </script>

    <!-- FONTS -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">

    <style>
        :root {{
            --rouge: {c["couleur_principale"]};
            --noir: {c["couleur_secondaire"]};
            --gris: #717171;
            --fond: #F7F7F7;
            --blanc: #FFFFFF;
            --radius: 16px;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: 'DM Sans', sans-serif;
            background: var(--blanc);
            color: var(--noir);
            line-height: 1.6;
        }}

        /* HEADER */
        header {{
            background: var(--blanc);
            border-bottom: 1px solid #eee;
            padding: 16px 5%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }}

        .logo {{ color: var(--rouge); font-size: 28px; font-weight: 700; letter-spacing: -1px; }}

        .btn-reserver {{
            background: var(--rouge);
            color: white;
            border: none;
            padding: 12px 28px;
            border-radius: 50px;
            font-size: 15px;
            font-weight: 500;
            cursor: pointer;
            text-decoration: none;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 15px rgba(255,56,92,0.35);
        }}

        .btn-reserver:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255,56,92,0.45);
        }}

        /* GALERIE */
        .galerie {{
            display: grid;
            grid-template-columns: 2fr 1fr 1fr;
            grid-template-rows: 280px 280px;
            gap: 8px;
            padding: 24px 5%;
            max-width: 1200px;
            margin: 0 auto;
        }}

        .galerie img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 12px;
            cursor: pointer;
            transition: opacity 0.2s;
        }}

        .galerie img:hover {{ opacity: 0.92; }}
        .photo-main {{ grid-row: span 2; border-radius: 16px !important; }}

        /* CONTENU PRINCIPAL */
        .contenu {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 32px 5%;
            display: grid;
            grid-template-columns: 1fr 340px;
            gap: 48px;
        }}

        /* TITRE */
        h1 {{
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 8px;
        }}

        .sous-titre {{ color: var(--gris); font-size: 17px; margin-bottom: 16px; }}

        .badges {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-bottom: 24px;
        }}

        .badge {{
            background: var(--fond);
            padding: 6px 14px;
            border-radius: 50px;
            font-size: 14px;
            font-weight: 500;
        }}

        .badge.superhost {{ background: #FFF8F0; color: #C45000; border: 1px solid #FFCF8B; }}

        /* NOTE */
        .note-ligne {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 16px;
            margin-bottom: 24px;
        }}

        .note-nombre {{ font-weight: 700; font-size: 20px; color: var(--rouge); }}
        .etoile {{ color: var(--rouge); }}
        .avis-count {{ color: var(--gris); }}

        hr {{ border: none; border-top: 1px solid #eee; margin: 28px 0; }}

        /* SECTION HÔTE */
        .hote {{
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 28px;
        }}

        .hote img {{
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid var(--rouge);
        }}

        .hote-info h3 {{ font-size: 18px; font-weight: 600; }}
        .hote-info p {{ color: var(--gris); font-size: 14px; }}

        /* DESCRIPTION */
        .description {{ font-size: 16px; color: #333; line-height: 1.8; white-space: pre-line; }}

        /* ÉQUIPEMENTS */
        h2 {{
            font-family: 'Playfair Display', serif;
            font-size: 1.5rem;
            margin-bottom: 20px;
        }}

        .equipements {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 12px;
        }}

        .equip-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 14px 16px;
            background: var(--fond);
            border-radius: 12px;
            font-size: 15px;
        }}

        .equip-icone {{ font-size: 22px; }}

        /* AVIS */
        .avis-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }}

        .avis-card {{
            background: var(--fond);
            border-radius: var(--radius);
            padding: 20px;
        }}

        .avis-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }}

        .avis-avatar {{
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: var(--rouge);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            font-weight: 700;
            flex-shrink: 0;
        }}

        .avis-auteur {{ font-weight: 600; font-size: 15px; }}
        .avis-pays {{ color: var(--gris); font-weight: 400; }}
        .avis-date {{ color: var(--gris); font-size: 13px; }}
        .avis-etoiles {{ margin-left: auto; color: var(--rouge); font-size: 14px; }}
        .avis-texte {{ font-size: 15px; color: #444; font-style: italic; line-height: 1.7; }}

        /* CARTE */
        .carte-container {{
            border-radius: var(--radius);
            overflow: hidden;
            height: 350px;
            border: 1px solid #eee;
        }}

        .carte-container iframe {{
            width: 100%;
            height: 100%;
            border: none;
        }}

        /* ENCART RÉSERVATION */
        .encart-resa {{
            background: var(--blanc);
            border: 1px solid #ddd;
            border-radius: 20px;
            padding: 28px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            position: sticky;
            top: 90px;
            height: fit-content;
        }}

        .prix-nuit {{
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 4px;
        }}

        .prix-nuit span {{ font-size: 16px; font-weight: 400; color: var(--gris); }}

        .resa-note {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 14px;
            color: var(--gris);
            margin-bottom: 20px;
        }}

        .resa-note .etoile {{ color: var(--rouge); }}

        .resa-dates {{
            border: 1px solid #ddd;
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 12px;
        }}

        .resa-ligne {{
            padding: 12px 16px;
            border-bottom: 1px solid #ddd;
        }}

        .resa-ligne:last-child {{ border-bottom: none; }}
        .resa-label {{ font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }}
        .resa-input {{ font-size: 15px; color: var(--gris); }}

        .resa-total {{
            display: flex;
            justify-content: space-between;
            font-weight: 700;
            font-size: 16px;
            padding: 16px 0 0;
            border-top: 1px solid #eee;
            margin-top: 16px;
        }}

        /* FOOTER */
        footer {{
            background: var(--noir);
            color: #aaa;
            text-align: center;
            padding: 32px 5%;
            margin-top: 60px;
            font-size: 14px;
        }}

        footer a {{ color: #ccc; text-decoration: none; }}

        /* RESPONSIVE */
        @media (max-width: 900px) {{
            .contenu {{ grid-template-columns: 1fr; }}
            .encart-resa {{ position: static; }}
            .galerie {{
                grid-template-columns: 1fr 1fr;
                grid-template-rows: auto;
            }}
            .photo-main {{ grid-row: span 1; }}
            h1 {{ font-size: 1.5rem; }}
        }}

        @media (max-width: 600px) {{
            .galerie {{
                grid-template-columns: 1fr;
                grid-template-rows: auto;
            }}
        }}

        /* ANIMATION */
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(24px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .galerie, .contenu {{ animation: fadeInUp 0.6s ease forwards; }}
    </style>
</head>
<body>

<!-- HEADER -->
<header>
    <div class="logo">airbnb</div>
    <a href="{c["lien_airbnb"]}" target="_blank" rel="noopener" class="btn-reserver">
        Voir sur Airbnb
    </a>
</header>

<!-- GALERIE PHOTOS -->
<div class="galerie">
    {photos_html}
</div>

<!-- CONTENU PRINCIPAL -->
<div class="contenu">
    <div class="info">

        <!-- TITRE & BADGES -->
        <h1>{c["titre"]}</h1>
        <p class="sous-titre">{c["sous_titre"]}</p>

        <div class="badges">
            <span class="badge">🏆 Superhost</span>
            <span class="badge">👥 {c["voyageurs_max"]} voyageurs</span>
            <span class="badge">🛏 {c["chambres"]} chambres · {c["lits"]} lits</span>
            <span class="badge">🚿 {c["salles_de_bain"]} salle de bain</span>
            <span class="badge superhost">⭐ Coup de cœur voyageurs</span>
        </div>

        <div class="note-ligne">
            <span class="etoile">★</span>
            <span class="note-nombre">{c["note_globale"]}</span>
            <span class="avis-count">· {c["nombre_avis"]} avis exceptionnels</span>
        </div>

        <hr>

        <!-- HÔTE -->
        <div class="hote">
            <img src="{c["hote_photo"]}" alt="Photo de {c["hote_nom"]}">
            <div class="hote-info">
                <h3>Logement proposé par {c["hote_nom"]}</h3>
                <p>Superhost · Hôte depuis {annees_exp} ans · Répond en moins d'une heure</p>
            </div>
        </div>

        <hr>

        <!-- DESCRIPTION -->
        <h2>À propos de ce logement</h2>
        <p class="description">{c["description_longue"].strip()}</p>

        <hr>

        <!-- ÉQUIPEMENTS -->
        <h2>Ce que propose ce logement</h2>
        <div class="equipements">
            {equip_html}
        </div>

        <hr>

        <!-- AVIS -->
        <h2>⭐ {c["note_globale"]} · {c["nombre_avis"]} avis</h2>
        <div class="avis-grid">
            {avis_html}
        </div>

        <hr>

        <!-- LOCALISATION -->
        <h2>📍 Localisation — {c["adresse_affichee"]}</h2>
        <div class="carte-container">
            <iframe
                src="https://maps.google.com/maps?q={c["latitude"]},{c["longitude"]}&z=15&output=embed"
                title="Localisation du logement"
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade">
            </iframe>
        </div>

    </div>

    <!-- ENCART RÉSERVATION -->
    <div class="encart-resa">
        <div class="prix-nuit">{c["prix_par_nuit"]} {c["devise"]} <span>/ nuit</span></div>
        <div class="resa-note">
            <span class="etoile">★</span>
            <strong>{c["note_globale"]}</strong>
            <span>· {c["nombre_avis"]} avis</span>
        </div>

        <div class="resa-dates">
            <div class="resa-ligne">
                <div class="resa-label">Arrivée</div>
                <div class="resa-input">Sélectionner une date</div>
            </div>
            <div class="resa-ligne">
                <div class="resa-label">Départ</div>
                <div class="resa-input">Sélectionner une date</div>
            </div>
            <div class="resa-ligne">
                <div class="resa-label">Voyageurs</div>
                <div class="resa-input">1 voyageur</div>
            </div>
        </div>

        <a href="{c["lien_airbnb"]}" target="_blank" rel="noopener" class="btn-reserver"
           style="display:block; text-align:center; width:100%; margin-top:12px;">
            Réserver sur Airbnb
        </a>

        <p style="text-align:center; color: #717171; font-size:13px; margin-top:12px;">
            Vous ne serez pas débité maintenant
        </p>

        <div class="resa-total">
            <span>{c["prix_par_nuit"]} {c["devise"]} × 7 nuits</span>
            <span>{c["prix_par_nuit"] * 7} {c["devise"]}</span>
        </div>
    </div>
</div>

<!-- FOOTER -->
<footer>
    <p style="margin-bottom:8px;">
        <a href="{c["lien_airbnb"]}" target="_blank">Réserver sur Airbnb</a> ·
        <a href="https://www.airbnb.fr">Airbnb.fr</a>
    </p>
    <p>© {datetime.now().year} {c["hote_nom"]} · {c["ville"]}, {c["pays"]}</p>
    <p style="margin-top:8px; font-size:12px; color:#666;">
        Page générée automatiquement pour améliorer la visibilité SEO de l'annonce Airbnb.
    </p>
</footer>

</body>
</html>"""

# ============================================================
#  MAIN
# ============================================================

if __name__ == "__main__":
    print("=" * 55)
    print("  🏠 Générateur SEO Airbnb")
    print("=" * 55)

    html = generer_html(CONFIG)

    output_file = "index.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n✅ Page générée : {output_file}")
    print(f"📄 Taille       : {len(html):,} caractères")
    print(f"\n📌 PROCHAINES ÉTAPES :")
    print("  1. Ouvrez 'index.html' dans votre navigateur pour prévisualiser")
    print("  2. Modifiez la section CONFIG dans le script")
    print("  3. Hébergez gratuitement sur :")
    print("     • GitHub Pages → github.com/pages")
    print("     • Netlify      → netlify.com (drag & drop)")
    print("     • Vercel       → vercel.com")
    print("\n🔍 POUR GOOGLE :")
    print("  • Soumettez l'URL sur search.google.com/search-console")
    print("  • Testez les données structurées sur :")
    print("    search.google.com/test/rich-results")
    print("=" * 55)
