# Como Rodar o Detector

Estrutura do projeto:

- camera/ para inferencia em tempo real
- detector/ para dataset e modelo treinado

## Opcao 1: VS Code (Play/Debug)

1. Abra um arquivo em camera/.
2. Abra Run and Debug.
3. Escolha uma configuracao:
   - Detector - RUN.PY
   - Webcam MacBook
   - Continuity Camera (iPhone)
   - Teste Modelo Atual (RUN.PY)
4. Rode e pare com q.

Observacao: as configuracoes apontam para ../detector/runs/train/weights/best.pt.

## Opcao 2: Terminal (Windows PowerShell)

Na raiz do projeto:

```powershell
.\.venv\Scripts\Activate.ps1
python .\camera\run.py --camera-id 0 --mode conveyor
```

Com iPhone/segunda camera:

```powershell
python .\camera\run.py --camera-id 1 --mode conveyor
```

Modo live (sem contagem por linha):

```powershell
python .\camera\run.py --camera-id 0 --mode live
```

Forcando um peso especifico:

```powershell
python .\camera\run.py --model .\detector\runs\train\weights\best.pt --camera-id 0 --mode conveyor
```

## Argumentos

- --model: caminho do .pt (opcional)
- --camera-id: id da camera
- --mode: conveyor ou live
- --conf: confianca minima
- --line-y: linha de contagem (0 a 1)
- --min-label-votes: estabilidade da classe por tracking

## Resumo de treino sem ler CSV manualmente

Na raiz do projeto:

```powershell
python .\detector\summarize_results.py --csv .\detector\runs\train\results.csv
```

Com outras opcoes:

```powershell
# Ordenar pelas melhores epocas de mAP50-95
python .\detector\summarize_results.py --metric "metrics/mAP50-95(B)"

# Mostrar top 10 epocas
python .\detector\summarize_results.py --top-k 10
```

## Troubleshooting rapido

- Erro de camera:
  - Feche apps que estejam usando a webcam.
  - Teste camera-id 0, 1, 2.
- Modulo nao encontrado:
  - Ative .venv antes de executar.
- Modelo nao encontrado:
  - Verifique se existe detector/runs/train/weights/best.pt.
