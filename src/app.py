from flask import Flask, render_template, request
import sys
sys.path.append("src")

from PhishScan import verificar_assunto, verificar_links

app = Flask(__name__, template_folder="../templates")

palavras_suspeitas = ["urgente", "bloqueada", "clique aqui", "acesse agora", "parabens", "voce ganhou", "premio"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analisar", methods=["POST"])
def analisar():
    email_texto = request.form["email_texto"]

    linhas = email_texto.split("\n")
    remetente = ""
    for linha in linhas:
        if linha.lower().startswith("from:"):
            remetente = linha[5:].strip()

    resultado_assunto = verificar_assunto(email_texto, palavras_suspeitas)
    resultado_corpo = verificar_assunto(email_texto, palavras_suspeitas)

    links_encontrados = verificar_links(email_texto)
    links_suspeitos = []
    for link in links_encontrados:
        if ".xyz" in link or ".tk" in link or ".click" in link:
            links_suspeitos.append(link)

    dominio_suspeito = False
    if "@" in remetente:
        dominio = remetente.split("@")[1]
        for tld in [".xyz", ".top", ".click", ".tk"]:
            if dominio.endswith(tld):
                dominio_suspeito = True

    pontuacao = 0
    if dominio_suspeito:
        pontuacao += 10
    pontuacao += len(resultado_assunto) * 5
    pontuacao += len(links_suspeitos) * 10

    if pontuacao >= 20:
        risco = "ALTO"
    elif pontuacao >= 10:
        risco = "MEDIO"
    else:
        risco = "BAIXO"

    return render_template("resultado.html",
        remetente=remetente,
        resultado_assunto=resultado_assunto,
        resultado_corpo=resultado_corpo,
        links_suspeitos=links_suspeitos,
        pontuacao=pontuacao,
        risco=risco
    )

if __name__ == "__main__":
    app.run(debug=True)