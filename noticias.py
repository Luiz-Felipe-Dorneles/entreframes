"""
Notícias de cinema (ao vivo, via RSS).

RSS é um formato em XML que muitos sites publicam com as suas últimas notícias.
Usamos o RSS de busca do Google Notícias, que junta manchetes de vários sites
brasileiros de cinema num único arquivo.

Funciona igual às notas do IMDb (imdb.py):
  1. baixamos o RSS e guardamos as manchetes em dados/noticias.json (o "cache");
  2. o site lê as notícias desse cache;
  3. quando o cache tem mais de 3 horas, baixamos de novo em segundo plano.

Para forçar a atualização na mão:  python noticias.py
"""

import json
import os
import threading
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime

# "q" é o que buscamos; hl/gl/ceid pedem notícias em português do Brasil
URL_RSS = ("https://news.google.com/rss/search"
           "?q=cinema+filmes+estreia&hl=pt-BR&gl=BR&ceid=BR:pt-419")
PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CACHE = os.path.join(PASTA, "dados", "noticias.json")
VALIDADE_CACHE = timedelta(hours=3)
MAXIMO = 18  # quantas notícias guardar

cache = {"atualizado_em": None, "noticias": []}
atualizando = False
ultimo_erro = None


def ler_cache():
    """Carrega o JSON salvo no disco. Se não existir ou estiver quebrado, ignora."""
    global cache
    try:
        with open(ARQUIVO_CACHE, encoding="utf-8") as arquivo:
            cache = json.load(arquivo)
    except (OSError, ValueError):
        pass


def cache_vencido():
    if not cache.get("atualizado_em"):
        return True
    atualizado = datetime.fromisoformat(cache["atualizado_em"])
    return datetime.now() - atualizado > VALIDADE_CACHE


def ler_rss(xml_texto):
    """Transforma o texto XML do RSS numa lista de notícias.

    Cada notícia no RSS fica dentro de uma tag <item>, assim:
        <item>
          <title>Manchete - Nome do site</title>
          <link>https://...</link>
          <pubDate>Tue, 28 Oct 2026 14:00:00 GMT</pubDate>
          <source>Nome do site</source>
        </item>
    """
    raiz = ET.fromstring(xml_texto)
    noticias = []
    for item in raiz.iter("item"):  # percorre todas as tags <item>
        titulo = item.findtext("title", "").strip()
        fonte = item.findtext("source", "").strip()
        # O Google coloca " - Nome do site" no fim do título; tiramos para não repetir
        if fonte and titulo.endswith(" - " + fonte):
            titulo = titulo[: -len(" - " + fonte)]

        data = item.findtext("pubDate")
        try:
            data = parsedate_to_datetime(data).strftime("%d/%m/%Y")
        except (TypeError, ValueError):
            data = ""

        noticias.append({
            "titulo": titulo,
            "link": item.findtext("link", "").strip(),
            "fonte": fonte,
            "data": data,
        })
        if len(noticias) == MAXIMO:
            break
    return noticias


def baixar_noticias():
    pedido = urllib.request.Request(URL_RSS, headers={"User-Agent": "EntreFrames/1.0"})
    with urllib.request.urlopen(pedido, timeout=20) as resposta:
        return ler_rss(resposta.read())


def salvar_cache(dados):
    """Grava num arquivo temporário e depois troca (para nunca corromper o JSON)."""
    os.makedirs(os.path.dirname(ARQUIVO_CACHE), exist_ok=True)
    temporario = ARQUIVO_CACHE + ".tmp"
    with open(temporario, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
    os.replace(temporario, ARQUIVO_CACHE)


def atualizar():
    """Baixa as notícias novas. Se der erro (ex.: sem internet), mantém as antigas."""
    global cache, atualizando, ultimo_erro
    try:
        noticias = baixar_noticias()
        dados = {"atualizado_em": datetime.now().isoformat(timespec="seconds"), "noticias": noticias}
        salvar_cache(dados)
        cache = dados
        ultimo_erro = None
        print(f"[Notícias] {len(noticias)} notícias atualizadas.")
    except Exception as erro:
        ultimo_erro = str(erro)
        print(f"[Notícias] Não foi possível atualizar: {erro}")
    finally:
        atualizando = False


def atualizar_se_preciso():
    """Se o cache venceu, começa um download em segundo plano (sem travar o site)."""
    global atualizando
    if atualizando or not cache_vencido():
        return
    if ultimo_erro and cache.get("noticias"):
        return  # já falhou e temos notícias antigas: não tenta a cada visita
    atualizando = True
    threading.Thread(target=atualizar, daemon=True).start()


ler_cache()


if __name__ == "__main__":
    atualizar()
    for noticia in cache["noticias"]:
        print(f"- {noticia['data']}  {noticia['titulo']}  ({noticia['fonte']})")
