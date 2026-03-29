# 📊 Estrutura do Projeto - EXPLICAÇÃO COMPLETA

Este arquivo explica tudo o que você vê no projeto. Leia para entender o que é cada pasta e arquivo.

---

## 🎯 O Projeto em 30 segundos

Este é um **detector de alimentos automático**. Você aponta uma câmera para alimentos e ele identifica se são **Arroz**, **Feijão** ou **Macarrão** e conta quantos tem.

**Pronto para usar!** Você não precisa fazer nada, só executar.

---

## 📁 Estrutura Completa (COM EXPLICAÇÃO)

```
detector-alimentos/
│
├─ LEIA ISTO PRIMEIRO ────────────────────────────────
│  ├─ README.md ......................... 👈 Comece aqui!
│  ├─ ESTRUTURA_PROJETO.md ............. Este arquivo
│  └─ docs/
│     ├─ COMO_RODAR.md ................. Guia de uso
│     └─ HISTORICO.md .................. Versões antigas
│
├─ 🚀 CÓDIGO PRINCIPAL (O QUE RODA) ──────────────────
│  └─ detector/
│     ├─ run.py ........................ 👈 EXECUTE ESTE!
│     ├─ detector.py ................... Lógica de detecção
│     ├─ requirements.txt .............. Bibliotecas necessárias
│     └─ yolo11n.pt .................... Modelo base YOLOv11
│
├─ 📊 DADOS E MODELOS (TREINAMENTO) ──────────────────
│  └─ detectors/
│     ├─ food-detector-v8/ ............. Imagens de treino
│     │  ├─ train/images/ .............. 100+ imagens de treino
│     │  ├─ valid/images/ .............. Imagens de validação
│     │  ├─ test/images/ ............... Imagens de teste
│     │  ├─ train/labels/ .............. Anotações (boxes)
│     │  └─ data.yaml .................. Configuração dataset
│     │
│     ├─ versions/v8/ .................. Modelo FINAL (use este)
│     │  ├─ best.pt .................... ⭐ Modelo treinado
│     │  └─ last.pt .................... Último checkpoint
│     │
│     └─ runs/food-v8-local/ ........... Histórico de treinos
│        ├─ weights/ ................... Pesos salvos
│        └─ results.csv ................ Métricas por época
│
├─ 🛠️ FERRAMENTAS AUXILIARES (NÃO USAR) ──────────────
│  └─ tools/
│     └─ webscrapping/ ................. Coleta de imagens
│        ├─ collect_images.py ......... Script 1
│        ├─ collect_images_bing.py .... Script 2
│        └─ README.md .................. Quando usar
│
└─ ⚙️ CONFIGURAÇÕES (IGNORADAS NO GIT) ───────────────
   ├─ .gitignore ...................... O que NÃO sincronizar
   ├─ .venv/ .......................... Bibliotecas Python (oculto)
   ├─ .vscode/ ........................ Configurações VS Code (oculto)
   └─ .git/ ........................... Histórico Git (oculto)
```

---

## 🎓 O Que É Cada Coisa?

### 🚀 `detector/run.py`
**Este é o arquivo que você executa!**
- Inicia a câmera
- Detecta alimentos
- Mostra a contagem na tela
- É a única coisa que você precisa rodar

### 📊 `detector/detector.py`
Contém a classe `FoodDetector` que faz o trabalho pesado:
- Carrega o modelo de IA
- Processa imagens da câmera
- Retorna detecções

### 📖 `.venv/`
**Ambiente Virtual Python**
> ⚠️ Você **não vê** isso no VS Code, é uma pasta oculta

É como um "mini Python" com todas as bibliotecas:
- YOLOv11 (modelo de IA)
- OpenCV (câmera)
- Ultralytics (framework)

**Precisa existir para rodar.** Já está configurado!

### 📦 `detectors/`
**Dados e modelos usados para a detecção**
- `food-detector-v8/` = ~400 imagens usadas no treino
- `versions/v8/best.pt` = Modelo final treinado ⭐
- `runs/` = Histórico dos treinamentos anteriores

> ℹ️ Você **não edita** isso, apenas usa!

### 🛠️ `tools/webscrapping/`
**Scripts para coletar imagens automaticamente**

Exemplo: Baixa 100 imagens de "arroz grão" do Bing

> ⚠️ **Você NÃO precisa** disso para rodar o detector!
> 
> Só use se quiser treinar um novo modelo com mais dados

### 📱 `.vscode/`
**Configurações do VS Code (pasta oculta)**
- Define os botões de play
- Define variáveis de ambiente
- Você não precisa mexer nisso

---

## 🤔 Perguntas Comuns

### "Posso deletar a pasta `.venv`?"
❌ **NÃO!** Ela tem as bibliotecas Python necessárias.
Se deletar, o programa não roda.

### "Posso deletar `detectors/`?"
❌ **NÃO!** Tem as imagens de treino e o modelo.
Sem isso, não há como detectar alimentos.

### "E se deletar `tools/webscrapping/`?"
✅ **SIM!** Você pode deletar sem problemas.
Só é necessário se quiser coletar mais imagens.

### "O que é `.gitignore`?"
Arquivo que diz ao Git (controle de versão):
- **Sincroniza:** `detector/`, `detectors/`, `docs/`
- **Ignora (não sincroniza):** `.venv/`, `.vscode/`, `__pycache__/`

Assim, outras pessoas podem clonar o repositório sem receber 5GB de bibliotecas Python.

---

## 📝 Hierarquia de Importância

```
1️⃣ detector/run.py .................... ⭐⭐⭐ CRÍTICO
2️⃣ detector/detector.py ............... ⭐⭐⭐ CRÍTICO
3️⃣ detectors/versions/v8/best.pt ...... ⭐⭐⭐ CRÍTICO
4️⃣ detectors/food-detector-v8/ ........ ⭐⭐ Importante
5️⃣ docs/ ............................ ⭐ Documentação
6️⃣ tools/webscrapping/ ............... ☆☆ Auxiliar
7️⃣ .venv/ ........................... ⭐⭐⭐ CRÍTICO mas oculto
8️⃣ .vscode/ ......................... ☆☆ Opcional
```

---

## ✅ Checklist para Começar

- [x] Arquivo `detector/run.py` existe
- [x] Arquivo `detectors/versions/v8/best.pt` existe
- [x] Pasta `.venv/` existe (e é oculta)
- [x] Documentação está em `docs/`
- [x] Web scrapping está em `tools/` (separado)
- [x] `.gitignore` ignora o que deve ignorar

**Tudo pronto! Use `README.md` para rodar! 🚀**

---

## 🔗 Próximas Etapas

1. **Para USAR:** Vá em [README.md](README.md)
2. **Para ENTENDER:** Vá em [docs/COMO_RODAR.md](docs/COMO_RODAR.md)
3. **Para HISTÓRIA:** Vá em [docs/HISTORICO.md](docs/HISTORICO.md)
