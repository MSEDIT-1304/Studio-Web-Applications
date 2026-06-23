from flask import Flask, render_template, request, redirect, session
import stripe
import os

app = Flask(__name__)
app.secret_key = "msedit_panier_2026"
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

PRIX = {
    "correction150": ("Correction littéraire 150 pages", 150),
    "correction220": ("Correction littéraire 250 pages", 220),
    "correction300": ("Correction littéraire 400 pages", 300),
    "correction420": ("Correction littéraire 500 pages", 420),

    "couv80": ("Couverture seule Standard", 80),
    "couv120": ("Couverture + 4e de couverture", 120),
    "couv170": ("Couverture + 4e + résumé", 170),

    "premium160": ("Couverture Premium seule", 160),
    "premium200": ("Couverture Premium + 4e", 200),
    "premium250": ("Couverture Premium + 4e + résumé", 250),

    "site550": ("Site vitrine Essentiel", 550),
    "site750": ("Site vitrine Premium", 750)
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/parcours")
def parcours():
    return render_template("parcours.html")


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

if __name__ == "__main__":
    app.run(debug=True)
