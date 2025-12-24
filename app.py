#!/usr/bin/env python3
"""
YouTube Video Downloader API
Aplicação Flask para download de vídeos do YouTube
Integração com n8n workflow
"""

import os
import json
import logging
from flask import Flask, request, jsonify, send_file
from pathlib import Path
import yt_dlp
import tempfile
import shutil

app = Flask(__name__)

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Diretório para downloads
DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR', './downloads')
Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)


def download_video(url, output_path=DOWNLOAD_DIR, format_type='best'):
    """
    Faz download de vídeo do YouTube

    Args:
        url: URL do vídeo do YouTube
        output_path: Diretório de saída
        format_type: Tipo de formato (best, audio, video)

    Returns:
        dict com informações do download
    """
    try:
        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        # Configurações baseadas no tipo de formato
        if format_type == 'audio':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        elif format_type == 'video':
            ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        else:  # best
            ydl_opts['format'] = 'best[ext=mp4]/best'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extrai informações do vídeo
            info = ydl.extract_info(url, download=True)

            # Constrói o caminho do arquivo baixado
            filename = ydl.prepare_filename(info)
            if format_type == 'audio':
                filename = os.path.splitext(filename)[0] + '.mp3'

            return {
                'success': True,
                'title': info.get('title'),
                'filename': os.path.basename(filename),
                'filepath': filename,
                'duration': info.get('duration'),
                'uploader': info.get('uploader'),
                'description': info.get('description'),
                'thumbnail': info.get('thumbnail'),
                'view_count': info.get('view_count'),
                'format': format_type
            }

    except Exception as e:
        logger.error(f"Erro ao fazer download: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'youtube-downloader'
    }), 200


@app.route('/download', methods=['POST'])
def download():
    """
    Endpoint para download de vídeos

    Body JSON:
        {
            "url": "https://youtube.com/watch?v=...",
            "format": "best|audio|video" (opcional, padrão: best)
        }
    """
    try:
        data = request.get_json()

        if not data or 'url' not in data:
            return jsonify({
                'success': False,
                'error': 'URL é obrigatória'
            }), 400

        url = data['url']
        format_type = data.get('format', 'best')

        logger.info(f"Iniciando download: {url} (formato: {format_type})")

        result = download_video(url, format_type=format_type)

        if result['success']:
            logger.info(f"Download concluído: {result['filename']}")
            return jsonify(result), 200
        else:
            logger.error(f"Falha no download: {result['error']}")
            return jsonify(result), 500

    except Exception as e:
        logger.error(f"Erro no endpoint /download: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/info', methods=['POST'])
def get_info():
    """
    Endpoint para obter informações do vídeo sem fazer download

    Body JSON:
        {
            "url": "https://youtube.com/watch?v=..."
        }
    """
    try:
        data = request.get_json()

        if not data or 'url' not in data:
            return jsonify({
                'success': False,
                'error': 'URL é obrigatória'
            }), 400

        url = data['url']

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            return jsonify({
                'success': True,
                'title': info.get('title'),
                'duration': info.get('duration'),
                'uploader': info.get('uploader'),
                'description': info.get('description'),
                'thumbnail': info.get('thumbnail'),
                'view_count': info.get('view_count'),
                'upload_date': info.get('upload_date'),
                'formats_available': len(info.get('formats', []))
            }), 200

    except Exception as e:
        logger.error(f"Erro ao obter informações: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/files', methods=['GET'])
def list_files():
    """Lista todos os arquivos baixados"""
    try:
        files = []
        for file in Path(DOWNLOAD_DIR).iterdir():
            if file.is_file():
                files.append({
                    'filename': file.name,
                    'size': file.stat().st_size,
                    'modified': file.stat().st_mtime
                })

        return jsonify({
            'success': True,
            'files': files,
            'count': len(files)
        }), 200

    except Exception as e:
        logger.error(f"Erro ao listar arquivos: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    """Retorna um arquivo específico"""
    try:
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        if not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'error': 'Arquivo não encontrado'
            }), 404

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        logger.error(f"Erro ao enviar arquivo: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/files/<filename>', methods=['DELETE'])
def delete_file(filename):
    """Deleta um arquivo específico"""
    try:
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        if not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'error': 'Arquivo não encontrado'
            }), 404

        os.remove(filepath)
        logger.info(f"Arquivo deletado: {filename}")

        return jsonify({
            'success': True,
            'message': f'Arquivo {filename} deletado com sucesso'
        }), 200

    except Exception as e:
        logger.error(f"Erro ao deletar arquivo: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
