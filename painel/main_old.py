from fastapi import FastAPI, Request, Form, UploadFile, File, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from urllib.parse import quote
from pathlib import Path
import shutil
import subprocess
import os
import re
from painel.logger_config import logger

app = FastAPI()

app.mount("/static", StaticFiles(directory="/opt/mkdocs/docs/assets"), name="static")
templates = Jinja2Templates(directory="painel/templates")
docs_path = Path("docs")


def listar_subdiretorios(caminho: Path):
    return [str(p.relative_to(caminho)) for p in caminho.rglob("*") if p.is_dir()]


def listar_arquivos(caminho: Path):
    return [str(f.relative_to(caminho)) for f in caminho.rglob("*.md")]


def configurar_permissoes_arquivo(caminho_arquivo: Path):
    """
    Configura as permissões e grupo do arquivo criado
    """
    try:
        # Alterar grupo para root:mkdocs
        subprocess.run(['chgrp', 'mkdocs', str(caminho_arquivo)], check=True)
        
        # Alterar permissões para 664 (rw-rw-r--)
        subprocess.run(['chmod', '664', str(caminho_arquivo)], check=True)
        
        logger.info(f"Permissões configuradas para {caminho_arquivo}: root:mkdocs 664")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao configurar permissões para {caminho_arquivo}: {e}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado ao configurar permissões: {e}")
        return False


def atualizar_index_diretorio(diretorio: str, nome_arquivo: str):
    """
    Adiciona o novo arquivo ao index.md do diretório correspondente
    """
    try:
        # Se diretório estiver vazio, é o diretório raiz
        if not diretorio:
            index_path = docs_path / "index.md"
        else:
            index_path = docs_path / diretorio / "index.md"
        
        # Verificar se o index.md existe
        if not index_path.exists():
            logger.warning(f"Index não encontrado: {index_path}")
            return False
        
        # Ler conteúdo atual do index
        conteudo_atual = index_path.read_text(encoding="utf-8")
        
        # Criar nome limpo do arquivo (sem .md)
        nome_limpo = nome_arquivo.replace('.md', '')
        
        # Criar título formatado (primeira letra maiúscula, underscores por espaços)
        titulo_formatado = nome_limpo.replace('_', ' ').replace('-', ' ').title()
        
        # Criar link markdown
        if diretorio:
            link_arquivo = f"- [{titulo_formatado}]({nome_arquivo})"
        else:
            link_arquivo = f"- [{titulo_formatado}]({nome_arquivo})"
        
        # Verificar se o link já existe
        if link_arquivo in conteudo_atual or nome_arquivo in conteudo_atual:
            logger.info(f"Arquivo {nome_arquivo} já está no index {index_path}")
            return True
        
        # Procurar por uma seção de lista existente ou adicionar no final
        linhas = conteudo_atual.split('\n')
        nova_linha_adicionada = False
        
        # Tentar encontrar uma lista existente para adicionar
        for i, linha in enumerate(linhas):
            if linha.strip().startswith('- [') and not nova_linha_adicionada:
                # Inserir antes da primeira entrada da lista
                linhas.insert(i, link_arquivo)
                nova_linha_adicionada = True
                break
        
        # Se não encontrou lista existente, adicionar no final
        if not nova_linha_adicionada:
            # Adicionar uma linha em branco se necessário
            if linhas and linhas[-1].strip():
                linhas.append('')
            
            # Adicionar seção de arquivos se não existir
            linhas.append('## Arquivos')
            linhas.append('')
            linhas.append(link_arquivo)
        
        # Escrever conteúdo atualizado
        novo_conteudo = '\n'.join(linhas)
        index_path.write_text(novo_conteudo, encoding="utf-8")
        
        # Configurar permissões do index também
        configurar_permissoes_arquivo(index_path)
        
        logger.info(f"Arquivo {nome_arquivo} adicionado ao index {index_path}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao atualizar index do diretório {diretorio}: {e}")
        return False


@app.get("/", response_class=HTMLResponse)
def editor(
    request: Request,
    nome: str = "index.md",
    mensagem: str = "",
    link_md: str = ""
):
    arquivos = listar_arquivos(docs_path)
    arquivo = docs_path / Path(nome)
    conteudo = ""
    if arquivo.exists():
        conteudo = arquivo.read_text(encoding="utf-8")
    subdirs = [""] + listar_subdiretorios(docs_path)
    return templates.TemplateResponse("editor.html", {
        "request": request,
        "arquivos": arquivos,
        "arquivo_atual": nome,
        "conteudo": conteudo,
        "diretorios": subdirs,
        "mensagem": mensagem,
        "link_md": link_md
    })


@app.get("/painel", response_class=HTMLResponse)
def painel_redirect(
    request: Request,
    nome: str = "index.md",
    mensagem: str = "",
    link_md: str = ""
):
    return editor(request, nome, mensagem, link_md)


