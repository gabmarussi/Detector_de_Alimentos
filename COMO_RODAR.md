# 🎬 Como Rodar o Detector

## ⚡ Opção 1: Apertar Play Button (MAIS FÁCIL)

### Passo 1: Abra o VS Code

```bash
cd /Users/gabmarussi/Documents/GitHub/Detector-de-Alimentos
code .
```

### Passo 2: Abra o arquivo `run.py`

1. Clique em `Camera/run.py` na sidebar
2. Você verá um **triângulo verde (play button)** no canto superior direito
3. Clique nele!

### Passo 3: Escolha a opção

Uma caixa de diálogo aparecerá no terminal:

```
Escolha uma opção:

  [1] 📱 Webcam do MacBook (câmera interna)
  [2] 🍎 Continuity Camera (iPhone)
  [3] 📷 Imagem estática
  [0] ❌ Sair
```

Digite `1`, `2` ou `3` e pressione Enter.

### Passo 4: Fechar

Quando terminar, pressione `q` para fechar a janela de câmera.

---

## 🖥️ Opção 2: Usar Debug Configurations do VS Code (RECOMENDADO)

1. Abra qualquer arquivo em `Camera/`
2. Pressione `Ctrl+Shift+D` (ou CMD+Shift+D no Mac)
3. No dropdown, selecione uma das configurações:
   - 🎬 **Detector - RUN.PY** (menu interativo)
   - 📱 **Webcam MacBook** (câmera interna direto)
   - 🍎 **Continuity Camera** (iPhone direto)
4. Clique no **play button verde**

---

## 🔧 Opção 3: Terminal (Clássico)

```bash
# Terminal 1: Ativar venv
cd /Users/gabmarussi/Documents/GitHub/Detector-de-Alimentos
source .venv/bin/activate

# Terminal 2: Rodar o script interativo
cd Camera
python run.py

# Ou rodar direto (sem menu)
python detector.py --model ../runs/food-v6-local/weights/best.pt --source webcam --camera-id 0

# Teste direto da versao v8 (busca automatica de pesos)
python run.py --version v8 --camera-id 0 --mode conveyor
```

---

## 🎯 Principais Mudanças

### ✅ Threshold Aumentado (0.4 → 0.6)

- **Antes:** Detectava tudo como arroz com confiança baixa
- **Depois:** Mais seletivo, apenas objetos com >60% confiança

### ✅ Câmera iPhone Melhorada

- Reduz delay com `BUFFERSIZE=1`
- Define FPS fixo em 30
- Mostra avisos se perder frame

### ✅ Script `run.py` Simples

- Menu interativo
- Sem argumentos de linha de comando
- Apertável com play button do VS Code

---

## 🐛 Se Ainda Houver Problemas

### Problema: "Tudo ainda é arroz"

- ✅ Verificamos o threshold, agora está 0.6
- Se persistir, é possível que o modelo tenha super-ajuste
- Solução: Fazer novo treinamento com data augmentation balanceada

### Problema: "iPhone para rapidamente"

- ✅ Corrigimos com `BUFFERSIZE=1` e `FPS=30`
- Se ainda assim parar, verifique:
  1. iPhone está conectado como Continuity Camera?
  2. Está em proximity do Mac?
  3. Tente usar camera-id 2 ou 3

### Problema: "Não consigo saber como rodar"

- ✅ Agora é só apertar play button em `run.py`
- VS Code mostra menu interativo no terminal

---

## 📱 Testar Agora

Abra o VS Code, vá em `Camera/run.py` e aperte o play button! 🎮

---

## 🧠 Treino v7 (YOLO11)

### Objetivo

Treinar a versão **v7** do detector usando o dataset em `food-detector-v7` e salvar os pesos em `runs/food-v7-local`.

### Pré-requisitos

```bash
cd /Users/gabmarussi/Documents/GitHub/Detector-de-Alimentos
source .venv/bin/activate
pip install -r detector/requirements.txt
```

### Comando de treino (v7)

Execute a partir da raiz do projeto:

```bash
cd /Users/gabmarussi/Documents/GitHub/Detector-de-Alimentos

yolo detect train \
  model=detector/yolo11n.pt \
  data=food-detector-v7/data.yaml \
  epochs=100 \
  batch=16 \
  imgsz=384 \
  patience=100 \
  project=runs \
  name=food-v7-local
```

### Saídas esperadas

- Pesos: `runs/food-v7-local/weights/best.pt` e `runs/food-v7-local/weights/last.pt`
- Métricas por época: `runs/food-v7-local/results.csv`
- Configuração final do treino: `runs/food-v7-local/args.yaml`

### Validar rapidamente o modelo treinado

```bash
cd detector
python detector.py --model ../runs/food-v7-local/weights/best.pt --source webcam --camera-id 0
```

### Observações

- O `args.yaml` do treino v7 registrado no projeto mostra: `epochs=100`, `batch=16`, `imgsz=384` e `name=food-v7-local`.
- Se quiser sobrescrever uma execução anterior com o mesmo nome, adicione `exist_ok=True` no comando.
