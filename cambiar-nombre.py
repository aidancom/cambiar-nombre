from pathlib import Path
import time
import chardet
import shutil
import subprocess
import os
import platform
def detectar_codificacion(ruta_archivo):
    with open(ruta_archivo, 'rb') as archivo:
        resultado = chardet.detect(archivo.read())
    return resultado['encoding']
def cambioEnArchivos(particular, nuevo_nombre):
    nombre = nuevo_nombre.lower()
    codificacion = detectar_codificacion(particular)
    with open(particular, "r", encoding=codificacion) as archivo:
        contenido = archivo.read()

    contenido_actualizado = contenido.replace("plugin_name", nombre.replace(" ", "_"))
    contenido_actualizado = contenido_actualizado.replace("plugin-name", nombre.replace(" ", "-"))
    contenido_actualizado = contenido_actualizado.replace("Plugin_Name", nombre.title().replace(" ", "_"))
    contenido_actualizado = contenido_actualizado.replace("PLUGIN_NAME_", nombre.upper().replace(" ", "_") + "_")
    contenido_actualizado = contenido_actualizado.replace("PluginName", nombre.title().replace(" ", ""))
    contenido_actualizado = contenido_actualizado.replace("Plugin Name", nombre.title())

    with open(particular, "w", encoding=codificacion) as archivo:
        archivo.write(contenido_actualizado)

def cambiarRuta(ruta, nuevo_nombre):
    if ruta.name == "plugin-name.php":
        linea_nueva = f" * Plugin Name:       {nuevo_nombre.capitalize()}\n"
        numero_linea = 16

        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

        lineas.pop(numero_linea -1)
        lineas.insert(numero_linea, linea_nueva)

        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.writelines(lineas)

    if "plugin-name" in ruta.name:
        nombre_a_cambiar = ruta.name[0:11]
        nombre_cambiado = ruta.name.replace(nombre_a_cambiar, nuevo_nombre)
        nueva = ruta.with_name(nombre_cambiado.replace(" ", "-"))
        ruta.rename(nueva)

def directorios(ruta):
    for particular in ruta.iterdir():
        if particular.is_dir():
           cambiarRuta(particular, nuevo_nombre)
           directorios(particular)
        elif particular.is_file():
            cambioEnArchivos(particular, nuevo_nombre)
            cambiarRuta(particular, nuevo_nombre)


directorio = os.getcwd()
ruta_repo = rf"{directorio}\WordPress-Plugin-Template"

if platform.system() == 'Windows':
    if not Path(ruta_repo).exists():
        subprocess.run(['git', 'clone', 'https://github.com/raulrodes/WordPress-Plugin-Template.git', ruta_repo], check=True)
elif platform.system() == 'Linux':
    if not Path(ruta_repo).exists():
        subprocess.run(['git clone https://github.com/raulrodes/WordPress-Plugin-Template.git', ruta_repo], check=True)

ruta_plugin = rf"{directorio}\WordPress-Plugin-Template\plugin-name"
ruta_deseada = directorio
ruta = Path(rf"{directorio}\plugin-name")

if not Path(ruta).exists():
    shutil.move(ruta_plugin, ruta_deseada)

if platform.system() == 'Windows':
    print(f"Tienes {platform.system()}")
    if Path(ruta_repo).exists():
        subprocess.run(['rmdir', '/s', '/q', ruta_repo], shell=True, check=True)
elif platform.system() == 'Linux':
    print(f"Tienes {platform.system()}")
    if Path(ruta_repo).exists():
        subprocess.run(['rm', '-rf', ruta_repo], shell=True, check=True)

while True:
    try:

        nuevo_nombre = str(input("Introduce el nombre a cambiar (sin guiones): "))

        if ruta.is_dir():
           print(ruta.cwd())
           directorios(ruta)
           nueva_ruta_principal = ruta.with_name(nuevo_nombre.replace(" ", "-"))
           ruta.rename(nueva_ruta_principal)
           print("Todo hecho")
           time.sleep(2)
           break;
        else:
            print("No Existe, prueba otra vez")
            continue
    except WindowsError:
        print(f"Error: la carpeta {nuevo_nombre} ya existe")
    except Exception as e:
         print(f"Error: {e}")