@app.post("/upload")
def upload_imagem(
    request: Request,
    diretorio: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        extensoes_validas = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}
        if not any(file.filename.lower().endswith(ext) for ext in extensoes_validas):
            logger.warning(f"Extensão inválida: {file.filename}")
            return HTMLResponse("Extensão de arquivo inválida.", status_code=400)

        destino = docs_path / diretorio / "assets"
        destino.mkdir(parents=True, exist_ok=True)

        caminho_arquivo = destino / file.filename
        with caminho_arquivo.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # AUTOMAÇÃO: Configurar permissões da imagem
        configurar_permissoes_arquivo(caminho_arquivo)

        link_md = f"![{file.filename}]({diretorio}/assets/{file.filename})" if diretorio else f"![{file.filename}](assets/{file.filename})"
        logger.info(f"Imagem enviada: {file.filename} para {destino}")
        
        mensagem = f"✅ Imagem '{file.filename}' enviada com sucesso!"
        return RedirectResponse(
            url=f"/painel?mensagem={quote(mensagem)}&link_md={quote(link_md)}",
            status_code=status.HTTP_303_SEE_OTHER
        )
    except Exception as e:
        logger.error("Erro no upload de imagem", exc_info=True)
        return HTMLResponse("Erro interno no servidor.", status_code=500)


@app.post("/criar")
def criar_arquivo(
    novo_nome: str = Form(...),
    diretorio_md: str = Form(default="")
):
    if not novo_nome.endswith(".md"):
        novo_nome += ".md"

    caminho = docs_path / diretorio_md / novo_nome
    caminho_pai = caminho.parent

    try:
        caminho_pai.mkdir(parents=True, exist_ok=True)
        if not caminho.exists():
            # Criar conteúdo inicial mais elaborado
            titulo = novo_nome.replace('.md', '').replace('_', ' ').replace('-', ' ').title()
            conteudo_inicial = f"""# {titulo}

## Descrição

Descreva aqui o conteúdo deste documento.

## Conteúdo

Adicione o conteúdo principal aqui.

---
*Documento criado automaticamente pelo sistema de documentação DTI*
"""
            
            caminho.write_text(conteudo_inicial, encoding="utf-8")
            logger.info(f"Arquivo criado: {caminho}")
            
            # AUTOMAÇÃO 1: Configurar permissões e grupo
            permissoes_ok = configurar_permissoes_arquivo(caminho)
            
            # AUTOMAÇÃO 2: Adicionar ao index do diretório
            index_ok = atualizar_index_diretorio(diretorio_md, novo_nome)
            
            # Mensagem de sucesso com status das automações
            if permissoes_ok and index_ok:
                mensagem = f"✅ Arquivo '{novo_nome}' criado com sucesso! (Permissões e índice atualizados)"
            elif permissoes_ok:
                mensagem = f"✅ Arquivo '{novo_nome}' criado com sucesso! (Permissões OK, erro no índice)"
            elif index_ok:
                mensagem = f"✅ Arquivo '{novo_nome}' criado com sucesso! (Índice OK, erro nas permissões)"
            else:
                mensagem = f"✅ Arquivo '{novo_nome}' criado com sucesso! (Verificar permissões e índice)"
                
        else:
            logger.warning(f"Arquivo já existe: {caminho}")
            mensagem = f"⚠️ Arquivo '{novo_nome}' já existe."
    except Exception as e:
        logger.error("Erro ao criar arquivo", exc_info=True)
        mensagem = f"❌ Erro ao criar arquivo '{novo_nome}'."

    return RedirectResponse(
        url=f"/painel?nome={quote(diretorio_md + '/' + novo_nome)}&mensagem={quote(mensagem)}",
        status_code=status.HTTP_303_SEE_OTHER
    )


@app.post("/salvar")
def salvar_arquivo(
    request: Request,
    nome: str = Form(...),
    conteudo: str = Form(...)
):
    caminho = docs_path / nome
    try:
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text(conteudo, encoding="utf-8")
        
        # AUTOMAÇÃO: Configurar permissões após salvar
        configurar_permissoes_arquivo(caminho)
        
        logger.info(f"Arquivo salvo com sucesso: {caminho}")
        arquivo_nome = Path(nome).name
        mensagem = f"✅ Arquivo '{arquivo_nome}' salvo com sucesso!"
    except Exception as e:
        logger.error("Erro ao salvar arquivo", exc_info=True)
        arquivo_nome = Path(nome).name
        mensagem = f"❌ Erro ao salvar arquivo '{arquivo_nome}'."

    return RedirectResponse(
        url=f"/painel?nome={quote(nome)}&mensagem={quote(mensagem)}",
        status_code=status.HTTP_303_SEE_OTHER
    )


