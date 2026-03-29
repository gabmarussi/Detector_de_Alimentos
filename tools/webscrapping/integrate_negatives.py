#!/usr/bin/env python3
"""
Script para integrar imagens negativas no dataset YOLO.
Copia imagens e cria labels vazios para imagens sem detecções.
"""

import argparse
import shutil
from pathlib import Path


def integrate_negative_samples(
    negative_dir: Path,
    dataset_dir: Path,
    split: str = "test",
    create_empty_labels: bool = True,
) -> None:
    """
    Integra imagens negativas no dataset YOLO.
    
    Args:
        negative_dir: Localização das imagens negativas
        dataset_dir: Raiz do dataset YOLO
        split: split do dataset (train/valid/test)
        create_empty_labels: Criar labels vazios (.txt) para imagens
    """
    
    # Validar caminhos
    if not negative_dir.exists():
        print(f"✗ Pasta de negativas não encontrada: {negative_dir}")
        return
    
    dataset_dir = dataset_dir.resolve()
    images_dir = dataset_dir / split / "images"
    labels_dir = dataset_dir / split / "labels"
    
    images_dir.mkdir(parents=True, exist_ok=True)
    labels_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Integrando imagens negativas ao dataset")
    print(f"Origem: {negative_dir}")
    print(f"Destino: {images_dir}")
    
    # Copiar imagens
    negative_images = sorted(negative_dir.glob("*.jpg"))
    if not negative_images:
        print("✗ Nenhuma imagem encontrada em negative_samples/")
        return
    
    copied_count = 0
    for img_path in negative_images:
        dest_path = images_dir / img_path.name
        try:
            shutil.copy2(img_path, dest_path)
            
            # Criar label vazio se solicitado
            if create_empty_labels:
                label_path = labels_dir / dest_path.with_suffix(".txt").name
                label_path.touch()
            
            copied_count += 1
        except Exception as e:
            print(f"✗ Erro ao copiar {img_path.name}: {e}")
    
    print(f"✓ {copied_count}/{len(negative_images)} imagens copiadas")
    print(f"✓ Labels vazios criados: {copied_count}")
    print(f"\nPróximo passo: Retreinar o modelo com 'python detector/run.py'")


def main():
    parser = argparse.ArgumentParser(
        description="Integra imagens negativas ao dataset YOLO"
    )
    parser.add_argument(
        "--negative-dir",
        type=str,
        default="negative_samples",
        help="Pasta com imagens negativas (default: negative_samples)",
    )
    parser.add_argument(
        "--dataset-dir",
        type=str,
        default="detector",
        help="Raiz da pasta do dataset YOLO (default: detector)",
    )
    parser.add_argument(
        "--split",
        type=str,
        default="test",
        choices=["train", "valid", "test"],
        help="Split do dataset para adicionar (default: test)",
    )
    parser.add_argument(
        "--no-labels",
        action="store_true",
        help="NÃO criar labels vazios",
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("INTEGRAÇÃO DE IMAGENS NEGATIVAS NO DATASET")
    print("=" * 60)
    
    integrate_negative_samples(
        negative_dir=Path(args.negative_dir),
        dataset_dir=Path(args.dataset_dir),
        split=args.split,
        create_empty_labels=not args.no_labels,
    )


if __name__ == "__main__":
    main()
