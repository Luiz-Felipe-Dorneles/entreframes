"""
Notas do IMDb.

O IMDb não tem uma API gratuita, mas publica todo dia um arquivo com a nota
e o número de votos de TODOS os títulos: https://datasets.imdbws.com/
(uso pessoal e não comercial).

Como o arquivo é grande, não dá para baixá-lo a cada visita. Então:
  1. baixamos o arquivo e guardamos só as notas dos nossos filmes em
     dados/notas_imdb.json (isso é o "cache");
  2. o site lê as notas desse cache;
  3. quando o cache tem mais de 1 dia, baixamos de novo em segundo plano
     (numa "thread"), para o site não ficar travado esperando o download.

Para forçar a atualização na mão:  python imdb.py
"""

import gzip
import io
import json
import os
import threading
import urllib.request
from datetime import datetime, timedelta

URL_NOTAS = "https://datasets.imdbws.com/title.ratings.tsv.gz"
PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CACHE = os.path.join(PASTA, "dados", "notas_imdb.json")
VALIDADE_CACHE = timedelta(days=1)

# Estado do módulo (variáveis "globais" que as funções abaixo usam)
cache = {"atualizado_em": None, "notas": {}}   # o que está no JSON
atualizando = False   # True enquanto um download está rodando (evita baixar 2x)
ultimo_erro = None    # mensagem do último erro de download (ou None)


def ler_cache():
    """Carrega o JSON salvo no disco. Se não existir ou estiver quebrado, ignora."""
    global cache
    try:
        with open(ARQUIVO_CACHE, encoding="utf-8") as arquivo:
            cache = json.load(arquivo)
    except (OSError, ValueError):
        pass  # sem cache: o site mostra "nota indisponível" até o download terminar


def cache_vencido():
    """True se o cache não existe ou tem mais de 1 dia."""
    if not cache.get("atualizado_em"):
        return True
    atualizado = datetime.fromisoformat(cache["atualizado_em"])
    return datetime.now() - atualizado > VALIDADE_CACHE


def baixar_notas(ids_imdb):
    """Baixa o arquivo do IMDb e devolve só as notas dos filmes pedidos.

    Retorno: {"tt0371746": {"nota": 7.9, "votos": 1200000}, ...}
    """
    pedido = urllib.request.Request(URL_NOTAS, headers={"User-Agent": "EntreFrames/1.0"})
    procurados = set(ids_imdb)  # set: procurar nele é muito mais rápido que numa lista
    notas = {}
    with urllib.request.urlopen(pedido, timeout=60) as resposta:
        # O arquivo vem compactado (.gz). Lemos linha por linha, descompactando
        # aos poucos, sem precisar guardar o arquivo inteiro na memória.
        texto = io.TextIOWrapper(gzip.GzipFile(fileobj=resposta), encoding="utf-8")
        for linha in texto:
            # Cada linha tem 3 colunas separadas por TAB: id, nota e votos
            colunas = linha.strip().split("\t")
            if colunas[0] in procurados:
                notas[colunas[0]] = {"nota": float(colunas[1]), "votos": int(colunas[2])}
                if len(notas) == len(procurados):
                    break  # já achamos todos, não precisa ler o resto
    return notas


def salvar_cache(dados):
    """Grava o JSON de forma segura.

    Primeiro escreve num arquivo temporário e só depois troca pelo verdadeiro.
    Assim, se o programa fechar no meio da gravação, o cache antigo continua inteiro.
    """
    os.makedirs(os.path.dirname(ARQUIVO_CACHE), exist_ok=True)
    temporario = ARQUIVO_CACHE + ".tmp"
    with open(temporario, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
    os.replace(temporario, ARQUIVO_CACHE)


def atualizar(ids_imdb):
    """Baixa as notas novas. Se der erro (ex.: sem internet), mantém as antigas."""
    global cache, atualizando, ultimo_erro
    try:
        notas = baixar_notas(ids_imdb)
        dados = {"atualizado_em": datetime.now().isoformat(timespec="seconds"), "notas": notas}
        salvar_cache(dados)
        cache = dados
        ultimo_erro = None
        print(f"[IMDb] {len(notas)} notas atualizadas.")
    except Exception as erro:  # sem internet, site do IMDb fora do ar, etc.
        ultimo_erro = str(erro)
        print(f"[IMDb] Não foi possível atualizar as notas: {erro}")
    finally:
        atualizando = False  # "finally" roda sempre, com ou sem erro


def atualizar_se_preciso(ids_imdb):
    """Se o cache venceu, começa um download em segundo plano.

    É chamada a cada visita (pelo app.py), então funciona mesmo que o
    servidor fique ligado vários dias seguidos.
    """
    global atualizando
    if atualizando or not cache_vencido():
        return
    if ultimo_erro and cache.get("notas"):
        # Já falhou antes e temos notas antigas: não tenta de novo a cada visita.
        # (Reinicie o servidor ou rode "python imdb.py" para tentar outra vez.)
        return
    atualizando = True
    # daemon=True: a thread não impede o servidor de fechar com Ctrl + C
    threading.Thread(target=atualizar, args=(list(ids_imdb),), daemon=True).start()


def nota(id_imdb):
    """Devolve {"nota": ..., "votos": ...} de um filme, ou None se não tiver."""
    return cache["notas"].get(id_imdb)


# Lê o cache assim que o módulo é importado
ler_cache()


if __name__ == "__main__":
    # "python imdb.py" atualiza as notas na hora (sem thread) e mostra o resultado
    from filmes import FILMES

    atualizar([filme["imdb"] for filme in FILMES])
    print(json.dumps(cache, ensure_ascii=False, indent=2))
