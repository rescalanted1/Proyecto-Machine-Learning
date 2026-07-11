import zipfile
import json
import os

model_path = 'backend/modelo_efficientnet_final.keras'
temp_path = 'backend/modelo_efficientnet_final_fixed.keras'

def remove_quantization_config(d):
    if isinstance(d, dict):
        d.pop('quantization_config', None)
        for k, v in d.items():
            remove_quantization_config(v)
    elif isinstance(d, list):
        for item in d:
            remove_quantization_config(item)

with zipfile.ZipFile(model_path, 'r') as zin:
    with zipfile.ZipFile(temp_path, 'w') as zout:
        for item in zin.infolist():
            content = zin.read(item.filename)
            if item.filename == 'config.json':
                config = json.loads(content)
                remove_quantization_config(config)
                content = json.dumps(config).encode('utf-8')
            zout.writestr(item, content)

os.replace(temp_path, model_path)
print("Model fixed successfully!")
