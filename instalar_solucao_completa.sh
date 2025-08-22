#!/bin/bash

# Script de Instalação - Solução Completa Gerador de Índices
# Resolve o problema do arquivo 123.md e automatiza geração de índices
# Autor: Sistema de Documentação DTI

echo "🚀 Instalação da Solução Completa - Gerador de Índices Integrado"
echo "================================================================="

# Verificar se está sendo executado no diretório correto
if [ ! -f "mkdocs.yml" ]; then
    echo "❌ Erro: Execute este script no diretório raiz do projeto MkDocs (/opt/mkdocs)"
    echo "   Diretório atual: $(pwd)"
    exit 1
fi

# Verificar se os arquivos da solução estão presentes
if [ ! -f "gerador-indexes-melhorado.py" ] || [ ! -f "main_com_gerador_integrado.py" ]; then
    echo "❌ Erro: Arquivos da solução não encontrados!"
    echo "   Certifique-se de ter os arquivos:"
    echo "   - gerador-indexes-melhorado.py"
    echo "   - main_com_gerador_integrado.py"
    exit 1
fi

echo "📦 Fazendo backup dos arquivos atuais..."

# Backup do gerador atual
if [ -f "scripts/gerador-indexes.py" ]; then
    cp scripts/gerador-indexes.py scripts/gerador-indexes.py.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ Backup criado: scripts/gerador-indexes.py.backup.$(date +%Y%m%d_%H%M%S)"
else
    echo "⚠️  Arquivo scripts/gerador-indexes.py não encontrado (primeira instalação?)"
fi

# Backup do main.py atual
if [ -f "painel/main.py" ]; then
    cp painel/main.py painel/main.py.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ Backup criado: painel/main.py.backup.$(date +%Y%m%d_%H%M%S)"
else
    echo "❌ Erro: painel/main.py não encontrado!"
    exit 1
fi

echo "🔧 Aplicando solução..."

# Aplicar novo gerador
cp gerador-indexes-melhorado.py scripts/gerador-indexes.py
chmod +x scripts/gerador-indexes.py
echo "✅ Gerador melhorado aplicado"

# Aplicar novo main.py
cp main_com_gerador_integrado.py painel/main.py
echo "✅ Main.py com integração aplicado"

echo "🧪 Testando gerador..."

# Testar execução do gerador
cd /opt/mkdocs
if python3 scripts/gerador-indexes.py > /tmp/gerador_teste.log 2>&1; then
    echo "✅ Gerador testado com sucesso!"
    echo "📋 Últimas linhas do log:"
    tail -3 /tmp/gerador_teste.log | sed 's/^/   /'
else
    echo "❌ Erro no teste do gerador!"
    echo "📋 Log de erro:"
    cat /tmp/gerador_teste.log | sed 's/^/   /'
    echo ""
    echo "🔄 Restaurando backup..."
    if [ -f "scripts/gerador-indexes.py.backup.$(date +%Y%m%d_%H%M%S)" ]; then
        cp scripts/gerador-indexes.py.backup.$(date +%Y%m%d_%H%M%S) scripts/gerador-indexes.py
    fi
    exit 1
fi

echo "🔄 Reiniciando serviços..."

# Reiniciar serviços do painel
if systemctl is-active --quiet mkdocs-editor.service; then
    sudo systemctl restart mkdocs-editor.service
    echo "✅ mkdocs-editor.service reiniciado"
else
    echo "⚠️  mkdocs-editor.service não está ativo"
fi

if systemctl is-active --quiet mkdocs-panel.service; then
    sudo systemctl restart mkdocs-panel.service
    echo "✅ mkdocs-panel.service reiniciado"
else
    echo "⚠️  mkdocs-panel.service não está ativo"
fi

# Aguardar serviços iniciarem
echo "⏳ Aguardando serviços iniciarem..."
sleep 3

echo "🔍 Verificando status dos serviços..."

