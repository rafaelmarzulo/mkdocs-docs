# 📘 Documentação – Servidor Zabbix & Grafana

## 🔹 Visão Geral
Este documento descreve a configuração, forma de acesso e informações relevantes dos servidores **Zabbix** e **Grafana** em produção.  
O objetivo é centralizar os dados para facilitar o gerenciamento e a manutenção do ambiente.

---

## 🔹 Servidor Zabbix

### 📍 Informações de Acesso
- **IP do servidor**: `10.10.1.64`  
- **URL de acesso**:  
  ```
  http://10.10.1.64/zabbix
  ```
- **Credenciais padrão (primeiro acesso)**:
  - Usuário: `Admin`
  - Senha: `zabbix`

> ⚠️ **Importante:** após o primeiro login, alterar a senha padrão do usuário `Admin`.

---

### 🔧 Serviços Instalados
- **Zabbix Server** 7.0 (banco de dados PostgreSQL/MariaDB).  
- **Zabbix Agent2** nos servidores monitorados.  
- **QEMU Guest Agent** integrado ao Proxmox.  

---

### 🔐 Segurança
- Acesso via **porta 80 (HTTP)** → recomendável habilitar **HTTPS (porta 443)**.  
- Firewall (UFW) configurado para permitir:
  - `80/tcp` → interface web.  
  - `10051/tcp` → comunicação de agentes com o servidor.  
- Integração opcional com **LDAP ou SAML** para autenticação corporativa.  

---

## 🔹 Servidor Grafana

### 📍 Informações de Acesso
- **IP do servidor**: `10.10.1.7`  
- **URL de acesso**:  
  ```
  http://10.10.1.7:3000
  ```
- **Credenciais padrão (primeiro acesso)**:
  - Usuário: `admin`
  - Senha: `admin`

> ⚠️ **Importante:** no primeiro login, o sistema obriga a alteração da senha.

---

### 🔧 Serviços Instalados
- **Grafana OSS** última versão estável.  
- **Plugin Zabbix para Grafana** integrado.  
- Dashboards customizados para monitoramento centralizado.  

---

### 🔐 Segurança
- Porta padrão de acesso: **3000/TCP**.  
- Recomendado configurar **proxy reverso Nginx/Apache** para expor via porta **443 (HTTPS)**.  
- Autenticação:
  - Alteração imediata da senha padrão do `admin`.  
  - Integração opcional com LDAP/Active Directory.  

---

## 🔹 Fluxo de Acesso

1. **Zabbix**  
   - Acesse: `http://10.10.1.64/zabbix`  
   - Login com credenciais definidas.  
   - Configure hosts e templates para monitoramento.  

2. **Grafana**  
   - Acesse: `http://10.10.1.7:3000`  
   - Login com credenciais definidas.  
   - Configure **Zabbix como fonte de dados**:
     - URL do Zabbix API:  
       ```
       http://10.10.1.64/zabbix/api_jsonrpc.php
       ```
     - Usuário API dedicado.  

---

## 🔹 Boas Práticas
- Alterar credenciais padrão imediatamente.  
- Restringir acesso externo às portas de administração.  
- Configurar **backup automático** de banco de dados e dashboards.  
- Monitorar logs em:
  - `/var/log/zabbix/`  
  - `/var/log/grafana/`  
