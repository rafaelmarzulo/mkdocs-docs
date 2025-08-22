# 📚 Projeto MkDocs com Painel Web Integrado

Este projeto oferece uma solução de documentação técnica com visual moderno utilizando [MkDocs](https://www.mkdocs.org/) e um **painel web de gerenciamento**, ideal para times de TI e DevOps.

---

## ✨ Funcionalidades

- 📄 **Documentação com MkDocs**: Interface moderna, organizada por tópicos como Instalação, APIs, e Usuário Final.
- 🧠 **Geração automática de índice (`index.md`)** com Python.
- 🖼️ **Painel Web**: Upload de imagens e criação de arquivos `.md` diretamente pela interface web.
- ⚙️ **Scripts Shell**: Automação da instalação e build da solução.
- 🚀 **Deploy facilitado** com `build.sh` e estrutura modular.

---

## 📂 Estrutura do Projeto

```bash
mkdocs/
├── docs/                  # Arquivos .md organizados em tópicos
├── painel/                # Painel Web em FastAPI
├── overrides/             # Customizações de tema
├── scripts/               # Scripts de build e automação
├── site/                  # Saída do build MkDocs (ignorada pelo Git)
├── mkdocs.yml             # Configuração do MkDocs
├── requirements.txt       # Dependências Python
├── VERSION                # Versão atual da aplicação
├── README.md              # Este arquivo
```

---

## 🖥️ Painel de Documentação Web

O painel em FastAPI permite:

- Upload de imagens (.png, .jpg...) para serem usadas nos `.md`
- Criação de arquivos `.md` em diretórios existentes
- Interface amigável para manter a documentação sem acessar o servidor

🔒 Recomendado uso com autenticação via proxy reverso (ex: Nginx + Basic Auth).

---

## 🧪 Pré-requisitos

- Python 3.10+
- MkDocs + Material Theme
- FastAPI e Uvicorn

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Scripts Importantes

| Script | Descrição |
|--------|-----------|
| `scripts/build.sh` | Gera a documentação com `mkdocs build` |
| `scripts/gerador-indexes.py` | Gera o arquivo `index.md` com os cards automaticamente |
| `scripts/instalar_automacao.sh` | Instala o painel e dependências |
| `scripts/instalar_solucao_completa.sh` | Instala toda a solução MkDocs + Painel |

---

## 🧾 Versão

```bash
cat VERSION
v1.0.0
```

---

## 🖼️ Como adicionar imagens

- Copie as imagens para o diretório `docs/assets/`.
- Referencie no `.md` assim:

```markdown
![Descrição](assets/nome-da-imagem.png)
```

---

## ✅ Checklist de Melhorias Implementadas

- [x] Remoção de menções institucionais
- [x] Licença `MIT` adicionada
- [x] Script `build.sh` e `.gitignore` validados
- [x] Arquivo `VERSION` criado
- [x] Estrutura modular do projeto organizada

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

---

## 📸 Capturas de Tela

### Página Inicial (MkDocs)

![Página Inicial](assets/Pagina_inicial.png)

### Painel de Gerenciamento

![Painel Web](assets/Painel-Web.png)

---

## 🙋‍♂️ Autor

Rafael Marzulo  
🔗 [GitHub](https://github.com/rafaelmarzulo) • 💼 [LinkedIn](https://www.linkedin.com/in/rafaelmarzulo)