# YouTube Video Downloader API

Aplicação Python Flask para download de vídeos do YouTube, desenvolvida para integração com workflows do n8n.

## Características

- Download de vídeos do YouTube via API REST
- Suporte para diferentes formatos (vídeo, áudio, melhor qualidade)
- Extração de informações de vídeos sem download
- Gerenciamento de arquivos baixados
- Containerização com Docker
- Pronto para integração com n8n

## Tecnologias

- Python 3.11
- Flask (API REST)
- yt-dlp (download de vídeos)
- Docker

## Endpoints da API

### Health Check
```bash
GET /health
```

### Download de Vídeo
```bash
POST /download
Content-Type: application/json

{
  "url": "https://youtube.com/watch?v=VIDEO_ID",
  "format": "best"  // Opções: best, video, audio
}
```

### Obter Informações do Vídeo
```bash
POST /info
Content-Type: application/json

{
  "url": "https://youtube.com/watch?v=VIDEO_ID"
}
```

### Listar Arquivos Baixados
```bash
GET /files
```

### Download de Arquivo
```bash
GET /files/{filename}
```

### Deletar Arquivo
```bash
DELETE /files/{filename}
```

## Instalação Local

### Pré-requisitos
- Python 3.11+
- FFmpeg

### Configuração

1. Clone o repositório:
```bash
git clone <repository-url>
cd "Youtube Downloader"
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute a aplicação:
```bash
python app.py
```

A API estará disponível em `http://localhost:5000`

## Usando Docker

### Build da Imagem
```bash
docker build -t youtube-downloader .
```

### Executar Container
```bash
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/downloads:/app/downloads \
  --name youtube-downloader \
  youtube-downloader
```

### Docker Compose (opcional)
```yaml
version: '3.8'
services:
  youtube-downloader:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./downloads:/app/downloads
    environment:
      - PORT=5000
      - DOWNLOAD_DIR=/app/downloads
```

## Integração com n8n

### 🚀 Workflows Prontos para Importar

Este projeto inclui **workflows completos** prontos para importar no n8n:

1. **n8n-workflow.json** - Workflow completo com validações e mensagens de status
2. **n8n-workflow-simple.json** - Workflow minimalista para uso rápido
3. **N8N_INTEGRATION_GUIDE.md** - Guia completo de integração

#### Como Importar:

1. Abra o arquivo `n8n-workflow.json` ou `n8n-workflow-simple.json`
2. Copie todo o conteúdo JSON
3. No n8n, vá em **Workflows** → **Import from File**
4. Cole o JSON e clique em **Import**
5. Ajuste as URLs dos endpoints HTTP Request conforme seu ambiente
6. Ative o workflow

📖 **Guia Completo:** Consulte [N8N_INTEGRATION_GUIDE.md](N8N_INTEGRATION_GUIDE.md) para instruções detalhadas

### Exemplo Manual de Workflow n8n

Se preferir criar manualmente:

1. **HTTP Request Node** - Para fazer download:
   - Method: POST
   - URL: `http://youtube-downloader:5000/download`
   - Body (JSON):
     ```json
     {
       "url": "{{$json.youtubeUrl}}",
       "format": "best"
     }
     ```

2. **HTTP Request Node** - Para obter o arquivo:
   - Method: GET
   - URL: `http://youtube-downloader:5000/files/{{$json.filename}}`

### Exemplo de Uso com cURL

```bash
# Download de vídeo
curl -X POST http://localhost:5000/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtube.com/watch?v=dQw4w9WgXcQ", "format": "best"}'

# Obter informações
curl -X POST http://localhost:5000/info \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtube.com/watch?v=dQw4w9WgXcQ"}'

# Listar arquivos
curl http://localhost:5000/files

# Download de arquivo
curl -O http://localhost:5000/files/nome-do-video.mp4

# Deletar arquivo
curl -X DELETE http://localhost:5000/files/nome-do-video.mp4
```

## Variáveis de Ambiente

- `PORT`: Porta da aplicação (padrão: 5000)
- `DOWNLOAD_DIR`: Diretório para salvar downloads (padrão: ./downloads)

## Deploy no Easy Panel (Hostinger)

1. Faça push do código para o GitHub
2. No Easy Panel, crie um novo projeto
3. Conecte ao repositório GitHub
4. Configure as variáveis de ambiente se necessário
5. O Easy Panel fará o build e deploy automaticamente

## Estrutura do Projeto

```
Youtube Downloader/
├── app.py              # Aplicação Flask principal
├── requirements.txt    # Dependências Python
├── Dockerfile         # Configuração Docker
├── .dockerignore      # Arquivos ignorados no build Docker
├── .gitignore         # Arquivos ignorados pelo Git
├── README.md          # Documentação
└── downloads/         # Diretório de downloads (criado automaticamente)
```

## Notas Importantes

- Os vídeos são baixados na melhor qualidade disponível por padrão
- O formato `audio` converte o vídeo para MP3
- Os arquivos são salvos no diretório `downloads/`
- FFmpeg é necessário para conversão de áudio

## Licença

MIT

## Autor

Alessandro Brotto
