"""
Baixa os pôsteres dos filmes para static/img/posteres/.

Os pôsteres vêm da Wikipédia (API pública "page/summary"). Eles ficam salvos
na pasta do projeto, então o site não depende de links externos para as imagens.
Rode só uma vez (ou quando adicionar um filme novo):

    python baixar_posteres.py
"""

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

from filmes import FILMES

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "img", "posteres")
CABECALHO = {"User-Agent": "PortalCine/1.0 (trabalho escolar de front-end)"}


def baixar(url, tentativas=4):
    pedido = urllib.request.Request(url, headers=CABECALHO)
    for tentativa in range(tentativas):
        try:
            with urllib.request.urlopen(pedido, timeout=30) as resposta:
                return resposta.read()
        except urllib.error.HTTPError as erro:
            # 429 = muitos pedidos seguidos: espera um pouco e tenta de novo
            if erro.code != 429 or tentativa == tentativas - 1:
                raise
            time.sleep(5 * (tentativa + 1))


def url_do_poster(idioma, pagina):
    endereco = (f"https://{idioma}.wikipedia.org/api/rest_v1/page/summary/"
                + urllib.parse.quote(pagina, safe=""))
    resumo = json.loads(baixar(endereco))
    imagem = resumo.get("originalimage") or resumo.get("thumbnail")
    return imagem["source"] if imagem else None


def main():
    os.makedirs(PASTA, exist_ok=True)
    for filme in FILMES:
        destino = os.path.join(PASTA, f"{filme['slug']}.jpg")
        if os.path.exists(destino) and os.path.getsize(destino) > 0:
            print(f"ok   {filme['titulo']} (já existe)")
            continue
        try:
            url = url_do_poster(*filme["wiki"])
            if not url:
                print(f"--   {filme['titulo']}: a página não tem imagem")
                continue
            imagem = baixar(url)  # baixa tudo antes de criar o arquivo
            with open(destino, "wb") as arquivo:
                arquivo.write(imagem)
            print(f"novo {filme['titulo']}")
        except Exception as erro:
            print(f"ERRO {filme['titulo']}: {erro}")
        time.sleep(1.5)  # educação com a Wikipédia: um pedido de cada vez


if __name__ == "__main__":
    main()
