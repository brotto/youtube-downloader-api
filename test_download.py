#!/usr/bin/env python3
"""
Script de teste para a aplicação YouTube Downloader
Execute este script para testar o download localmente
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5000"

def test_health():
    """Testa o endpoint de health check"""
    print("🔍 Testando health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200

def test_info(url):
    """Testa obter informações do vídeo"""
    print(f"📋 Obtendo informações do vídeo: {url}")
    response = requests.post(
        f"{BASE_URL}/info",
        json={"url": url}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Título: {data.get('title')}")
        print(f"Duração: {data.get('duration')}s")
        print(f"Uploader: {data.get('uploader')}")
        print(f"Views: {data.get('view_count')}\n")
        return True
    else:
        print(f"Erro: {response.json()}\n")
        return False

def test_download(url, format_type="best"):
    """Testa download do vídeo"""
    print(f"⬇️  Fazendo download do vídeo (formato: {format_type})...")
    response = requests.post(
        f"{BASE_URL}/download",
        json={"url": url, "format": format_type}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Download concluído!")
        print(f"Título: {data.get('title')}")
        print(f"Arquivo: {data.get('filename')}\n")
        return data.get('filename')
    else:
        print(f"❌ Erro: {response.json()}\n")
        return None

def test_list_files():
    """Testa listagem de arquivos"""
    print("📁 Listando arquivos baixados...")
    response = requests.get(f"{BASE_URL}/files")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total de arquivos: {data.get('count')}")
        for file in data.get('files', []):
            print(f"  - {file['filename']} ({file['size']} bytes)\n")
        return True
    else:
        print(f"Erro: {response.json()}\n")
        return False

def main():
    """Executa os testes"""
    print("=" * 60)
    print("YouTube Downloader - Script de Teste")
    print("=" * 60)
    print()

    # URL de teste (vídeo curto do YouTube)
    test_url = input("Digite a URL do YouTube (ou Enter para usar URL de teste): ").strip()
    if not test_url:
        # URL de teste padrão - vídeo curto
        test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
        print(f"Usando URL de teste: {test_url}\n")

    try:
        # Teste 1: Health Check
        if not test_health():
            print("❌ Servidor não está respondendo. Certifique-se de que a aplicação está rodando.")
            print("Execute: python app.py")
            sys.exit(1)

        # Teste 2: Obter informações
        if not test_info(test_url):
            print("❌ Falha ao obter informações do vídeo.")
            sys.exit(1)

        # Teste 3: Download
        filename = test_download(test_url, format_type="best")
        if not filename:
            print("❌ Falha no download.")
            sys.exit(1)

        # Teste 4: Listar arquivos
        if not test_list_files():
            print("❌ Falha ao listar arquivos.")
            sys.exit(1)

        print("=" * 60)
        print("✅ Todos os testes passaram com sucesso!")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("\n❌ Erro de conexão!")
        print("Certifique-se de que a aplicação está rodando:")
        print("  python app.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
