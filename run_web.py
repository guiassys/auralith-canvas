"""Script alternativo para executar a interface Web do Auralith de qualquer diretório."""

import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

def get_server_port():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            return config.get("web_settings", {}).get("server_port", 7860)
    except Exception:
        return 7860

def get_server_host():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            return config.get("web_settings", {}).get("server_host", "0.0.0.0")
    except Exception:
        return "0.0.0.0"

def main():
    # Encontra o diretório raiz do projeto independentemente de onde o script é executado
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Assume que este script está na raiz do projeto
    project_root = current_dir

    # Verifica se estamos no diretório correto procurando por 'src'
    if not os.path.exists(os.path.join(project_root, 'src')):
        print("❌ Erro: Execute este script a partir do diretório raiz do projeto (auralith/)")
        print("📁 Diretório atual:", project_root)
        return

    # Adiciona ao path
    sys.path.insert(0, project_root)
    server_host = get_server_host()
    server_port = get_server_port()

    try:
        from src.web.app import interface
        print("🚀 Iniciando Auralith Canvas...")
        print(f"📱 Acesse: http://{server_host}:{server_port}")
        print("❌ Pressione Ctrl+C para parar")

        interface.launch(
            server_name=server_host,
            server_port=server_port,
            show_error=True
        )
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Certifique-se de que todas as dependências estão instaladas:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()