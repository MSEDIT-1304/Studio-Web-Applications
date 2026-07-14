from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def accueil():
    return render_template("accueil.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/regions")
def regions():
    return render_template("regions.html")

@app.route("/photos")
def photos():
    return render_template("photos.html")

if __name__ == "__main__":
    app.run(debug=True)
