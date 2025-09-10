from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/get_data", methods=["POST"])
def get_data():
    data = request.json
    channel_id = data.get("channel_id")
    api_key = data.get("api_key")
    results = data.get("results", 20)

    if not channel_id:
        return jsonify({"error": "Channel ID é obrigatório"}), 400

    # Monta a URL da API
    if api_key:
        url = f"https://api.thingspeak.com/channels/2943258/feeds.json?api_key=G3BDQS6I5PRGFEWR&results=20"
    else:
        url = f"https://api.thingspeak.com/channels/2943258/feeds.json?results=20"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        feeds = data.get("feeds", [])
        channel_info = data.get("channel", {})

        if not feeds:
            return jsonify({"error": "Nenhum dado encontrado."}), 404

        # Pega todos os fields dinamicamente
        fields = {k: v for k, v in channel_info.items() if k.startswith("field") and v}

        labels = [f["created_at"] for f in feeds]

        values = {}
        for key, field_name in fields.items():
            values[field_name] = [f.get(key) for f in feeds]

        return jsonify({"labels": labels, "values": values})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
    #nsdw
