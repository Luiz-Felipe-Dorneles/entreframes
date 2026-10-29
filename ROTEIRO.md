# Roteiro da apresentação: EntreFrames

Integrantes: Cauã, João, Ryan, Mateus. São 12 etapas, 3 por pessoa, cerca de 1 minuto cada (12 a 15 minutos no total).

## Antes de começar

1. Rode `python baixar_posteres.py` e depois `python app.py` (com internet, para os modelos 3D, as notas e as notícias carregarem).
2. Abra http://127.0.0.1:5000/aula no navegador e aperte `F11` para tela cheia.
3. Use **Próximo →** e **← Anterior** no rodapé da lousa. As bolinhas mostram a inicial de quem apresenta cada etapa.
4. O link **Mostrar no site** abre a página certa numa aba nova. Mostre e volte para a aba da lousa.
5. Este mesmo roteiro também está no site, em http://127.0.0.1:5000/aula/roteiro.

> Não precisa decorar: use as falas como guia e fale com as suas palavras.

## Cauã

### Etapa 1: O que é o EntreFrames?

*Mostrar no site:* `/catalogo`

> Boa tarde! Nós somos o Cauã, o João, o Ryan e o Mateus, e vamos apresentar o EntreFrames, um portal de filmes famosos. Em cada filme dá para ver a nota do IMDb e explorar um modelo 3D. O site foi feito com Python, usando o Flask, mais HTML e CSS. Uma escolha nossa foi não escrever JavaScript: tudo o que é interativo, como busca, filtros e a roleta, funciona com formulários que o Python processa. Cada endereço do site, como /catalogo, é ligado a uma função Python, como vocês veem na lousa.

### Etapa 2: Identidade visual: nome, ícone e cores

> O nome EntreFrames vem do fato de que um filme é uma sequência de quadros, os frames. O ícone mostra isso: uma fita de filme com um play entre dois quadros. As cores foram escolhidas pensando na experiência de ir ao cinema: o fundo quase preto é a sala com a luz apagada, e deixa o pôster e o modelo 3D em destaque. O vermelho é o das cortinas e poltronas. O amarelo é a cor oficial do IMDb, então sempre que aparece uma nota ele está lá. E o texto é um creme, parecido com a luz do projetor, que cansa menos a vista que o branco puro. Todas as cores ficam em variáveis do CSS, então trocar uma cor no site inteiro é mudar uma linha.

### Etapa 3: A intro de cinema só com CSS

*Mostrar no site:* `/`

> Quando abrimos o site, aparece uma sala de cinema. Ao clicar, a tela amplia, as cortinas abrem e o catálogo aparece. Isso foi feito só com CSS. O truque é um checkbox escondido: a sala inteira é o label dele, então clicar em qualquer lugar marca o checkbox. Todas as animações começam pausadas, e o seletor :checked muda para running. Agora passo para o João, que vai explicar como as páginas são montadas.

## João

### Etapa 4: Como o Flask monta uma página

*Mostrar no site:* `/filme/shrek`

> Toda página segue o mesmo caminho. O navegador pede um endereço, por exemplo /filme/shrek. O Flask vê que esse endereço combina com a rota /filme/<slug> e chama a função filme, passando 'shrek' como slug. A função procura o filme e, se não existir, devolve o erro 404. Se existir, ela chama o render_template, que pega o arquivo filme.html e troca as marcações com chaves duplas pelos dados do filme. O resultado é o HTML que chega no navegador.

### Etapa 5: Onde ficam os dados dos filmes

*Mostrar no site:* `/catalogo`

> Os dados dos filmes ficam no arquivo filmes.py, numa lista de dicionários. Cada dicionário é um filme, com título, ano, diretor, o código do filme no IMDb e o código do modelo 3D. Não usamos banco de dados porque são poucos filmes e eles quase não mudam. Na hora de mostrar, a função montar junta esses dados fixos com o que muda, como a nota do IMDb e os links do pôster e do modelo.

### Etapa 6: Busca, filtro por marca e ordenação

*Mostrar no site:* `/catalogo?q=aneis`

