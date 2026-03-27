# 🍽️ Detector de Alimentos - YOLOv8

Sistema inteligente de detecção e contagem de embalagens de alimentos em tempo real usando visão computacional.

**Status:** ✅ Produção (v6 - 99.2% acurácia)

---

## 🎯 Características

- ✅ Detecta **Arroz**, **Feijão** e **Macarrão** em tempo real
- ✅ Funciona com **webcam MacBook** ou **Continuity Camera (iPhone)**
- ✅ Conta automaticamente quantidade de embalagens
- ✅ Alta precisão (99.2% mAP@50)

---

## 🚀 Quick Start (1 minuto)

### 1. Webcam do MacBook

```bash
cd /Users/gabmarussi/Documents/GitHub/Detector-de-Alimentos/Camera

/Users/gabmarussi/Documents/GitHub/Detector-de-Alimentos/.venv/bin/python detector.py \
  --model ../runs/food-v6-local/weights/best.pt \
  --source webcam \
  --camera-id 0
```

### 2. iPhone Continuity Camera

```bash
# Troque camera-id para 1
--camera-id 1
```

**Feche com:** Pressione `q`

---

## 📊 Resultados Finais

```
Modelo v6 - Época 100/100
├── mAP@50:     99.2% ✅
├── Precision:  96.8% ✅
├── Recall:     98.9% ✅
└── Dataset:    665 imagens (575 base + augmentation)
```

---

## 📁 Estrutura

```
├── Camera/
│   ├── detector.py              # 🔧 Script refatorado
│   ├── requirements.txt
│   └── ...
├── Alimentos/dataset_base/
│   ├── Arroz/        (123 imgs)
│   ├── Feijão/       (209 imgs)
│   └── Macarrão/     (243 imgs)
├── runs/food-v6-local/
│   └── weights/best.pt          # 🤖 Modelo final
└── RELATORIO_ENTREGA.md         # 📋 Relatório completo
```

---

## 📖 Documentação Completa

Veja [RELATORIO_ENTREGA.md](RELATORIO_ENTREGA.md) para:

- ✅ Processo de treinamento detalhado
- ✅ Coleta e augmentation de dados
- ✅ Análise de resultados
- ✅ Próximas etapas
- ✅ Troubleshooting

---

## 🔧 Requisitos

- Python 3.13+
- macOS com Apple Silicon (M1/M2/M3) ou Intel
- Webcam funcionando
- Virtual environment ativado

---

## 🎓 Refatoração do Código

O `detector.py` foi completamente refatorado:

**✨ Melhorias:**

- Classe `FoodDetector` bem estruturada
- Type hints em todas as funções
- Docstrings detalhadas
- Configurações centralizadas
- Tratamento de erros robusto
- Exemplos de uso integrados

**Antes:** 100 linhas procedurais  
**Depois:** ~300 linhas orientadas a objetos, profissionais

---

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique se virtual environment está ativado
2. Confirme que a câmera está funcionando
3. Verifique permissões de acesso à câmera no macOS
4. Consulte logs em `runs/food-v6-local/`

---

## 📅 Histórico

- **27/03/2026:** Coleta de 120 imagens de arroz
- **27/03/2026:** Treinamento v6 completado (100 épocas)
- **27/03/2026:** Refatoração de código finalizada
- **27/03/2026:** Documentação de entrega concluída

---

**Desenvolvedor:** Gabriel Marussi  
**Versão:** 6.0  
**Data:** Março 2026

---

**[Ir para Relatório Completo →](RELATORIO_ENTREGA.md)**
