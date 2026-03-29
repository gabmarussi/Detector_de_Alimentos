# Documentacao do Projeto

## Estrutura de Pastas

```text
Detector de Alimentos/
|- camera/                       # inferencia em tempo real
|  |- detector.py                # classe FoodDetector
|  |- run.py                     # script principal
|  |- requirements.txt
|  `- yolo11n.pt
|- detector/                     # dataset + modelo treinado
|  |- data.yaml
|  |- train/                     # 551 imagens
|  |- valid/                     # 161 imagens
|  |- test/                      # 80 imagens
|  `- runs/train/
|     |- results.csv             # metricas por epoca
|     `- weights/
|        |- best.pt              # modelo principal
|        `- last.pt              # ultimo checkpoint
|- common/
|  |- constants.py               # cores, nomes, configs
|  `- model_utils.py             # resolucao de modelos
|- docs/
|- tools/webscrapping/           # scripts de coleta
|- README.md
`- .vscode/launch.json
```

## Componentes Principais

- camera/run.py: script de execucao com camera
- camera/detector.py: classe principal de deteccao
- detector/runs/train/weights/best.pt: modelo usado por padrao

## Dataset e Modelo

- Framework: Ultralytics YOLOv11 nano
- Dataset: Roboflow v8 (981 imagens)
- Classes: beans package (283), pasta package (259), rice package (262)
- Negative samples: 191 imagens
- Divisao: 60% train (589) / 20% valid (196) / 20% test (196)

## Metricas

Roboflow (Test Set, Industry Standard off):
- Precision: 93.7%
- Recall: 69.8%
- mAP@50: 76.2%

Google Colab (Validation Set, epoca 200):
- Precision: 90.25%
- Recall: 70.44%
- mAP@50: 71.79%
- mAP@50-95: 62.73%

## Modos de Operacao

- conveyor: contagem por linha com tracking
- live: deteccao instantanea sem contagem acumulada

## Comandos Uteis

Ver metricas do treino:
```powershell
python detector\summarize_results.py
```

Executar detector:
```powershell
python camera\run.py --camera-id 0 --mode conveyor
```
