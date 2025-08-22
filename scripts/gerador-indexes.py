#!/usr/bin/env python3
"""
Gerador de Índices Melhorado - MkDocs
Gera automaticamente os arquivos index.md para todos os diretórios
Integrado com a automação do painel FastAPI
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Configurações
DOCS_DIR = "docs"
INTRO_DOCUMENTACAO = """# 📄 Guia de Documentação Interna

Bem-vindo ao sistema de documentação interna da empresa. Este guia oferece instruções, boas práticas e informações essenciais para o uso, manutenção e atualização dos documentos técnicos e operacionais utilizados pela organização.

Nosso objetivo é garantir que todos os colaboradores tenham acesso fácil, claro e organizado às informações necessárias para suas atividades diárias, assegurando a padronização e a qualidade dos processos internos.

---
"""

# Configurações específicas por diretório
DIRETORIOS_CONFIG = {
    "apis": {
        "titulo": "🔌 Integrações via API",
        "descricao": "Aqui estão documentadas as APIs disponíveis para integração com os sistemas internos da DTI.\n\nInclui exemplos de requisições, tokens, autenticação e boas práticas de uso.",
        "incluir_intro": False
    },
    "documentacao": {
        "titulo": "📄 Guia de Documentação Interna", 
        "descricao": "",
        "incluir_intro": True
    },
    "instalacao": {
        "titulo": "⚙️ Guia de Instalação",
        "descricao": "Guia de instalação e configuração de sistemas.\n\nInstruções passo a passo para setup e configuração dos sistemas da DTI.",
        "incluir_intro": False
    },
    "usuario-final": {
        "titulo": "👤 Documentação do Usuário Final",
        "descricao": "Manuais e guias para usuários finais dos sistemas.\n\nInstruções de uso, tutoriais e resolução de problemas comuns.",
        "incluir_intro": False
    },
    "visao-geral": {
        "titulo": "🔍 Visão Geral",
        "descricao": "Informações gerais sobre os sistemas da DTI.\n\nVisão geral da arquitetura, tecnologias e processos utilizados.",
        "incluir_intro": False
    }
}

SVG_DOC = """<svg width="32" height="32" viewBox="0 0 20 20" fill="#1976d2" style="vertical-align:middle;"><path d="M4 2h9l5 5v11a2 2 0 01-2 2H4a2 2 0 01-2-2V4a2 2 0 012-2z"/><path d="M13 2v6h6"/></svg>"""

def log_info(mensagem):
    """Log com timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {mensagem}")

def obter_titulo_arquivo(nome_arquivo):
    """
    Converte nome do arquivo em título formatado
    Exemplo: minha_api_rest.md -> Minha Api Rest
    """
    nome = nome_arquivo.replace('.md', '')
    # Substituir underscores e hífens por espaços
    nome = nome.replace('_', ' ').replace('-', ' ')
    # Capitalizar cada palavra
    return nome.title()

