# 🍽️ Detector de Alimentos - YOLOv11

Sistema inteligente de detecção e contagem de embalagens de alimentos em tempo real.

**Status:** ✅ Pronto para produção (YOLOv11 v8)

---

## 📁 Estrutura do Projeto (EXPLICADA)

```
detector-alimentos/
│
├── 🚀 detector/                         # CÓDIGO PRINCIPAL (aqui é onde roda!)
│   ├── detector.py                      # Classe FoodDetector
│   ├── run.py                           # Script para rodar a detecção
│   ├── requirements.txt                 # Dependências Python
│   └── yolo11n.pt                       # Modelo base YOLOv11
│
├── 📊 detectors/                        # DATASETS E MODELOS TREINADOS
│   ├── food-detector-v8/                # Dataset com imagens e labels
│   ├── versions/v8/                     # Modelo treinado (best.pt)
│   └── runs/food-v8-local/              # Histórico de treinamento
│
├── 🛠️ tools/                            # SCRIPTS AUXILIARES (não é código principal!)
│   └── webscrapping/                    # Coleta automática de imagens
│       ├── collect_images.py            # Script 1: Coleta de URLs
│       └── collect_images_bing.py       # Script 2: Coleta do Bing Search
│
├── 📚 docs/                             # DOCUMENTAÇÃO
│   ├── COMO_RODAR.md                    # Como executar o detector
│   └── HISTORICO.md                     # Histórico técnico (v6, v7, v8)
│
└── ⚙️ Configurações (IGNORADAS NO GIT)
    ├── .gitignore                       # O que NÃO sincronizar
    ├── .venv/                           # Ambiente virtual Python
    └── .vscode/                         # Configurações VS Code
```

---

## ❓ O que é cada pasta?

| Pasta                   | O que faz                                 | Preciso?                          |
| ----------------------- | ----------------------------------------- | --------------------------------- |
| **detector/**           | Código que roda a detecção de alimentos   | ✅ **SIM**                        |
| **detectors/**          | Imagens de treino e modelo final          | ✅ **SIM**                        |
| **tools/webscrapping/** | Programas para coletar imagens (auxiliar) | ⚠️ Não (só se treinar)            |
| **docs/**               | Documentação (como usar, histórico)       | 📖 Referência                     |
| **.venv/**              | Bibliotecas Python instaladas             | ✅ **SIM** mas não aparece no Git |
| **.vscode/**            | Configurações do VS Code                  | ⚠️ Opcional                       |
| **.gitignore**          | Diz ao Git quais arquivos ignorar         | ✅ **SIM**                        |

---

## 🚀 Como Usar (3 passos)

### Opção 1: Play Button (Mais Fácil) ⭐

1. Abra VS Code
2. Clique em `detector/run.py` na lateral esquerda
3. Clique no triângulo verde ▶️ no canto superior direito
4. **Pronto!** A câmera vai iniciar

### Opção 2: Terminal

```bash
# 1. Entrar na pasta
cd /Users/gabmarussi/Documents/GitHub/Detector-de-Alimentos

# 2. Ativar ambiente virtual
source .venv/bin/activate

# 3. Entrar em detector
cd detector

# 4. Rodar (escolha um):
python run.py --camera-id 0 --mode conveyor    # Webcam, contar objetos
python run.py --camera-id 1 --mode conveyor    # iPhone Continuity, contar
python run.py --camera-id 0 --mode live        # Webcam, só detectar
```

### Para Fechar

Pressione `q` no teclado

---

## 🎯 Características

- ✅ Detecta **Arroz**, **Feijão** e **Macarrão**
- ✅ Funciona com webcam MacBook ou iPhone (Continuity)
- ✅ Conta quantidade de embalagens
- ✅ Roda em tempo real (30 FPS)

---

## 📖 Documentação Completa

- **[COMO_RODAR.md](docs/COMO_RODAR.md)** - Instruções detalhadas
- **[HISTORICO.md](docs/HISTORICO.md)** - Versões anteriores (v6, v7) e detalhes técnicos

---

## 🔧 Requisitos

- **Python** 3.13+
- **macOS** (Intel ou Apple Silicon M1/M2/M3)
- **Webcam** funcionando
- Arquivo `.venv` já configurado

---

## 📅 Histórico

- **27/03:** v6 (YOLOv8)
- **28/03:** v7-v8 (YOLOv11)
- **29/03:** Projet simplificado, apenas v8

---

**Versão:** 8.0 (YOLOv11)  
**Desenvolvedor:** Gabriel Marussi  
**Data:** 29/03/2026
