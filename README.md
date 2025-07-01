## 📰 Projeto: Curadoria Inteligente de Notícias sobre Economia e Tecnologia

Este é um projeto pessoal de uso real no meu dia a dia.

Aplicação web desenvolvida em **Python + Flask**, que realiza a **coleta automatizada de notícias** a partir de fontes confiáveis e utiliza **modelos da OpenAI** para **filtrar e resumir as mais relevantes** nas áreas de **Economia** e **Tecnologia**. A interface web exibe as manchetes com resumos gerados por IA, além de apresentar o link para navegar ao site e visualizar a notícia na integra.

---

### 🚀 Escopo do Projeto

- 🔎 Web scraping com `requests` e `BeautifulSoup`
- 🤖 Filtragem e resumo das notícias com `openai` (GPT-4o-mini)
- 🌐 Interface web com `Flask`
- 📸 Exibição de perfil com foto e link do LinkedIn
- 🐳 Deploy com Docker

---

### 🧠 Tecnologias utilizadas

- Python=3.11
- Flask=3.0.3
- Requests=2.32.3
- BeautifulSoup=4.13.4
- Python Dotenv=1.1.0
- OpenAI_API=gpt40-mini
- Docker

---

### 🛠 Como executar localmente

#### 1. Clone este repositório em uma pasta local

```bash
git clone https://github.com/sturaro-ds/curadoria_de_noticias.git
```

#### 2. Adicione sua chave da OpenAI no arquivo `.env`

Na pasta onde clonou o repositório, crie um arquivo `.env` com o seguinte conteúdo:

```
OPENAI_API_KEY=sua-chave-aqui
```

---

### 🐳 Rodando com Docker

#### Build da imagem:

```bash
docker build -t noticias-app .
```

#### Executando o contêiner:

```bash
docker run -p 8000:8000 noticias-app
```

#### Acesse no navegador:

[http://localhost:8000](http://localhost:8000)

---

### 👤 Sobre o autor

**Claudio Sturaro**  
Data Scientist at Lefosse  
MBA USP/ESALQ – Data Science  
MBA FGV – Gestão de Processos  
[Ver perfil no LinkedIn](https://www.linkedin.com/in/claudiosturaro/)

---

### 📄 Licença

Este projeto está licenciado sob a **MIT License**.