def gerar_index_md(diretorio_path, config):
    """
    Gera o arquivo index.md para um diretório específico
    """
    try:
        # Listar arquivos .md válidos
        arquivos = []
        for arquivo in os.listdir(diretorio_path):
            if (arquivo.endswith('.md') and 
                not arquivo.startswith('index') and 
                '_old' not in arquivo and 
                '.bkp' not in arquivo and
                '.backup' not in arquivo):
                arquivos.append(arquivo)
        
        # Ordenar arquivos alfabeticamente
        arquivos.sort()
        
        log_info(f"Processando {diretorio_path}: {len(arquivos)} arquivos encontrados")
        
        # Gerar cards HTML
        cards = []
        for arquivo in arquivos:
            titulo = obter_titulo_arquivo(arquivo)
            # Link sem extensão .md (padrão MkDocs Material)
            link = arquivo.replace('.md', '')
            
            card_html = f"""<a class="doc-card" href="{link}">
  <div class="doc-icon">{SVG_DOC}</div>
  <div class="doc-title">{titulo}</div>
</a>"""
            cards.append(card_html)
        
        # Montar conteúdo do index
        conteudo = []
        
        # Adicionar introdução se configurado
        if config.get("incluir_intro", False):
            conteudo.append(INTRO_DOCUMENTACAO)
        else:
            # Adicionar título e descrição personalizados
            conteudo.append(f"# {config['titulo']}\n")
            if config.get("descricao"):
                conteudo.append(f"{config['descricao']}\n")
            conteudo.append("---\n")
        
        # Adicionar cards se houver arquivos
        if cards:
            cards_html = '<div class="cards-container">\n' + '\n'.join(cards) + '\n</div>'
            conteudo.append(cards_html)
        else:
            conteudo.append("*Nenhum documento disponível nesta seção.*")
        
        # Escrever arquivo
        index_path = os.path.join(diretorio_path, "index.md")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write('\n'.join(conteudo))
        
        log_info(f"✅ Gerado: {index_path} ({len(arquivos)} arquivos)")
        return True
        
    except Exception as e:
        log_info(f"❌ Erro ao processar {diretorio_path}: {e}")
        return False

def gerar_todos_indexes():
    """
    Gera índices para todos os diretórios configurados
    """
    log_info("🚀 Iniciando geração de índices...")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists(DOCS_DIR):
        log_info(f"❌ Diretório {DOCS_DIR} não encontrado!")
        return False
    
    sucessos = 0
    total = 0
    
    # Processar cada diretório configurado
    for nome_dir, config in DIRETORIOS_CONFIG.items():
        total += 1
        dir_path = os.path.join(DOCS_DIR, nome_dir)
        
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            if gerar_index_md(dir_path, config):
                sucessos += 1
        else:
            log_info(f"⚠️  Diretório não encontrado: {dir_path}")
    
    # Processar diretórios não configurados (com configuração padrão)
    for item in os.listdir(DOCS_DIR):
        dir_path = os.path.join(DOCS_DIR, item)
        if (os.path.isdir(dir_path) and 
            item not in DIRETORIOS_CONFIG and 
            item != "assets" and 
            not item.startswith(".")):
            
            total += 1
            config_padrao = {
                "titulo": f"📁 {item.replace('_', ' ').replace('-', ' ').title()}",
                "descricao": f"Documentação da seção {item}.",
                "incluir_intro": False
            }
            
            if gerar_index_md(dir_path, config_padrao):
                sucessos += 1
    
    log_info(f"🎯 Concluído: {sucessos}/{total} índices gerados com sucesso")
    return sucessos == total

def gerar_index_especifico(diretorio):
    """
    Gera índice para um diretório específico
    Usado pela automação do painel
    """
    log_info(f"🎯 Gerando índice específico para: {diretorio}")
    
    # Determinar caminho do diretório
    if diretorio == "" or diretorio == ".":
        # Diretório raiz - não gerar index automático
        log_info("⚠️  Diretório raiz - pulando geração automática")
        return True
    
    dir_path = os.path.join(DOCS_DIR, diretorio)
    
    if not os.path.exists(dir_path):
        log_info(f"❌ Diretório não encontrado: {dir_path}")
        return False
    
    # Usar configuração específica ou padrão
    config = DIRETORIOS_CONFIG.get(diretorio, {
        "titulo": f"📁 {diretorio.replace('_', ' ').replace('-', ' ').title()}",
        "descricao": f"Documentação da seção {diretorio}.",
        "incluir_intro": False
    })
    
    return gerar_index_md(dir_path, config)

if __name__ == "__main__":
    # Verificar argumentos da linha de comando
    if len(sys.argv) > 1:
        # Gerar índice específico
        diretorio = sys.argv[1]
        sucesso = gerar_index_especifico(diretorio)
        sys.exit(0 if sucesso else 1)
    else:
        # Gerar todos os índices
        log_info("Diretório atual: " + os.getcwd())
        sucesso = gerar_todos_indexes()
        sys.exit(0 if sucesso else 1)

