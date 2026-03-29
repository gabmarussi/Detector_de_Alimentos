# ============================================================================
# GUIA COMPLETO - TREINO YOLO11 COM NEGATIVE SAMPLES
# ============================================================================

DATASET:
- 790 imagens com anotações (beans, pasta, rice)
- 200 imagens negativas (sem anotações)
- Total: 990 imagens

PORCENTAGENS RECOMENDADAS:
- Train: 60% (~594 imgs: 474 positivas + 120 negativas)
- Valid: 20% (~198 imgs: 158 positivas + 40 negativas)
- Test: 20% (~198 imgs: 158 positivas + 40 negativas)

MOTIVO:
- 60% treino garante dados suficientes para aprender
- 20/20 valid/test dá avaliação equilibrada
- Negative samples distribuídos proporcionalmente

# ============================================================================
# CÓDIGO GOOGLE COLAB - PARTE 1: SETUP E DOWNLOAD
# ============================================================================

# 1. Instalar Ultralytics YOLO11
!pip install ultralytics roboflow

# 2. Download do dataset (com suas 200 imagens negativas já adicionadas)
from roboflow import Roboflow

rf = Roboflow(api_key="GXO0UpkRHsAfnSH7NoRA")
project = rf.workspace("pessoagenerica666-gmail-com").project("food-detector-9zgsn-d8m90")

# IMPORTANTE: Use a versão NOVA com negative samples!
# Assumindo que você criou v8 no Roboflow com 60/20/20
dataset = project.version(8).download("yolov11")

# 3. Verificar o dataset baixado
!ls -la {dataset.location}
!cat {dataset.location}/data.yaml

# ============================================================================
# CÓDIGO GOOGLE COLAB - PARTE 2: TREINO OTIMIZADO
# ============================================================================

from ultralytics import YOLO
import torch

# Verificar se GPU está disponível
print(f"CUDA disponível: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")

# Carregar modelo YOLOv11 nano (CORRETO!)
model = YOLO('yolo11n.pt')

# TREINO OTIMIZADO COM HIPERPARÂMETROS AJUSTADOS
results = model.train(
    # Dataset
    data=f'{dataset.location}/data.yaml',
    
    # Épocas e batch
    epochs=150,              # ← AUMENTADO! Com negative samples, mais épocas ajudam
    batch=16,                # Mantenha 16 se Colab free, 32 se Pro
    imgsz=640,
    
    # Early stopping e checkpoints
    patience=30,             # Para se não melhorar em 30 épocas
    save=True,
    save_period=10,          # Salvar checkpoint a cada 10 épocas
    
    # Otimizador
    optimizer='AdamW',       # Melhor que SGD para datasets pequenos
    lr0=0.001,              # Learning rate inicial (reduzido)
    lrf=0.01,               # Learning rate final
    momentum=0.937,
    weight_decay=0.0005,
    
    # Augmentations (importantes!)
    hsv_h=0.015,            # Variação de matiz
    hsv_s=0.7,              # Saturação
    hsv_v=0.4,              # Valor (brightness)
    degrees=10.0,           # ← AUMENTADO! Rotação até 10 graus
    translate=0.1,          # Translação
    scale=0.5,              # Escala
    shear=2.0,              # ← ADICIONADO! Cisalhamento
    perspective=0.0001,     # ← ADICIONADO! Perspectiva
    flipud=0.0,             # Não inverter verticalmente (embalagens têm orientação)
    fliplr=0.5,             # Inverter horizontalmente (50% chance)
    mosaic=1.0,             # Mosaic augmentation (importante!)
    mixup=0.15,             # ← AUMENTADO! Mix de imagens (ajuda com negatives)
    copy_paste=0.1,         # ← ADICIONADO! Copy-paste augmentation
    
    # Performance
    device=0,               # GPU 0
    workers=8,              # Threads de carregamento
    cache=True,             # ← IMPORTANTE! Cache imagens na RAM (mais rápido)
    
    # Validação
    val=True,
    plots=True,             # Gerar gráficos
    
    # Projeto
    project='runs/detect',
    name='food_v8_optimized',
    exist_ok=False,
    
    # Outros
    pretrained=True,        # Transfer learning
    verbose=True,
    seed=42                 # Reprodutibilidade
)

# ============================================================================
# CÓDIGO GOOGLE COLAB - PARTE 3: AVALIAÇÃO E EXPORTAÇÃO
# ============================================================================

# 1. Avaliar no Test Set
test_results = model.val(
    data=f'{dataset.location}/data.yaml',
    split='test',
    batch=16,
    imgsz=640,
    plots=True
)

