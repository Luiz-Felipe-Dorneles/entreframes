"""
Conteúdo do Modo Aula (a lousa verde em /aula).

Cada etapa tem:
  - quem:    integrante que apresenta a etapa
  - titulo:  título escrito na lousa
  - pontos:  tópicos que aparecem na lousa
  - codigo:  trecho do código mostrado na lousa (simplificado)
  - arquivo: de qual arquivo o trecho veio
  - mostrar: página do site para abrir durante a fala (ou None)
  - fala:    o que a pessoa fala (aparece só no roteiro, em /aula/roteiro)

Para mudar a apresentação, é só editar esta lista.
"""

INTEGRANTES = ["Cauã", "Vitor", "Ryan", "Mateus"]

# Cores do site (as mesmas variáveis do style.css), explicadas na etapa 2
CORES = [
    {"nome": "Preto-cinema", "hex": "#0b0a10",
     "motivo": "Fundo escuro como uma sala de cinema com a luz apagada: o pôster e o modelo 3D viram a \"tela\"."},
    {"nome": "Vermelho-cortina", "hex": "#c8102e",
     "motivo": "A cor das cortinas e poltronas de cinema. Usada no nome \"Frames\", na intro e nos destaques."},
    {"nome": "Amarelo-IMDb", "hex": "#f5c518",
     "motivo": "O amarelo oficial do IMDb. Aparece nas notas e nos botões, ligando a cor à avaliação dos filmes."},
    {"nome": "Creme-tela", "hex": "#f3efe6",
     "motivo": "Branco levemente amarelado, como a luz do projetor. Cansa menos a vista que o branco puro."},
]

