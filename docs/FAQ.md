# Perguntas Frequentes (FAQ)

## Instalação e Configuração

### Q: Quais são os requisitos mínimos do sistema?

**A:**

- Python 3.8 ou superior
- 4GB RAM (recomendado 8GB)
- Webcam funcional
- Windows, Linux ou macOS
- ~500MB de espaço em disco para dependências

### Q: Como instalo as dependências?

**A:**

```powershell
# Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r camera\requirements.txt
```

### Q: Posso usar sem ambiente virtual?

**A:** Sim, mas não é recomendado. O ambiente virtual evita conflitos com outras instalações Python.

## Execução

### Q: Como inicio o detector?

**A:** Forma mais simples:

```powershell
python camera\run.py --camera-id 0 --mode conveyor
```

### Q: Qual é a diferença entre os modos "conveyor" e "live"?

**A:**

- **Live:** Detecção instantânea frame a frame. Mostra contagem atual no frame.
- **Conveyor:** Simula esteira transportadora. Objetos são contados ao cruzar uma linha horizontal. A contagem é acumulada.

### Q: Como escolho qual câmera usar?

**A:** Use `--camera-id` com diferentes números:

```powershell
# Webcam principal
python camera\run.py --camera-id 0

# Segunda câmera (iPhone via Continuity, webcam externa)
python camera\run.py --camera-id 1

# Terceira câmera
python camera\run.py --camera-id 2
```

### Q: Como ajusto a sensibilidade da detecção?

**A:** Use `--conf` para ajustar o threshold de confiança (0.0 a 1.0):

```powershell
# Mais sensível (mais detecções, mas pode ter falsos positivos)
python camera\run.py --conf 0.5

# Menos sensível (menos detecções, mais confiáveis)
python camera\run.py --conf 0.8

# Padrão (balanceado)
python camera\run.py --conf 0.7
```

### Q: Posso ajustar a posição da linha de contagem no modo conveyor?

**A:** Sim, use `--line-y` com valor entre 0.0 (topo) e 1.0 (fundo):

```powershell
# Linha no meio da tela
python camera\run.py --mode conveyor --line-y 0.5

# Linha mais embaixo (padrão)
python camera\run.py --mode conveyor --line-y 0.6
```

## Problemas Comuns

### Q: "Nao foi possivel abrir camera X"

**A:** Possíveis soluções:

1. Feche outros apps usando a webcam (Teams, Zoom, Skype)
2. Tente outro camera-id: `--camera-id 1` ou `--camera-id 2`
3. Verifique permissões de câmera no Windows (Configurações > Privacidade > Câmera)
4. Reinicie o computador

### Q: "Modelo treinado nao encontrado"

**A:** Verifique se existe `detector/runs/train/weights/best.pt`. Se não:

1. Certifique-se de estar na raiz do projeto
2. Ou especifique o caminho manualmente: `--model caminho\para\modelo.pt`

### Q: "Modulo nao encontrado" ou "ImportError"

**A:**

1. Ative o ambiente virtual: `.\.venv\Scripts\Activate.ps1`
2. Reinstale as dependências: `pip install -r camera\requirements.txt`
3. Verifique se está usando Python 3.8+: `python --version`

### Q: A detecção está muito lenta (< 10 FPS)

**A:** Otimizações possíveis:

1. Feche outros programas pesados
2. Use modelo mais leve (já estamos usando nano)
3. Reduza a resolução no código (editar `DEFAULT_CAMERA_WIDTH` em `common/constants.py`)
4. Aumente o threshold: `--conf 0.8`

### Q: Objetos estão sendo contados múltiplas vezes

**A:** No modo conveyor, isso pode acontecer se:

1. Objeto cruza a linha múltiplas vezes (solução: posicionar melhor a câmera)
2. Tracking perdendo IDs (solução: aumentar `--min-label-votes 5`)

### Q: Detecções estão "piscando" entre classes

**A:** Use `--min-label-votes` maior:

```powershell
python camera\run.py --min-label-votes 5
```

Isso exige 5 frames consecutivos com a mesma classe antes de estabilizar.

## Uso Avançado

### Q: Como uso o detector em meu próprio script Python?

**A:** Exemplo básico:

```python
from camera.detector import FoodDetector

detector = FoodDetector("detector/runs/train/weights/best.pt", conf=0.7)

# Imagem estática
counts = detector.predict_image("minha_foto.jpg")
print(counts)

# Webcam em tempo real
detector.predict_webcam(camera_id=0, mode="live")
```

Veja [docs/API.md](API.md) para documentação completa.

### Q: Posso salvar as detecções em arquivo?

**A:** Sim, modifique o código ou capture o output:

```python
from camera.detector import FoodDetector

detector = FoodDetector("detector/runs/train/weights/best.pt")
counts = detector.predict_image("imagem.jpg")

# Salvar em arquivo
with open("resultados.txt", "w") as f:
    f.write(str(dict(counts)))
```