> A busca é um formulário HTML normal. Quando você clica em Buscar, o navegador coloca o texto na URL, depois do ponto de interrogação, e o Python lê com request.args. Para a busca não depender de acento, a função sem_acento separa cada letra do seu acento e joga o acento fora. Por isso, se eu buscar 'aneis' sem acento, o Senhor dos Anéis aparece. Agora o Ryan vai mostrar a parte do 3D.

## Ryan

### Etapa 7: Como os modelos 3D aparecem

*Mostrar no site:* `/filme/homem-de-ferro`

> Os modelos 3D não ficam no nosso projeto. Eles estão no Sketchfab, um site onde artistas publicam modelos 3D. Cada modelo tem um código, o uid. Com esse código, o Python monta o endereço de embed, e o template coloca esse endereço num iframe, que é uma janela para outra página dentro da nossa. Quem desenha o 3D é o visualizador do Sketchfab, então não precisamos escrever código 3D. Como os modelos têm licença Creative Commons, que exige dar crédito ao autor, fizemos a página Créditos 3D com o autor e o link da licença.

### Etapa 8: Os pôsteres vêm da Wikipédia

*Mostrar no site:* `/catalogo`

> Os pôsteres são baixados por um script separado, o baixar_posteres.py, que rodamos uma vez. Ele usa a API da Wikipédia: pede o resumo da página de cada filme, que vem em JSON, e pega o endereço da imagem principal, que é o pôster. A imagem fica salva no projeto, então o site não depende da Wikipédia para funcionar. O script também espera um pouco entre um pedido e outro, para não sobrecarregar o site deles.

### Etapa 9: Linha do tempo, Roleta e Onde assistir

*Mostrar no site:* `/roleta`

> Também criamos dois menus. A Linha do tempo mostra os filmes do catálogo por ordem de lançamento, separados por década. Para achar a década, dividimos o ano por 10 sem resto e multiplicamos por 10. A Roleta responde à pergunta 'o que eu assisto hoje?': você escolhe um gênero ou uma marca, o Python filtra os filmes e o random.choice sorteia um. A animação de girar é feita com CSS. Depois de sortear, o botão Onde assistir leva direto para aquele filme no menu Onde assistir, usando uma âncora: o endereço termina com # e o slug do filme. Nesse menu mostramos o streaming do dono do filme, como Disney+ para a Marvel, e um link para o JustWatch, porque os catálogos mudam toda hora. Agora o Mateus vai falar dos dados que vêm da internet.

## Mateus

### Etapa 10: As notas do IMDb

*Mostrar no site:* `/catalogo?ordem=nota`

> O IMDb não tem uma API gratuita, mas publica todo dia um arquivo com a nota de todos os títulos que existem. Esse arquivo é grande, então não dá para baixar a cada visita. O nosso código baixa o arquivo, lê linha por linha e guarda só os nossos filmes num JSON, que chamamos de cache. O site lê o cache, que é rápido. Quando o cache passa de um dia, o download é feito de novo numa thread, que é uma tarefa em segundo plano, para o site não ficar travado esperando. E se não tiver internet, o site continua com as notas antigas.

### Etapa 11: Notícias ao vivo com RSS

*Mostrar no site:* `/noticias`

> A página de notícias mostra manchetes reais de cinema. Para isso usamos RSS, um formato em XML que os sites publicam com as suas últimas notícias. Pegamos o RSS do Google Notícias, que junta vários sites brasileiros. O Python lê o XML com a biblioteca xml.etree, que já vem com ele, e pega o título, o link e o nome do site de cada notícia. Reaproveitamos a mesma ideia do IMDb: as notícias ficam num cache que é atualizado a cada três horas.

### Etapa 12: Testes, acessibilidade e conclusão

> Para ter certeza de que tudo funciona, escrevemos testes automáticos. Eles abrem as páginas sem navegador e conferem o resultado, por exemplo se a busca sem acento acha o Senhor dos Anéis. Se alguém mexer no código e quebrar algo, o teste avisa. Também cuidamos da acessibilidade: as imagens têm texto alternativo, dá para usar tudo pelo teclado, e quem ativa 'reduzir movimento' no sistema vê animações mais curtas. O site também se adapta ao celular. Esse foi o EntreFrames. Obrigado, e estamos abertos a perguntas!
