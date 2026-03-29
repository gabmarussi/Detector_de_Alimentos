# Detector de Alimentos - YOLO

Sistema de detecção em tempo real para identificação de produtos alimentícios (arroz, feijão e macarrão) utilizando YOLO11 e OpenCV.

## 🎯 Características

- **Detecção em tempo real** via webcam com YOLO11 nano
- **Dois modos de operação:**
  - 🎥 **Live:** Detecção frame a frame sem contagem acumulada
  - 📦 **Conveyor:** Modo esteira com tracking e contagem de objetos
- **Tracking inteligente** com ByteTrack para IDs persistentes
- **Interface visual** com overlays e contadores
- **Estabilização de detecções** via votação de múltiplos frames

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.8+
- Webcam disponível
- Windows (testado) ou Linux/macOS

### Instalação

1. **Clone o repositório (se ainda não fez)**

   ```powershell
   cd "Detector de Alimentos"
   ```

2. **Crie e ative o ambiente virtual:**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Instale as dependências:**
   ```powershell
   pip install -r camera\requirements.txt
   ```

### Execução Rápida

**Menu Principal (recomendado):**

```powershell
python main.py
```

Abre um menu interativo com as opções:

```
0️⃣  📹 Camera (detecção em tempo real)
1️⃣  📷 Foto (captura via webcam)
2️⃣  🖼️  Arquivo Salvo (imagem do disco)
q️  ❌ Sair
```

O script guiará você através de:

- Detecção em **modo Conveyor** (com contagem na esteira) ou **Live** (simples)
- Seleção da câmera disponível
- Análise de imagens salvas em disco

### Script de Teste Rápido

Para testes rápidos com argumentos de linha de comando:

```powershell
# Teste padrão (modo conveyor)
python camera\run.py

# Modo live com câmera específica
python camera\run.py --mode live --camera-id 1

# Modificar confiança
python camera\run.py --conf 0.5

# Ver todos os argumentos
python camera\run.py --help
```

**Argumentos disponíveis para `camera/run.py`:**

| Argumento           | Descrição                           | Padrão   |
| ------------------- | ----------------------------------- | -------- |
| `--model`           | Caminho para modelo .pt customizado | Auto     |
| `--camera-id`       | ID da câmera (0, 1, 2, ...)         | 0        |
| `--mode`            | Modo (conveyor/live)                | conveyor |
| `--conf`            | Confiança mínima (0.0-1.0)          | 0.7      |
| `--line-y`          | Posição da linha (0.0-1.0)          | 0.6      |
| `--min-label-votes` | Frames para estabilizar detecção    | 3        |

## 📁 Estrutura do Projeto

```text
Detector de Alimentos/
├── main.py                    # 🍽️  Menu interativo principal
│
├── camera/                    # Aplicação de inferência
│   ├── detector.py           # Classe FoodDetector
│   ├── run.py                # Script de teste rápido (com argumentos)
│   ├── requirements.txt       # Dependências do projeto
│   └── yolo11n.pt            # Modelo base YOLO11 nano
│
├── detector/                  # Dataset e modelo treinado
│   ├── data.yaml             # Configuração do dataset (paths atualizados)
│   ├── data/                 # **NOVO** - Dados organizados (código separado de dados)
│   │   ├── train/            # 551 imagens de treino
│   │   │   └── images/, labels/
│   │   ├── valid/            # 161 imagens de validação
│   │   │   └── images/, labels/
│   │   └── test/             # 80 imagens de teste
│   │       └── images/, labels/
│   ├── runs/train/           # Resultados do treino
│   │   ├── results.csv       # Métricas por época
│   │   └── weights/
│   │       ├── best.pt       # Melhor modelo (usado por padrão)
│   │       └── last.pt       # Último checkpoint
│   └── summarize_results.py  # Análise de métricas
│
├── common/                    # Código compartilhado
│   ├── constants.py          # Constantes e configurações
│   └── model_utils.py        # Utilitários de modelo
│
├── docs/                      # Documentação completa
│   ├── COMO_RODAR.md         # Guia de execução detalhado
│   └── DOCUMENTACAO.md       # Documentação geral
│
└── tools/                     # Ferramentas auxiliares
    └── webscrapping/         # Scripts de coleta de imagens
```

**Alterações Estruturais (v2025):**

- ✨ **[main.py](main.py)** - Menu interativo sofisticado para usuários (recomendado)
- 🔧 **[camera/run.py](camera/run.py)** - Script de teste rápido com argumentos (desenvolvimento)
- 📦 **`detector/data/`** - Dados organizados separados de código (train/valid/test)
- 🔒 **`.gitignore`** - Atualizado para ignorar `runs/` e modelos `*.pt`

## 📊 Métricas do Modelo (v8)

**Dataset:**

- Classes: `beans package`, `pasta package`, `rice package`
- Total: 981 imagens (589 train / 196 valid / 196 test)
- Negative samples: 191 imagens (reduzem falsos positivos)
- Fonte: Roboflow

**Performance (Google Colab (200 épocas) - Validation):**

- Precision: 90.25%
- Recall: 70.44%
- mAP50: 71.79%

**Performance (Roboflow - Test Set):**

- Precision: 93.7%
- Recall: 69.8%
- mAP50: 76.2%

**Analisar métricas detalhadas:**

```powershell
python detector\summarize_results.py --csv detector\runs\train\results.csv
```

## 🔧 Uso Programático

```python
from camera.detector import FoodDetector
from pathlib import Path

# Inicializar detector
model_path = Path("detector/runs/train/weights/best.pt")
detector = FoodDetector(str(model_path), conf=0.7)

# Detecção em imagem
counts = detector.predict_image("teste.jpg")
print(f"Detectados: {dict(counts)}")

# Detecção em tempo real
detector.predict_webcam(camera_id=0, mode="conveyor")
```

## 🛠️ Tecnologias

- **[Ultralytics YOLO](https://github.com/ultralytics/ultralytics)** - Framework de detecção
- **[OpenCV](https://opencv.org/)** - Processamento de imagem e vídeo
- **[ByteTrack](https://github.com/ifzhang/ByteTrack)** - Algoritmo de tracking multi-objeto
- **Python 3.8+** - Linguagem de programação

## 📖 Documentação

- **[Como Rodar](docs/COMO_RODAR.md)** - Guia completo de execução
- **[Documentação](docs/DOCUMENTACAO.md)** - Organização de pastas e arquivos
