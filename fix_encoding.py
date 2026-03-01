import os
import glob

# Busca todos los archivos test_*.py dentro de la carpeta tests
for filename in glob.glob("tests/test_*.py"):
    try:
        # Intenta leer con codificación latín-1 (acepta cualquier byte)
        with open(filename, 'r', encoding='latin-1') as f:
            content = f.read()
        # Añadir la cabecera de encoding si no existe
        if not content.startswith('# -*- coding: utf-8 -*-'):
            content = '# -*- coding: utf-8 -*-\n' + content
        # Guardar como UTF-8
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Corregido: {filename}")
    except Exception as e:
        print(f"❌ Error en {filename}: {e}")