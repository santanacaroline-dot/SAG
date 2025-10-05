from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)  # permite acesso do navegador

# 🔑 Coloque sua chave da OpenAI aqui
openai.api_key = "SUA_CHAVE_DA_OPENAI_AQUI"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Texto vazio"}), 400

    prompt = f"""
    Você é um analista jurídico especializado em pareceres do CARF.
    Analise o seguinte texto de parecer e produza:
    - Um resumo técnico;
    - Pontos fortes e fracos;
    - Sugestões de melhoria;
    - Uma conclusão geral.

    Texto do parecer:
    {text}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # você pode usar gpt-4o ou gpt-3.5-turbo
            messages=[{"role": "system", "content": "Você é um especialista jurídico."},
                      {"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.7
        )
        analysis = response.choices[0].message["content"]
        return jsonify({"analysis": analysis})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
