# EntreFrames 🎬

Portal de filmes famosos com **notas do IMDb** e **modelos 3D interativos**.
Projeto da matéria de Front-end, feito só com **Python, HTML e CSS**.

## Como rodar

Precisa do **Python 3.10 ou mais novo** ([python.org](https://www.python.org/downloads/)).
Na instalação no Windows, marque a opção *"Add python.exe to PATH"*.

Abra um terminal **dentro da pasta do projeto** (onde está o `app.py`) e rode:

```bash
pip install -r requirements.txt
python baixar_posteres.py
python app.py
```

O `baixar_posteres.py` baixa da Wikipédia os pôsteres que estiverem faltando
(precisa de internet; só é necessário na primeira vez ou depois de adicionar um filme).

Depois abra **http://127.0.0.1:5000** no navegador.
Para desligar o servidor, aperte `Ctrl + C` no terminal.

> No Windows também dá para dar dois cliques em **`iniciar.bat`**, que faz os dois passos.

**Modo debug** (recarrega sozinho ao salvar um arquivo e mostra os erros no navegador):
no Windows rode `set FLASK_DEBUG=1` antes de `python app.py`; no Linux/Mac, `export FLASK_DEBUG=1`.
Ele vem desligado porque não é seguro deixá-lo ligado num site público.

## Testes

```bash
python -m unittest -v
```

O arquivo `test_app.py` abre as páginas do site sem navegador e confere busca,
filtros, página do filme, 404 e créditos. Se aparecer `OK` no fim, está tudo certo.

## Publicar na internet (GitHub + Render)

O GitHub Pages só hospeda sites estáticos e não roda Python. Por isso o código fica no
**GitHub** e quem roda o site é o **Render** (gratuito), que gera um link fixo.

1. Crie um repositório no GitHub (ex.: `entreframes`) e envie os arquivos desta pasta.
2. Crie uma conta em [render.com](https://render.com) entrando com o GitHub.
3. No Render: **New → Blueprint** → escolha o repositório → **Apply**.
   O `render.yaml` já diz tudo: instalar, baixar os pôsteres e ligar com `gunicorn app:app`.
4. Em alguns minutos o site fica no ar em `https://entreframes.onrender.com`
   (ou parecido, se esse nome já estiver em uso).

Cada `git push` no GitHub atualiza o site sozinho.
No plano gratuito o site "dorme" depois de 15 min sem visitas, e a primeira visita
seguinte demora uns 50 segundos. **Abra o link um pouco antes da apresentação.**

## O que o portal faz

1. **Intro de cinema** — uma sala com cortinas, poltronas e a tela. Ao **clicar** (ou tocar,
   no celular), a tela **amplia**, as cortinas abrem e o catálogo aparece.
   Com o mouse em cima, a tela brilha mais para convidar ao clique.
2. **Catálogo** — filmes famosos, cada um com **pôster, nota do IMDb, nome e marca**
   (Marvel, DC, Lucasfilm, Pixar…). Dá para **buscar** (sem se preocupar com acentos),
   **filtrar por marca** e **ordenar** por nota, ano ou título.
3. **Página do filme** — ao clicar num filme, abre um **modelo 3D interativo** do filme
   (Homem de Ferro → armadura do Homem de Ferro, Jurassic Park → T-Rex, etc.).
   Dá para girar, dar zoom, mover e ver em tela cheia. Também tem sinopse, diretor,
   duração, gêneros e links para o IMDb e o Sketchfab.
4. **Notícias** — manchetes reais de cinema, via RSS do Google Notícias.
5. **Curiosidades** — fatos de bastidores de cada filme (também aparecem na página do filme).
6. **Linha do tempo** — os filmes em ordem de lançamento, década por década.
7. **Roleta** — "o que assistir hoje?": sorteia um filme, com filtro de gênero e marca.
8. **Créditos 3D** — página com o autor e a licença de cada modelo.
9. **Onde assistir** — o streaming do dono de cada filme (Disney+, HBO Max, Paramount+),
   lojas para alugar/comprar e o JustWatch com a disponibilidade atualizada.
   Depois de girar a Roleta, o botão "Onde assistir" leva direto para o filme sorteado.
10. **Modo aula** — botão verde no canto superior direito. Abre uma lousa que explica
   o código em 12 etapas, para a apresentação (veja abaixo).
11. **Página 404** personalizada para endereços que não existem.

Funciona em computador, tablet e celular (layout responsivo).

## Estrutura

```
Cinema/
├── app.py               # servidor Flask: rotas, busca, filtros e ordenação
├── filmes.py            # dados dos filmes (título, marca, IMDb, modelo 3D...)
├── imdb.py              # baixa e guarda as notas oficiais do IMDb
├── noticias.py          # baixa e guarda as notícias de cinema (RSS)
├── aula.py              # conteúdo do Modo aula (etapas, falas e cores)
├── ROTEIRO.md           # roteiro da apresentação (quem fala o quê)
├── baixar_posteres.py   # baixa os pôsteres da Wikipédia (rodar só uma vez)
├── test_app.py          # testes automáticos (python -m unittest -v)
├── requirements.txt     # dependências (Flask e gunicorn)
├── render.yaml          # configuração para publicar no Render
├── .gitignore           # arquivos que não vão para o Git (ex.: __pycache__)
├── iniciar.bat          # atalho para rodar no Windows
├── dados/
│   ├── notas_imdb.json  # cache das notas (atualizado sozinho 1x por dia)
│   └── noticias.json    # cache das notícias (criado sozinho, atualizado a cada 3h)
├── static/
│   ├── css/style.css    # todo o visual, incluindo a animação da intro
│   └── img/             # ícone e pôsteres
├── templates/           # páginas HTML (Jinja2)
│   ├── base.html        # topo e rodapé comuns
│   ├── index.html       # intro + catálogo
│   ├── filme.html       # página do filme com o modelo 3D
│   ├── noticias.html, curiosidades.html, linha_do_tempo.html, roleta.html, onde_assistir.html
│   ├── aula.html        # a lousa verde (página própria, sem o topo do site)
│   ├── roteiro.html     # o roteiro da apresentação dentro do site
│   ├── creditos.html
│   └── 404.html
├── README.md
└── MODELOS_3D.md        # documentação dos modelos 3D usados
```

## Como funciona por dentro

### A intro sem JavaScript (só CSS)

O HTML tem um `<input type="checkbox">` escondido e um `<label>` que cobre a tela inteira.
Todas as animações (tela ampliando, cortinas abrindo, poltronas descendo) começam
**pausadas** com `animation-play-state: paused`.

Clicar em qualquer lugar do `<label>` marca o checkbox, e o seletor
`.intro-gatilho:checked + .intro` coloca as animações em `running`. Como o checkbox
continua marcado, a animação sempre vai até o fim.
Pelo teclado: `Tab` destaca a tela e `Espaço` entra.

No fim, a animação deixa a intro com `visibility: hidden` e `animation-fill-mode: forwards`
faz ela continuar assim. A intro só aparece em `/`. Os links internos levam para
`/catalogo`, para não repetir a animação toda vez.

### Notas do IMDb

O IMDb não tem API gratuita, mas publica todo dia os seus **dados oficiais** em
[datasets.imdbws.com](https://datasets.imdbws.com/) (uso pessoal/não comercial).
O `imdb.py` baixa o arquivo `title.ratings.tsv.gz` (nota e número de votos de todos os
títulos), guarda só os nossos filmes em `dados/notas_imdb.json` e atualiza esse cache
**uma vez por dia, em segundo plano**, sem deixar o site lento. A conferência
acontece a cada visita, então funciona mesmo com o servidor ligado vários dias.
O JSON é gravado primeiro num arquivo temporário e só depois trocado pelo
verdadeiro, para nunca ficar corrompido se o programa fechar no meio.
Sem internet, o site continua funcionando com as últimas notas salvas
(e mostra "nota indisponível" para filmes que ainda não têm nota).
Para forçar a atualização: `python imdb.py`.

### Notícias (RSS)

RSS é um arquivo XML que os sites publicam com as suas últimas notícias. O `noticias.py`
baixa o RSS de busca do Google Notícias (manchetes de cinema em português), lê cada
`<item>` com o `xml.etree` (que já vem com o Python) e guarda em `dados/noticias.json`.
Funciona igual às notas: o cache vale 3 horas e é atualizado em segundo plano.
Para forçar a atualização: `python noticias.py`.

### Roleta e Linha do tempo

A Roleta é um formulário GET: o gênero e a marca vão para a URL, o Python filtra os filmes
e usa `random.choice()` para sortear. A animação é CSS: uma coluna de pôsteres desliza
para cima e para no sorteado. A Linha do tempo ordena os filmes por ano e agrupa por
década (`ano // 10 * 10`).

### Onde assistir

Em `filmes.py`, cada filme tem `"streaming"`: a plataforma do **dono** do filme, quando ele tem
uma no Brasil (a Marvel é da Disney → Disney+; a DC é da Warner → HBO Max), ou `None`.
Não colocamos as outras plataformas porque os catálogos mudam toda semana; para isso há o
link do JustWatch. Cada filme tem um `id` com o seu slug, então `/onde-assistir#shrek` abre
a página já no Shrek, e o seletor CSS `:target` destaca o cartão dele.

### Modo aula

O botão **Modo aula** (canto superior direito) abre `/aula`, uma lousa verde com 12 etapas.
Cada etapa mostra os pontos principais, um trecho do código e um link para a página do site
que está sendo explicada. O conteúdo fica todo em `aula.py`, então dá para mudar a
apresentação sem mexer no HTML. As falas de cada integrante estão em **[ROTEIRO.md](ROTEIRO.md)**
e também no site, em `/aula/roteiro`.

### Por que essas cores?

| Cor | Hex | Motivo |
|-----|-----|--------|
| Preto-cinema | `#0b0a10` | Sala de cinema com a luz apagada: o pôster e o 3D viram a "tela". |
| Vermelho-cortina | `#c8102e` | Cortinas e poltronas de cinema. Destaques e o "Frames" do logo. |
| Amarelo-IMDb | `#f5c518` | Cor oficial do IMDb: aparece nas notas e liga a cor à avaliação. |
| Creme-tela | `#f3efe6` | Como a luz do projetor; cansa menos a vista que o branco puro. |

As fontes são Bebas Neue (parece letra de cartaz de cinema) e Inter (fácil de ler).
No Modo aula, a lousa usa verde `#1f4b3a`, moldura de madeira e a fonte Nunito, arredondada e fácil de ler de longe no projetor.

### Modelos 3D

Os modelos ficam hospedados no Sketchfab e são mostrados com o visualizador oficial deles
(`<iframe>`). Detalhes, autores e licenças em **[MODELOS_3D.md](MODELOS_3D.md)**.
A página `/creditos` tem link para o texto de cada licença, como pede a Creative Commons.

### Pôsteres

Baixados da Wikipédia pelo `baixar_posteres.py` e salvos em `static/img/posteres/`,
então o site não depende de imagens de outros sites.

## Como adicionar um filme

1. Em `filmes.py`, copie um dos blocos `{ ... }` e troque os dados
   (o código `imdb` é o `tt...` do link do filme no IMDb).
   Se o modelo 3D usar uma licença nova, adicione o link dela em `LICENCAS`, no fim do arquivo.
2. Rode `python baixar_posteres.py` para baixar o pôster.
3. Rode `python imdb.py` para buscar a nota.
4. Reinicie o servidor e rode os testes (`python -m unittest -v`).

## Observações para a apresentação

- **Linguagens:** o código do projeto é só Python (servidor), HTML (templates Jinja2) e CSS.
  Não há nenhum arquivo JavaScript nosso; busca e filtros funcionam com formulários HTML
  processados pelo Python. O único JavaScript que roda é o do próprio visualizador do
  Sketchfab, dentro do `<iframe>`, que é ele quem desenha o 3D.
- **Acessibilidade:** textos alternativos nos pôsteres, link "Pular para o conteúdo",
  navegação por teclado com foco visível, e animações mais curtas para quem ativa
  "reduzir movimento" no sistema (`prefers-reduced-motion`).
- **Internet:** o site precisa de internet para carregar os modelos 3D (Sketchfab), as
  notícias e as fontes. Teste tudo no computador da apresentação antes!
