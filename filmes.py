"""
Catálogo de filmes do portal.

Cada filme tem:
  - imdb:   código do filme no IMDb (usado para buscar a nota)
  - marca:  chave da marca/estúdio (ver MARCAS abaixo)
  - curiosidades: fatos sobre o filme (aparecem na página do filme e em /curiosidades)
  - streaming: chave de PLATAFORMAS (streaming do dono do filme) ou None
  - wiki:   página da Wikipédia de onde o pôster é baixado (baixar_posteres.py)
  - modelo: modelo 3D do Sketchfab exibido na página do filme
            (a lista completa com créditos está em MODELOS_3D.md)
"""

MARCAS = {
    "marvel": "Marvel",
    "dc": "DC",
    "lucasfilm": "Lucasfilm",
    "pixar": "Pixar",
    "universal": "Universal",
    "warner": "Warner Bros.",
    "newline": "New Line Cinema",
    "paramount": "Paramount",
    "dreamworks": "DreamWorks",
    "disney": "Disney",
    "columbia": "Columbia Pictures",
}

FILMES = [
    {
        "slug": "homem-de-ferro",
        "titulo": "Homem de Ferro",
        "original": "Iron Man",
        "ano": 2008,
        "imdb": "tt0371746",
        "marca": "marvel",
        "diretor": "Jon Favreau",
        "duracao": "2h 6min",
        "generos": ["Ação", "Aventura", "Ficção científica"],
        "sinopse": "Depois de ser sequestrado, o bilionário Tony Stark constrói uma "
                   "armadura blindada para escapar e decide usá-la para proteger o mundo.",
        "curiosidades": [
            "A frase final “Eu sou o Homem de Ferro” não estava no roteiro original e foi decidida durante as filmagens.",
            "Foi o primeiro filme do Universo Cinematográfico Marvel, que depois chegou a dezenas de filmes.",
        ],
        # Onde assistir: plataforma do dono do filme (ou None) e o motivo
        "streaming": "disney",
        "streaming_motivo": "A Marvel pertence à Disney, que coloca os filmes dela no Disney+.",
        "wiki": ("en", "Iron_Man_(2008_film)"),
        "modelo": {
            "uid": "9865dc82c37542ef8d5bd8769e58cb59",
            "nome": "Marvel Iron Man Mark 6",
            "autor": "Mittergen",
            "licenca": "CC BY 4.0",
        },
    },
    {
        "slug": "vingadores-ultimato",
        "titulo": "Vingadores: Ultimato",
        "original": "Avengers: Endgame",
        "ano": 2019,
        "imdb": "tt4154796",
        "marca": "marvel",
        "diretor": "Anthony e Joe Russo",
        "duracao": "3h 1min",
        "generos": ["Ação", "Aventura", "Drama"],
        "sinopse": "Depois do estalo de Thanos, os Vingadores que sobraram se unem "
                   "uma última vez para tentar desfazer a destruição do universo.",
        "curiosidades": [
            "Em 2019 virou a maior bilheteria da história do cinema, passando Avatar (que retomou o posto em 2021).",
            "Para evitar vazamentos, vários atores receberam só as páginas do roteiro com as próprias cenas.",
        ],
        # Onde assistir: plataforma do dono do filme (ou None) e o motivo
        "streaming": "disney",
        "streaming_motivo": "A Marvel pertence à Disney, que coloca os filmes dela no Disney+.",
        "wiki": ("en", "Avengers:_Endgame"),
        "modelo": {
            "uid": "b466a8b8bfc64d7aa4dc5d4a919cfed9",
            "nome": "Thanos : The Endgame",
            "autor": "Virtual Void Studio",
            "licenca": "CC BY 4.0",
        },
    },
    {
        "slug": "homem-aranha-sem-volta-para-casa",
        "titulo": "Homem-Aranha: Sem Volta para Casa",
        "original": "Spider-Man: No Way Home",
        "ano": 2021,
        "imdb": "tt10872600",
        "marca": "marvel",
        "diretor": "Jon Watts",
        "duracao": "2h 28min",
        "generos": ["Ação", "Aventura", "Fantasia"],
        "sinopse": "Com a identidade revelada, Peter Parker pede ajuda ao Doutor Estranho, "
                   "mas o feitiço dá errado e abre as portas do multiverso.",
        "curiosidades": [
            "Reuniu os três Homens-Aranha do cinema: Tom Holland, Tobey Maguire e Andrew Garfield.",
            "Os atores negaram por meses que Maguire e Garfield estariam no filme, para manter a surpresa.",
        ],
        # Onde assistir: plataforma do dono do filme (ou None) e o motivo
        "streaming": None,
        "streaming_motivo": "O Homem-Aranha do cinema é da Sony, que não tem streaming próprio no Brasil, então o filme muda de plataforma de tempos em tempos.",
        "wiki": ("en", "Spider-Man:_No_Way_Home"),
        "modelo": {
            "uid": "9f0f2ab778194c52911a549110e597e0",
            "nome": "Spider-Man No Way Home (Rigged)",
            "autor": "Visiion",
            "licenca": "CC BY 4.0",
        },
    },
    {
        "slug": "pantera-negra",
        "titulo": "Pantera Negra",
        "original": "Black Panther",
        "ano": 2018,
        "imdb": "tt1825683",
        "marca": "marvel",
        "diretor": "Ryan Coogler",
        "duracao": "2h 14min",
        "generos": ["Ação", "Aventura", "Ficção científica"],
        "sinopse": "T'Challa volta para Wakanda para assumir o trono e precisa enfrentar "
                   "um inimigo que ameaça o futuro da nação e do mundo.",
        "curiosidades": [
            "Foi o primeiro filme de super-herói indicado ao Oscar de Melhor Filme.",
            "Ganhou 3 Oscars: figurino, design de produção e trilha sonora.",
        ],
        # Onde assistir: plataforma do dono do filme (ou None) e o motivo
        "streaming": "disney",
        "streaming_motivo": "A Marvel pertence à Disney, que coloca os filmes dela no Disney+.",
        "wiki": ("en", "Black_Panther_(film)"),
        "modelo": {
            "uid": "83a0d1ce2d124bcd84f92608c1ed422b",
            "nome": "Black Panther Mask",
            "autor": "Brandon Shirk",
            "licenca": "Sketchfab Standard (somente visualização)",
        },
    },
    {
        "slug": "batman-o-cavaleiro-das-trevas",
        "titulo": "Batman: O Cavaleiro das Trevas",
        "original": "The Dark Knight",
        "ano": 2008,
        "imdb": "tt0468569",
        "marca": "dc",
        "diretor": "Christopher Nolan",
        "duracao": "2h 32min",
        "generos": ["Ação", "Crime", "Drama"],
        "sinopse": "Batman, o tenente Gordon e o promotor Harvey Dent enfrentam o Coringa, "
                   "um criminoso que quer mergulhar Gotham no caos.",
        "curiosidades": [
            "Heath Ledger ganhou o Oscar de Ator Coadjuvante pelo Coringa, após a sua morte.",
            "O Batmóvel (Tumbler) foi construído de verdade e andava pelas ruas nas filmagens.",
        ],
        # Onde assistir: plataforma do dono do filme (ou None) e o motivo
        "streaming": "max",
        "streaming_motivo": "A DC pertence à Warner Bros. Discovery, dona da HBO Max.",
        "wiki": ("en", "The_Dark_Knight"),
        "modelo": {
            "uid": "7ae346a9724a40faa467a3107dfb09e9",
            "nome": "Batmobile - The Dark Knight Tumbler",
            "autor": "Gravity Jack",
            "licenca": "CC BY 4.0",
        },
    },
    {
        "slug": "star-wars-uma-nova-esperanca",
        "titulo": "Star Wars: Uma Nova Esperança",
        "original": "Star Wars",
        "ano": 1977,
        "imdb": "tt0076759",
        "marca": "lucasfilm",
        "diretor": "George Lucas",
        "duracao": "2h 1min",
        "generos": ["Ação", "Aventura", "Fantasia"],
        "sinopse": "Luke Skywalker se junta a um cavaleiro Jedi, a um piloto e a dois "
                   "droides para salvar a princesa Leia das garras de Darth Vader.",
        "curiosidades": [
            "O corpo de Darth Vader era do ator David Prowse, mas a voz era de James Earl Jones.",
            "Para criar os efeitos do filme, George Lucas fundou a empresa ILM, que existe até hoje.",
        ],
        # Onde assistir: plataforma do dono do filme (ou None) e o motivo
        "streaming": "disney",
        "streaming_motivo": "A Lucasfilm pertence à Disney, que coloca os filmes dela no Disney+.",
        "wiki": ("en", "Star_Wars_(film)"),
        "modelo": {
            "uid": "bde24275c4314886ac9ef9b98342cfa7",
            "nome": "Darth Vader by Oscar Creativo",
            "autor": "Oscar Creativo",
            "licenca": "CC BY 4.0",
        },
    },
    {
        "slug": "toy-story",
        "titulo": "Toy Story",
        "original": "Toy Story",
        "ano": 1995,
        "imdb": "tt0114709",
        "marca": "pixar",
        "diretor": "John Lasseter",
        "duracao": "1h 21min",
        "generos": ["Animação", "Aventura", "Comédia"],
        "sinopse": "O caubói Woody sente ciúmes quando o patrulheiro espacial Buzz "
                   "Lightyear vira o brinquedo favorito do quarto de Andy.",
        "curiosidades": [
            "Foi o primeiro longa-metragem feito inteiramente em computação gráfica.",
            "Cada quadro do filme levava horas para ser renderizado pelos computadores da Pixar.",
        ],
        # Onde assistir: plataforma do dono do filme (ou None) e o motivo
        "streaming": "disney",
        "streaming_motivo": "A Pixar pertence à Disney, que coloca os filmes dela no Disney+.",
        "wiki": ("en", "Toy_Story"),
        "modelo": {
            "uid": "f17faf6de76d4fee961c692e997ea9cc",
            "nome": "Buzz Lightyear Toy Story",
            "autor": "Jamessmartguy",
            "licenca": "CC BY 4.0",
        },
    },
    {
        "slug": "jurassic-park",
        "titulo": "Jurassic Park: O Parque dos Dinossauros",
        "original": "Jurassic Park",
        "ano": 1993,
        "imdb": "tt0107290",
        "marca": "universal",
        "diretor": "Steven Spielberg",
        "duracao": "2h 7min",
        "generos": ["Aventura", "Ficção científica", "Suspense"],
        "sinopse": "Um parque com dinossauros clonados parece um sonho, até que a energia "
                   "cai e os animais escapam durante a visita de um grupo de cientistas.",
        "curiosidades": [
            "O T-Rex mistura um robô (animatrônico) em tamanho real com dinossauros feitos em computador.",
            "O rugido do T-Rex foi criado misturando sons de vários animais, como elefante, tigre e jacaré.",
        ],
        # Onde assistir: plataforma do dono do filme (ou None) e o motivo
        "streaming": None,
        "streaming_motivo": "A Universal não tem streaming próprio no Brasil, então o filme muda de plataforma de tempos em tempos.",
        "wiki": ("en", "Jurassic_Park_(film)"),
        "modelo": {
            "uid": "6465a297fa784598adc49f6e0042d449",
            "nome": "Tyrant King - Tyrannosaurus",
            "autor": "Marcel Schanz",
            "licenca": "CC BY 4.0",
        },
    },
    {
        "slug": "de-volta-para-o-futuro",
        "titulo": "De Volta para o Futuro",
        "original": "Back to the Future",
        "ano": 1985,
        "imdb": "tt0088763",
        "marca": "universal",
        "diretor": "Robert Zemeckis",
        "duracao": "1h 56min",
        "generos": ["Aventura", "Comédia", "Ficção científica"],
        "sinopse": "Marty McFly viaja acidentalmente para 1955 num DeLorean e precisa "
                   "garantir que seus pais se apaixonem para poder voltar para casa.",
        "curiosidades": [
            "Marty McFly começou sendo interpretado por Eric Stoltz, que foi trocado por Michael J. Fox depois de semanas de filmagem.",
            "No roteiro original, a máquina do tempo era uma geladeira, e não um DeLorean.",
        ],
        # Onde assistir: plataforma do dono do filme (ou None) e o motivo
        "streaming": None,
        "streaming_motivo": "A Universal não tem streaming próprio no Brasil, então o filme muda de plataforma de tempos em tempos.",
        "wiki": ("en", "Back_to_the_Future"),
        "modelo": {
            "uid": "c6d865257d344523be373f543323ae18",
            "nome": "1985 DeLorean DMC-12 Time Machine BTTF",
            "autor": "Ddiaz Design",
            "licenca": "CC BY-NC-SA 4.0",
        },
    },
    {
        "slug": "o-senhor-dos-aneis",
        "titulo": "O Senhor dos Anéis: A Sociedade do Anel",
        "original": "The Lord of the Rings: The Fellowship of the Ring",
        "ano": 2001,
        "imdb": "tt0120737",
        "marca": "newline",
        "diretor": "Peter Jackson",
        "duracao": "2h 58min",
        "generos": ["Aventura", "Drama", "Fantasia"],
        "sinopse": "O hobbit Frodo recebe a missão de destruir o Um Anel e parte com oito "
                   "companheiros rumo à Montanha da Perdição.",
        "curiosidades": [
            "Os três filmes da trilogia foram gravados ao mesmo tempo, na Nova Zelândia.",
            "Viggo Mortensen (Aragorn) entrou no elenco já com as filmagens começando, substituindo outro ator.",
        ],
        # Onde assistir: plataforma do dono do filme (ou None) e o motivo
        "streaming": "max",
        "streaming_motivo": "A New Line Cinema pertence à Warner Bros. Discovery, dona da HBO Max.",
        "wiki": ("en", "The_Lord_of_the_Rings:_The_Fellowship_of_the_Ring"),
        "modelo": {
            "uid": "39eb401be92c49d39520fadd5ecff8d3",
            "nome": "The One Ring (Lord of The Rings)",
            "autor": "Yanez Designs",
            "licenca": "CC BY 4.0",
        },
    },
    {
        "slug": "harry-potter-e-a-pedra-filosofal",
        "titulo": "Harry Potter e a Pedra Filosofal",
        "original": "Harry Potter and the Sorcerer's Stone",
        "ano": 2001,
        "imdb": "tt0241527",
        "marca": "warner",
        "diretor": "Chris Columbus",
        "duracao": "2h 32min",
        "generos": ["Aventura", "Família", "Fantasia"],
        "sinopse": "No seu aniversário de 11 anos, Harry descobre que é bruxo e vai estudar "
                   "em Hogwarts, onde um segredo está escondido no castelo.",
        "curiosidades": [
            "Nos Estados Unidos, o filme se chama “Harry Potter and the Sorcerer’s Stone”.",
            "A autora J. K. Rowling exigiu que o elenco principal fosse britânico.",
        ],
        # Onde assistir: plataforma do dono do filme (ou None) e o motivo
        "streaming": "max",
        "streaming_motivo": "A Warner Bros. pertence à Warner Bros. Discovery, dona da HBO Max.",
        "wiki": ("pt", "Harry_Potter_e_a_Pedra_Filosofal_(filme)"),
        "modelo": {
            "uid": "203784d1e8704cfba3af8a2b224b74ff",
            "nome": "Hogwarts Grand Hall",
            "autor": "zack_graham",
            "licenca": "CC BY 4.0",
        },
    },
    {
        "slug": "transformers",
        "titulo": "Transformers",
        "original": "Transformers",
        "ano": 2007,
        "imdb": "tt0418279",
        "marca": "paramount",
        "diretor": "Michael Bay",
        "duracao": "2h 24min",
        "generos": ["Ação", "Aventura", "Ficção científica"],
        "sinopse": "O jovem Sam Witwicky se vê no meio da guerra entre Autobots e "
                   "Decepticons, robôs alienígenas que se disfarçam de veículos.",
        "curiosidades": [
            "Optimus Prime é dublado (em inglês) por Peter Cullen, a mesma voz do desenho dos anos 1980.",
            "O filme foi produzido por Steven Spielberg e dirigido por Michael Bay.",
        ],
        # Onde assistir: plataforma do dono do filme (ou None) e o motivo
        "streaming": "paramount",
        "streaming_motivo": "A Paramount tem a sua própria plataforma, o Paramount+.",
        "wiki": ("en", "Transformers_(film)"),
        "modelo": {
            "uid": "35f9cb09b1b248c7bd6b12912ac8cd3a",
            "nome": "Bumblebee - Optimus Prime Transform Animation",
            "autor": "DIO",
            "licenca": "CC BY 4.0",
        },
    },
    {
        "slug": "shrek",
        "titulo": "Shrek",
        "original": "Shrek",
        "ano": 2001,
        "imdb": "tt0126029",
        "marca": "dreamworks",
        "diretor": "Andrew Adamson e Vicky Jenson",
        "duracao": "1h 30min",
        "generos": ["Animação", "Aventura", "Comédia"],
        "sinopse": "Para ter seu pântano de volta, o ogro Shrek aceita resgatar a princesa "
                   "Fiona, com a ajuda de um Burro que não para de falar.",
        "curiosidades": [
            "Ganhou o primeiro Oscar da história na categoria Melhor Animação, criada em 2002.",
            "O filme brinca o tempo todo com os contos de fadas clássicos da própria Disney.",
        ],
        # Onde assistir: plataforma do dono do filme (ou None) e o motivo
        "streaming": None,
        "streaming_motivo": "A DreamWorks Animation pertence à Universal, que não tem streaming próprio no Brasil, então o filme muda de plataforma de tempos em tempos.",
        "wiki": ("en", "Shrek"),
        "modelo": {
            "uid": "ff6a111c58c94d328b0880a38b912428",
            "nome": "Shrek",
            "autor": "burnt.melon",
            "licenca": "CC BY 4.0",
        },
    },
    {
        "slug": "tubarao",
        "titulo": "Tubarão",
        "original": "Jaws",
        "ano": 1975,
        "imdb": "tt0073195",
        "marca": "universal",
        "diretor": "Steven Spielberg",
        "duracao": "2h 4min",
        "generos": ["Aventura", "Suspense"],
        "sinopse": "Um tubarão-branco gigante ataca banhistas na ilha de Amity, e o chefe de "
                   "polícia, um biólogo marinho e um velho pescador partem para caçá-lo.",
        "curiosidades": [
            "O tubarão mecânico foi apelidado de “Bruce” e quebrava tanto que aparece bem pouco no filme, o que aumentou o suspense.",
            "É considerado o primeiro “blockbuster” de verão da história do cinema.",
        ],
        # Onde assistir: plataforma do dono do filme (ou None) e o motivo
        "streaming": None,
        "streaming_motivo": "A Universal não tem streaming próprio no Brasil, então o filme muda de plataforma de tempos em tempos.",
        "wiki": ("en", "Jaws_(film)"),
        "modelo": {
            "uid": "fbcbc3a96dab42d6a1c1a50c4913c6aa",
            "nome": "Bruce the Great White Shark from JAWS 1975",
            "autor": "AllThingsSaurus",
            "licenca": "CC BY 4.0",
        },
    },
    {
        "slug": "os-cacadores-da-arca-perdida",
        "titulo": "Os Caçadores da Arca Perdida",
        "original": "Raiders of the Lost Ark",
        "ano": 1981,
        "imdb": "tt0082971",
        "marca": "lucasfilm",
        "diretor": "Steven Spielberg",
        "duracao": "1h 55min",
        "generos": ["Ação", "Aventura"],
        "sinopse": "O arqueólogo Indiana Jones corre contra os nazistas para encontrar a "
                   "Arca da Aliança, um artefato que daria poderes ao exército de Hitler.",
        "curiosidades": [
            "Tom Selleck foi a primeira escolha para Indiana Jones, mas não pôde aceitar por causa da série Magnum.",
            "O filme é uma parceria de George Lucas (criador) com Steven Spielberg (diretor).",
        ],
        # Onde assistir: plataforma do dono do filme (ou None) e o motivo
        "streaming": None,
        "streaming_motivo": "A Lucasfilm é da Disney, mas os filmes antigos do Indiana Jones foram lançados pela Paramount, então a plataforma pode variar.",
        "wiki": ("en", "Raiders_of_the_Lost_Ark"),
        "modelo": {
            "uid": "96cd3caac3f44d2583a91175541dd093",
            "nome": "Indiana Jones Hat",
            "autor": "AlexTheBaBa",
            "licenca": "CC BY 4.0",
        },
    },
    {
        "slug": "os-caca-fantasmas",
        "titulo": "Os Caça-Fantasmas",
        "original": "Ghostbusters",
        "ano": 1984,
        "imdb": "tt0087332",
        "marca": "columbia",
        "diretor": "Ivan Reitman",
        "duracao": "1h 45min",
        "generos": ["Ação", "Comédia", "Fantasia"],
        "sinopse": "Três cientistas demitidos abrem uma empresa para caçar fantasmas em Nova "
                   "York, bem quando a cidade vira alvo de um antigo deus sumério.",
        "curiosidades": [
            "O carro Ecto-1 é um Cadillac de 1959 que era usado como ambulância e carro funerário.",
            "A música-tema “Ghostbusters”, de Ray Parker Jr., foi indicada ao Oscar.",
        ],
        # Onde assistir: plataforma do dono do filme (ou None) e o motivo
        "streaming": None,
        "streaming_motivo": "A Columbia Pictures (Sony) não tem streaming próprio no Brasil, então o filme muda de plataforma de tempos em tempos.",
        "wiki": ("en", "Ghostbusters"),
        "modelo": {
            "uid": "cbd3cf6ca77b40a783ab182c8e3ccdcd",
            "nome": "Ecto-1",
            "autor": "kukusa0909",
            "licenca": "CC BY 4.0",
        },
    },
    {
        "slug": "o-rei-leao",
        "titulo": "O Rei Leão",
        "original": "The Lion King",
        "ano": 1994,
        "imdb": "tt0110357",
        "marca": "disney",
        "diretor": "Roger Allers e Rob Minkoff",
        "duracao": "1h 28min",
        "generos": ["Animação", "Aventura", "Drama"],
        "sinopse": "O leãozinho Simba foge do reino depois da morte do pai, armada pelo tio "
                   "Scar, e precisa crescer para voltar e assumir seu lugar como rei.",
        "curiosidades": [
            "A trilha sonora de Hans Zimmer e a música “Can You Feel the Love Tonight”, de Elton John, ganharam o Oscar.",
            "Os animadores estudaram leões de verdade, levados ao estúdio, para desenhar os movimentos.",
        ],
        # Onde assistir: plataforma do dono do filme (ou None) e o motivo
        "streaming": "disney",
        "streaming_motivo": "É um filme da própria Disney, então fica no Disney+.",
        "wiki": ("en", "The_Lion_King"),
        "modelo": {
            "uid": "e6786e860dca4ed588bebfea8d9f3790",
            "nome": "Simba (Lion King)",
            "autor": "KillerBear",
            "licenca": "CC BY 4.0",
        },
    },
    {
        "slug": "titanic",
        "titulo": "Titanic",
        "original": "Titanic",
        "ano": 1997,
        "imdb": "tt0120338",
        "marca": "paramount",
        "diretor": "James Cameron",
        "duracao": "3h 14min",
        "generos": ["Drama", "Romance"],
        "sinopse": "A bordo da viagem inaugural do Titanic, a jovem rica Rose e o artista "
                   "pobre Jack se apaixonam, pouco antes do navio bater num iceberg.",
        "curiosidades": [
            "Ganhou 11 Oscars, empatando com Ben-Hur como o filme mais premiado da história.",
            "As mãos que desenham Rose nas cenas de perto são do próprio diretor, James Cameron.",
        ],
        # Onde assistir: plataforma do dono do filme (ou None) e o motivo
        "streaming": "disney",
        "streaming_motivo": "Fora dos Estados Unidos, o filme é da 20th Century Studios, que pertence à Disney.",
        "wiki": ("en", "Titanic_(1997_film)"),
        "modelo": {
            "uid": "ef2d50dd2f4f458cac4d7bbdad5ab69a",
            "nome": "Rms Titanic",
            "autor": "andreysouzanascimento692",
            "licenca": "CC BY 4.0",
        },
    },
]

# Dicionário para achar um filme pelo slug (o pedaço do endereço depois de /filme/).
# Ex.: FILMES_POR_SLUG["shrek"] devolve o dicionário do Shrek.
FILMES_POR_SLUG = {filme["slug"]: filme for filme in FILMES}

# Plataformas de streaming por assinatura (usadas em "Onde assistir").
# Só indicamos a plataforma quando o dono do filme tem uma no Brasil,
# porque o catálogo das outras muda o tempo todo.
PLATAFORMAS = {
    "disney": {"nome": "Disney+", "url": "https://www.disneyplus.com/pt-br"},
    "max": {"nome": "HBO Max", "url": "https://www.hbomax.com/br/pt"},
    "paramount": {"nome": "Paramount+", "url": "https://www.paramountplus.com/br/"},
}

# Link de cada licença. As licenças Creative Commons pedem que o crédito
# tenha um link para o texto da licença (usado na página de créditos).
LICENCAS = {
    "CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/deed.pt-br",
    "CC BY-NC-SA 4.0": "https://creativecommons.org/licenses/by-nc-sa/4.0/deed.pt-br",
    "Sketchfab Standard (somente visualização)": "https://sketchfab.com/licenses",
}
