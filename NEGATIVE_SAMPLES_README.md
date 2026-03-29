# Imagens Negativas para Validação

## Descrição
Pasta contendo **100 imagens negativas** (não-produtos) coletadas automaticamente via webscrapping.

**Localização:** `negative_samples/`

## O que são imagens negativas?
Imagens que NÃO contêm arroz, feijão ou macarrão. Incluem:
- Plantas e flores
- Animais
- Objetos domésticos
- Frutas soltas
- Rostos
- Natureza
- Outros alimentos (pizza, bolo, salada, pão)

## Como usar no dataset para treinar

### 1. Copiar para o dataset
```bash
# Copiar as imagens negativas para a pasta de validação (ou teste)
cp negative_samples/*.jpg detector/test/images/
```

### 2. Estrutura do dataset esperada
```
detector/
├── train/
│   ├── images/     # imagens de treinamento (arroz, feijão, macarrão)
│   └── labels/     # arquivos .txt com anotações
├── valid/
│   ├── images/     # imagens de validação
│   └── labels/
└── test/
    ├── images/     # imagens de teste (ADICIONAR NEGATIVAS AQUI)
    └── labels/
```

### 3. Criar labels vazios (imagens negativas)
Como essas imagens não contêm os produtos alertados, você pode:

**Opção A: Remover o arquivo de label**
```bash
# Cria um arquivo .txt vazio para cada imagem negativa
for img in negative_samples/*.jpg; do
    base=$(basename "$img" .jpg)
    touch "detector/test/labels/${base}.txt"  # arquivo vazio = sem detecções
done
```

**Opção B: Usar em validação sem labels**
```bash
# Copiar apenas as imagens, sem labels
# O modelo usará isso para testar se consegue ignorar não-produtos
cp negative_samples/*.jpg detector/test/images/
```

### 4. Retreinar o modelo (opcional)
Se quiser usar essas imagens para melhorar o modelo:

```bash
cd detector
python run.py --epochs 50 --img 416
```

## Informações das Imagens Coletadas

- **Total:** 100 imagens
- **Formato:** JPG
- **Tamanho mínimo:** 200x200 pixels
- **Qualidade:** 92 (JPEG)
- **Fontes de busca:** 
  - DuckDuckGo (seeds iniciais)
  - Pesquisas complementares em português e inglês

## Próximos Passos

1. **Revisar as imagens:** Verificar se todas fazem sentido (não contêm arroz, feijão ou macarrão)
2. **Ajustar o dataset:** Distribuir entre train/valid/test conforme necessário
3. **Retreinar o modelo:** Com essas imagens negativas, o modelo ficará melhor em ignorar não-produtos
4. **Testar:** Avaliar se o modelo mantém boa acurácia com essas imagens negativas

## Estatísticas das Categorias

As imagens foram coletadas de:
- Plantas e flores: ~20 imagens
- Árvores e natureza: ~27 imagens  
- Outros itens variados: ~53 imagens

## Caso Haja Problemas

Se o dataset ficar muito desbalanceado, você pode:
1. Remover algumas imagens randomicamente
2. Reduzir o tamanho do dataset original
3. Usar data augmentation nas imagens de produtos

---

**Criado em:** 2026-03-29  
**Método:** Webscrapping automático (DuckDuckGo + metadados)
