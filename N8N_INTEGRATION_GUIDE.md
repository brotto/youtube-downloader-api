# Guia de Integração com n8n

Este guia explica como importar e configurar os workflows do YouTube Downloader no n8n.

## 📦 Arquivos de Workflow Disponíveis

### 1. **n8n-workflow.json** (Completo)
Workflow completo com:
- ✅ Validação de URL
- ✅ Exibição de informações do vídeo antes do download
- ✅ Mensagens de status em tempo real
- ✅ Tratamento de erros robusto
- ✅ Opção de deletar arquivo após download

### 2. **n8n-workflow-simple.json** (Simples)
Workflow minimalista com:
- ✅ Download direto sem validações extras
- ✅ Apenas 3 nós (Chat Trigger → Download → Response)
- ✅ Ideal para uso rápido

---

## 🚀 Como Importar o Workflow no n8n

### Passo 1: Copiar o JSON

Escolha um dos arquivos:
- `n8n-workflow.json` (recomendado para produção)
- `n8n-workflow-simple.json` (mais rápido e simples)

Abra o arquivo e copie todo o conteúdo JSON.

### Passo 2: Importar no n8n

1. Acesse seu n8n
2. Clique em **"+ Add workflow"** ou vá em **Workflows** → **Import from File**
3. Cole o JSON copiado
4. Clique em **"Import"**

### Passo 3: Configurar a URL do Serviço

**IMPORTANTE:** Você precisa ajustar a URL do serviço nos nós HTTP Request.

#### Se estiver usando Docker Compose:
```
URL: http://youtube-downloader:5000
```

#### Se estiver usando Easy Panel/Hostinger:
```
URL: https://seu-dominio.easypanel.host
```
ou
```
URL: http://seu-ip:5000
```

#### Para atualizar:
1. Clique em cada nó **HTTP Request** (Get Video Info, Download Video, etc.)
2. Altere o campo **URL** com a URL correta do seu serviço
3. Salve o workflow

---

## 📋 Detalhes do Workflow Completo

### Fluxo de Execução

```
1. Chat Trigger
   ↓
2. Extract YouTube URL
   ↓
3. Get Video Info (POST /info)
   ↓
4. Video Info Valid? (IF)
   ├─ TRUE → 5. Prepare Video Data
   │          ↓
   │       6. Send Info Message
   │          ↓
   │       7. Download Video (POST /download)
   │          ↓
   │       8. Download Success? (IF)
   │          ├─ TRUE → 9. Get Video File (GET /files/{filename})
   │          │         ↓
   │          │      10. Send Success Message
   │          │         ↓
   │          │      11. Delete Video File (Optional)
   │          │
   │          └─ FALSE → 12. Send Download Error
   │
   └─ FALSE → 13. Send Info Error
```

### Nós e suas Funções

#### 1. **When chat message received** (Trigger)
- Tipo: Manual Chat Trigger
- Função: Recebe mensagem do usuário com o link do YouTube

#### 2. **Extract YouTube URL**
- Tipo: Set
- Função: Extrai e prepara a URL do YouTube e formato

#### 3. **Get Video Info**
- Tipo: HTTP Request
- Método: POST
- URL: `http://youtube-downloader:5000/info`
- Body: `{ "url": "{{ $json.youtubeUrl }}" }`
- Timeout: 30 segundos

#### 4. **Video Info Valid?**
- Tipo: IF
- Condição: `$json.success === true`

#### 5. **Prepare Video Data**
- Tipo: Set
- Função: Organiza dados do vídeo para exibição

#### 6. **Send Info Message**
- Tipo: Send Message
- Função: Envia informações do vídeo ao usuário

#### 7. **Download Video**
- Tipo: HTTP Request
- Método: POST
- URL: `http://youtube-downloader:5000/download`
- Body: `{ "url": "{{ $json.youtubeUrl }}", "format": "best" }`
- Timeout: 300 segundos (5 minutos)

#### 8. **Download Success?**
- Tipo: IF
- Condição: `$json.success === true`

#### 9. **Get Video File**
- Tipo: HTTP Request
- Método: GET
- URL: `http://youtube-downloader:5000/files/{{ encodeURIComponent($json.filename) }}`
- Response Format: File

#### 10. **Send Success Message**
- Tipo: Send Message
- Função: Confirma download ao usuário

#### 11. **Delete Video File (Optional)**
- Tipo: HTTP Request
- Método: DELETE
- URL: `http://youtube-downloader:5000/files/{{ encodeURIComponent($json.filename) }}`
- **NOTA:** Este nó está desabilitado por padrão. Habilite se quiser deletar o arquivo após o download.

