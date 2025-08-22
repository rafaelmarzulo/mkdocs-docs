# 📚 Plataforma MkDocs com Painel Web para Gestão de Documentação Técnica

![GitHub last commit](https://img.shields.io/github/last-commit/SEU_USUARIO/SEU_REPO?style=flat-square)
![Python](https://img.shields.io/badge/python-3.12-blue?style=flat-square)
![License](https://img.shields.io/github/license/SEU_USUARIO/SEU_REPO?style=flat-square)

Documentação técnica e operacional dos sistemas da Diretoria de Tecnologia da Informação.

---

## 🧩 Visão Geral

Este projeto utiliza o MkDocs com tema `Material` para gerar sites estáticos com documentação técnica. Adicionalmente, um painel web baseado em **FastAPI** foi integrado para permitir a edição e organização dos conteúdos `.md` diretamente pela interface web.

---

## ✨ Funcionalidades

- Criação e edição de arquivos Markdown via painel
- Execução automática do `mkdocs build` após cada modificação
- Separação por seções: Visão Geral, Instalação, APIs, Documentação Final
- Organização por usuário final e área técnica
- Script de geração automatizada de índice de arquivos
- Configuração com systemd (`mkdocs-panel.service`, `mkdocs-editor.service`, etc.)

---

## 🖼️ Interface

### Página Inicial

![Página Inicial](https://user-images.githubusercontent.com/SEU_USUARIO/000000/pagina-inicial.png)

### Painel Web

![Painel Editor](https://user-images.githubusercontent.com/SEU_USUARIO/000000/painel-editor.png)

> ⚠️ As imagens acima são ilustrativas. Substitua com capturas reais em produção.

---

## 🏗️ Instalação Local

```bash
git clone https://github.com/SEU_USUARIO/seu-repo.git
cd seu-repo
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn painel.main:app --reload
```

Acesse `http://localhost:8000/painel` para abrir o painel.

---

## 📁 Estrutura do Projeto

```
.
├── docs/
│   ├── visao-geral/
│   ├── instalacao/
│   ├── usuario-final/
│   ├── documentacao/
├── painel/
│   ├── main.py
│   ├── forms, views, routes...
├── scripts/
│   ├── build.sh
├── mkdocs.yml
└── requirements.txt
```

---

## ⚙️ Serviços no Systemd

- `mkdocs-panel.service`: Inicia o painel FastAPI
- `mkdocs-editor.service`: Editor/preview em background
- `mkdocs-build.timer`: Recompila a documentação automaticamente
- `fix-mkdocs-perms.service`: Corrige permissões após build

---

## 📌 Observações

- Projeto inicialmente desenvolvido para uma instituição de ensino.
- Dados sensíveis e nomes institucionais foram removidos para publicação pública.

---

## 🤝 Contribuições

Sinta-se livre para abrir *Issues* e enviar *Pull Requests*. Toda contribuição é bem-vinda!

---

## 📝 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

