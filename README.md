# 📚 MkDocs Institucional

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python)](https://www.python.org/) [![Status: WIP](https://img.shields.io/badge/status-WIP-yellow)](https://github.com/rafaelmarzulo/mkdocs-institucional)

Documentação técnica e operacional dos sistemas da Diretoria de Tecnologia da Informação – .

## 🚀 Visão Geral
- **Tema:** Material for MkDocs  
- **Navegação:** Cards automáticos por diretório  
- **Painel Web:** Criar, editar e gerenciar Markdown  
- **Automação:** Scripts Python geram índices dinâmicos  
- **Estilo:** Cores e SVG seguindo identidade visual personalizada  

## 🛠️ Como Rodar Localmente
```bash
# 1. Clone o repositório
git clone https://github.com/rafaelmarzulo/mkdocs-institucional.git
cd mkdocs-institucional

# 2. Ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Inicie o servidor
mkdocs serve

# Acesse http://localhost:8000
```

## 📁 Estrutura do Projeto
```
mkdocs-institucional/
├── docs/
│   ├── apis/
│   ├── assets/
│   ├── documentacao/
│   ├── instalacao/
│   ├── usuario-final/
│   ├── visao-geral/
│   └── index.md
├── overrides/
├── painel/             (FastAPI panel)
├── scripts/            (Automação de índices)
├── site/               (Build estático)
├── mkdocs.yml          (Configuração)
└── requirements.txt
```

## 📸 Capturas de Tela
![Painel Editor Markdown](https://user-images.githubusercontent.com/SEU_USUARIO/000000/painel-editor.png)
![Home com Cards](https://user-images.githubusercontent.com/SEU_USUARIO/000000/home-cards.png)

## ⚙️ Automatizações
- Geração automática de `index.md` em cada diretório Markdown.  
- Exclusão de arquivos `_old.md` e `.bkp`.  
- Frontmatter opcional para descrições customizadas.

## 🔒 Proteção e Deploy
- Deploy em Ubuntu 24.04+ com Nginx ou Apache.  
- Proteção de painel via autenticação básica (FastAPI).  
- Gerar site estático com `mkdocs build` (diretório `site/`).  

---

> Desenvolvido por Rafael Marzulo  
> [GitHub](https://github.com/rafaelmarzulo) • [Email](mailto:rafael@example.com)  