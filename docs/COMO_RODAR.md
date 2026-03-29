# 🎬 Como Rodar o Detector

Existem 3 formas de rodar o detector. Escolha a mais conveniente!

---

## ⭐ Opção 1: Play Button (Mais Fácil)

Essa é a forma **mais rápida** e **sem complicações**.

### Passo a Passo:

1. Abra o VS Code:

   ```bash
   cd /Users/gabmarussi/Documents/GitHub/Detector-de-Alimentos
   code .
   ```

2. Na barra lateral esquerda, clique em `detector/run.py`

3. Você verá um **triângulo verde ▶️** no canto superior direito

4. Clique nele e **pronto!** A câmera vai iniciar

5. Para parar, pressione `q` no teclado

---

## 💻 Opção 2: Debug Configurations (VS Code)

Usa configurações pré-definidas do VS Code para diferentes câmeras.

### Passo a Passo:

1. Abra qualquer arquivo em `detector/`
2. Pressione **`Ctrl+Shift+D`** (ou **`Cmd+Shift+D`** no Mac)
3. Você verá um dropdown com opções:
   - 🎬 **Detector - Modo Conveyor** (webcam interna, conta alimentos)
   - 📱 **Webcam MacBook** (webcam, modo ao vivo)
   - 🍎 **Continuity Camera** (iPhone, conta alimentos)
4. Selecione uma e clique no play button verde
5. Para parar, pressione `q`

---

## 🖥️ Opção 3: Terminal (Clássico)

Para quem prefere linha de comando ou usa outro editor.

### Preparação (primeira vez):

```bash
cd /Users/gabmarussi/Documents/GitHub/Detector-de-Alimentos

# Ativar ambiente virtual
source .venv/bin/activate

# Entrar na pasta do detector
cd detector
```

### Escolha um comando:

```bash
# Webcam interna - modo contagem (padrão)
python run.py --camera-id 0 --mode conveyor

# Webcam interna - modo ao vivo (sem contar)
python run.py --camera-id 0 --mode live

# iPhone via Continuity Camera - modo contagem
python run.py --camera-id 1 --mode conveyor

# Customizar confiança detecção (padrão 0.7)
python run.py --camera-id 0 --mode live --conf 0.5
```

### Para parar:

- Pressione `q` no teclado
- Ou pressione `Ctrl+C` no terminal

---

## 📊 Sobre os Modos

| Modo              | Camera ID | Descrição                              |
| ----------------- | --------- | -------------------------------------- |
| `--mode conveyor` | 0 ou 1    | Conta objetos que atravessam uma linha |
| `--mode live`     | 0 ou 1    | Apenas detecta, não conta              |
| `--camera-id 0`   | -         | Webcam interna do MacBook              |
| `--camera-id 1`   | -         | iPhone conectado via Continuity        |

---

## 🎥 Configurando o iPhone (Continuity)

Para usar o iPhone como câmera:

1. **iPhone e Mac conectados na mesma WiFi**
2. **Proximity:** iPhone bem perto do Mac
3. **Continuity ativado** nas configurações de ambos
4. No comando use `--camera-id 1`

Se não funcionar com camera-id 1, tente:

- `--camera-id 2` ou `--camera-id 3`

---

## ❓ Troubleshooting

### Problema: "Erro de câmera"

- Verifique se a webcam não está sendo usada por outro app
- No macOS: System Preferences → Security & Privacy → Camera

### Problema: "Módulo não encontrado"

- Certifique-se de ativar o ambiente virtual:
  ```bash
  source .venv/bin/activate
  ```

### Problema: "iPhone não aparece"

- Verifique se está em Continuity (System Preferences)
- Tente camera-id 2 ou 3 em vez de 1

---

## 🔧 Argumentos Disponíveis

```bash
python run.py [OPTIONS]

OPTIONS:
  --camera-id INT         ID da câmera (0=webcam, 1=iPhone). Default: 0
  --mode TEXT             Modo: 'conveyor' ou 'live'. Default: conveyor
  --conf FLOAT            Confiança mínima (0-1). Default: 0.7
  --line-y FLOAT          Posição da linha de contagem (0-1). Default: 0.6
  --min-label-votes INT   Votos para confirmar label. Default: 3
```

Exemplo:

```bash
python run.py --camera-id 1 --mode live --conf 0.5 --line-y 0.5
```

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

Abra o VS Code, vá em `detector/run.py` e aperte o play button! 🎮
