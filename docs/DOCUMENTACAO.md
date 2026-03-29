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

- Framework: Ultralytics YOLO11 nano
- Dataset: Roboflow v7 (790 imagens)
- Classes: beans package (283), pasta package (259), rice package (262)
- Divisao: 25% train (198) / 25% valid (198) / 50% test (394)

## Metricas

Roboflow (Industry Standard off):
- Precision: 96.6%
- Recall: 68.8%
- mAP@50: 75.7%

Local (Google Colab, dataset anterior 665 imgs):
- Precision: 73.74%
- Recall: 48.49%
- mAP@50: 46.16%

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
