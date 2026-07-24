from flask import Flask, render_template, request, redirect, session
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

SEO_PAGES = {

    "creation-site-plombier": {

        "title": "Création de site internet pour plombier",

        "meta_description": "Création de site internet professionnel pour plombier avec référencement Google, paiement en ligne, formulaire de devis et réservation.",

        "keywords": "site internet plombier, création site plombier, plombier, référencement",

        "h1": "Création de site internet pour plombier",

        "slogan": "Développez votre activité grâce à un site internet professionnel.",

        "introduction": "Studio Web & Applications développe des sites internet modernes destinés aux plombiers souhaitant améliorer leur visibilité et trouver de nouveaux clients.",

        "texte": "Chaque site est entièrement personnalisé selon votre activité. Il peut intégrer un formulaire de devis, un paiement en ligne, une galerie de réalisations, Google Maps, des avis clients et bien d'autres fonctionnalités.",

        "faq": [

            {
                "question": "Combien coûte un site internet pour plombier ?",
                "reponse": "Le tarif dépend des fonctionnalités souhaitées. Consultez la page Services pour découvrir nos offres."
            },

            {
                "question": "Puis-je accepter les paiements en ligne ?",
                "reponse": "Oui. Nous pouvons intégrer Stripe et d'autres solutions de paiement sécurisées."
            }

        ],

        "liens": [

            {
                "nom": "Création de site internet avec paiement en ligne",
                "url": "/creation-site-paiement-en-ligne"
            },

            {
                "nom": "Création de site internet en France",
                "url": "/creation-site-france"
            }

        ]

    }

}


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

if __name__ == "__main__":
    app.run(debug=True)
