"""
EntreFrames — portal de filmes com modelos 3D interativos.

Para rodar:
    pip install -r requirements.txt
    python app.py
e abra http://127.0.0.1:5000 no navegador.
"""

import os
import random
import unicodedata
import urllib.parse
from datetime import datetime

from flask import Flask, abort, render_template, request, url_for
from markupsafe import Markup, escape

import aula
import imdb
import noticias
from filmes import FILMES, FILMES_POR_SLUG, LICENCAS, MARCAS, PLATAFORMAS

app = Flask(__name__)

# Opções do <select> "Ordenar por": chave que vai na URL -> texto que aparece
ORDENS = {
    "nota": "Maior nota",
    "ano": "Mais recentes",
    "titulo": "Título (A-Z)",
}


# Lojas onde dá para alugar ou comprar filmes digitais.
# O {} é trocado pelo nome do filme (já preparado para ir numa URL).
LOJAS = [
    ("Apple TV", "https://tv.apple.com/br/search?term={}"),
    ("Google Play", "https://play.google.com/store/search?q={}&c=movies"),
    ("Prime Video", "https://www.primevideo.com/search?phrase={}"),
]


# ---------------------------------------------------------------------
# Funções auxiliares
# ---------------------------------------------------------------------

def sem_acento(texto):
    """Deixa o texto minúsculo e sem acentos: 'Anéis' -> 'aneis'.

    Assim a busca acha "Senhor dos Anéis" mesmo se a pessoa digitar "aneis".
    O NFD separa a letra do acento ('é' vira 'e' + '´') e depois
    jogamos fora os acentos (categoria "Mn").
    """
    separado = unicodedata.normalize("NFD", texto.lower())
    return "".join(letra for letra in separado if unicodedata.category(letra) != "Mn")


def formatar_votos(votos):
    """1595476 -> '1,6 mi'   |   25300 -> '25 mil'   |   800 -> '800'"""
    if votos >= 1_000_000:
        return f"{votos / 1_000_000:.1f} mi".replace(".", ",")
    if votos >= 1_000:
        return f"{votos // 1_000} mil"
    return str(votos)


def endereco_poster(filme):
    """Link do pôster do filme, ou None se o arquivo .jpg não existir."""
    caminho = os.path.join(app.static_folder, "img", "posteres", f"{filme['slug']}.jpg")
    if os.path.exists(caminho):
        return url_for("static", filename=f"img/posteres/{filme['slug']}.jpg")
    return None


def montar(filme):
    """Junta os dados fixos do filme (filmes.py) com o que é calculado na hora:
    nota do IMDb, link do pôster e links do IMDb e do Sketchfab.

    Devolve um dicionário NOVO; o original em filmes.py não é alterado.
    """
    nota = imdb.nota(filme["imdb"])  # None se ainda não temos a nota
    uid = filme["modelo"]["uid"]
    completo = dict(filme)  # cópia do dicionário
    completo["nota"] = nota["nota"] if nota else None
    completo["votos"] = formatar_votos(nota["votos"]) if nota else None
    completo["marca_nome"] = MARCAS[filme["marca"]]
    completo["poster"] = endereco_poster(filme)
    completo["link_imdb"] = f"https://www.imdb.com/title/{filme['imdb']}/"
    completo["modelo_embed"] = f"https://sketchfab.com/models/{uid}/embed?autostart=1&ui_theme=dark&dnt=1"
    completo["modelo_pagina"] = f"https://sketchfab.com/3d-models/{uid}"
    completo["licenca_link"] = LICENCAS.get(filme["modelo"]["licenca"])

    # Onde assistir. quote() prepara o texto para a URL: "Rei Leão" -> "Rei%20Le%C3%A3o"
    nome_na_url = urllib.parse.quote(filme["titulo"])
    completo["plataforma"] = PLATAFORMAS.get(filme["streaming"])  # None se não tiver
    completo["lojas"] = [(nome, link.format(nome_na_url)) for nome, link in LOJAS]
    # JustWatch: site que mostra em qual plataforma o filme está HOJE
    completo["justwatch"] = f"https://www.justwatch.com/br/busca?q={nome_na_url}"
    return completo


# ---------------------------------------------------------------------
# Coisas que rodam em toda página
# ---------------------------------------------------------------------

@app.before_request
def conferir_notas():
    """Antes de cada visita: se as notas venceram, baixa de novo em segundo plano."""
    imdb.atualizar_se_preciso(filme["imdb"] for filme in FILMES)


