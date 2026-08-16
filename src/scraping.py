import requests
from bs4 import BeautifulSoup
from datetime import datetime
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import os
import random
import re

load_dotenv()

_project = AIProjectClient(
    endpoint=os.getenv("FOUNDRY_PROJ_ENDPOINT"),
    credential=DefaultAzureCredential(),
)
client = _project.get_openai_client()

sites = [
    {"nome": "G1 - Economia", "url": "https://g1.globo.com/economia/", "categoria": "economia"},
    {"nome": "CNN Brasil - Economia", "url": "https://www.cnnbrasil.com.br/economia/", "categoria": "economia"},
    {"nome": "Jornal de Notícias (JN)", "url": "https://www.jn.pt/", "categoria": "economia"},
    {"nome": "Diário de Notícias (DN)", "url": "https://www.dn.pt/", "categoria": "economia"},
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

# FONTES RETIRADAS
""" 
{"nome": "Olhar Digital", "url": "https://olhardigital.com.br/", "categoria": "tecnologia"} 
"""

def obter_data_real(link):  
    try:
        resposta = requests.get(link, timeout=5)
        soup = BeautifulSoup(resposta.text, "html.parser")

        time_tag = soup.find("time")
        if time_tag and time_tag.get("datetime"):
            return time_tag["datetime"][:10]

        meta_date = soup.find("meta", {"property": "article:published_time"})
        if meta_date and meta_date.get("content"):
            return meta_date["content"][:10]

        match = re.search(r'/(\d{4})/(\d{2})/(\d{2})/', link)
        if match:
            return f"{match.group(3)}/{match.group(2)}/{match.group(1)}"

    except Exception:
        pass

    return "DATA INDEFINIDA"


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
        "Filtre apenas as notícias RELEVÂNTES sobre ECONOMIA ou TECNOLOGIA publicadas HOJE. "
        "Use a data real fornecida no final de cada linha (Publicado em: ...) para filtrar, e use essa data como 'Data da Notícia'. "
        "IGNORE assuntos como esporte, celebridades, fofocas, pets, mega sena, horóscopo, anúncios e similares. "
        "Ordene as notícias por relevância, e deixe as notícias em inglês por último. "
        "A Data das Notícias podem estar em formatos diferentes, padronize para (DD-MM-YYYY). "
        "Para cada item, devolva no seguinte formato com '|||' como separador:\n\n"
        "Fonte ||| Data da Noticia / Publicacao (DD-MM-YYYY) ||| Título Resumido ||| Categoria ||| Link\n"
    )

    lista_textos = "\n".join(
        f"{n['fonte']} - {n['texto']} - {n['categoria_sugerida']} - {n['link']} - Publicado em: {obter_data_real(n['link'])}"
        for n in raw_noticias
    )

    full_prompt = prompt + lista_textos

    # Modelo AI
    llm = "gpt-5.4-mini : endpoint-azure-foundry"
    temperatura = 0.1

    response = client.chat.completions.create(
        model=llm,
        messages=[{"role": "user", "content": full_prompt}],
        temperature=temperatura,
        max_completion_tokens=1500
    )

    texto = response.choices[0].message.content.strip()
    linhas = texto.split("\n")
    tokens_qtd = response.usage.total_tokens

    # Função para extrair link limpo de "[Texto](URL)"
    def extrair_link_correto(linha):
        match = re.search(r"\((https?://[^\)]+)\)", linha)
        if match:
            return match.group(1)
        return linha.strip()

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
                    "Link da Matéria": extrair_link_correto(link),
                    "Data e Hora da Captura": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Modelo LLM": llm,
                    "Temperatura": temperatura,
                    "Tokens Qtd": tokens_qtd
                })
        except Exception:
            continue
        
        except Exception as e:
            print(f"[ERRO] Linha mal formatada: {linha}")
            print(f"Detalhes: {e}")

    return dados