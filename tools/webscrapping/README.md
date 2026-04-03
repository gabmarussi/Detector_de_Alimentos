# Web Scrapping (Auxiliary Tools)

These scripts collect images from the internet to expand the training dataset.

They are not required to run real-time camera detection.

## Files

- collect_images.py
- collect_images_bing.py

## Usage (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
cd .\tools\webscrapping
python .\collect_images_bing.py
```

## Expected Output

Images should be organized in:

```text
detector/
|- train/images/
|- valid/images/
`- test/images/
```

## Note

For real-time inference, use camera/run.py.