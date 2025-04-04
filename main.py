"""
Autor / Author: Ricardo Orlando Castillo Olivera
Proyecto / Project: XML Dynamic Extractor API
Descripción / Description:
API que recibe un archivo ZIP con múltiples archivos XML y retorna un JSON dinámico por cada XML,
preservando jerarquía, etiquetas y atributos.

API that receives a ZIP file with multiple XMLs and returns a dynamic JSON per XML,
preserving hierarchy, tags, and attributes.
"""

# ------------------------------------------------------------------------
# 🔧 Importaciones / Imports
# ------------------------------------------------------------------------

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import zipfile
import io
import xml.etree.ElementTree as ET

# ------------------------------------------------------------------------
# 🚀 Inicialización de la aplicación FastAPI / FastAPI App Initialization
# ------------------------------------------------------------------------

app = FastAPI(
    title="XML Extractor API",
    description=(
        "API que transforma archivos XML en objetos JSON dinámicos, manteniendo la jerarquía completa.\n"
        "API that transforms XML files into dynamic JSON objects, preserving full hierarchy."
    ),
    version="1.0.0",
    contact={
        "name": "Ricardo Orlando Castillo Olivera",
        "email": "ricaror@hotmail.com"
    }
)

# ------------------------------------------------------------------------
# 🌐 Configuración CORS / CORS Configuration
# ------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes / Allow all origins
    allow_credentials=True,
    allow_methods=["*"],   # Permitir todos los métodos HTTP
    allow_headers=["*"],   # Permitir todos los headers
)

# ------------------------------------------------------------------------
# 🧠 Función recursiva para transformar un XML en JSON / Recursive XML → JSON
# ------------------------------------------------------------------------

def xml_element_to_dict(element):
    """
    Convierte un nodo XML y sus hijos en un diccionario
    Converts an XML node and its children into a dictionary
    """
    node = {}

    # Atributos / Attributes
    if element.attrib:
        node.update(element.attrib)

    # Hijos / Children
    for child in element:
        child_key = child.tag
        child_value = xml_element_to_dict(child)

        if child_key in node:
            if not isinstance(node[child_key], list):
                node[child_key] = [node[child_key]]
            node[child_key].append(child_value)
        else:
            node[child_key] = child_value

    return node

# ------------------------------------------------------------------------
# 📦 Procesamiento de XML individual / Single XML Parsing
# ------------------------------------------------------------------------

def parse_xml_content(xml_bytes):
    """
    Parsea el contenido de un XML en bytes y lo convierte en JSON
    Parses the XML content in bytes and converts it to JSON
    """
    try:
        root = ET.fromstring(xml_bytes)
        parsed = {root.tag: xml_element_to_dict(root)}
        return parsed
    except Exception as e:
        return {"error": f"No se pudo procesar XML: {str(e)}"}

# ------------------------------------------------------------------------
# 📥 Endpoint: /procesar-zip/ → Recibe ZIP con XMLs y devuelve JSONs
# ------------------------------------------------------------------------

@app.post("/procesar-zip/", summary="Procesar archivo ZIP", tags=["XML Parser"])
async def procesar_zip(file: UploadFile = File(...)):
    """
    Procesa un archivo ZIP que contiene múltiples XMLs y los convierte en objetos JSON
    Processes a ZIP file containing multiple XML files and returns their content as JSON objects
    """
    if not file.filename.endswith(".zip"):
        return JSONResponse(status_code=400, content={"error": "El archivo debe ser un .zip"})

    content = await file.read()
    results = []

    # Descomprimir ZIP y procesar cada XML / Unzip and process each XML
    with zipfile.ZipFile(io.BytesIO(content), "r") as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.endswith(".xml"):
                with zip_ref.open(file_info) as xml_file:
                    xml_content = xml_file.read()
                    parsed_xml = parse_xml_content(xml_content)
                    results.append({
                        "archivo": file_info.filename,
                        "contenido": parsed_xml
                    })

    return JSONResponse(content=results)
