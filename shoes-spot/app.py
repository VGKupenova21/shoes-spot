from flask import Flask, render_template
from controllers.auth_controller import auth_bp
from controllers.catalog_controller import catalog_bp
from controllers.cart_controller import cart_bp
app = Flask(__name__)
app.secret_key = "supersecretkey"

app.register_blueprint(auth_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(catalog_bp)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