#### 12. **Send Download Error**
- Tipo: Send Message
- Função: Notifica erro no download

#### 13. **Send Info Error**
- Tipo: Send Message
- Função: Notifica erro ao obter informações

---

## 🎯 Como Usar

### Workflow Completo

1. Ative o workflow no n8n
2. Abra o chat
3. Cole um link do YouTube (ex: `https://youtu.be/03kRWE1ezfQ`)
4. Aguarde as mensagens:
   - Informações do vídeo (título, canal, duração, views)
   - Status do download
   - Confirmação de conclusão

### Workflow Simples

1. Ative o workflow no n8n
2. Abra o chat
3. Cole um link do YouTube
4. Receba a mensagem de sucesso ou erro

---

## ⚙️ Configurações Avançadas

### Alterar Formato do Download

No nó **Download Video**, altere o body:

```json
{
  "url": "{{ $json.youtubeUrl }}",
  "format": "audio"  // Opções: best, video, audio
}
```

### Ajustar Timeouts

Para vídeos muito longos, aumente o timeout:

1. Clique no nó **Download Video**
2. Vá em **Options** → **Timeout**
3. Aumente para 600000 (10 minutos) ou mais

### Manter Arquivos no Servidor

Se quiser manter os arquivos:

1. Mantenha o nó **Delete Video File (Optional)** desabilitado
2. Use o endpoint `/files` para listar arquivos
3. Use o endpoint `/files/{filename}` para baixar depois

### Personalizar Mensagens

Edite os nós **Send Message** para customizar:

```javascript
=✅ Vídeo Pronto!

🎬 {{ $json.title }}
📁 {{ $json.filename }}

Download concluído com sucesso! 🎉
```

---

## 🐛 Solução de Problemas

### Erro: "Connection refused"
- Verifique se a URL do serviço está correta
- Confirme que o container está rodando
- No Easy Panel, verifique se a aplicação está ativa

### Erro: "Timeout"
- Aumente o timeout nos nós HTTP Request
- Vídeos muito longos podem demorar mais

### Erro: "Requested format is not available"
- A API já possui user-agent configurado
- Verifique se a URL do YouTube é válida
- Tente com outro vídeo

### Arquivo não aparece
- Verifique o nó **Get Video File**
- Confirme que o response format está como "file"
- Verifique se o filename está correto

---

## 🔗 URLs dos Endpoints

### Produção (Easy Panel)
```
https://seu-dominio.easypanel.host/info
https://seu-dominio.easypanel.host/download
https://seu-dominio.easypanel.host/files
```

### Docker Local
```
http://youtube-downloader:5000/info
http://youtube-downloader:5000/download
http://youtube-downloader:5000/files
```

### Localhost (Desenvolvimento)
```
http://localhost:5000/info
http://localhost:5000/download
http://localhost:5000/files
```

---

## 📊 Exemplos de Teste

### Teste com cURL (opcional)

```bash
# Obter informações
curl -X POST http://localhost:5000/info \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtu.be/03kRWE1ezfQ"}'

# Download
curl -X POST http://localhost:5000/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtu.be/03kRWE1ezfQ", "format": "best"}'

# Listar arquivos
curl http://localhost:5000/files

# Health check
curl http://localhost:5000/health
```

---

## 🎨 Customizações Sugeridas

### 1. Adicionar Escolha de Formato

Adicione um nó **Set** antes do download:

```javascript
{
  "format": "{{ $json.chatInput.includes('audio') ? 'audio' : 'best' }}"
}
```

### 2. Validar URL do YouTube

Adicione um nó **IF** após o trigger:

```javascript
{{ $json.chatInput.includes('youtube.com') || $json.chatInput.includes('youtu.be') }}
```

### 3. Adicionar Logging

Adicione um nó **HTTP Request** para enviar logs para outro serviço.

### 4. Notificação por Email

Adicione um nó **Send Email** após o download concluir.

---

## 📚 Recursos Adicionais

- **Documentação n8n:** https://docs.n8n.io
- **API YouTube Downloader:** Veja README.md
- **Repositório GitHub:** https://github.com/brotto/youtube-downloader-api

---

## ✅ Checklist de Implantação

- [ ] Workflow importado no n8n
- [ ] URLs atualizadas para o ambiente correto
- [ ] Serviço YouTube Downloader rodando
- [ ] Teste com um vídeo curto realizado
- [ ] Mensagens de erro testadas
- [ ] Timeout ajustado se necessário
- [ ] Workflow ativado no n8n

---

**Última atualização:** 24 de Dezembro de 2025
**Versão do Workflow:** 1.0.0
**Compatível com:** n8n v1.0+
