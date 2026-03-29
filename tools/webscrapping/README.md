# 🛠️ Web Scrapping (Ferramentas Auxiliares)

> ⚠️ **AVISO:** Este é código **auxiliar**, não faz parte do detector principal!

Esses scripts são usados para **coletar imagens automaticamente** da internet para treinar o modelo.

---

## 💡 Quando Usar?

Você **NÃO precisa** usar isso para rodar o detector!

Use apenas se quiser:

- ✅ Treinar um novo modelo com mais imagens
- ✅ Atualizar o dataset com novos alimentos
- ✅ Coletar mais exemplos de uma categoria

---

## 📂 Arquivos

| Arquivo                  | Função                    |
| ------------------------ | ------------------------- |
| `collect_images.py`      | Coleta imagens de URLs    |
| `collect_images_bing.py` | Coleta do Bing Search API |

---

## 🚀 Como Usar

### Coleta do Bing (Mais Fácil)

```bash
cd /Users/gabmarussi/Documents/GitHub/Detector-de-Alimentos
source .venv/bin/activate

cd tools/webscrapping
python collect_images_bing.py
```

### Coleta de URLs Customizadas

```bash
python collect_images.py
```

---

## 📝 Saída

As imagens coletadas são salvas em:

```
detectors/food-detector-v8/
├── train/images/
├── valid/images/
└── test/images/
```

---

## ⚠️ Lembrete

- Essas imagens precisam ser **anotadas** com labels (bounding boxes)
- Depois precisam ser usadas para **treinar** um novo modelo
- Esse processo é **longo e complexo**

Para apenas **usar** o detector, vá para [`detector/run.py`](../../detector/).