# 2. Imprimir métricas finais
print("\n" + "="*60)
print("MÉTRICAS FINAIS - TEST SET")
print("="*60)
print(f"mAP@50: {test_results.box.map50:.4f} ({test_results.box.map50*100:.2f}%)")
print(f"mAP@50-95: {test_results.box.map:.4f} ({test_results.box.map*100:.2f}%)")
print(f"Precision: {test_results.box.mp:.4f} ({test_results.box.mp*100:.2f}%)")
print(f"Recall: {test_results.box.mr:.4f} ({test_results.box.mr*100:.2f}%)")
print("="*60)

# 3. Exportar modelo otimizado (opcional, para inferência mais rápida)
model.export(format='onnx', imgsz=640, half=False)

# 4. Compactar resultados para download
!zip -r food_v8_results.zip runs/detect/food_v8_optimized

# ============================================================================
# CÓDIGO GOOGLE COLAB - PARTE 4: ANÁLISE DETALHADA (OPCIONAL)
# ============================================================================

# Visualizar confusion matrix
from IPython.display import Image, display
display(Image('runs/detect/food_v8_optimized/confusion_matrix.png'))

# Ver curvas de aprendizado
display(Image('runs/detect/food_v8_optimized/results.png'))

# Análise por classe
print("\n" + "="*60)
print("MÉTRICAS POR CLASSE")
print("="*60)
for i, name in enumerate(model.names.values()):
    print(f"\n{name}:")
    print(f"  AP@50: {test_results.box.class_result(i)[2]:.4f}")
    print(f"  Precision: {test_results.box.class_result(i)[0]:.4f}")
    print(f"  Recall: {test_results.box.class_result(i)[1]:.4f}")

# ============================================================================
# CÓDIGO GOOGLE COLAB - PARTE 5: TESTE RÁPIDO COM IMAGEM
# ============================================================================

# Testar com uma imagem do test set
import glob
import random

test_images = glob.glob(f'{dataset.location}/test/images/*.jpg')
test_img = random.choice(test_images)

# Predição
results = model(test_img, conf=0.7)

# Visualizar
from matplotlib import pyplot as plt
import cv2

img = cv2.imread(test_img)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Plot com detecções
results_img = results[0].plot()
plt.figure(figsize=(12, 8))
plt.imshow(results_img)
plt.axis('off')
plt.title(f"Teste: {test_img.split('/')[-1]}")
plt.show()

# ============================================================================
# DOWNLOAD DOS RESULTADOS
# ============================================================================

from google.colab import files

# Download do modelo treinado
!cp runs/detect/food_v8_optimized/weights/best.pt ./food_v8_best.pt
files.download('food_v8_best.pt')

# Download do ZIP completo (opcional)
files.download('food_v8_results.zip')

print("\n✅ TREINO CONCLUÍDO!")
print("Arquivos prontos para download:")
print("  - food_v8_best.pt (modelo)")
print("  - food_v8_results.zip (resultados completos)")

# ============================================================================
# MÉTRICAS ESPERADAS COM OTIMIZAÇÕES
# ============================================================================

# Com 990 imagens (790 + 200 negatives) e hiperparâmetros otimizados:
#
# ESTIMATIVA:
# - mAP@50: 78-82% (melhora de ~3-7% vs v7)
# - Precision: 94-97% (mantém alta, pode melhorar)
# - Recall: 72-78% (melhora significativa com negative samples)
#
# NEGATIVE SAMPLES AJUDAM:
# - Reduzem falsos positivos (precision se mantém ou melhora)
# - Modelo aprende o que NÃO é alimento
# - Mais robusto em ambientes diversos
#
# MAIS ÉPOCAS (150 vs 100):
# - Permite convergência melhor
# - Patience 30 evita overfitting
# - Early stopping para no momento ideal

# ============================================================================
# DICAS IMPORTANTES
# ============================================================================

# 1. Se Colab crashar por falta de RAM:
#    - Reduza batch para 8
#    - Desative cache: cache=False
#    - Use imgsz=512 ao invés de 640

# 2. Se quiser treino AINDA MAIS LONGO:
#    - epochs=200, patience=40
#    - Mas cuidado com overfitting!

# 3. Monitoramento durante treino:
#    - Acompanhe mAP50 no validation
#    - Se estabilizar, vai parar automático (patience)

# 4. Após treino:
#    - Compare v8 com v7 no mesmo test set
#    - Veja confusion matrix para erros comuns
#    - Teste em imagens reais não vistas

# ============================================================================
# FIM DO GUIA
# ============================================================================