### Q: Como treino um novo modelo com mais dados?

**A:**

1. Colete e anote novas imagens usando Roboflow
2. Exporte no formato YOLO
3. Atualize `detector/data.yaml` com novos caminhos
4. Use Ultralytics CLI para treinar:
   ```powershell
   yolo detect train data=detector/data.yaml model=yolo11n.pt epochs=100
   ```
5. Novos pesos estarão em `runs/detect/train/weights/best.pt`

### Q: Posso adicionar novas classes de alimentos?

**A:** Sim! Veja [docs/DESENVOLVIMENTO.md](DESENVOLVIMENTO.md#adicionar-nova-classe-de-alimento) para guia completo. Resumo:

1. Retreinar modelo com nova classe
2. Atualizar `DISPLAY_NAMES` e `CLASS_COLORS` em `common/constants.py`
3. Opcionalmente ajustar overlays em `camera/detector.py`

### Q: Como integro com banco de dados ou API externa?

**A:** Use o FoodDetector programaticamente:

```python
from camera.detector import FoodDetector
import requests

detector = FoodDetector("modelo.pt")
counts = detector.predict_image("foto.jpg")

# Enviar para API
requests.post("https://minha-api.com/detections", json=dict(counts))

# Ou salvar em banco
# db.save_detection(counts)
```

## Desempenho

### Q: Quantos FPS consigo?

**A:** Depende do hardware:

- **GPU:** 30-60 FPS (ideal)
- **CPU moderno (i5/i7):** 15-30 FPS (bom)
- **CPU antigo:** 5-15 FPS (usável)

### Q: Posso usar GPU para acelerar?

**A:** Sim, se tiver CUDA instalado. O PyTorch detecta automaticamente.

```powershell
# Verificar se GPU está disponível
python -c "import torch; print(torch.cuda.is_available())"
```

### Q: Qual o consumo de memória?

**A:** Aproximadamente:

- Modelo carregado: ~50MB
- Webcam ativa: ~200MB
- Total: ~300-400MB RAM

## Desenvolvimento

### Q: Como contribuo com o projeto?

**A:** Veja [docs/DESENVOLVIMENTO.md](DESENVOLVIMENTO.md) para:

- Setup de ambiente de desenvolvimento
- Padrões de código
- Como fazer pull requests

### Q: Posso usar este código comercialmente?

**A:** Depende da licença do projeto. Consulte o arquivo LICENSE na raiz.

### Q: Onde reporto bugs ou sugiro features?

**A:** Abra uma issue no repositório GitHub com:

- Descrição clara do problema/sugestão
- Passos para reproduzir (se bug)
- Versão do Python e sistema operacional
- Logs de erro (se aplicável)

## Modelos e Dataset

### Q: Qual modelo YOLO está sendo usado?

**A:** YOLO11 nano (yolo11n) como base, treinado com dataset customizado de alimentos.

### Q: Quais classes o modelo detecta?

**A:** Atualmente:

- `Feijao` (beans package)
- `Macarrao` (pasta package)
- `Arroz` (rice package)

### Q: Quantas imagens tem o dataset?

**A:** Dataset v7:

- Treino: 551 imagens
- Validação: 161 imagens
- Teste: 80 imagens
- **Total: 792 imagens**

### Q: Qual a acurácia do modelo?

**A:** Métricas da época 100:

- Precision: 73.74%
- Recall: 48.48%
- mAP50: 46.16%
- mAP50-95: 38.49%

### Q: Como vejo métricas detalhadas do treino?

**A:**

```powershell
python detector\summarize_results.py --csv detector\runs\train\results.csv
```

## Outros

### Q: O projeto funciona em tempo real mesmo?

**A:** Sim! Com hardware adequado (CPU i5+ ou GPU), você consegue 15-60 FPS, o que é em tempo real.

### Q: Posso usar com vídeos gravados em vez de webcam?

**A:** Sim, modifique o código para usar arquivo em vez de câmera:

```python
# Em vez de cv2.VideoCapture(camera_id)
cap = cv2.VideoCapture("caminho/para/video.mp4")
```

### Q: Funciona em Raspberry Pi?

**A:** Sim, mas o desempenho será limitado (5-10 FPS). Considere usar modelo ainda menor ou resolução reduzida.

### Q: Preciso de internet para rodar?

**A:** Não, após instalar as dependências. O modelo roda localmente.

### Q: Quanto tempo leva para treinar um novo modelo?

**A:** Depende:

- **GPU (NVIDIA):** ~1-2 horas para 100 épocas
- **CPU:** Várias horas a dias (não recomendado)

Recomendamos usar Google Colab (grátis) ou Kaggle para treino com GPU.
