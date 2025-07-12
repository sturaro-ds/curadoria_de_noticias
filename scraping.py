import requests
from bs4 import BeautifulSoup
from datetime import datetime
import openai
from dotenv import load_dotenv
import os
import random

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

sites = [
    {"nome": "G1 - Economia", "url": "https://g1.globo.com/economia/", "categoria": "economia"},
    {"nome": "CNN Brasil - Economia", "url": "https://www.cnnbrasil.com.br/economia/", "categoria": "economia"},
    {"nome": "Jornal de Notícias (JN)", "url": "https://www.jn.pt/", "categoria": "economia"},
    {"nome": "Diário de Notícias (DN)", "url": "https://www.dn.pt/", "categoria": "economia"},
    {"nome": "Olhar Digital", "url": "https://olhardigital.com.br/", "categoria": "tecnologia"},
    {"nome": "Expresso", "url": "https://expresso.pt/", "categoria": "economia"},
    {"nome": "Público", "url": "https://www.publico.pt/", "categoria": "economia"},
    {"nome": "CNN Internacional", "url": "https://edition.cnn.com/", "categoria": "economia"},
    {"nome": "The Economist", "url": "https://www.economist.com/", "categoria": "economia"},
    {"nome": "Towards Data Science", "url": "https://towardsdatascience.com/", "categoria": "tecnologia"},
    {"nome": "TechCrunch", "url": "https://techcrunch.com/", "categoria": "tecnologia"},
    {"nome": "TechTudo", "url": "https://www.techtudo.com.br/", "categoria": "tecnologia"},
    {"nome": "Bloomberg", "url": "https://www.bloomberg.com", "categoria": "economia"},
    {"nome": "Financial Times (FT)", "url": "https://www.ft.com", "categoria": "economia"},
    {"nome": "Reuters – Business News", "url": "https://www.reuters.com/finance", "categoria": "economia"},
    {"nome": "Wall Street Journal (WSJ)", "url": "https://www.wsj.com", "categoria": "economia"},
    {"nome": "The Verge", "url": "https://www.theverge.com", "categoria": "tecnologia"},
    {"nome": "Wired", "url": "https://www.wired.com", "categoria": "tecnologia"},
    {"nome": "Ars Technica", "url": "https://arstechnica.com", "categoria": "tecnologia"},
    {"nome": "Estadão – Economia", "url": "https://economia.estadao.com.br", "categoria": "economia"},
    {"nome": "Exame – Economia", "url": "https://exame.com/economia", "categoria": "economia"},
    {"nome": "InfoMoney", "url": "https://www.infomoney.com.br", "categoria": "economia"},
    {"nome": "Folha de S.Paulo – Mercado", "url": "https://www1.folha.uol.com.br/mercado", "categoria": "economia"},
    {"nome": "Canaltech", "url": "https://www.canaltech.com.br", "categoria": "tecnologia"},
    {"nome": "Startups.com.br", "url": "https://startups.com.br", "categoria": "tecnologia"},
    {"nome": "Tilt (UOL)", "url": "https://www.uol.com.br/tilt", "categoria": "tecnologia"},
]

random.shuffle(sites)

def extrair_links(site):
    try:
        r = requests.get(site["url"], timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")
        links = []

        for a in soup.find_all("a", href=True):
            texto = a.get_text(strip=True)
            href = a["href"]

            if texto and len(texto) > 40 and href.startswith("http"):
                links.append({
                    "fonte": site["nome"],
                    "categoria_sugerida": site["categoria"],
                    "texto": texto,
                    "link": href
                })

        return links
    except Exception:
        return []

def coletar_noticias_filtradas():
    raw_noticias = []
    for site in sites:
        raw_noticias.extend(extrair_links(site))

    prompt = (
        "Filtre apenas as notícias que sejam relevantes sobre ECONOMIA ou TECNOLOGIA. "
        "Ignore assuntos como esporte, celebridades, fofocas ou anúncios. "
        "Selecione para cada site apenas uma das noticias, escolha a mais relevante. "
        "Ordene as notícias por relevância, e deixe as notícias em inglês por último. "
        "Para cada item relevante, devolva no seguinte formato, usando '|||' como separador:\n\n"
        "Fonte ||| Data e Hora da Notícia (DD-MM-YYYY às HH:MM) ||| Título Resumido ||| Categoria: Economia/Tecnologia ||| Link da Notícia\n\n"
        "A Data e Hora das Notícias podem estar em formatos diferentes, padronize para (DD-MM-YYYY às HH:MM) "
    )

    lista_textos = "\n".join(
        f"{n['fonte']} - {n['texto']} - {n['categoria_sugerida']} - {n['link']}" for n in raw_noticias
    )

    full_prompt = prompt + lista_textos

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.4,
        max_tokens=3000
    )

    texto = response.choices[0].message.content.strip()
    linhas = texto.split("\n")
    dados = []

    for linha in linhas:
        try:
            partes = linha.split(" ||| ")
            if len(partes) == 5:
                fonte, data_hora, resumo, categoria, link = partes
                dados.append({
                    "Data da Notícia": data_hora.strip(),
                    "Fonte": fonte.strip(),
                    "Categoria": categoria.strip(),
                    "Resumo": resumo.strip(),
                    "Link da Matéria": link.strip(),
                    "Data e Hora da Captura": datetime.now().strftime("%Y-%m-%d %H:%M"),
                })
        except Exception:
            continue
        
        except Exception as e:
            print(f"[ERRO] Linha mal formatada: {linha}")
            print(f"Detalhes: {e}")

    return dados

# testes
coletar_noticias_filtradas()