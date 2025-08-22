# 📘 Documentação – Template Ubuntu 24.04 (Noble) Cloud-Init com Hardening

## 🔹 Visão Geral
Este documento descreve o processo de criação de um **template base Ubuntu 24.04 (Noble) LTS Cloud-Init** para uso em ambientes virtualizados com **Proxmox VE**.  
O template inclui:
- **Imagem cloudimg oficial (amd64)**.
- **Integração com Cloud-Init**.
- **Instalação do QEMU Guest Agent** para gerenciamento.
- **Expansão de disco personalizada**.
- **Configurações de hardening** (SSH, firewall, atualizações automáticas, Fail2Ban).

---

## 🔹 Configuração Final no Proxmox

### Recursos da VM Base (Template)
- **Memória**: 6 GiB  
- **Processadores**: 6 (2 sockets × 3 cores)  
- **BIOS**: SeaBIOS (padrão)  
- **Display**: Serial terminal 0 (serial0)  
- **Máquina**: i440fx (padrão)  
- **Controladora SCSI**: VirtIO SCSI  
- **CloudInit Drive (ide2)**: `local-lvm:vm-1010-cloudinit,media=cdrom`  
- **Disco principal (scsi0)**: `local-lvm:base-1010-disk-0, size=100 GiB`  
- **Placa de rede (net0)**: VirtIO → bridge `vmbr0` (tag=1)  
- **Serial Port (serial0)**: socket  

---

### Configurações do Cloud-Init
- **Usuário padrão**: `ubuntu`  
- **Senha padrão**: `J*41fsh@` (⚠️ ver observação de segurança abaixo)  
- **DNS domain**: herdado do host  
- **DNS servers**: herdados do host  
- **Chave pública SSH**: cadastrada (exemplo: `ti@exemplo.com`)  
- **Upgrade packages**: ativado → atualizações automáticas na primeira inicialização  
- **Configuração de rede**: DHCP padrão  

---

## 🔹 Observação Importante de Segurança – Senha Padrão
No estado atual, **qualquer VM criada a partir deste template pode ser acessada pelo console do Proxmox** utilizando o usuário `ubuntu` com a senha `J*41fsh@`.  

### ⚠️ Riscos
- Todas as VMs compartilham a mesma senha fixa.
- A senha **não funciona no SSH remoto** porque o `sshd_config` já está configurado com `PasswordAuthentication no`.
- Porém, a senha **continua funcionando no console Proxmox**, já que ele simula login local direto no terminal.

### ✅ Recomendações
1. **Ambiente mais seguro (recomendado)**:
   - Remova a senha do campo **Cloud-Init → Password** no Proxmox.
   - Trabalhe apenas com **chaves SSH** para login remoto.
   - Confirme no `/etc/ssh/sshd_config`:
     ```bash
     PermitRootLogin no
     PasswordAuthentication no
     PubkeyAuthentication yes
     ```

2. **Ambiente controlado (senha apenas no console)**:
   - Pode manter a senha para uso de emergência no console.
   - Certifique-se de que o login por senha esteja **desativado no SSH remoto**.

3. **Automatizado (segurança avançada)**:
   - Configure um script via Cloud-Init ou Ansible para gerar uma senha aleatória em cada VM.
   - Assim, não haverá uma senha padrão repetida.

4. **Controle de acesso ao Proxmox**:
   - Restringir o acesso ao Proxmox apenas a administradores confiáveis.
   - Habilitar **2FA** no Proxmox para reduzir riscos de uso indevido.  

---

## 🔹 Hardening Ativado (via `sshd_config`)

### Configuração aplicada
```bash
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
PermitEmptyPasswords no
KbdInteractiveAuthentication no

X11Forwarding no
AllowTcpForwarding no
PermitTunnel no
AllowAgentForwarding no

Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group16-sha512

LogLevel INFO
```

### Benefícios
- **Root desabilitado** → impede acessos diretos ao root.  
- **Apenas chave SSH** → elimina risco de brute-force com senha.  
- **Forwarding, túnel e X11 desativados** → reduz vetores de ataque.  
- **Criptografia moderna** → garante comunicação segura.  
- **Logs detalhados** → rastreabilidade de acessos.  

---

## 🔹 Fluxo Resumido
1. Download da imagem → `wget`  
2. Customização com `virt-customize`  
3. Criação da VM base (`qm create`)  
4. Importar disco (`qm importdisk`)  
5. Configurações (Cloud-Init, agente, disco)  
6. Converter em template (`qm template`)  
7. Clonar para novas VMs  
8. Acessar com `ssh ubuntu@ip` usando **chave SSH**  

---

## 🔹 Vantagens do Template
- Padrão corporativo unificado para novos servidores.  
- Provisionamento rápido com Cloud-Init.  
- Segurança básica aplicada desde o primeiro boot.  
- Compatível com automação via Terraform ou Ansible.  
- Pronto para integração com monitoramento (ex.: Zabbix Agent).  

