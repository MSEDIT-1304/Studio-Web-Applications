from flask import Flask, render_template, request, redirect, session, Response
import stripe
import os


app = Flask(__name__)
app.secret_key = "msedit_panier_2026"
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

PRIX = {

    "site550": ("Site vitrine Essentiel", 550),
    "site750": ("Site vitrine Premium", 750),
    "application2500": ("Application web personnalisée", 2500)

}

METIERS = [

    "plombier",
    "chauffagiste",
    "électricien",
    "menuisier",
    "maçon",
    "peintre",
    "couvreur",
    "charpentier",
    "carreleur",
    "plaquiste",
    "serrurier",
    "vitrier",
    "paysagiste",
    "jardinier",
    "élagueur",
    "pisciniste",
    "garagiste",
    "mécanicien",
    "carrossier",
    "dépanneur",
    "coiffeur",
    "esthéticienne",
    "restaurant",
    "boulanger",
    "pâtissier",
    "boucher",
    "traiteur",
    "photographe",
    "architecte",
    "avocat",
    "notaire",
    "expert-comptable",
    "médecin",
    "dentiste",
    "kinésithérapeute",
    "psychologue",
    "coach sportif",
    "agent immobilier",
    "artisan",
    "entreprise"

]

def creer_page(
    metier,
    titre=None,
    description=None,
    mots_cles=None
):

    if titre is None:
        titre = f"Création de site internet pour {metier}"

    if description is None:
        description = (
            f"Création de site internet professionnel pour {metier}. "
            "Développement sur mesure, référencement Google, paiement en ligne et réservation."
        )

    if mots_cles is None:
        mots_cles = (
            f"site internet {metier}, création site {metier}, "
            f"site web {metier}"
        )

    contenu = CONTENUS_METIERS.get(metier, {})

    intro = contenu.get(
        "intro",
        f"Vous êtes {metier} et vous souhaitez développer votre activité ? Studio Web & Applications crée des sites internet professionnels entièrement personnalisés, conçus pour améliorer votre visibilité sur Google et faciliter la prise de contact avec vos futurs clients."
    )

    fonctionnalites = contenu.get(
        "fonctionnalites",
        [
            "Formulaire de contact",
            "Demande de devis",
            "Google Maps",
            "Avis clients",
            "Site responsive"
        ]
    )

    return {

        "title": titre,

        "meta_description": description,

        "keywords": mots_cles,

        "h1": titre,

        "slogan": "Développez votre visibilité grâce à un site internet professionnel.",

        "introduction": intro,
        "texte":
            "Fonctionnalités pouvant être intégrées à votre site internet : "
            + ", ".join(fonctionnalites) + ".",

        "faq": [

    {
        "question": f"Pourquoi un(e) {metier} a-t-il besoin d'un site internet ?",
        "reponse": f"Un site internet professionnel permet à un(e) {metier} d'être visible sur Google, de présenter ses prestations, d'inspirer confiance et de recevoir de nouvelles demandes de contact."
    },

    {
        "question": f"Quelles fonctionnalités sont utiles pour un(e) {metier} ?",
        "reponse": "Selon votre activité, votre site peut intégrer un formulaire de contact, une demande de devis, une galerie photos, Google Maps, des avis clients, un agenda de réservation ou un espace d'administration."
    },

    {
        "question": "Le site est-il compatible avec les téléphones mobiles ?",
        "reponse": "Oui. Tous les sites développés sont compatibles avec les ordinateurs, les tablettes et les smartphones."
    }

],

"liens": [

    {
        "nom": "Nos services",
        "url": "/services"
    },

    {
        "nom": "Nous contacter",
        "url": "/contact"
    }

]

}

