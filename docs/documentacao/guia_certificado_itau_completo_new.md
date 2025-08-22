# 🔐 Geração e Solicitação de Certificado Digital (OpenSSL + API Itaú)

> **Pré-requisito:** Este procedimento deve ser realizado em um ambiente Linux com o `OpenSSL` e `curl` instalados.

Este guia explica como:

1. Gerar um **par de chaves e CSR** (Certificate Signing Request) com `OpenSSL`
2. Realizar a **solicitação de certificado** junto ao Itaú usando `curl`
3. Converter o certificado para o formato `.pfx` com segurança

---

## ✅ Etapa 1 — Gerar o CSR com OpenSSL

### Comando:

```bash
openssl req -new   -subj "/CN=api.seudominio.com/OU=nome_da_instituicao/L=Cidade/ST=Estado/C=BR"   -out nome_do_certificado.csr   -nodes   -sha512   -newkey rsa:2048   -keyout nome_do_certificado.key
```

### Explicação dos parâmetros:

| Parâmetro               | Significado                                |
|-------------------------|---------------------------------------------|
| `-newkey rsa:2048`      | Cria uma nova chave RSA de 2048 bits        |
| `-keyout`               | Nome do arquivo da chave privada gerada     |
| `-out`                  | Nome do arquivo CSR (requisitado pelo Itaú) |
| `-subj`                 | Informações da organização                  |
| `-sha512`               | Algoritmo de hash mais seguro (recomendado) |
| `-nodes`                | Remove criptografia da chave privada        |

### Arquivos gerados:

- `nome_do_certificado.csr` → Pedido de assinatura
- `nome_do_certificado.key` → Chave privada (NUNCA compartilhe)

---

## ✅ Etapa 2 — Enviar CSR para o Itaú via `curl`

### Comando:

```bash
curl -i -k -X POST   --url https://sts.itau.com.br/seguranca/v1/certificado/solicitacao   -H "Content-Type: text/plain"   -H 'Authorization: Bearer colocar aqui o token gerado pelo itau'   -d 'colar aqui o certificado csr gerado'
```

### Exemplo real:

```bash
curl -i -k -X POST   --url https://sts.itau.com.br/seguranca/v1/certificado/solicitacao   -H "Content-Type: text/plain"   -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.FAKE_TOKEN123456'   -d '-----BEGIN CERTIFICATE REQUEST-----
MIICvzCCAa...conteúdo do CSR...
-----END CERTIFICATE REQUEST-----'
```

---

## ✅ Etapa 3 — Conversão para .pfx


Execute o seguinte comando para gerar o arquivo `.pfx`:

```bash
openssl pkcs12 -export   -out certificado_itau.pfx   -inkey chave_privada.key   -in certificado.crt
```

> 💡 O comando solicitará uma senha para proteger o `.pfx`. Guarde-a com segurança — ela será usada na importação do certificado.

---

## ✅ Resultado Esperado

- Um arquivo chamado `certificado_itau.pfx` será criado no diretório atual.
- Esse arquivo pode ser importado em navegadores ou sistemas que exijam o certificado digital.

---
## 🔒 Segurança

- **NUNCA** compartilhe a chave `.key`
- **Sempre** valide o domínio no campo `CN`
- Use `chmod 600 nome_do_certificado.key` para restringir acesso à chave

---

# 🛡️ Guia de Certificado Itaú – Completo

Este guia apresenta um passo a passo completo para configurar certificados digitais utilizados pelo Itaú. Siga atentamente cada etapa e consulte as imagens de apoio.

---

## 📷 Etapas ilustradas

### 1. Início da configuração

![Etapa 1](assets/092d4ebd-4dcd-4a90-9f28-edff435acf4b.png)

---

### 2. Verificando os dados

![Etapa 2](assets/210fc524-8394-4a62-97f8-23cce5301b1a.png)

---

### 3. Baixando o certificado

![Etapa 3](assets/4c011b60-3b6b-478c-87fe-c6a9fea9683c.png)

---

### 4. Instalação do certificado

![Etapa 4](assets/b161125b-a58e-4a42-ac81-561b10fd6743.png)

---

### 5. Validação final

![Etapa 5](assets/dcf29681-36ed-4a68-a5a4-4ae0af5c2cd2.png)

---

## ✅ Conclusão

Após seguir todas as etapas e validar a instalação, o certificado estará pronto para uso no ambiente seguro do Itaú.

Se encontrar algum problema, entre em contato com o suporte da DTI.

