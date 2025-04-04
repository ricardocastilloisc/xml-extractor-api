# 🧩 XML Dynamic Extractor API

API desarrollada en Python con FastAPI que permite procesar múltiples archivos XML comprimidos en un archivo `.zip`. Convierte cada XML en un objeto JSON respetando jerarquía, etiquetas, atributos y estructura completa.

---

## 📌 ¿Qué hace esta API? / What does this API do?

**Español:**

- Recibe un archivo `.zip` que contiene múltiples archivos `.xml`.
- Cada XML es analizado de forma **dinámica** y convertido a un objeto JSON.
- Se respetan etiquetas con prefijos (`cfdi:`, `nomina12:`, etc.) y sus atributos.
- No hay estructura fija: funciona con cualquier XML válido.

**English:**

- Accepts a `.zip` file containing multiple `.xml` files.
- Each XML is parsed **dynamically** and converted into a JSON object.
- Preserves tag names (with namespaces like `cfdi:`, `nomina12:`) and attributes.
- Fully flexible: works with any well-formed XML.

---

## 🚀 ¿Cómo usarla? / How to use it?

1. Ejecuta el servidor localmente:
   ```bash
   uvicorn main:app --reload
   ```

2. Accede a la documentación interactiva de Swagger:
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

3. Prueba el endpoint `POST /procesar-zip/`:
   - Sube un archivo `.zip` que contenga uno o varios `.xml`.
   - Recibirás una respuesta en formato JSON por cada archivo.

---

## 🔧 Requisitos / Requirements

```txt
fastapi
uvicorn
mangum
```

Instala las dependencias:
```bash
pip install -r requirements.txt
```

---

## 📁 Estructura esperada del proyecto

```
xml-extractor-api/
├── main.py
├── requirements.txt
└── README.md
```

---

## 👤 Autor / Author

**Ricardo Orlando Castillo Olivera**  
Ingeniero en Sistemas / Software Engineer  
Email: `ricaror@hotmail.com`  
Versión: `1.0.0`
