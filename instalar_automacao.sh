#!/bin/bash

# Script de Instalação da Automação MkDocs + FastAPI
# Autor: Sistema de Documentação DTI
# Data: $(date)

echo "🤖 Instalação da Automação MkDocs + FastAPI"
echo "============================================="

# Verificar se está sendo executado como root ou com sudo
if [[ $EUID -eq 0 ]]; then
    echo "⚠️  Este script não deve ser executado como root."
    echo "   Execute como usuário normal que tem acesso sudo."
    exit 1
fi

# Verificar se o arquivo main.py existe
if [ ! -f "painel/main.py" ]; then
    echo "❌ Arquivo painel/main.py não encontrado!"
    echo "   Certifique-se de estar no diretório correto do projeto."
    exit 1
fi

# Fazer backup do arquivo atual
echo "📦 Fazendo backup do arquivo atual..."
cp painel/main.py painel/main.py.backup.$(date +%Y%m%d_%H%M%S)
echo "✅ Backup criado: painel/main.py.backup.$(date +%Y%m%d_%H%M%S)"

# Verificar se o grupo mkdocs existe
echo "🔍 Verificando grupo mkdocs..."
if ! getent group mkdocs > /dev/null 2>&1; then
    echo "⚠️  Grupo 'mkdocs' não encontrado. Criando..."
    sudo groupadd mkdocs
    if [ $? -eq 0 ]; then
        echo "✅ Grupo 'mkdocs' criado com sucesso!"
    else
        echo "❌ Erro ao criar grupo 'mkdocs'!"
        exit 1
    fi
else
    echo "✅ Grupo 'mkdocs' já existe!"
fi

# Adicionar usuário atual ao grupo mkdocs (opcional)
echo "👤 Adicionando usuário atual ao grupo mkdocs..."
sudo usermod -a -G mkdocs $USER
if [ $? -eq 0 ]; then
    echo "✅ Usuário $USER adicionado ao grupo mkdocs!"
else
    echo "⚠️  Aviso: Não foi possível adicionar usuário ao grupo mkdocs."
fi

# Copiar arquivo com automação
echo "📝 Aplicando automação..."
if [ -f "main_com_automacao.py" ]; then
    cp main_com_automacao.py painel/main.py
    echo "✅ Automação aplicada com sucesso!"
else
    echo "❌ Arquivo main_com_automacao.py não encontrado!"
    echo "   Certifique-se de ter o arquivo na pasta atual."
    exit 1
fi

# Verificar permissões dos diretórios docs
echo "🔍 Verificando estrutura de diretórios..."
if [ -d "docs" ]; then
    echo "✅ Diretório docs encontrado!"
    
    # Listar diretórios e verificar index.md
    for dir in docs/*/; do
        if [ -d "$dir" ]; then
            dirname=$(basename "$dir")
            if [ -f "${dir}index.md" ]; then
                echo "✅ ${dirname}/index.md encontrado"
            else
                echo "⚠️  ${dirname}/index.md não encontrado - será necessário criar"
            fi
        fi
    done
else
    echo "❌ Diretório docs não encontrado!"
    echo "   Certifique-se de estar no diretório correto do projeto MkDocs."
    exit 1
fi

# Configurar permissões básicas
echo "🔐 Configurando permissões básicas..."
sudo chgrp -R mkdocs docs/ 2>/dev/null || echo "⚠️  Aviso: Não foi possível alterar grupo dos arquivos existentes"
sudo chmod -R 664 docs/*.md 2>/dev/null || echo "⚠️  Aviso: Não foi possível alterar permissões dos arquivos existentes"

echo ""
echo "🎉 Instalação da Automação Concluída!"
echo "====================================="
echo ""
echo "📋 Próximos passos:"
echo "1. Reinicie o servidor FastAPI:"
echo "   python -m uvicorn painel.main:app --reload --host 0.0.0.0 --port 8001"
echo ""
echo "2. Teste a automação criando um novo arquivo"
echo ""
echo "3. Verifique os logs para confirmar funcionamento"
echo ""
echo "📚 Funcionalidades ativadas:"
echo "✅ Criação automática de conteúdo estruturado"
echo "✅ Configuração automática de permissões (root:mkdocs 664)"
echo "✅ Atualização automática dos índices dos diretórios"
echo "✅ Aplicação de permissões em uploads de imagem"
echo "✅ Reconfiguração de permissões ao salvar arquivos"
echo ""
echo "📖 Consulte DOCUMENTACAO_AUTOMACAO.md para detalhes completos"
echo ""

# Verificar se precisa fazer logout/login para grupo mkdocs
if ! groups | grep -q mkdocs; then
    echo "⚠️  IMPORTANTE: Faça logout e login novamente para que as"
    echo "   alterações de grupo tenham efeito, ou execute:"
    echo "   newgrp mkdocs"
fi

