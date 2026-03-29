# ============================================================================
# CONFIGURAÇÃO RÁPIDA - COLE NO COLAB (VERSÃO SIMPLIFICADA)
# ============================================================================

# SETUP INICIAL
!pip install ultralytics roboflow -q

# DOWNLOAD DATASET v8 (com negative samples)
from roboflow import Roboflow
rf = Roboflow(api_key="GXO0UpkRHsAfnSH7NoRA")
project = rf.workspace("pessoagenerica666-gmail-com").project("food-detector-9zgsn-d8m90")
dataset = project.version(8).download("yolov11")  # ← Ajuste versão conforme criada

# TREINO OTIMIZADO
from ultralytics import YOLO

model = YOLO('yolo11n.pt')  # ← YOLOv11 (correto!)

results = model.train(
    data=f'{dataset.location}/data.yaml',
    epochs=150,
    batch=16,
    imgsz=640,
    patience=30,
    optimizer='AdamW',
    lr0=0.001,
    degrees=10.0,
    shear=2.0,
    perspective=0.0001,
    mixup=0.15,
    copy_paste=0.1,
    cache=True,  # ← Importante para velocidade
    device=0,
    workers=8,
    project='runs/detect',
    name='food_v8_optimized',
    verbose=True,
    seed=42
)

# AVALIAÇÃO NO TEST SET
test_results = model.val(split='test', plots=True)

print(f"\n🎯 RESULTADOS FINAIS:")
print(f"mAP@50: {test_results.box.map50*100:.2f}%")
print(f"Precision: {test_results.box.mp*100:.2f}%")
print(f"Recall: {test_results.box.mr*100:.2f}%")

# DOWNLOAD DO MODELO
from google.colab import files

# ============================================================================
# DOWNLOAD COMPLETO - DATASET + RUN
# ============================================================================

print("\n📦 Compactando arquivos para download...")

# 1. Compactar toda a pasta de treino (results, weights, plots)
!zip -r food_v8_run_completo.zip runs/detect/food_v8_optimized

# 2. Compactar dataset completo (train/valid/test/data.yaml)
!zip -r food_v8_dataset.zip {dataset.location}

# 3. Copiar best.pt separado (para uso rápido)
!cp runs/detect/food_v8_optimized/weights/best.pt ./food_v8_best.pt

print("✅ Arquivos prontos para download!\n")

# DOWNLOAD DOS ARQUIVOS
print("📥 Baixando arquivos...")
print("  1/3: Modelo best.pt (~12MB)")
files.download('food_v8_best.pt')

print("  2/3: Run completo com métricas (~50-100MB)")
files.download('food_v8_run_completo.zip')

print("  3/3: Dataset completo (~200-300MB)")
files.download('food_v8_dataset.zip')

print("\n✅ DOWNLOAD CONCLUÍDO!")
print("\nArquivos baixados:")
print("  📄 food_v8_best.pt - Modelo treinado")
print("  📦 food_v8_run_completo.zip - Métricas, gráficos, checkpoints")
print("  📦 food_v8_dataset.zip - Dataset completo (train/valid/test)")
print("\n💡 Extraia os ZIPs no seu projeto local:")
print("  - Veja INSTRUCOES_ORGANIZACAO.txt no projeto")
print("  - Dataset → detector/")
print("  - Run → detector/runs/train/")
