# coding: utf-8
"""
export_custom_mvt_structure.py

Este script recorre tu proyecto en D:\Programas_D\admin_kiosk
y genera uno o varios .txt con la estructura de carpetas/archivos,
incrustando SOLO el contenido de archivos que tú has escrito:
(.py, .html, .css, .js, .jsc, .json, .md).

Excluye carpetas de sistema (ej. .git, __pycache__, etc.) y 
archivos sin extensión relevante (p. ej. .pyc, .exe, .dll, etc.).

USO:
  cd D:\Programas_D\admin_kiosk
  python scripts\export_custom_mvt_structure.py

Luego verás uno o varios .txt (project_custom_structure.txt, numerados si excede CHAR_LIMIT).
¡Listo!
"""

import os
import datetime
# CONFIGURACIONES
# Ruta raíz donde se encuentra el proyecto
ROOT_DIR = r"D:\Programas_D\admin_kiosk"

# Límite máximo de caracteres por archivo de salida
CHAR_LIMIT = 30000000

# Extensiones "tuyas" para las que incrustaremos el contenido (ajusta a tus necesidades)
YOUR_EXTENSIONS = (".py", ".html", ".css", ".js", ".jsc", ".json", ".md")

# Carpetas de sistema a excluir
EXCLUDED_DIRS = {".git", "__pycache__", "venv", "env", ".svn", ".hg"}

# Archivos de sistema a ignorar (extensiones o patrones)
EXCLUDED_FILE_EXT = {".pyc", ".exe", ".dll", ".so", ".pyd"}

# Nombre base para el/los archivo(s) de salida
OUTPUT_BASENAME = "project_custom_structure"

def main():
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = (
        f"=== PROYECTO MVT PERSONALIZADO: {os.path.basename(ROOT_DIR)} ===\n"
        f"Fecha de creación del archivo: {now_str}\n\n"
        f"Carpeta raíz analizada: {ROOT_DIR}\n\n"
        "Incluimos SOLO el contenido de archivos con extensiones:\n"
        f"  {YOUR_EXTENSIONS}\n\n"
        "Excluimos carpetas de sistema:\n"
        f"  {EXCLUDED_DIRS}\n"
        "Excluimos archivos con extensiones:\n"
        f"  {EXCLUDED_FILE_EXT}\n\n"
        "Estructura y contenido de archivos relevantes:\n"
        "----------------------------------------------\n\n"
    )

    # Acumulamos todo el texto aquí
    all_text_parts = [header]

    def build_structure_tree(current_path, indent=""):
        """Recorre recursivamente la carpeta actual, listando subcarpetas/archivos.
           Incrusta contenido de los archivos con extensiones en YOUR_EXTENSIONS."""
        # Obtenemos el listado ordenado (alfabético) para consistencia
        try:
            entries = sorted(os.listdir(current_path), key=str.lower)
        except PermissionError:
            all_text_parts.append(f"{indent}[Sin permisos para acceder a {current_path}]\n")
            return

        for entry in entries:
            entry_path = os.path.join(current_path, entry)

            # Si es carpeta, verificamos si está excluida
            if os.path.isdir(entry_path):
                if entry in EXCLUDED_DIRS:
                    # No entramos a carpetas excluidas
                    continue
                # Mostramos carpeta
                all_text_parts.append(f"{indent}Carpeta: {entry}\n")
                # Recursemos dentro (indentación adicional)
                build_structure_tree(entry_path, indent + "    ")
            else:
                # Es archivo
                # Revisamos extensión
                _, ext = os.path.splitext(entry)
                ext = ext.lower()

                if ext in EXCLUDED_FILE_EXT:
                    # Es un archivo de sistema (ej. .pyc), lo omitimos
                    continue

                all_text_parts.append(f"{indent}Archivo: {entry}\n")

                # Si es extensión que consideramos "nuestra", incrustamos contenido
                if ext in YOUR_EXTENSIONS:
                    try:
                        with open(entry_path, "r", encoding="utf-8", errors="replace") as f:
                            file_data = f.read()
                        all_text_parts.append(f"{indent}--- CONTENIDO de {entry} ---\n")
                        # No se va a indentar el código para no distorsionarlo;
                        # si prefieres, podrías añadir "indent" aquí.
                        all_text_parts.append(file_data + "\n")
                    except Exception as e:
                        all_text_parts.append(f"{indent}[No se pudo leer {entry}: {e}]\n")

    # Iniciamos la construcción de la estructura desde la carpeta raíz
    build_structure_tree(ROOT_DIR)

    # Unimos todo en un solo string
    final_text = "".join(all_text_parts)

    # Partimos en trozos si excede CHAR_LIMIT
    total_len = len(final_text)
    num_chunks = (total_len + CHAR_LIMIT - 1) // CHAR_LIMIT

    start_idx = 0
    for i in range(num_chunks):
        end_idx = min(start_idx + CHAR_LIMIT, total_len)
        chunk_text = final_text[start_idx:end_idx]

        # Definimos el nombre de archivo
        if num_chunks == 1:
            out_filename = f"{OUTPUT_BASENAME}.txt"
        else:
            out_filename = f"{OUTPUT_BASENAME}_{i+1}.txt"

        with open(out_filename, "w", encoding="utf-8") as out_f:
            out_f.write(chunk_text)

        print(f"Se ha creado '{out_filename}' (caracteres {start_idx+1} a {end_idx} de {total_len}).")

        start_idx = end_idx

    print("\n¡Exportación completada! Revisa tus archivos .txt.")

if __name__ == "__main__":
    main()