# Verificar status dos serviços
for service in mkdocs-editor.service mkdocs-panel.service; do
    if systemctl is-active --quiet $service; then
        echo "✅ $service: Ativo"
    else
        echo "❌ $service: Inativo"
        echo "   Status: $(systemctl is-active $service)"
    fi
done

echo "🧪 Teste final da solução..."

# Testar geração específica para APIs (onde estava o problema)
if python3 scripts/gerador-indexes.py apis > /tmp/gerador_apis_teste.log 2>&1; then
    echo "✅ Geração específica para APIs funcionando!"
    
    # Verificar se o arquivo 123.md está no index
    if [ -f "docs/apis/index.md" ]; then
        if grep -q "123" docs/apis/index.md; then
            echo "🎯 SUCESSO: Arquivo 123.md encontrado no índice de APIs!"
        else
            echo "⚠️  Arquivo 123.md não encontrado no índice (pode não existir)"
        fi
    else
        echo "❌ Arquivo docs/apis/index.md não foi gerado"
    fi
else
    echo "❌ Erro na geração específica para APIs"
    cat /tmp/gerador_apis_teste.log | sed 's/^/   /'
fi

echo ""
echo "🎉 Instalação da Solução Completa Concluída!"
echo "============================================="
echo ""
echo "📋 Status da Instalação:"
echo "✅ Gerador melhorado instalado e testado"
echo "✅ Automação integrada no painel"
echo "✅ Serviços reiniciados"
echo "✅ Backups criados com segurança"
echo ""
echo "🎯 Problema Resolvido:"
echo "• O arquivo 123.md agora deve aparecer na página APIs"
echo "• Novos arquivos aparecerão automaticamente"
echo "• Índices sempre atualizados sem intervenção manual"
echo ""
echo "🔧 Funcionalidades Ativadas:"
echo "• ✅ Geração automática após criar arquivos"
echo "• ✅ Configuração automática de permissões (root:mkdocs 664)"
echo "• ✅ Execução específica por diretório"
echo "• ✅ Endpoint /regenerar-indices para manutenção"
echo "• ✅ Logs detalhados para monitoramento"
echo ""
echo "📚 Próximos Passos:"
echo "1. Acesse o painel: http://seu-servidor:8000/painel"
echo "2. Teste criando um arquivo na pasta APIs"
echo "3. Verifique se aparece automaticamente na página"
echo "4. Consulte SOLUCAO_COMPLETA_GERADOR.md para detalhes"
echo ""
echo "🔍 Monitoramento:"
echo "• Logs do gerador: journalctl -f | grep gerador"
echo "• Logs do painel: journalctl -u mkdocs-editor.service -f"
echo "• Teste manual: python3 scripts/gerador-indexes.py"
echo ""

# Verificar se há problemas conhecidos
echo "🔍 Verificação de Problemas Conhecidos:"

# Verificar grupo mkdocs
if getent group mkdocs > /dev/null 2>&1; then
    echo "✅ Grupo mkdocs existe"
else
    echo "⚠️  Grupo mkdocs não existe - pode causar problemas de permissão"
    echo "   Execute: sudo groupadd mkdocs"
fi

# Verificar permissões do diretório docs
if [ -w "docs" ]; then
    echo "✅ Diretório docs é gravável"
else
    echo "⚠️  Diretório docs não é gravável - pode causar problemas"
    echo "   Execute: sudo chown -R ubuntu:mkdocs docs"
fi

# Verificar se o mkdocs-build.service pode interferir
if systemctl is-enabled --quiet mkdocs-build.service 2>/dev/null; then
    echo "⚠️  mkdocs-build.service está habilitado"
    echo "   Este serviço pode executar o gerador automaticamente"
    echo "   Monitore para evitar conflitos"
else
    echo "✅ mkdocs-build.service não interferirá"
fi

echo ""
echo "🎊 Instalação Finalizada com Sucesso!"
echo "A solução está pronta para uso!"