CONTENUS_METIERS = {

    "plombier": {
        "intro": "Vous êtes plombier et souhaitez développer votre clientèle ? Un site internet professionnel vous permet d'être trouvé sur Google, de présenter vos prestations et de recevoir rapidement des demandes de devis.",
        "fonctionnalites": [
            "Formulaire de demande de devis",
            "Présentation des prestations",
            "Intervention d'urgence",
            "Carte Google Maps",
            "Avis clients"
        ]
    },

    "chauffagiste": {
        "intro": "Présentez vos installations, entretiens et dépannages grâce à un site internet moderne qui inspire confiance et facilite la prise de contact.",
        "fonctionnalites": [
            "Demande de devis",
            "Contrats d'entretien",
            "Présentation des services",
            "Google Maps",
            "Avis clients"
        ]
    },

    "électricien": {
        "intro": "Développez votre visibilité locale avec un site internet optimisé pour mettre en avant vos installations, dépannages et mises aux normes.",
        "fonctionnalites": [
            "Demande d'intervention",
            "Présentation des réalisations",
            "Google Maps",
            "Avis clients",
            "Formulaire de contact"
        ]
    },

    "restaurant": {
        "intro": "Donnez envie à vos futurs clients grâce à un site internet mettant en valeur votre établissement, votre carte et vos services.",
        "fonctionnalites": [
            "Présentation du menu",
            "Réservation",
            "Galerie photos",
            "Google Maps",
            "Horaires"
        ]
    },

    "avocat": {
        "intro": "Présentez vos domaines d'intervention et permettez à vos futurs clients de prendre facilement contact avec votre cabinet.",
        "fonctionnalites": [
            "Présentation du cabinet",
            "Prise de rendez-vous",
            "Formulaire sécurisé",
            "Google Maps",
            "Contact rapide"
        ]
    },

    "boulanger": {
        "intro": "Présentez votre boulangerie, vos spécialités et vos horaires grâce à un site internet professionnel qui donne envie à vos clients de vous rendre visite.",
        "fonctionnalites": [
            "Présentation des produits",
            "Horaires",
            "Google Maps",
            "Galerie photos",
            "Formulaire de contact"
        ]
    },

    "pâtissier": {
        "intro": "Mettez en valeur vos créations, vos commandes personnalisées et vos prestations grâce à un site internet moderne et élégant.",
        "fonctionnalites": [
            "Galerie de réalisations",
            "Commande de gâteaux",
            "Formulaire de devis",
            "Google Maps",
            "Contact"
        ]
    },

    "boucher": {
        "intro": "Valorisez votre savoir-faire, vos produits et vos services avec un site internet professionnel adapté à votre activité.",
        "fonctionnalites": [
            "Présentation des produits",
            "Horaires",
            "Google Maps",
            "Avis clients",
            "Contact"
        ]
    },

    "traiteur": {
        "intro": "Présentez vos menus, vos prestations et permettez à vos clients de demander facilement un devis en ligne.",
        "fonctionnalites": [
            "Présentation des menus",
            "Demande de devis",
            "Galerie photos",
            "Google Maps",
            "Contact"
        ]
    },

    "photographe": {
        "intro": "Exposez votre portfolio et facilitez la prise de rendez-vous grâce à un site internet professionnel.",
        "fonctionnalites": [
            "Portfolio",
            "Galerie photos",
            "Réservation",
            "Contact",
            "Avis clients"
        ]
    },

    "architecte": {
        "intro": "Présentez vos réalisations, vos domaines d'expertise et permettez à vos futurs clients de découvrir votre savoir-faire grâce à un site internet professionnel.",
        "fonctionnalites": [
            "Présentation des projets",
            "Galerie photos",
            "Formulaire de contact",
            "Google Maps",
            "Avis clients"
        ]
    },

    "notaire": {
        "intro": "Présentez votre étude, vos domaines d'intervention et facilitez la prise de rendez-vous avec un site internet professionnel.",
        "fonctionnalites": [
            "Présentation des services",
            "Prise de rendez-vous",
            "Formulaire sécurisé",
            "Google Maps",
            "Informations pratiques"
        ]
    },

    "expert-comptable": {
        "intro": "Développez votre visibilité et présentez vos missions grâce à un site internet clair, moderne et rassurant.",
        "fonctionnalites": [
            "Présentation des prestations",
            "Prise de rendez-vous",
            "Formulaire de contact",
            "Google Maps",
            "Espace client"
        ]
    },

    "médecin": {
        "intro": "Informez vos patients et simplifiez la prise de rendez-vous grâce à un site internet professionnel adapté à votre cabinet.",
        "fonctionnalites": [
            "Présentation du cabinet",
            "Prise de rendez-vous",
            "Informations pratiques",
            "Google Maps",
            "Contact"
        ]
    },

    "dentiste": {
        "intro": "Présentez votre cabinet, vos soins et facilitez la prise de rendez-vous avec un site internet moderne.",
        "fonctionnalites": [
            "Présentation des soins",
            "Prise de rendez-vous",
            "Informations pratiques",
            "Google Maps",
            "Contact"
        ]
    },

    "kinésithérapeute": {
        "intro": "Présentez votre cabinet, vos spécialités et simplifiez la prise de rendez-vous grâce à un site internet professionnel.",
        "fonctionnalites": [
            "Présentation des soins",
            "Prise de rendez-vous",
            "Informations pratiques",
            "Google Maps",
            "Contact"
        ]
    },

    "psychologue": {
        "intro": "Présentez votre approche thérapeutique et permettez à vos futurs patients de vous contacter en toute simplicité.",
        "fonctionnalites": [
            "Présentation du cabinet",
            "Prise de rendez-vous",
            "Formulaire de contact",
            "Google Maps",
            "Informations pratiques"
        ]
    },

    "coach sportif": {
        "intro": "Développez votre clientèle grâce à un site internet mettant en avant vos accompagnements, vos programmes et vos résultats.",
        "fonctionnalites": [
            "Présentation des programmes",
            "Réservation",
            "Galerie photos",
            "Avis clients",
            "Contact"
        ]
    },

    "agent immobilier": {
        "intro": "Présentez vos biens immobiliers et facilitez les demandes de renseignements grâce à un site internet moderne.",
        "fonctionnalites": [
            "Présentation des biens",
            "Formulaire de contact",
            "Google Maps",
            "Galerie photos",
            "Avis clients"
        ]
    },

    "artisan": {
        "intro": "Valorisez votre savoir-faire et présentez vos prestations grâce à un site internet professionnel adapté à votre activité.",
        "fonctionnalites": [
            "Présentation des prestations",
            "Demande de devis",
            "Galerie photos",
            "Google Maps",
            "Contact"
        ]
    },

    "entreprise": {
        "intro": "Renforcez votre présence en ligne avec un site internet professionnel qui présente votre entreprise, vos services et vos valeurs.",
        "fonctionnalites": [
            "Présentation de l'entreprise",
            "Présentation des services",
            "Formulaire de contact",
            "Google Maps",
            "Avis clients"
        ]
    }

}    

