import requests
from bs4 import BeautifulSoup
from datetime import datetime
import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

sites = [
    {"nome": "Valor Econômico", "url": "https://valor.globo.com/", "categoria": "economia"},
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
    {"nome": "Olhar Digital", "url": "https://olhardigital.com.br/", "categoria": "tecnologia"},
]

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
        "Para cada item relevante, devolva no seguinte formato, usando '|||' como separador:\n\n"
        "Fonte ||| Data e Hora (YYYY-MM-DD HH:MM) ||| Título Resumido ||| Categoria: Economia/Tecnologia ||| Link\n\n"
    )

    lista_textos = "\n".join(
        f"{n['fonte']} - {n['texto']} - {n['categoria_sugerida']} - {n['link']}" for n in raw_noticias
    )

    full_prompt = prompt + lista_textos

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.4,
        max_tokens=2000
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