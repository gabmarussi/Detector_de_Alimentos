1#!/usr/bin/env python
"""
🎬 RUN.PY - Detector de Alimentos - Fácil de Usar

Simplesmente rode este arquivo com o play button do VS Code.
Você será solicitado a escolher entre:
- Webcam do MacBook (câmera interna)
- Continuity Camera (iPhone)
- Imagem estática

Sem necessidade de terminal ou argumentos de linha de comando!
"""

from detector import FoodDetector
from pathlib import Path


def show_menu():
    """Exibe menu de opções ao usuário."""
    print("\n" + "="*60)
    print("🍽️  DETECTOR DE ALIMENTOS - YOLOv8")
    print("="*60)
    print("\nEscolha uma opção:\n")
    print("  [1] 📱 Webcam do MacBook (câmera interna)")
    print("  [2] 🍎 Continuity Camera (iPhone)")
    print("  [3] 📷 Imagem estática")
    print("  [0] ❌ Sair")
    print("\n" + "-"*60)
    
    while True:
        choice = input("Digite sua opção (0-3): ").strip()
        if choice in ["0", "1", "2", "3"]:
            return choice
        print("❌ Opção inválida! Tente novamente.")


def main():
    """Função principal."""
    choice = show_menu()
    
    if choice == "0":
        print("\n👋 Até logo!\n")
        return
    
    # Caminho do modelo
    model_path = Path(__file__).parent.parent / "runs" / "food-v6-local" / "weights" / "best.pt"
    
    if not model_path.exists():
        print(f"\n❌ ERRO: Modelo não encontrado em {model_path}")
        print("📝 Verifique se o treinamento foi concluído com sucesso.\n")
        return
    
    try:
        print(f"\n✅ Modelo carregado: {model_path.name}")
        print(f"📊 Confiança mínima: 60%\n")
        
        detector = FoodDetector(str(model_path), confidence=0.6)
        
        if choice == "1":
            # MacBook
            print("📱 Iniciando câmera interna do MacBook...")
            print("💡 Dica: Aponte para arroz, feijão ou macarrão")
            print("⌨️  Pressione 'q' para fechar\n")
            detector.detect_from_webcam(camera_id=0)
        
        elif choice == "2":
            # iPhone Continuity
            print("🍎 Iniciando Continuity Camera (iPhone)...")
            print("💡 Dica: Certifique-se de que o iPhone está conectado")
            print("⌨️  Pressione 'q' para fechar\n")
            try:
                detector.detect_from_webcam(camera_id=1)
            except RuntimeError as e:
                print(f"\n⚠️  Aviso: {e}")
                print("💡 Solução: Verifique se o iPhone está conectado como câmera contínua.")
                print("   Acesse: System Preferences > General > AirPlay and Continuity > Camera\n")
        
        elif choice == "3":
            # Imagem
            image_path = input("\n📁 Digite o caminho da imagem: ").strip()
            if not Path(image_path).exists():
                print(f"\n❌ ERRO: Imagem não encontrada em {image_path}\n")
                return
            
            print(f"\n📷 Analisando imagem...")
            detector.detect_from_image(image_path)
    
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        print("📝 Verifique o terminal para mais detalhes.\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
