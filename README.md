# 🕵️ Quem Matou Joffrey?

Aplicação web desenvolvida como projeto acadêmico da disciplina de **Estrutura de Dados**, inspirada no universo de *Game of Thrones*. O projeto apresenta uma investigação fictícia sobre a morte de Joffrey Baratheon, utilizando estruturas de dados e algoritmos para organizar evidências, relacionar suspeitos e analisar informações.

## 🌐 Acesse o projeto

**Site publicado:** (https://quem-matou-joffrey.onrender.com/)

**Repositório:** https://github.com/Gisele0304/Quem-Matou-Joffrey

## 🎯 Objetivo

Demonstrar, de maneira prática e interativa, a aplicação de estruturas de dados e algoritmos na resolução de um problema investigativo, utilizando suspeitos, evidências e relações entre os elementos da investigação.

## ⚙️ Funcionalidades

- **Suspeitos:** visualização dos personagens envolvidos na investigação.
- **Evidências:** cadastro, consulta e organização das evidências.
- **Estruturas de dados:** utilização de lista sequencial, lista encadeada, pilha, fila, deque e tabela hash.
- **Grafo interativo:** representação das relações entre suspeitos e evidências, permitindo adicionar e remover conexões.
- **Mapa:** visualização das evidências e de suas respectivas localizações.
- **Ordenação:** comparação dos algoritmos Bubble Sort, Insertion Sort, Selection Sort e Quick Sort, considerando a importância das evidências.

## 🧰 Tecnologias utilizadas

- Python
- Flask
- NetworkX
- HTML
- CSS
- JavaScript
- JSON para armazenamento dos dados

## 📁 Estrutura do projeto

```text
Quem-Matou-Joffrey/
│
├── web/
│   ├── app.py
│   ├── dados.py
│   ├── estruturas.py
│   ├── tabela_hash.py
│   ├── grafos.py
│   ├── ordenacao.py
│   ├── evidencias.json
│   ├── relacoes.json
│   ├── requirements.txt
│   │
│   ├── templates/
│   └── static/
│
└── README.md
```

## ▶️ Como executar localmente

**1. Clone o repositório:**

```bash
git clone https://github.com/Gisele0304/Quem-Matou-Joffrey.git
```

**2. Entre na pasta da aplicação web:**

```bash
cd Quem-Matou-Joffrey/web
```

**3. Crie um ambiente virtual:**

```bash
python -m venv .venv
```

**4. Ative o ambiente virtual no Windows:**

```bash
.venv\Scripts\activate
```

**5. Instale as dependências:**

```bash
pip install -r requirements.txt
```

**6. Execute a aplicação:**

```bash
python app.py
```

**7. Acesse no navegador:**

```text
http://127.0.0.1:5000
```

## 📚 Contexto acadêmico

Este projeto foi desenvolvido com finalidade educacional, buscando relacionar os conceitos teóricos de Estrutura de Dados com uma aplicação prática e interativa.

A temática de *Game of Thrones* foi escolhida para tornar a investigação mais dinâmica e facilitar a compreensão das estruturas de dados e dos algoritmos utilizados.

---

**Desenvolvimento:** Projeto acadêmico – Estrutura de Dados.
**Autores:** Gisele Amorim, Emerson Danillo