ETAPAS = [
    # ------------------------------------------------------------ Cauã
    {
        "quem": "Cauã",
        "titulo": "O que é o EntreFrames?",
        "pontos": [
            "Portal de filmes famosos com nota do IMDb e modelo 3D interativo",
            "Python + Flask no servidor, HTML (Jinja2) e CSS no visual",
            "Nenhum arquivo JavaScript nosso: busca, filtros e roleta são formulários processados pelo Python",
            "Menus: Catálogo, Notícias, Curiosidades, Linha do tempo, Roleta, Onde assistir e Créditos 3D",
        ],
        "codigo": """\
# Cria o site (o "app" do Flask)
app = Flask(__name__)

# Liga o endereço /catalogo a esta função:
# quem acessar /catalogo recebe o que ela devolver
@app.route("/catalogo")
def catalogo():
    # Monta a página do catálogo, sem a intro
    return mostrar_catalogo(mostrar_intro=False)""",
        "arquivo": "app.py",
        "mostrar": "/catalogo",
        "fala": "Boa tarde! Nós somos o Cauã, o Vitor, o Ryan e o Mateus, e vamos apresentar o "
                "EntreFrames, um portal de filmes famosos. Em cada filme dá para ver a nota do IMDb "
                "e explorar um modelo 3D. O site foi feito com Python, usando o Flask, mais HTML e CSS. "
                "Uma escolha nossa foi não escrever JavaScript: tudo o que é interativo, como busca, "
                "filtros e a roleta, funciona com formulários que o Python processa. "
                "Cada endereço do site, como /catalogo, é ligado a uma função Python, como vocês veem na lousa.",
    },
    {
        "quem": "Cauã",
        "titulo": "Identidade visual: nome, ícone e cores",
        "pontos": [
            "EntreFrames: um filme é uma sequência de quadros (frames), e o site fica \"entre\" eles",
            "Ícone: uma fita de filme com um botão de play entre dois quadros",
            "Fontes: Bebas Neue (letras de cartaz de cinema) e Inter (fácil de ler)",
            "Cores escolhidas pela experiência de ir ao cinema (veja abaixo)",
        ],
        "codigo": """\
/* :root guarda variáveis que valem no site todo.
   Mudou aqui, muda em todas as páginas. */
:root {
  --fundo: #0b0a10;     /* sala de cinema escura */
  --vermelho: #c8102e;  /* cortina e poltronas */
  --ouro: #f5c518;      /* amarelo oficial do IMDb */
  --texto: #f3efe6;     /* creme: luz do projetor */
}

/* Para usar uma variável: var(--nome) */
body { background: var(--fundo); }""",
        "arquivo": "static/css/style.css",
        "mostrar": None,
        "cores": True,  # mostra as amostras de cor na lousa
        "fala": "O nome EntreFrames vem do fato de que um filme é uma sequência de quadros, os frames. "
                "O ícone mostra isso: uma fita de filme com um play entre dois quadros. "
                "As cores foram escolhidas pensando na experiência de ir ao cinema: o fundo quase preto "
                "é a sala com a luz apagada, e deixa o pôster e o modelo 3D em destaque. O vermelho é o "
                "das cortinas e poltronas. O amarelo é a cor oficial do IMDb, então sempre que aparece "
                "uma nota ele está lá. E o texto é um creme, parecido com a luz do projetor, que cansa "
                "menos a vista que o branco puro. Todas as cores ficam em variáveis do CSS, então "
                "trocar uma cor no site inteiro é mudar uma linha.",
    },
    {
        "quem": "Cauã",
        "titulo": "A intro de cinema só com CSS",
        "pontos": [
            "Um checkbox escondido + um <label> que cobre a tela inteira",
            "Clicar no label marca o checkbox",
            "O seletor :checked dá \"play\" nas animações (começam pausadas)",
            "No fim, a intro fica invisível e libera o catálogo",
        ],
        "codigo": """\
/* Todas as animações da intro começam pausadas */
.intro, .intro .anima {
  animation-play-state: paused;
}

/* Quando o checkbox é marcado (:checked),
   o "+" pega a intro logo depois dele
   e solta (running) as animações */
.intro-gatilho:checked + .intro .anima {
  animation-play-state: running;
}""",
        "arquivo": "static/css/style.css",
        "mostrar": "/",
        "fala": "Quando abrimos o site, aparece uma sala de cinema. Ao clicar, a tela amplia, as "
                "cortinas abrem e o catálogo aparece. Isso foi feito só com CSS. O truque é um checkbox "
                "escondido: a sala inteira é o label dele, então clicar em qualquer lugar marca o checkbox. "
                "Todas as animações começam pausadas, e o seletor :checked muda para running. "
                "Agora passo para o Vitor, que vai explicar como as páginas são montadas.",
    },
    # ------------------------------------------------------------ Vitor
    {
        "quem": "Vitor",
        "titulo": "Como o Flask monta uma página",
        "pontos": [
            "1. O navegador pede um endereço: /filme/shrek",
            "2. O Flask chama a função ligada a esse endereço",
            "3. A função busca os dados e chama render_template()",
            "4. O Jinja2 preenche o HTML com os dados: {{ filme.titulo }}",
        ],
        "codigo": """\
# <slug> é uma parte variável do endereço:
# em /filme/shrek, o slug vale "shrek"
@app.route("/filme/<slug>")
def filme(slug):
    # Filme que não existe: mostra a página 404
    if slug not in FILMES_POR_SLUG:
        abort(404)
    # Procura o filme no dicionário pelo slug
    atual = FILMES_POR_SLUG[slug]
    # Preenche o filme.html com os dados do filme
    return render_template("filme.html",
                           filme=montar(atual))""",
        "arquivo": "app.py",
        "mostrar": "/filme/shrek",
        "fala": "Toda página segue o mesmo caminho. O navegador pede um endereço, por exemplo /filme/shrek. "
                "O Flask vê que esse endereço combina com a rota /filme/<slug> e chama a função filme, "
                "passando 'shrek' como slug. A função procura o filme e, se não existir, devolve o erro 404. "
                "Se existir, ela chama o render_template, que pega o arquivo filme.html e troca as marcações "
                "com chaves duplas pelos dados do filme. O resultado é o HTML que chega no navegador.",
    },
    {
        "quem": "Vitor",
        "titulo": "Onde ficam os dados dos filmes",
        "pontos": [
            "filmes.py: uma lista de dicionários, um por filme",
            "Cada filme tem título, ano, diretor, gêneros, código do IMDb e modelo 3D",
            "Para adicionar um filme, é só copiar um bloco e trocar os dados",
            "montar() junta os dados fixos com a nota e os links calculados na hora",
        ],
        "codigo": """\
# Cada filme é um dicionário: "chave": valor
{
    "slug": "shrek",        # parte do endereço: /filme/shrek
    "titulo": "Shrek",
    "ano": 2001,            # número (int), dá para ordenar
    "imdb": "tt0126029",    # código do filme no IMDb
    "marca": "dreamworks",  # chave do dicionário MARCAS
    # dicionário dentro de dicionário:
    # dados do modelo 3D no Sketchfab
    "modelo": {"uid": "ff6a111c...",
               "autor": "burnt.melon"},
}""",
        "arquivo": "filmes.py",
        "mostrar": "/catalogo",
        "fala": "Os dados dos filmes ficam no arquivo filmes.py, numa lista de dicionários. Cada dicionário "
                "é um filme, com título, ano, diretor, o código do filme no IMDb e o código do modelo 3D. "
                "Não usamos banco de dados porque são poucos filmes e eles quase não mudam. "
                "Na hora de mostrar, a função montar junta esses dados fixos com o que muda, "
                "como a nota do IMDb e os links do pôster e do modelo.",
    },
    {
        "quem": "Vitor",
        "titulo": "Busca, filtro por marca e ordenação",
        "pontos": [
            "Os filtros vão na própria URL: /catalogo?q=batman&marca=dc&ordem=ano",
            "request.args lê esses valores no Python",
            "sem_acento(): \"Anéis\" vira \"aneis\", então a busca ignora acentos",
            "Valores inválidos na URL são ignorados (segurança)",
        ],
        "codigo": """\
def sem_acento(texto):
    # NFD separa a letra do acento: "é" vira "e" + "´"
    separado = unicodedata.normalize("NFD", texto.lower())
    # Junta de volta só o que NÃO é acento
    # (acentos são da categoria "Mn")
    return "".join(letra for letra in separado
                   if unicodedata.category(letra) != "Mn")

# Exemplo: sem_acento("Anéis") devolve "aneis" (sem acento)""",
        "arquivo": "app.py",
        "mostrar": "/catalogo?q=aneis",
        "fala": "A busca é um formulário HTML normal. Quando você clica em Buscar, o navegador coloca o "
                "texto na URL, depois do ponto de interrogação, e o Python lê com request.args. "
                "Para a busca não depender de acento, a função sem_acento separa cada letra do seu acento "
                "e joga o acento fora. Por isso, se eu buscar 'aneis' sem acento, o Senhor dos Anéis aparece. "
                "Agora o Ryan vai mostrar a parte do 3D.",
    },
    # ------------------------------------------------------------ Ryan
    {
        "quem": "Ryan",
        "titulo": "Como os modelos 3D aparecem",
        "pontos": [
            "Os modelos ficam hospedados no Sketchfab, um site de modelos 3D",
            "Cada modelo tem um código único (uid)",
            "Montamos o endereço de \"embed\" e colocamos num <iframe>",
            "O Sketchfab desenha o 3D: girar, zoom, luz e tela cheia",
            "Licenças Creative Commons pedem crédito ao autor → página Créditos 3D",
        ],
        "codigo": """\
# app.py: o código (uid) do modelo vem do filmes.py
uid = filme["modelo"]["uid"]
# Monta o endereço do visualizador do Sketchfab
embed = (f"https://sketchfab.com/models/"
         f"{uid}/embed?autostart=1")

<!-- filme.html: o iframe é uma "janela" que
     mostra outra página (o Sketchfab) dentro da nossa -->
<iframe src="{{ filme.modelo_embed }}"
        allow="autoplay; fullscreen; xr-spatial-tracking">
<!-- allow: libera rodar sozinho, tela cheia e VR -->""",
        "arquivo": "app.py e templates/filme.html",
        "mostrar": "/filme/homem-de-ferro",
        "fala": "Os modelos 3D não ficam no nosso projeto. Eles estão no Sketchfab, um site onde artistas "
                "publicam modelos 3D. Cada modelo tem um código, o uid. Com esse código, o Python monta o "
                "endereço de embed, e o template coloca esse endereço num iframe, que é uma janela para "
                "outra página dentro da nossa. Quem desenha o 3D é o visualizador do Sketchfab, então não "
                "precisamos escrever código 3D. Como os modelos têm licença Creative Commons, que exige "
                "dar crédito ao autor, fizemos a página Créditos 3D com o autor e o link da licença.",
    },
    {
        "quem": "Ryan",
        "titulo": "Os pôsteres vêm da Wikipédia",
        "pontos": [
            "baixar_posteres.py usa a API pública da Wikipédia",
            "Pede o resumo da página do filme e pega a imagem principal",
            "Salva em static/img/posteres/ (o site não depende de links externos)",
            "Só baixa os que faltam; espera entre pedidos para não sobrecarregar a Wikipédia",
        ],
        "codigo": """\
# Endereço da API da Wikipédia com o resumo da página
endereco = (f"https://{idioma}.wikipedia.org/api/rest_v1"
            f"/page/summary/{pagina}")
# baixar() faz o pedido; json.loads() transforma
# o texto JSON num dicionário do Python
resumo = json.loads(baixar(endereco))
# A imagem principal da página é o pôster do filme
imagem = resumo.get("originalimage")
# .get() devolve None se a chave não existir
# (em vez de dar erro)""",
        "arquivo": "baixar_posteres.py",
        "mostrar": "/catalogo",
        "fala": "Os pôsteres são baixados por um script separado, o baixar_posteres.py, que rodamos uma vez. "
                "Ele usa a API da Wikipédia: pede o resumo da página de cada filme, que vem em JSON, e pega "
                "o endereço da imagem principal, que é o pôster. A imagem fica salva no projeto, então o site "
                "não depende da Wikipédia para funcionar. O script também espera um pouco entre um pedido e "
                "outro, para não sobrecarregar o site deles.",
    },
    {
        "quem": "Ryan",
        "titulo": "Linha do tempo, Roleta e Onde assistir",
        "pontos": [
            "Linha do tempo: filmes ordenados por ano e agrupados por década",
            "Década = ano // 10 * 10   (1994 → 1990)",
            "Roleta: random.choice() sorteia um filme, com filtro de gênero e marca",
            "A animação da roleta é CSS: uma coluna de pôsteres que desliza e para no sorteado",
            "Onde assistir: streaming do dono do filme + lojas + JustWatch; o botão da roleta pula para #slug",
        ],
        "codigo": """\
# Filtra: fica só com os filmes do gênero escolhido
# ("not genero" = nenhum gênero escolhido: vale todos)
candidatos = [f for f in FILMES
              if not genero or genero in f["generos"]]

# Sorteia um item da lista, com a mesma chance para todos
sorteado = random.choice(candidatos)""",
        "arquivo": "app.py",
        "mostrar": "/roleta",
        "fala": "Também criamos dois menus. A Linha do tempo mostra os filmes do catálogo por ordem de "
                "lançamento, separados por década. Para achar a década, dividimos o ano por 10 sem resto e "
                "multiplicamos por 10. A Roleta responde à pergunta 'o que eu assisto hoje?': você escolhe "
                "um gênero ou uma marca, o Python filtra os filmes e o random.choice sorteia um. A animação "
                "de girar é feita com CSS. Depois de sortear, o botão Onde assistir leva direto para aquele "
                "filme no menu Onde assistir, usando uma âncora: o endereço termina com # e o slug do filme. "
                "Nesse menu mostramos o streaming do dono do filme, como Disney+ para a Marvel, e um link "
                "para o JustWatch, porque os catálogos mudam toda hora. "
                "Agora o Mateus vai falar dos dados que vêm da internet.",
    },
    # ------------------------------------------------------------ Mateus
    {
        "quem": "Mateus",
        "titulo": "As notas do IMDb",
        "pontos": [
            "O IMDb publica todo dia um arquivo com as notas de todos os títulos",
            "Baixamos o arquivo compactado (.gz) e lemos linha por linha",
            "Guardamos só os nossos filmes em dados/notas_imdb.json (o cache)",
            "O cache vale 1 dia; a atualização roda numa thread, sem travar o site",
        ],
        "codigo": """\
# O arquivo do IMDb tem uma linha por título:
# código <TAB> nota <TAB> votos
for linha in texto:
    # strip() tira o "enter" do fim; split("\\t")
    # quebra a linha nas 3 colunas
    colunas = linha.strip().split("\\t")
    # Guarda só se for um dos nossos filmes
    if colunas[0] in procurados:
        notas[colunas[0]] = {"nota": float(colunas[1]),
                             "votos": int(colunas[2])}
        # float: número com vírgula / int: número inteiro""",
        "arquivo": "imdb.py",
        "mostrar": "/catalogo?ordem=nota",
        "fala": "O IMDb não tem uma API gratuita, mas publica todo dia um arquivo com a nota de todos os "
                "títulos que existem. Esse arquivo é grande, então não dá para baixar a cada visita. "
                "O nosso código baixa o arquivo, lê linha por linha e guarda só os nossos filmes num JSON, "
                "que chamamos de cache. O site lê o cache, que é rápido. Quando o cache passa de um dia, "
                "o download é feito de novo numa thread, que é uma tarefa em segundo plano, para o site "
                "não ficar travado esperando. E se não tiver internet, o site continua com as notas antigas.",
    },
    {
        "quem": "Mateus",
        "titulo": "Notícias ao vivo com RSS",
        "pontos": [
            "RSS: um arquivo XML com as últimas notícias de um site",
            "Usamos o RSS do Google Notícias, com manchetes de cinema em português",
            "xml.etree (já vem com o Python) lê cada <item> do XML",
            "Mesmo esquema do IMDb: cache em JSON que vale 3 horas",
        ],
        "codigo": """\
# Transforma o texto XML numa "árvore" de tags
raiz = ET.fromstring(xml_texto)
# Cada notícia do RSS fica dentro de uma tag <item>
for item in raiz.iter("item"):
    # findtext() pega o texto de dentro da tag:
    # <title>Manchete</title>  ->  "Manchete"
    titulo = item.findtext("title")
    link = item.findtext("link")      # endereço da notícia
    fonte = item.findtext("source")   # nome do site""",
        "arquivo": "noticias.py",
        "mostrar": "/noticias",
        "fala": "A página de notícias mostra manchetes reais de cinema. Para isso usamos RSS, um formato em "
                "XML que os sites publicam com as suas últimas notícias. Pegamos o RSS do Google Notícias, "
                "que junta vários sites brasileiros. O Python lê o XML com a biblioteca xml.etree, que já vem "
                "com ele, e pega o título, o link e o nome do site de cada notícia. Reaproveitamos a mesma "
                "ideia do IMDb: as notícias ficam num cache que é atualizado a cada três horas.",
    },
    {
        "quem": "Mateus",
        "titulo": "Testes, acessibilidade e conclusão",
        "pontos": [
            "test_app.py: testes automáticos que abrem as páginas sem navegador",
            "python -m unittest -v  →  OK",
            "Acessibilidade: texto alternativo, navegação por teclado, \"reduzir movimento\"",
            "Funciona no celular, tablet e computador",
            "Obrigado! Perguntas?",
        ],
        "codigo": """\
# Todo método que começa com "test_" é um teste
def test_busca_ignora_acento(self):
    # Abre a página de busca sem navegador
    # (o "_" ignora o código HTTP, só queremos o HTML)
    _, html = self.abrir("/catalogo?q=aneis")
    # Confere se o filme apareceu no resultado;
    # se não aparecer, o teste falha e avisa
    self.assertIn("O Senhor dos Anéis", html)""",
        "arquivo": "test_app.py",
        "mostrar": None,
        "fala": "Para ter certeza de que tudo funciona, escrevemos testes automáticos. Eles abrem as páginas "
                "sem navegador e conferem o resultado, por exemplo se a busca sem acento acha o Senhor dos "
                "Anéis. Se alguém mexer no código e quebrar algo, o teste avisa. Também cuidamos da "
                "acessibilidade: as imagens têm texto alternativo, dá para usar tudo pelo teclado, e quem "
                "ativa 'reduzir movimento' no sistema vê animações mais curtas. O site também se adapta "
                "ao celular. Esse foi o EntreFrames. Obrigado, e estamos abertos a perguntas!",
    },
]
