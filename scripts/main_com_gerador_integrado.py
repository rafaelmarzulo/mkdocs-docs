from fastapi import FastAPI, Request, Form, UploadFile, File, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from urllib.parse import quote
from pathlib import Path
import shutil
import subprocess
import os
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


def executar_gerador_indices(diretorio_especifico=None):
    """
    Executa o gerador de índices melhorado
    Se diretorio_especifico for fornecido, gera apenas para esse diretório
    Caso contrário, gera para todos os diretórios
    """
    try:
        script_path = "/opt/mkdocs/scripts/gerador-indexes.py"
        
        if diretorio_especifico:
            # Executar para diretório específico
            cmd = ['python3', script_path, diretorio_especifico]
            logger.info(f"Executando gerador para diretório: {diretorio_especifico}")
        else:
            # Executar para todos os diretórios
            cmd = ['python3', script_path]
            logger.info("Executando gerador para todos os diretórios")
        
        # Executar o comando
        result = subprocess.run(
            cmd,
            cwd="/opt/mkdocs",
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            logger.info(f"Gerador executado com sucesso: {result.stdout}")
            return True
        else:
            logger.error(f"Erro no gerador: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("Timeout ao executar gerador de índices")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado ao executar gerador: {e}")
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
            
            # AUTOMAÇÃO 2: Executar gerador de índices para o diretório específico
            gerador_ok = executar_gerador_indices(diretorio_md if diretorio_md else None)
            
            # Mensagem de sucesso com status das automações
            if permissoes_ok and gerador_ok:
                mensagem = f"✅ Arquivo '{novo_nome}' criado com sucesso! (Permissões e índice atualizados automaticamente)"
            elif permissoes_ok:
                mensagem = f"✅ Arquivo '{novo_nome}' criado com sucesso! (Permissões OK, verificar logs do gerador)"
            elif gerador_ok:
                mensagem = f"✅ Arquivo '{novo_nome}' criado com sucesso! (Índice OK, erro nas permissões)"
            else:
                mensagem = f"✅ Arquivo '{novo_nome}' criado com sucesso! (Verificar permissões e logs do gerador)"
                
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


@app.post("/regenerar-indices")
def regenerar_indices():
    """
    Endpoint para regenerar todos os índices manualmente
    Útil para manutenção ou resolução de problemas
    """
    try:
        sucesso = executar_gerador_indices()
        if sucesso:
            mensagem = "✅ Todos os índices foram regenerados com sucesso!"
        else:
            mensagem = "⚠️ Houve problemas ao regenerar alguns índices. Verifique os logs."
        
        return RedirectResponse(
            url=f"/painel?mensagem={quote(mensagem)}",
            status_code=status.HTTP_303_SEE_OTHER
        )
    except Exception as e:
        logger.error("Erro ao regenerar índices", exc_info=True)
        mensagem = "❌ Erro ao regenerar índices."
        return RedirectResponse(
            url=f"/painel?mensagem={quote(mensagem)}",
            status_code=status.HTTP_303_SEE_OTHER
        )

