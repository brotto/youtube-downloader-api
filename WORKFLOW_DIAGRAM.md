# Diagrama do Workflow n8n - YouTube Downloader

## 📊 Workflow Completo (n8n-workflow.json)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           YouTube Downloader Workflow                        │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────┐
    │  Chat Trigger        │ ← Usuário envia URL do YouTube
    │  (Manual Chat)       │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │ Extract YouTube URL  │
    │ - youtubeUrl         │
    │ - format: "best"     │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │  Get Video Info      │
    │  POST /info          │
    │  Timeout: 30s        │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │ Video Info Valid?    │ ◄─── IF: success === true
    └─────┬────────────┬───┘
          │            │
      ✅ TRUE      ❌ FALSE
          │            │
          │            ▼
          │     ┌─────────────────┐
          │     │ Send Info Error │
          │     │ ❌ Link Inválido│
          │     └─────────────────┘
          │
          ▼
   ┌──────────────────┐
   │ Prepare Video    │
   │ Data             │
   │ - title          │
   │ - duration       │
   │ - uploader       │
   │ - view_count     │
   └────────┬─────────┘
            │
            ▼
   ┌──────────────────┐
   │ Send Info        │
   │ Message          │
   │ 📹 Título        │
   │ 👤 Canal         │
   │ ⏱️ Duração       │
   │ 👁️ Views         │
   └────────┬─────────┘
            │
            ▼
   ┌──────────────────┐
   │ Download Video   │
   │ POST /download   │
   │ Timeout: 300s    │
   └────────┬─────────┘
            │
            ▼
   ┌──────────────────┐
   │ Download         │
   │ Success?         │ ◄─── IF: success === true
   └─────┬────────┬───┘
         │        │
     ✅ TRUE  ❌ FALSE
         │        │
         │        ▼
         │   ┌────────────────────┐
         │   │ Send Download Error│
         │   │ ❌ Erro no Download│
         │   └────────────────────┘
         │
         ▼
   ┌────────────────┐
   │ Get Video File │
   │ GET /files/... │
   │ Format: File   │
   └────────┬───────┘
            │
            ▼
   ┌────────────────┐
   │ Send Success   │
   │ Message        │
   │ ✅ Download OK │
   │ 📁 Filename    │
   └────────┬───────┘
            │
            ▼
   ┌────────────────┐
   │ Delete Video   │ ⚠️ OPCIONAL (Desabilitado)
   │ (Optional)     │
   │ DELETE /files  │
   └────────────────┘
```

---

## 🎯 Workflow Simples (n8n-workflow-simple.json)

```
┌─────────────────────────────────────────────────────────┐
│           YouTube Downloader Workflow - Simple          │
└─────────────────────────────────────────────────────────┘

    ┌──────────────────┐
    │  Chat Trigger    │ ← Usuário envia URL
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────────┐
    │ Download YouTube     │
    │ Video                │
    │ POST /download       │
    │                      │
    │ Body:                │
    │ {                    │
    │   url: chatInput,    │
    │   format: "best"     │
    │ }                    │
    └────────┬─────────────┘
             │
             ▼
    ┌──────────────────────┐
    │ Send Response        │
    │                      │
    │ IF success:          │
    │   ✅ Download OK     │
    │   📹 Title           │
    │   👤 Uploader        │
    │   📁 Filename        │
    │ ELSE:                │
    │   ❌ Error           │
    └──────────────────────┘
