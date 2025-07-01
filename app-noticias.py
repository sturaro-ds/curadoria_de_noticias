from flask import Flask, render_template_string
from scraping import coletar_noticias_filtradas

app = Flask(__name__)

@app.route('/')
def exibir_noticias():
    noticias = coletar_noticias_filtradas()

    html = """<!DOCTYPE html>
    <html>
        <head>
            <title>Notícias Relevantes</title>
            <style>
                body {
                    font-family: 'Segoe UI', sans-serif;
                    margin: 0;
                    padding: 80px 40px 40px 40px;
                    background: linear-gradient(120deg, #f6f9fc, #e0eafc);
                }
                header {
                    display: flex;
                    align-items: center;
                    padding: 30px 0;
                    border-bottom: 2px solid #ccc;
                }
                .perfil img {
                    width: 90px;
                    height: 90px;
                    border-radius: 50%;
                    margin-right: 20px;
                    border: 2px solid #444;
                }
                .perfil-info h2 {
                    margin: 0;
                }
                .perfil-info p {
                    margin: 4px 0;
                }
                .perfil-info a {
                    text-decoration: none;
                    color: #0a66c2;
                    font-weight: bold;
                }
                h1 {
                    margin-top: 30px;
                }
                h3 {
                    color: #555;
                    font-weight: normal;
                    margin-top: -10px;
                    margin-bottom: 10px;
                }
                h4 {
                    color: #666;
                    font-weight: normal;
                    margin-top: 0;
                    margin-bottom: 30px;
                }
                ul {
                    list-style: none;
                    padding: 0;
                }
                li {
                    background: #ffffffcc;
                    margin-bottom: 20px;
                    padding: 20px;
                    border-left: 5px solid #0a66c2;
                    border-radius: 8px;
                    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
                }
                li a {
                    color: #0a66c2;
                    text-decoration: none;
                }
                li strong {
                    font-size: 1.1em;
                }
            </style>
        </head>
        <body>
            <div class="perfil">
                <img src="/static/claudio.jpg" alt="Foto Claudio">
                <div class="perfil-info">
                    <h2>Claudio Sturaro</h2>
                    <p>Data Scientist at Lefosse | MBA USP Data Science | MBA FGV Gestão de Processos</p>
                    <p><a href="https://www.linkedin.com/in/claudiosturaro/" target="_blank">Ver perfil no LinkedIn</a></p>
                </div>
            </div>

            <h1>Principais Notícias sobre Economia e Tecnologia 📰</h1>
            <h3>Curadoria inteligente de fontes confiáveis com resumos por Inteligência Artificial</h3>
            <h4>Projeto desenvolvido com Python, Flask, BeautifulSoup, LLMs da OpenAI e Docker</h4>

            <ul>
            {% for noticia in noticias %}
                <li>
                    <strong>{{ noticia['Resumo'] }}</strong><br>
                    Fonte: {{ noticia['Fonte'] }} – {{ noticia['Categoria'] }}<br>
                    Publicado: {{ noticia['Data da Notícia'] }}<br>
                    <a href="{{ noticia['Link da Matéria'] }}" target="_blank">Ler matéria na íntegra</a>
                </li>
            {% endfor %}
            </ul>
        </body>
    </html>
    """
    return render_template_string(html, noticias=noticias)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
