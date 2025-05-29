import os
from flask import Flask, render_template, request, redirect
from scraper import scrape_amazon

app = Flask(__name__)

# Cache the products using a global variable
cached_products = []

@app.route("/", methods=["GET", "POST"])
def index():
    global cached_products
    if request.method == "POST":
        search_term = request.form.get("search_term")
        cached_products = scrape_amazon(search_term)
        return render_template("results.html", products=cached_products)
    return render_template("results.html", products=[])

@app.route("/sort", methods=["POST"])
def sort():
    global cached_products
    sort_by = request.form.get("sort_by")
    if not cached_products:
        return redirect("/")  # fallback if no products

    def price_to_int(p):
        try:
            return int(p.replace(",", "").split()[0])
        except:
            return float("inf")

    def rating_to_float(r):
        try:
            return float(r.split()[0])
        except:
            return 0

    if sort_by == "name":
        cached_products.sort(key=lambda x: x['name'].lower())
    elif sort_by == "price":
        cached_products.sort(key=lambda x: price_to_int(x['price']))
    elif sort_by == "rating":
        cached_products.sort(key=lambda x: rating_to_float(x['rating']), reverse=True)

    return render_template("results.html", products=cached_products)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)