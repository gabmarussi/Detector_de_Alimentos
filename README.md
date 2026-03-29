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

**Modo Conveyor (recomendado):**

```powershell
python camera\run.py --camera-id 0 --mode conveyor
```

**Modo Live:**

```powershell
python camera\run.py --camera-id 0 --mode live
```

**Controles:**

- Pressione `q` para sair

## 📋 Argumentos de Linha de Comando

| Argumento           | Descrição                                | Padrão                  |
| ------------------- | ---------------------------------------- | ----------------------- |
| `--model`           | Caminho para o modelo .pt                | Detecta automaticamente |
| `--camera-id`       | ID da câmera (0, 1, 2...)                | 0                       |
| `--mode`            | Modo de operação (conveyor/live)         | conveyor                |
| `--conf`            | Confiança mínima (0.0 a 1.0)             | 0.7                     |
| `--line-y`          | Posição da linha de contagem (0.0 a 1.0) | 0.6                     |
| `--min-label-votes` | Frames mínimos para estabilizar classe   | 3                       |

## 📁 Estrutura do Projeto

```text
Detector de Alimentos/
├── camera/                     # Aplicação de inferência
│   ├── detector.py            # Classe FoodDetector
│   ├── run.py                 # Script principal de execução
│   ├── requirements.txt       # Dependências do projeto
│   └── yolo11n.pt            # Modelo base YOLO11 nano
│
├── detector/                   # Dataset e modelo treinado (v7)
│   ├── data.yaml              # Configuração do dataset
│   ├── train/                 # 551 imagens de treino
│   ├── valid/                 # 161 imagens de validação
│   ├── test/                  # 80 imagens de teste
│   ├── runs/train/            # Resultados do treino
│   │   ├── results.csv        # Métricas por época
│   │   └── weights/
│   │       ├── best.pt        # Melhor modelo (usado por padrão)
│   │       └── last.pt        # Último checkpoint
│   └── summarize_results.py   # Análise de métricas
│
├── common/                     # Código compartilhado
│   ├── constants.py           # Constantes e configurações
│   └── model_utils.py         # Utilitários de modelo
│
├── docs/                       # Documentação completa
│   ├── API.md                 # Documentação da API
│   ├── ARQUITETURA.md         # Arquitetura do sistema
│   ├── COMO_RODAR.md          # Guia de execução detalhado
│   ├── DESENVOLVIMENTO.md     # Guia de desenvolvimento
│   ├── ESTRUTURA_PROJETO.md   # Estrutura detalhada
│   └── HISTORICO.md           # Histórico do projeto
│
└── tools/                      # Ferramentas auxiliares
    └── webscrapping/          # Scripts de coleta de imagens
```

## 📊 Métricas do Modelo Atual (v7)

**Dataset:**

- Classes: `beans package`, `pasta package`, `rice package`
- Total: 792 imagens (551 treino / 161 validação / 80 teste)
- Fonte: Roboflow

**Performance (época 100):**

- Precision: 0.7374
- Recall: 0.4848
- mAP50: 0.4616
- mAP50-95: 0.3849

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

Veja mais exemplos em [docs/API.md](docs/API.md).

## 🛠️ Tecnologias

- **[Ultralytics YOLO](https://github.com/ultralytics/ultralytics)** - Framework de detecção
- **[OpenCV](https://opencv.org/)** - Processamento de imagem e vídeo
- **[ByteTrack](https://github.com/ifzhang/ByteTrack)** - Algoritmo de tracking multi-objeto
- **Python 3.8+** - Linguagem de programação

## 🤝 Contribuindo

Contribuições são bem-vindas! Consulte o [Guia de Desenvolvimento](docs/DESENVOLVIMENTO.md) para:

- Configurar ambiente de desenvolvimento
- Padrões de código e commits
- Como adicionar novas funcionalidades
- Debugging e troubleshooting

## ⚠️ Troubleshooting

**Câmera não abre:**

- Feche outros aplicativos usando a webcam
- Tente diferentes IDs de câmera: `--camera-id 1`, `--camera-id 2`
- Verifique permissões de câmera no Windows

**Modelo não encontrado:**

- Verifique se `detector/runs/train/weights/best.pt` existe
- Use `--model` para especificar caminho customizado

**Performance lenta:**

- Reduza a resolução da câmera
- Aumente o threshold de confiança: `--conf 0.8`

Mais soluções em [docs/DESENVOLVIMENTO.md](docs/DESENVOLVIMENTO.md#debugging).

## 📖 Documentação Completa

### Guias de Usuário

- **[FAQ](docs/FAQ.md)** - Perguntas frequentes e soluções rápidas
- **[Como Rodar](docs/COMO_RODAR.md)** - Guia completo de execução
- **[Estrutura do Projeto](docs/ESTRUTURA_PROJETO.md)** - Organização de pastas e arquivos
- **[Histórico](docs/HISTORICO.md)** - Histórico de versões e mudanças

### Documentação Técnica

- **[API](docs/API.md)** - Documentação da API do FoodDetector
- **[Arquitetura](docs/ARQUITETURA.md)** - Arquitetura do sistema e fluxo de dados
- **[Desenvolvimento](docs/DESENVOLVIMENTO.md)** - Guia para contribuidores

**📚 [Índice Completo da Documentação](docs/README.md)**
