from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Simple homepage with single listing form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        part_number = request.form.get("part_number")
        title = request.form.get("title")
        price = request.form.get("price")
        return f"Submitted listing: {title} (Part #{part_number}) for ${price}"
    return render_template_string("""
        <h1>Single Listing Form</h1>
        <form method="post">
            Part Number: <input type="text" name="part_number"><br>
            Title: <input type="text" name="title"><br>
            Price: <input type="text" name="price"><br>
            <button type="submit">Submit</button>
        </form>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