```

---

## 📋 Comparação de Workflows

| Característica                | Workflow Completo | Workflow Simples |
|------------------------------|-------------------|------------------|
| **Nós Totais**               | 13                | 3                |
| **Validação de URL**         | ✅ Sim            | ❌ Não           |
| **Info antes do Download**   | ✅ Sim            | ❌ Não           |
| **Mensagens de Status**      | ✅ Múltiplas      | ✅ Uma           |
| **Tratamento de Erros**      | ✅ Completo       | ✅ Básico        |
| **Download de Arquivo**      | ✅ Sim            | ❌ Não           |
| **Deleção Automática**       | ✅ Opcional       | ❌ Não           |
| **Tempo de Setup**           | ~5 minutos        | ~1 minuto        |
| **Recomendado para**         | Produção          | Testes/Dev       |

---

## 🔄 Endpoints Utilizados

### 1. GET /health
- **Uso:** Health check (não usado nos workflows, mas disponível)
- **Response:** `{ "status": "healthy", "service": "youtube-downloader" }`

### 2. POST /info
- **Uso:** Obter informações do vídeo sem baixar
- **Request:** `{ "url": "https://youtube.com/..." }`
- **Response:** `{ "success": true, "title": "...", "duration": 123, ... }`
- **Usado em:** Workflow Completo

### 3. POST /download
- **Uso:** Baixar vídeo
- **Request:** `{ "url": "https://youtube.com/...", "format": "best" }`
- **Response:** `{ "success": true, "filename": "...", "filepath": "...", ... }`
- **Usado em:** Ambos workflows

### 4. GET /files
- **Uso:** Listar todos arquivos baixados
- **Response:** `{ "success": true, "files": [...], "count": 5 }`
- **Usado em:** Não usado nos workflows (disponível para expansão)

### 5. GET /files/{filename}
- **Uso:** Baixar arquivo específico
- **Response:** Binary file
- **Usado em:** Workflow Completo

### 6. DELETE /files/{filename}
- **Uso:** Deletar arquivo
- **Response:** `{ "success": true, "message": "..." }`
- **Usado em:** Workflow Completo (opcional)

---

## 💡 Dicas de Uso

### Quando usar o Workflow Completo?
- ✅ Ambiente de produção
- ✅ Precisa validar URLs antes do download
- ✅ Quer mostrar informações do vídeo ao usuário
- ✅ Precisa do arquivo binário no n8n
- ✅ Quer limpar arquivos após o download

### Quando usar o Workflow Simples?
- ✅ Desenvolvimento e testes
- ✅ Download rápido sem validações
- ✅ Apenas precisa confirmar que o download foi feito
- ✅ Arquivos ficam no servidor para uso posterior

---

## 🛠️ Customizações Possíveis

### 1. Adicionar Seleção de Formato
Adicione um nó **Set** que pergunta ao usuário:
```javascript
{{ $json.chatInput.includes('mp3') ? 'audio' : 'best' }}
```

### 2. Adicionar Queue
Use um nó **Queue** para processar múltiplos downloads:
```
Chat → Queue → Download (Loop)
```

### 3. Salvar Metadados
Adicione um nó **Database** após o download:
```
Download → Save to DB (title, url, filename, timestamp)
```

### 4. Notificação Email
Adicione após o sucesso:
```
Success → Send Email → Done
```

### 5. Integração com Drive
Adicione upload para Google Drive:
```
Get File → Upload to Drive → Delete Local File
```

---

## 📊 Fluxo de Dados

### Workflow Completo - Dados por Nó

```
Chat Trigger
  └─> { chatInput: "https://youtu.be/..." }

Extract URL
  └─> { youtubeUrl: "https://youtu.be/...", format: "best" }

Get Info
  └─> { success: true, title: "...", duration: 123, uploader: "...", ... }

Prepare Data
  └─> { title: "...", duration: 123, uploader: "...", view_count: 1000, youtubeUrl: "..." }

Download Video
  └─> { success: true, filename: "video.mp4", filepath: "./downloads/video.mp4", ... }

Get File
  └─> Binary file data

Delete File
  └─> { success: true, message: "File deleted" }
```

---

**Criado por:** Alessandro Brotto
**Data:** 24 de Dezembro de 2025
**Versão:** 1.0.0
**Repositório:** https://github.com/brotto/youtube-downloader-api