@app.context_processor
def dados_globais():
    """Variáveis que ficam disponíveis em TODOS os templates (ex.: no rodapé)."""
    atualizado = imdb.cache.get("atualizado_em")
    if atualizado:
        atualizado = datetime.fromisoformat(atualizado).strftime("%d/%m/%Y às %H:%M")
    return {
        "notas_atualizadas_em": atualizado,
        # Se o download ainda está rodando, a nota "está carregando";
        # se não está, a nota que falta não vai chegar (ex.: sem internet).
        "notas_carregando": imdb.atualizando,
        "ano_atual": datetime.now().year,
    }


# ---------------------------------------------------------------------
# Rotas (cada função responde a um endereço do site)
# ---------------------------------------------------------------------

def mostrar_catalogo(mostrar_intro):
    """Monta a página do catálogo com busca, filtro de marca e ordenação.

    Os filtros chegam pela URL, por exemplo:  /catalogo?q=batman&marca=dc&ordem=ano
    """
    busca = request.args.get("q", "").strip()
    marca = request.args.get("marca", "")
    ordem = request.args.get("ordem", "nota")

    # Valores inválidos na URL (ex.: ?marca=xyz) são ignorados
    if marca not in MARCAS:
        marca = ""
    if ordem not in ORDENS:
        ordem = "nota"

    filmes = [montar(filme) for filme in FILMES]

    # 1. Filtro por marca
    if marca:
        filmes = [f for f in filmes if f["marca"] == marca]

    # 2. Busca: procura o termo no título, título original, diretor e marca
    if busca:
        termo = sem_acento(busca)
        resultado = []
        for f in filmes:
            onde_procurar = f"{f['titulo']} {f['original']} {f['diretor']} {f['marca_nome']}"
            if termo in sem_acento(onde_procurar):
                resultado.append(f)
        filmes = resultado

    # 3. Ordenação
    if ordem == "nota":
        # filme sem nota (None) conta como 0 e vai para o fim
        filmes.sort(key=lambda f: f["nota"] or 0, reverse=True)
    elif ordem == "ano":
        filmes.sort(key=lambda f: f["ano"], reverse=True)
    else:
        filmes.sort(key=lambda f: sem_acento(f["titulo"]))

    # A intro de cinema só aparece em "/" e sem nenhum filtro na URL
    if busca or marca or "ordem" in request.args:
        mostrar_intro = False

    return render_template(
        "index.html",
        filmes=filmes,
        total=len(FILMES),
        busca=busca,
        marca=marca,
        marcas=MARCAS,
        ordem=ordem,
        ordens=ORDENS,
        mostrar_intro=mostrar_intro,
    )


@app.route("/")
def inicio():
    return mostrar_catalogo(mostrar_intro=True)


@app.route("/catalogo")
def catalogo():
    # Mesmo catálogo, mas sem a intro (para não repetir a animação toda hora)
    return mostrar_catalogo(mostrar_intro=False)


@app.route("/filme/<slug>")
def filme(slug):
    if slug not in FILMES_POR_SLUG:
        abort(404)  # chama a função nao_encontrado() lá embaixo

    atual = FILMES_POR_SLUG[slug]
    posicao = FILMES.index(atual)
    # Links "Anterior" e "Próximo". O % faz dar a volta: depois do último vem o primeiro.
    # (FILMES[-1] já é o último da lista, então o "anterior" do primeiro também funciona.)
    anterior = FILMES[posicao - 1]
    proximo = FILMES[(posicao + 1) % len(FILMES)]

    return render_template("filme.html", filme=montar(atual), anterior=anterior, proximo=proximo)


@app.route("/noticias")
def pagina_noticias():
    # Se as notícias têm mais de 3 horas, baixa de novo em segundo plano
    noticias.atualizar_se_preciso()
    atualizado = noticias.cache.get("atualizado_em")
    if atualizado:
        atualizado = datetime.fromisoformat(atualizado).strftime("%d/%m/%Y às %H:%M")
    return render_template(
        "noticias.html",
        noticias=noticias.cache.get("noticias", []),
        atualizado_em=atualizado,
        carregando=noticias.atualizando,
    )


@app.route("/curiosidades")
def curiosidades():
    filmes = [montar(f) for f in FILMES]
    filmes.sort(key=lambda f: sem_acento(f["titulo"]))
    return render_template("curiosidades.html", filmes=filmes)


@app.route("/linha-do-tempo")
def linha_do_tempo():
    """Filmes em ordem de lançamento, agrupados por década."""
    filmes = sorted((montar(f) for f in FILMES), key=lambda f: f["ano"])

    # decadas fica assim: {1970: [Tubarão], 1980: [...], ...}
    decadas = {}
    for f in filmes:
        decada = f["ano"] // 10 * 10   # // é divisão sem resto: 1994 // 10 = 199 → 1990
        if decada not in decadas:
            decadas[decada] = []
        decadas[decada].append(f)

    return render_template("linha_do_tempo.html", decadas=decadas)


