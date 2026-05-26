from datetime import datetime
import os

# ================================
# PhishScan - Analisador de Phishing
# Autor: Samuel Caldeira
# Versao: 1.0
# ================================

def verificar_assunto(assunto, palavras_suspeitas):
    alertas = []
    assunto = assunto.lower()
    for palavra in palavras_suspeitas:
        if palavra in assunto:
            alertas.append(palavra)
    return alertas

def ler_email(caminho):
    import email
    arquivo = open(caminho, "r", encoding="utf-8")
    conteudo = arquivo.read()
    arquivo.close()
    msg = email.message_from_string(conteudo)
    remetente = msg["From"]
    assunto = msg["Subject"]
    corpo = msg.get_payload()
    return remetente, assunto, corpo

def verificar_links(corpo):
    links = []
    palavras = corpo.split()
    for palavra in palavras:
        if palavra.startswith("http"):
            links.append(palavra)
    return links

def listar_emails():
    arquivos = os.listdir("samples")
    emails = []
    for arquivo in arquivos:
        if arquivo.endswith(".eml"):
            emails.append(arquivo)
    return emails

if __name__ == "__main__":
    palavras_suspeitas = ["urgente", "bloqueada", "clique aqui", "acesse agora", "parabens", "voce ganhou", "premio"]

    emails_disponiveis = listar_emails()

    print("\n=== EMAILS DISPONIVEIS ===")
    for i, email in enumerate(emails_disponiveis):
        print(i + 1, "-", email)

    escolha = int(input("\nEscolha o numero do email: "))
    caminho = "samples/" + emails_disponiveis[escolha - 1]
    remetente, assunto, corpo = ler_email(caminho)

    print("=== EMAIL LIDO DO ARQUIVO ===")
    print("Remetente:", remetente)
    print("Assunto:", assunto)
    print("Corpo:", corpo)

    links_encontrados = verificar_links(corpo)
    if len(links_encontrados) > 0:
        print("Links encontrados no email:", links_encontrados)
        for link in links_encontrados:
            if ".xyz" in link or ".tk" in link or ".click" in link:
                print("ALERTA - Link suspeito:", link)
    else:
        print("Nenhum link encontrado")

    resultado_assunto = verificar_assunto(assunto, palavras_suspeitas)
    resultado_corpo = verificar_assunto(corpo, palavras_suspeitas)

    if len(resultado_assunto) > 0:
        print("Palavras suspeitas no assunto:", resultado_assunto)
    if len(resultado_corpo) > 0:
        print("Palavras suspeitas no corpo:", resultado_corpo)

    dominio = remetente.split("@")[1]
    dominios_suspeitos = [".xyz", ".top", ".click", ".tk"]
    dominio_suspeito = False

    for tld in dominios_suspeitos:
        if dominio.endswith(tld):
            print("ALERTA - Dominio suspeito:", dominio)
            dominio_suspeito = True

    pontuacao = 0
    if dominio_suspeito:
        pontuacao = pontuacao + 10
    pontuacao = pontuacao + (len(resultado_assunto) * 5)
    pontuacao = pontuacao + (len(resultado_corpo) * 5)

    print("Pontuacao total:", pontuacao)

    if pontuacao >= 20:
        risco = "ALTO"
    elif pontuacao >= 10:
        risco = "MEDIO"
    else:
        risco = "BAIXO"

    print("RISCO:", risco)

    arquivo = open("reports/relatorio.txt", "w")
    arquivo.write("=== RELATORIO DE ANALISE ===\n")
    arquivo.write("Data: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
    arquivo.write("Remetente: " + remetente + "\n")
    arquivo.write("Assunto: " + assunto + "\n")
    arquivo.write("Palavras suspeitas no assunto: " + str(resultado_assunto) + "\n")
    arquivo.write("Palavras suspeitas no corpo: " + str(resultado_corpo) + "\n")
    arquivo.write("Pontuacao: " + str(pontuacao) + "\n")
    arquivo.write("Risco: " + risco + "\n")
    arquivo.close()

    print("Relatorio salvo em reports/relatorio.txt")