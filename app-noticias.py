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
        <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/21/21601.png" type="image/png">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
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
                gap: 20px;
                padding: 30px 0;
                border-bottom: 2px solid #ccc;
                flex-wrap: wrap;
            }

            .perfil img {
                width: 140px;
                height: 140px;
                border-radius: 50%;
                border: 2px solid #444;
                object-fit: cover;
            }

            .perfil-info {
                flex: 1;
                min-width: 250px;
                margin-left: -5px;
            }

            .perfil-info h2 {
                margin: 0 0 5px 0;
                font-size: 1.6rem;
            }

            .perfil-info p {
                margin: 4px 0;
                font-size: 1rem;
                color: #333;
            }

            .perfil-info .links a {
                display: inline-block;
                text-decoration: none;
                padding: 6px 12px;
                margin-right: 10px;
                margin-top: 10px;
                border-radius: 6px;
                color: white;
                font-weight: 500;
                transition: 0.3s;
            }

            .perfil-info .links a.linkedin {
                background-color: #0a66c2; /* cor oficial LinkedIn */
            }

            .perfil-info .links a.github {
                background-color: #333; /* cor escura típica do GitHub */
            }

            .perfil-info .links a.linkedin:hover {
                background-color: #004182;
            }

            .perfil-info .links a.github:hover {
                background-color: #000;
            }

            .perfil-info .links a:hover {
                background-color: #e0e0e0;
                color: #000;
            }

            .container {
                max-width: 900px;
                margin: 40px auto;
                padding: 0 20px;
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

            @media (max-width: 600px) {
                header {
                    flex-direction: column;
                    align-items: flex-start;
                }
            }
        </style>
    </head>
    <body>
        <header>
            <div class="perfil">
                <img src="/static/fotoperfil.png" alt="Foto Claudio">
            </div>
            <div class="perfil-info">
                <h2>Claudio Sturaro</h2>
                <p>Data Scientist at Lefosse</p>
                <p>MBA USP Data Science | MBA FGV Gestão de Processos</p>
                <div class="links">
                    <a href="https://www.linkedin.com/in/claudiosturaro/" target="_blank" class="linkedin">
                        <i class="fab fa-linkedin"></i> LinkedIn
                    </a>
                    <a href="https://github.com/sturaro-ds/curadoria_de_noticias" target="_blank" class="github">
                        <i class="fab fa-github"></i> GitHub
                    </a>
                </div>
            </div>
        </header>

        <h1>Principais notícias sobre Economia e Tecnologia </h1>
        <h3>Curadoria inteligente de fontes confiáveis com resumos por Inteligência Artificial</h3>
        <h4>Projeto desenvolvido com Python, Flask, BeautifulSoup, LLM da OpenAI e Docker</h4>

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