@app.route("/onde-assistir")
def onde_assistir():
    """Onde assistir cada filme. Cada filme tem uma âncora (#slug) na página,
    então /onde-assistir#shrek já rola até o Shrek."""
    filmes = [montar(f) for f in FILMES]
    filmes.sort(key=lambda f: sem_acento(f["titulo"]))
    return render_template("onde_assistir.html", filmes=filmes)


@app.route("/roleta")
def roleta():
    """Sorteia um filme. Os filtros chegam pela URL: /roleta?genero=Ação&marca=marvel&girar=1"""
    generos = sorted({g for f in FILMES for g in f["generos"]})  # {} sem repetição = set
    genero = request.args.get("genero", "")
    marca = request.args.get("marca", "")
    if genero not in generos:
        genero = ""
    if marca not in MARCAS:
        marca = ""

    sorteado = None
    carretel = []
    nenhum = False
    if "girar" in request.args:
        # Filmes que combinam com os filtros escolhidos
        candidatos = [f for f in FILMES
                      if (not genero or genero in f["generos"])
                      and (not marca or f["marca"] == marca)]
        if candidatos:
            sorteado = random.choice(candidatos)
            # "Carretel" da animação: alguns filmes aleatórios passando
            # e o sorteado por último (é nele que a roleta para)
            carretel = random.sample(FILMES, 7) + [sorteado]
            carretel = [montar(f) for f in carretel]
            sorteado = carretel[-1]
        else:
            nenhum = True

    return render_template("roleta.html", generos=generos, genero=genero,
                           marcas=MARCAS, marca=marca,
                           sorteado=sorteado, carretel=carretel, nenhum=nenhum)


# ---------------------------------------------------------------------
# Modo Aula (a lousa verde)
# ---------------------------------------------------------------------

@app.template_filter("comentarios")
def destacar_comentarios(codigo):
    """Pinta os comentários do código da lousa com outra cor.

    Coloca cada comentário (# ..., /* ... */ ou <!-- ... -->) dentro de um
    <span class="lousa__comentario">. Uso no template: {{ etapa.codigo|comentarios }}
    """
    linhas = []
    dentro = None  # fim do comentário de várias linhas que está aberto ("*/" ou "-->")
    for linha in codigo.split("\n"):
        if dentro:  # continuação de um /* ... */ ou <!-- ... --> da linha anterior
            inicio = 0
            procurar_fim_em = 0
        else:
            # procura onde começa um comentário nesta linha
            posicoes = [linha.find(marca) for marca in ("# ", "/*", "<!--") if marca in linha]
            if not posicoes:
                linhas.append(escape(linha))  # escape: troca < por &lt; etc. (segurança)
                continue
            inicio = min(posicoes)
            if linha.startswith("/*", inicio):
                dentro = "*/"
            elif linha.startswith("<!--", inicio):
                dentro = "-->"
            procurar_fim_em = inicio + 2  # pula o próprio "/*" ou "<!--"
        if dentro and dentro in linha[procurar_fim_em:]:
            dentro = None  # o comentário fecha nesta mesma linha
        codigo_antes = escape(linha[:inicio])
        comentario = escape(linha[inicio:])
        linhas.append(codigo_antes + Markup('<span class="lousa__comentario">') + comentario + Markup("</span>"))
    return Markup("\n").join(linhas)


@app.route("/aula")
@app.route("/aula/<int:numero>")
def modo_aula(numero=1):
    """Mostra uma etapa da apresentação. As etapas ficam em aula.py."""
    total = len(aula.ETAPAS)
    if numero < 1 or numero > total:
        abort(404)
    etapa = aula.ETAPAS[numero - 1]  # a lista começa no 0, as etapas no 1
    return render_template("aula.html", etapa=etapa, numero=numero, total=total,
                           etapas=aula.ETAPAS, cores=aula.CORES)


@app.route("/aula/roteiro")
def roteiro():
    """O roteiro com a fala de cada integrante (para ler ou imprimir)."""
    return render_template("roteiro.html", etapas=aula.ETAPAS, integrantes=aula.INTEGRANTES)


@app.route("/creditos")
def creditos():
    return render_template("creditos.html", filmes=[montar(f) for f in FILMES])


@app.errorhandler(404)
def nao_encontrado(erro):
    return render_template("404.html"), 404


if __name__ == "__main__":
    # O modo debug recarrega o servidor ao salvar um arquivo e mostra os erros
    # detalhados no navegador. Ele é ótimo para desenvolver, mas NÃO deve ficar
    # ligado num site público (ele deixa rodar código pelo navegador).
    # Para ligar:  set FLASK_DEBUG=1  (Windows)  ou  export FLASK_DEBUG=1  (Linux/Mac)
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
