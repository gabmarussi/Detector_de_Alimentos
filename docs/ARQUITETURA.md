# Arquitetura do Projeto

## Visão Geral

O projeto é um detector de alimentos em tempo real que utiliza YOLO (You Only Look Once) para identificar três tipos de produtos alimentícios: arroz, feijão e macarrão.

## Componentes Principais

### 1. Camera (Inferência)

Responsável pela execução do modelo em tempo real.

```
camera/
├── detector.py       # Classe principal FoodDetector
├── run.py            # Script de teste rápido (com argumentos)
├── requirements.txt  # Dependências do projeto
└── yolo11n.pt       # Modelo base YOLO11 nano
```

**FoodDetector** (`camera/detector.py`):

- Gerencia o modelo YOLO carregado
- Implementa dois modos de operação:
  - **Live**: Detecção frame a frame sem contagem
  - **Conveyor**: Tracking com contagem ao cruzar linha
- Desenha overlays com contadores e informações
- Estabiliza detecções via votação de múltiplos frames

### 2. Detector (Dataset e Treino)

Contém o dataset e os modelos treinados.

```
detector/
├── data.yaml              # Configuração do dataset YOLO
├── data/                  # **NOVO** - Dados organizados (separado de código)
│   ├── train/             # Imagens de treino (551 imagens)
│   ├── valid/             # Imagens de validação (161 imagens)
│   └── test/              # Imagens de teste (80 imagens)
├── runs/train/            # Resultados do treino
│   ├── results.csv        # Métricas por época
│   ├── args.yaml          # Argumentos do treino
│   └── weights/
│       ├── best.pt        # Melhor modelo por mAP
│       └── last.pt        # Último checkpoint
└── summarize_results.py   # Utilitário para análise de treino
```

### 3. Common (Código Compartilhado)

Utilitários e constantes usados por múltiplos módulos.

```
common/
├── __init__.py
├── constants.py      # Cores, nomes, configurações padrão
└── model_utils.py    # Funções para resolver caminhos de modelo
```

### 4. Tools (Ferramentas Auxiliares)

Scripts para coleta de dados e outras utilidades.

```
tools/
└── webscrapping/
    ├── collect_images.py
    ├── collect_images_bing.py
    └── README.md
```

## Fluxo de Dados

### Modo Conveyor (Esteira)

```
┌──────────────┐
│   Webcam     │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│  FoodDetector.model  │
│   .track()           │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  ByteTrack           │
│  (tracking IDs)      │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Votação de Labels   │
│  (min_label_votes)   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Detecção de Cruzam. │
│  linha_y             │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Contador Acumulado  │
│  + Overlay           │
└──────────────────────┘
```

**Características:**

- Usa tracking (ByteTrack) para manter IDs consistentes
- Estabiliza labels com votação de múltiplos frames
- Conta apenas quando objeto cruza a linha de cima para baixo
- Evita dupla contagem com set de IDs já contados

### Modo Live

```
┌──────────────┐
│   Webcam     │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│  FoodDetector.model  │
│   .predict()         │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Contagem por Frame  │
│  (sem tracking)      │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Overlay de Contagem │
│  Instantânea         │
└──────────────────────┘
```

**Características:**

- Não usa tracking
- Contagem instantânea por frame
- Mais simples, ideal para demonstrações

## Tecnologias Utilizadas

### Framework de IA

- **Ultralytics YOLO**: Framework de detecção de objetos
- **Modelo**: YOLO11 nano (yolo11n.pt) como base

### Processamento de Imagem

- **OpenCV (cv2)**: Captura de vídeo e processamento de imagens
- **ByteTrack**: Algoritmo de tracking multi-objeto

### Dataset

- **Roboflow**: Plataforma de preparação de dataset
- **Formato**: YOLO (txt annotations)
- **Classes**: 3 (beans package, pasta package, rice package)

### Estrutura de Código

- **Python 3.x**
- **Pathlib**: Manipulação de caminhos
- **Collections**: Counter, defaultdict, deque
- **argparse**: Parsing de argumentos CLI

## Otimizações de Performance

### Camera

```python
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)      # Buffer mínimo
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Resolução otimizada
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
```

### Modelo

- Usa modelo nano (yolo11n) para inferência rápida
- Confidence threshold configurável (padrão 0.7)
- `verbose=False` para reduzir logs

### Tracking

- `persist=True` mantém IDs entre frames
- `maxlen=10` na deque limita memória de histórico
- Votação evita mudanças erráticas de classe

## Extensibilidade

### Adicionar Nova Classe

1. Treinar novo modelo com classe adicional
2. Atualizar `common/constants.py`:

   ```python
   DISPLAY_NAMES = {
       "beans package": "Feijao",
       "pasta package": "Macarrao",
       "rice package": "Arroz",
       "nova_classe": "NovaClasse",  # Adicionar aqui
   }

   CLASS_COLORS = {
       "Feijao": (80, 180, 255),
       "Macarrao": (110, 245, 140),
       "Arroz": (255, 215, 120),
       "NovaClasse": (255, 100, 50),  # Adicionar cor
   }
   ```

3. Atualizar overlays em `camera/detector.py` se necessário

### Adicionar Novo Modo de Detecção

1. Implementar novo método em `FoodDetector`
2. Adicionar opção no argparser de `camera/run.py`
3. Documentar em `docs/COMO_RODAR.md`

### Integrar com Sistema Externo

O FoodDetector pode ser importado e usado programaticamente:

```python
from camera.detector import FoodDetector

detector = FoodDetector("modelo.pt", conf=0.7)
counts = detector.predict_image("imagem.jpg")

# Processar counts conforme necessário
# Ex: enviar para API, salvar em banco, etc.
```
