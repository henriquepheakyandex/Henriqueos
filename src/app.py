from flask import Flask, jsonify
from src.routes.tasks import tasks_bp
from src.routes.products import product_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(product_bp)
app.register_blueprint(tasks_bp)

@app.route('/')
def index():
    return jsonify({"message": "Task Management API"})

if __name__ == '__main__':
    app.run(debug=True)
