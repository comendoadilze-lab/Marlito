#!/usr/bin/env python3
"""
Gera index.html a partir de template.html, preenchendo com as notícias
internacionais mais recentes, em português, organizadas por categoria.

Fontes gratuitas (RSS público), sem necessidade de chave de API.
"""

import re
import html
import datetime
from pathlib import Path

import feedparser

ROOT = Path(__file__).parent
TEMPLATE_PATH = ROOT / "template.html"
OUTPUT_PATH = ROOT / "index.html"

# Feeds em português, organizados por categoria.
FEEDS = {
    "mundo": [
        "https://feeds.bbci.co.uk/portuguese/rss.xml",
        "https://rss.dw.com/rdf/rss-por-all",
    ],
    "tecnologia": [
        "https://www.tecmundo.com.br/rss",
        "https://olhardigital.com.br/feed/",
    ],
    "ciencia": [
        "https://super.abril.com.br/feed/",
    ],
    "cultura": [
        "https://www.omelete.com.br/feed",
    ],
}

MAX_POR_CATEGORIA = 3
MAX_HERO_SIDE = 3
RESUMO_MAX_CHARS = 220


def limpar_html(texto):
    if not texto:
        return ""
    texto = re.sub(r"<[^>]+>", " ", texto)
    texto = html.unescape(texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def truncar(texto, limite):
    if len(texto) <= limite:
        return texto
    corte = texto[:limite].rsplit(" ", 1)[0]
    return corte + "…"


def coletar(feeds):
    itens = []
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            fonte = feed.feed.get("title", url)
            for entrada in feed.entries:
                titulo = limpar_html(entrada.get("title", "")).strip()
                link = entrada.get("link", "")
                resumo = limpar_html(
                    entrada.get("summary", entrada.get("description", ""))
                )
                if not titulo or not link:
                    continue

                if entrada.get("published_parsed"):
                    data_pub = datetime.datetime(*entrada.published_parsed[:6])
                elif entrada.get("updated_parsed"):
                    data_pub = datetime.datetime(*entrada.updated_parsed[:6])
                else:
                    data_pub = datetime.datetime.min

                itens.append(
                    {
                        "titulo": titulo,
                        "link": link,
                        "resumo": truncar(resumo, RESUMO_MAX_CHARS),
                        "fonte": fonte,
                        "data": data_pub,
                    }
                )
        except Exception as erro:
            print(f"Aviso: falha ao ler feed {url}: {erro}")
            continue

    vistos = set()
    unicos = []
    for item in sorted(itens, key=lambda x: x["data"], reverse=True):
        chave = item["titulo"].lower()
        if chave in vistos:
            continue
        vistos.add(chave)
        unicos.append(item)
    return unicos


def render_card(item):
    titulo = html.escape(item["titulo"])
    link = html.escape(item["link"])
    fonte = html.escape(item["fonte"])
    resumo = html.escape(item["resumo"])
    return f"""<article class="card">
      <h3><a href="{link}" target="_blank" rel="noopener">{titulo}</a></h3>
      <p>{resumo}</p>
      <div class="fonte">{fonte}</div>
    </article>"""


def render_side_item(item):
    titulo = html.escape(item["titulo"])
    link = html.escape(item["link"])
    return f"""<div class="side-item">
      <h3><a href="{link}" target="_blank" rel="noopener">{titulo}</a></h3>
      <div class="fonte">{html.escape(item["fonte"])}</div>
    </div>"""


def main():
    coletados = {cat: coletar(urls) for cat, urls in FEEDS.items()}

    if not coletados["mundo"]:
        print("Nenhuma notícia de Mundo encontrada — mantendo index.html atual.")
        return

    manchete = coletados["mundo"][0]
    hero_side = coletados["mundo"][1 : 1 + MAX_HERO_SIDE]

    blocos = {}
    for cat, itens in coletados.items():
        inicio = 1 if cat == "mundo" else 0
        selecionados = itens[inicio : inicio + MAX_POR_CATEGORIA]
        if not selecionados:
            blocos[cat] = (
                '<p style="grid-column:1/-1;color:var(--muted);font-size:0.9rem;">'
                "Sem novas matérias no momento nesta categoria.</p>"
            )
        else:
            blocos[cat] = "\n".join(render_card(i) for i in selecionados)

    agora = datetime.datetime.now()
    meses = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
    ]
    data_longa = f"{agora.day} de {meses[agora.month - 1]} de {agora.year}"

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    saida = (
        template
        .replace("{{DATE_LONG}}", data_longa)
        .replace("{{LEAD_TITLE}}", html.escape(manchete["titulo"]))
        .replace("{{LEAD_SUMMARY}}", html.escape(manchete["resumo"]))
        .replace("{{LEAD_SOURCE}}", html.escape(manchete["fonte"]))
        .replace("{{HERO_SIDE_ITEMS}}", "\n".join(render_side_item(i) for i in hero_side))
        .replace("{{MUNDO_ITEMS}}", blocos["mundo"])
        .replace("{{TECNOLOGIA_ITEMS}}", blocos["tecnologia"])
        .replace("{{CIENCIA_ITEMS}}", blocos["ciencia"])
        .replace("{{CULTURA_ITEMS}}", blocos["cultura"])
    )

    OUTPUT_PATH.write_text(saida, encoding="utf-8")
    print(f"index.html gerado com sucesso — manchete: {manchete['titulo']}")


if __name__ == "__main__":
    main()
