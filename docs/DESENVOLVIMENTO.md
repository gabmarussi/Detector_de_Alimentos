# Desenvolvimento e Contribuição

## Configuração do Ambiente de Desenvolvimento

### 1. Clone o Repositório

```powershell
git clone <url-do-repositorio>
cd "Detector de Alimentos"
```

### 2. Crie um Ambiente Virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instale as Dependências

```powershell
pip install -r camera\requirements.txt
```

### 4. Verifique a Instalação

**Opção A: Menu Interativo (Recomendado)**

```powershell
python main.py
```

**Opção B: Teste Rápido**

```powershell
python camera\run.py --camera-id 0 --mode live
```

## Estrutura de Commits

Siga o padrão de commits semânticos:

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `refactor:` Refatoração de código
- `test:` Adição ou modificação de testes
- `chore:` Tarefas de manutenção

**Exemplos:**

```
feat: adicionar modo de detecção em lote
fix: corrigir contagem duplicada no modo conveyor
docs: atualizar documentação da API
refactor: extrair lógica de overlay para função separada
```

## Testando Mudanças

### Teste Manual Básico

1. **Modo Live (detecção instantânea):**

   ```powershell
   python camera\run.py --camera-id 0 --mode live
   ```

2. **Modo Conveyor (com contagem):**

   ```powershell
   python camera\run.py --camera-id 0 --mode conveyor --line-y 0.6
   ```

3. **Teste com imagem estática:**
   ```powershell
   # No menu interativo, escolha opção 2
   python camera\run.py
   ```

### Validação de Modelo

Verifique as métricas do treino:

```powershell
python detector\summarize_results.py --csv detector\runs\train\results.csv
```

## Guia de Estilo

### Python

Seguimos PEP 8 com algumas adaptações:

- **Indentação:** 4 espaços
- **Linha máxima:** 100 caracteres (preferencial, mas flexível para strings)
- **Imports:** Agrupados em stdlib, third-party, local
- **Docstrings:** Google style para classes e funções públicas

**Exemplo:**

```python
"""Breve descrição do módulo."""

import sys
from pathlib import Path

import cv2
from ultralytics import YOLO

from common.constants import DEFAULT_CONFIDENCE


class MinhaClasse:
    """
    Descrição da classe.

    Args:
        param1: Descrição do parâmetro
        param2: Descrição do segundo parâmetro
    """
    def __init__(self, param1: str, param2: int):
        self.param1 = param1
        self.param2 = param2

    def meu_metodo(self, arg: str) -> str:
        """
        Descrição do método.

        Args:
            arg: Descrição do argumento

        Returns:
            Descrição do retorno
        """
        return f"{self.param1}: {arg}"
```

### Nomeação

- **Variáveis e funções:** `snake_case`
- **Classes:** `PascalCase`
- **Constantes:** `UPPER_SNAKE_CASE`
- **Arquivos:** `snake_case.py`

## Adicionando Novas Funcionalidades

### 1. Adicionar Nova Classe de Alimento

**Passo 1:** Preparar dataset

- Colete imagens da nova classe
- Anote usando Roboflow ou ferramenta similar
- Exporte no formato YOLO

**Passo 2:** Retreinar o modelo

```powershell
# Atualizar detector/data.yaml com nova classe
# Executar treino com Ultralytics
```

**Passo 3:** Atualizar constantes

```python
# common/constants.py
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
    "NovaClasse": (200, 100, 255),  # Adicionar cor BGR
}
```

**Passo 4:** Atualizar overlays (se necessário)

```python
# camera/detector.py
# Modificar _draw_counts() e _draw_conveyor_overlay()
# para incluir a nova classe na UI
```

### 2. Adicionar Novo Modo de Operação

**Exemplo: Modo "Snapshot" (captura periódica)**

**Passo 1:** Implementar no FoodDetector

```python
# camera/detector.py
def predict_snapshot(self, camera_id: int = 0, interval: int = 5):
    """Captura e analisa a cada N segundos."""
    cap = cv2.VideoCapture(camera_id)
    last_capture = 0

    while True:
        current_time = time.time()
        if current_time - last_capture >= interval:
            ok, frame = cap.read()
            if ok:
                # Processar frame
                result = self.model.predict(frame, conf=self.conf)
                counts = self._count(result)
                print(f"Snapshot: {dict(counts)}")
                last_capture = current_time

        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

    cap.release()
```

**Passo 2:** Adicionar ao argparser

```python
# camera/run.py
parser.add_argument("--mode", choices=["conveyor", "live", "snapshot"], default="conveyor")
parser.add_argument("--snapshot-interval", type=int, default=5)
```

**Passo 3:** Documentar

```markdown
# docs/COMO_RODAR.md

## Modo Snapshot

python camera\run.py --mode snapshot --snapshot-interval 10
```

## Debugging

### Problemas Comuns

**1. Modelo não encontrado:**

```
FileNotFoundError: Modelo treinado nao encontrado
```

**Solução:** Verifique se `detector/runs/train/weights/best.pt` existe.

**2. Câmera não abre:**

```
RuntimeError: Nao foi possivel abrir camera 0
```

**Solução:**

- Feche outros apps usando a webcam
- Tente outro camera-id (1, 2, etc.)
- Verifique permissões de câmera no Windows

**3. Tracking inconsistente:**

```
# IDs mudam frequentemente entre frames
```

**Solução:** Aumente `--min-label-votes` para estabilizar:

```powershell
python camera\run.py --min-label-votes 5
```

### Ferramentas de Debug

**1. Verbose do YOLO:**

```python
# Temporariamente remover verbose=False
result = self.model.predict(source=frame, conf=self.conf, verbose=True)[0]
```

**2. Salvar frames problemáticos:**

```python
# Adicionar em camera/detector.py
cv2.imwrite(f"debug_frame_{time.time()}.jpg", frame)
```

**3. Logs de tracking:**

```python
# Adicionar prints no loop de tracking
print(f"Track ID: {track_id}, Label: {label}, Y: {cy}, Line: {line_y}")
```

## Performance

### Otimizações Aplicadas

1. **Buffer de câmera mínimo:** `cv2.CAP_PROP_BUFFERSIZE = 1`
2. **Resolução otimizada:** 1280x720
3. **Modelo nano:** yolo11n para inferência rápida
4. **Deque limitada:** `maxlen=10` para histórico de labels

### Benchmarking

Para medir FPS:

```python
import time

frame_count = 0
start_time = time.time()

while True:
    # ... seu loop de inferência ...
    frame_count += 1

    if frame_count % 30 == 0:
        elapsed = time.time() - start_time
        fps = frame_count / elapsed
        print(f"FPS: {fps:.2f}")
```

### Quando Otimizar

- FPS < 15: Considerar reduzir resolução ou usar modelo menor
- FPS > 30: Já está ótimo, não precisa otimizar
- Latência alta: Verificar processamento de tracking

## Contribuindo

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feat/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: adicionar nova funcionalidade'`)
4. Push para a branch (`git push origin feat/nova-funcionalidade`)
5. Abra um Pull Request

### Checklist antes do PR

- [ ] Código testado manualmente
- [ ] Documentação atualizada (se aplicável)
- [ ] Commits seguem o padrão semântico
- [ ] Não há referências hardcoded a caminhos locais
- [ ] Constantes extraídas para `common/constants.py`

## Recursos Adicionais

- [Ultralytics YOLO Docs](https://docs.ultralytics.com/)
- [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Roboflow Documentation](https://docs.roboflow.com/)
- [ByteTrack Paper](https://arxiv.org/abs/2110.06864)
