import os, csv, requests
from flask import Flask, request

app = Flask(__name__)

# ---- Listing Template ----
def build_template(title, description, price, condition, compatibility):
    return f"""
    {title}
    Genuine Auto Parts – Fast Shipping

    Condition: {condition}
    Price: ${price}

    Compatibility:
    {compatibility}

    {description}

    📦 Free returns within 30 days
    🚀 Fast shipping with tracking
    """

# ---- Auto-fitment lookup ----
def get_fitment(part_number):
    app_id = os.getenv("EBAY_APP_ID")
    url = f"https://api.sandbox.ebay.com/commerce/parts_compatibility/v1/part_number/{part_number}"
    headers = {"Authorization": f"Bearer {os.getenv('EBAY_TOKEN')}"}
    try:
        resp = requests.get(url, headers=headers)
        data = resp.json()
        vehicles = [f"{v['make']} {v['model']} {v['year']}" for v in data.get("compatibilities",[])]
        return "\n".join(vehicles) if vehicles else "See description for compatibility"
    except Exception as e:
        return f"Fitment lookup failed: {e}"

# ---- Routes ----
@app.route("/")
def index():
    return """
    <h2>Single Listing Form</h2>
    <form action="/single_listing" method="post">
      Part Number: <input type="text" name="part_number"><br>
      Title: <input type="text" name="title"><br>
      Price: <input type="text" name="price"><br>
      <input type="submit" value="Submit">
    </form>

    <h2>Bulk Upload</h2>
    <form action="/bulk_upload" method="post" enctype="multipart/form-data">
      CSV File: <input type="file" name="csv_file"><br>
      <input type="submit" value="Upload CSV">
    </form>
    """

@app.route("/single_listing", methods=["POST"])
def single_listing():
    part_number = request.form["part_number"]
    title = request.form["title"]
    price = request.form["price"]

    compatibility = get_fitment(part_number)
    description = build_template(title, "Auto part listing", price, "New", compatibility)

    return f"Submitted listing: {title} (Part #{part_number}) for ${price}<br><pre>{description}</pre>"

@app.route("/bulk_upload", methods=["POST"])
def bulk_upload():
    file = request.files["csv_file"]
    reader = csv.DictReader(file.stream.read().decode("utf-8").splitlines())
    listings = []
    for row in reader:
        part_number = row.get("part_number")
        title = row.get("title")
        price = row.get("price")
        compatibility = get_fitment(part_number)
        description = build_template(title, "Bulk auto part", price, "New", compatibility)
        listings.append(f"{title} (#{part_number}) for ${price}\n{description}")
    return "<h3>Bulk Upload Complete</h3><pre>" + "\n\n".join(listings) + "</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
