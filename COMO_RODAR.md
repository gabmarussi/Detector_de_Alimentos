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

