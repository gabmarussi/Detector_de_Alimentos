# Web Scrapping (Ferramentas Auxiliares)

Estes scripts servem para coletar imagens da internet e aumentar dataset de treino.

Nao sao necessarios para rodar a deteccao em camera.

## Arquivos

- collect_images.py
- collect_images_bing.py

## Uso (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
cd .\tools\webscrapping
python .\collect_images_bing.py
```

## Saida esperada

As imagens devem ser organizadas em:

```text
detector/
|- train/images/
|- valid/images/
`- test/images/
```

## Observacao

Para inferencia em tempo real, use camera/run.py.