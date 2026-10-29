"""
Testes automáticos do site.

Eles "visitam" as páginas sem abrir o navegador (usando o test_client do Flask)
e conferem se a resposta está certa. Para rodar:

    python -m unittest -v

Se aparecer "OK" no fim, está tudo funcionando.
"""

import unittest

import aula
import imdb
import noticias
from app import app, destacar_comentarios, formatar_votos, sem_acento
from filmes import FILMES

TOTAL = len(FILMES)  # quantos filmes existem no catálogo


class TestFuncoes(unittest.TestCase):
    """Testa as funções auxiliares do app.py, sem precisar abrir páginas."""

    def test_sem_acento(self):
        self.assertEqual(sem_acento("Anéis"), "aneis")
        self.assertEqual(sem_acento("AÇÃO"), "acao")

    def test_destacar_comentarios(self):
        html = destacar_comentarios('x = 1  # um comentário')
        self.assertEqual(html, 'x = 1  <span class="lousa__comentario"># um comentário</span>')

    def test_todo_codigo_da_aula_tem_comentario(self):
        for etapa in aula.ETAPAS:
            self.assertIn("lousa__comentario", destacar_comentarios(etapa["codigo"]), etapa["titulo"])

    def test_formatar_votos(self):
        self.assertEqual(formatar_votos(1_595_476), "1,6 mi")
        self.assertEqual(formatar_votos(25_300), "25 mil")
        self.assertEqual(formatar_votos(800), "800")


class TestNoticias(unittest.TestCase):
    """Testa a leitura do RSS com um XML de exemplo (sem internet)."""

    def test_ler_rss(self):
        xml = """<rss><channel>
            <item>
              <title>Filme novo estreia nos cinemas - Site de Cinema</title>
              <link>https://exemplo.com/noticia</link>
              <pubDate>Tue, 28 Oct 2026 14:00:00 GMT</pubDate>
              <source url="https://exemplo.com">Site de Cinema</source>
            </item>
        </channel></rss>"""
        lista = noticias.ler_rss(xml)
        self.assertEqual(len(lista), 1)
        self.assertEqual(lista[0]["titulo"], "Filme novo estreia nos cinemas")  # sem " - Site..."
        self.assertEqual(lista[0]["fonte"], "Site de Cinema")
        self.assertEqual(lista[0]["data"], "28/10/2026")


class TestPaginas(unittest.TestCase):
    """Abre as páginas do site e confere o resultado."""

    def setUp(self):
        # setUp roda antes de cada teste.
        # Fingimos que o cache está em dia para os testes não baixarem nada da internet.
        imdb.cache = {
            "atualizado_em": "2999-01-01T00:00:00",
            "notas": {"tt0371746": {"nota": 7.9, "votos": 1_200_000}},
        }
        self.cliente = app.test_client()

    def abrir(self, endereco):
        """Abre um endereço e devolve (código HTTP, HTML da página)."""
        resposta = self.cliente.get(endereco)
        return resposta.status_code, resposta.get_data(as_text=True)

    def test_inicio_tem_intro(self):
        codigo, html = self.abrir("/")
        self.assertEqual(codigo, 200)
        self.assertIn('class="intro', html)

    def test_catalogo_sem_intro(self):
        codigo, html = self.abrir("/catalogo")
        self.assertEqual(codigo, 200)
        self.assertNotIn('class="intro', html)
        self.assertIn(f"{TOTAL} de {TOTAL} filmes", html)

    def test_busca_ignora_acento(self):
        _, html = self.abrir("/catalogo?q=aneis")
        self.assertIn("O Senhor dos Anéis", html)
        self.assertIn(f"1 de {TOTAL} filmes", html)

    def test_busca_sem_resultado(self):
        _, html = self.abrir("/catalogo?q=filme-que-nao-existe")
        self.assertIn("Nenhum filme encontrado", html)

    def test_filtro_por_marca(self):
        _, html = self.abrir("/catalogo?marca=dc")
        self.assertIn("Batman", html)
        self.assertNotIn("Toy Story", html)

    def test_marca_invalida_mostra_tudo(self):
        _, html = self.abrir("/catalogo?marca=xyz")
        self.assertIn(f"{TOTAL} de {TOTAL} filmes", html)

    def test_pagina_do_filme(self):
        codigo, html = self.abrir("/filme/homem-de-ferro")
        self.assertEqual(codigo, 200)
        self.assertIn("Homem de Ferro", html)
        self.assertIn("7.9", html)          # nota do cache falso do setUp
        self.assertIn("sketchfab.com", html)  # o modelo 3D

    def test_filme_sem_nota(self):
        # Shrek não está no cache falso e não há download rodando
        _, html = self.abrir("/filme/shrek")
        self.assertIn("indisponível", html)

    def test_filme_inexistente_da_404(self):
        codigo, html = self.abrir("/filme/nao-existe")
        self.assertEqual(codigo, 404)
        self.assertIn("não está em cartaz", html)

    def test_nome_do_site(self):
        _, html = self.abrir("/catalogo")
        self.assertIn("EntreFrames", html)

    def test_creditos_tem_link_da_licenca(self):
        codigo, html = self.abrir("/creditos")
        self.assertEqual(codigo, 200)
        self.assertIn("creativecommons.org/licenses/by/4.0", html)