SEO_PAGES = {}

for metier in METIERS:

    slug = (
        "creation-site-"
        + metier.lower()
        .replace(" ", "-")
        .replace("é", "e")
        .replace("è", "e")
        .replace("ê", "e")
        .replace("à", "a")
        .replace("ç", "c")
        .replace("î", "i")
        .replace("ï", "i")
        .replace("ô", "o")
        .replace("ù", "u")
        .replace("û", "u")
        .replace("'", "-")
    )

    SEO_PAGES[slug] = creer_page(metier)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/realisations")
def parcours():
    return render_template("realisations.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/panier")
def panier():

    panier = session.get("panier", [])

    articles = []
    total = 0

    for produit in panier:
        if produit in PRIX:
            nom, prix = PRIX[produit]
            articles.append({
                "code": produit,
                "nom": nom,
                "prix": prix
            })
            total += prix

    return render_template(
        "panier.html",
        articles=articles,
        total=total
    )


@app.route("/ajouter/<produit>")
def ajouter(produit):

    panier = session.get("panier", [])
    panier.append(produit)

    session["panier"] = panier

    return redirect("/panier")


@app.route("/supprimer/<produit>")
def supprimer(produit):

    panier = session.get("panier", [])

    if produit in panier:
        panier.remove(produit)

    session["panier"] = panier

    return redirect("/panier")
    
@app.route("/payer")
def payer():

    panier = session.get("panier", [])

    total = 0

    for produit in panier:
        if produit in PRIX:
            total += PRIX[produit][1]
            

    if total == 0:
        return redirect("/panier")

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": "Commande M.S Édit"
                    },
                    "unit_amount": int(total * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="https://services-aux-ecrivains.onrender.com/success",
        cancel_url="https://services-aux-ecrivains.onrender.com/panier",
    )

    return redirect(checkout_session.url, code=303)


@app.route("/success")
def success():

    session["panier"] = []

    return """
    <h1>Paiement réussi</h1>
    <p>Merci pour votre commande.</p>
    <a href='/'>Retour à l'accueil</a>
    """

@app.route("/<slug>")
def seo(slug):

    if slug not in SEO_PAGES:
        return "Page introuvable", 404

    return render_template(
        "seo.html",
        page=SEO_PAGES[slug]
    )

@app.route("/sitemap.xml")
def sitemap():

    base_url = "https://studio-web-applications.onrender.com"

    pages = [

        "",

        "/services",

        "/realisations",

        "/contact",

    ]

    for slug in SEO_PAGES:

        pages.append("/" + slug)

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'

    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for page in pages:

        xml += "  <url>\n"

        xml += f"    <loc>{base_url}{page}</loc>\n"

        xml += "  </url>\n"

    xml += "</urlset>"

    return Response(xml, mimetype="application/xml")

@app.route("/robots.txt")
def robots():

    robots_txt = """User-agent: *
Allow: /

Sitemap: https://studio-web-applications.onrender.com/sitemap.xml
"""

    return Response(robots_txt, mimetype="text/plain")
    

if __name__ == "__main__":
    app.run(debug=True)
