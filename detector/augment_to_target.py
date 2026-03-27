import argparse
import random
from pathlib import Path

from PIL import Image, ImageEnhance


CLASS_PATTERNS = {
    "rice_package": "rice_package_*.jpg",
    "beans_package": "beans_package_*.jpg",
    "pasta_package": "pasta_package_*.jpg",
}


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def random_augment(img: Image.Image) -> Image.Image:
    out = img.convert("RGB")

    # Mild transforms preserve package readability while increasing variability.
    angle = random.uniform(-8.0, 8.0)
    out = out.rotate(angle, expand=False, fillcolor=(255, 255, 255))

    if random.random() < 0.5:
        out = out.transpose(Image.FLIP_LEFT_RIGHT)

    brightness = ImageEnhance.Brightness(out)
    out = brightness.enhance(random.uniform(0.85, 1.15))

    contrast = ImageEnhance.Contrast(out)
    out = contrast.enhance(random.uniform(0.85, 1.2))

    color = ImageEnhance.Color(out)
    out = color.enhance(random.uniform(0.85, 1.15))

    width, height = out.size
    scale = random.uniform(0.9, 1.0)
    crop_w = int(width * scale)
    crop_h = int(height * scale)
    left = random.randint(0, max(width - crop_w, 0))
    top = random.randint(0, max(height - crop_h, 0))
    out = out.crop((left, top, left + crop_w, top + crop_h)).resize((width, height))

    return out


def next_index(class_dir: Path, class_name: str) -> int:
    max_idx = 0
    for p in class_dir.glob(f"{class_name}_*.jpg"):
        stem = p.stem
        try:
            idx = int(stem.split("_")[-1])
            max_idx = max(max_idx, idx)
        except ValueError:
            continue

    for p in class_dir.glob(f"{class_name}_aug_*.jpg"):
        stem = p.stem
        try:
            idx = int(stem.split("_")[-1])
            max_idx = max(max_idx, idx)
        except ValueError:
            continue

    return max_idx + 1


def collect_base_images(class_dir: Path, class_name: str) -> list[Path]:
    base = list(class_dir.glob(f"{class_name}_*.jpg"))
    base.extend(class_dir.glob(f"{class_name}_aug_*.jpg"))
    return sorted(base)


def top_up_class(class_dir: Path, class_name: str, target: int) -> None:
    ensure_dir(class_dir)

    current = len(collect_base_images(class_dir, class_name))
    print(f"[{class_name}] atual: {current} | alvo: {target}")
    if current == 0:
        print(f"[{class_name}] sem imagens base, pulando")
        return

    idx = next_index(class_dir, class_name)
    while current < target:
        sources = collect_base_images(class_dir, class_name)
        src = random.choice(sources)

        with Image.open(src) as img:
            aug = random_augment(img)

        out_path = class_dir / f"{class_name}_aug_{idx:05d}.jpg"
        aug.save(out_path, format="JPEG", quality=92)

        idx += 1
        current += 1

    print(f"[{class_name}] final: {current}")


def parse_args():
    parser = argparse.ArgumentParser(description="Completa dataset por augmentations")
    parser.add_argument("--root", type=str, default="../Alimentos")
    parser.add_argument("--target", type=int, default=250)
    parser.add_argument("--only", type=str, default="")
    return parser.parse_args()


def main():
    args = parse_args()
    root = Path(args.root).resolve()

    class_names = list(CLASS_PATTERNS.keys())
    if args.only:
        if args.only not in CLASS_PATTERNS:
            raise ValueError("Classe invalida em --only")
        class_names = [args.only]

    for class_name in class_names:
        class_dir = root / class_name
        top_up_class(class_dir, class_name, args.target)

    print("\nAugmentation finalizada.")


if __name__ == "__main__":
    main()