class TestMenusNovos(unittest.TestCase):
    """Notícias, Curiosidades, Linha do tempo, Roleta e Modo aula."""

    def setUp(self):
        imdb.cache = {"atualizado_em": "2999-01-01T00:00:00", "notas": {}}
        noticias.cache = {
            "atualizado_em": "2999-01-01T00:00:00",
            "noticias": [{"titulo": "Manchete de teste", "link": "https://exemplo.com",
                          "fonte": "Site X", "data": "29/10/2026"}],
        }
        self.cliente = app.test_client()

    def abrir(self, endereco):
        resposta = self.cliente.get(endereco)
        return resposta.status_code, resposta.get_data(as_text=True)

    def test_noticias(self):
        codigo, html = self.abrir("/noticias")
        self.assertEqual(codigo, 200)
        self.assertIn("Manchete de teste", html)

    def test_curiosidades(self):
        codigo, html = self.abrir("/curiosidades")
        self.assertEqual(codigo, 200)
        self.assertIn("Bruce", html)  # curiosidade do Tubarão

    def test_linha_do_tempo_em_ordem(self):
        codigo, html = self.abrir("/linha-do-tempo")
        self.assertEqual(codigo, 200)
        # Tubarão (1975) tem que aparecer antes de Ultimato (2019)
        self.assertLess(html.index("Tubarão"), html.index("Vingadores: Ultimato"))

    def test_roleta_respeita_filtro(self):
        for _ in range(10):  # sorteio: testamos várias vezes
            _, html = self.abrir("/roleta?marca=pixar&girar=1")
            self.assertIn("A roleta escolheu", html)
            self.assertIn('<h2 class="roleta__titulo">Toy Story</h2>', html)

    def test_roleta_sem_resultado(self):
        _, html = self.abrir("/roleta?genero=Romance&marca=marvel&girar=1")
        self.assertIn("Nenhum filme do catálogo combina", html)

    def test_todas_as_etapas_da_aula(self):
        for numero in range(1, len(aula.ETAPAS) + 1):
            codigo, html = self.abrir(f"/aula/{numero}")
            self.assertEqual(codigo, 200)
            self.assertIn(aula.ETAPAS[numero - 1]["quem"], html)

    def test_etapa_inexistente_da_404(self):
        codigo, _ = self.abrir(f"/aula/{len(aula.ETAPAS) + 1}")
        self.assertEqual(codigo, 404)

    def test_roteiro_tem_os_quatro(self):
        _, html = self.abrir("/aula/roteiro")
        for nome in aula.INTEGRANTES:
            self.assertIn(nome, html)

    def test_onde_assistir(self):
        codigo, html = self.abrir("/onde-assistir")
        self.assertEqual(codigo, 200)
        self.assertIn('id="homem-de-ferro"', html)  # âncora do filme
        self.assertIn("Disney+", html)               # Marvel -> Disney+
        self.assertIn("HBO Max", html)               # DC -> HBO Max
        self.assertIn("justwatch.com/br/busca?q=Shrek", html)

    def test_roleta_tem_botao_onde_assistir(self):
        _, html = self.abrir("/roleta?marca=pixar&girar=1")
        self.assertIn("/onde-assistir#toy-story", html)

    def test_rodape(self):
        _, html = self.abrir("/catalogo")
        self.assertIn("A2 Desenvolvimento Front-end para Web", html)

    def test_botao_modo_aula_no_topo(self):
        _, html = self.abrir("/catalogo")
        self.assertIn('class="botao-aula"', html)


if __name__ == "__main__":
    unittest.main()
