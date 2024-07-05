
# XYZ Inventory System

## Descripción

La empresa XYZ es una tienda de productos electrónicos que desea implementar un sistema de gestión de ventas y de inventario para llevar un registro detallado de sus operaciones comerciales. Este sistema permite a los vendedores registrar las ventas realizadas e indicar el producto vendido, la cantidad, el precio de venta y la fecha de la transacción. También permite gestionar el inventario disponible en la tienda, asegurando la integridad de los datos mediante un mecanismo de transacciones.

## Características

- **Gestión de Ventas**: Registra ventas indicando el producto, cantidad, precio de venta y fecha de la transacción.
- **Gestión de Inventario**: Mantiene un registro del inventario disponible en la tienda, indicando la cantidad de unidades de cada producto disponible y su precio de venta.
- **Integridad de Datos**: Utiliza transacciones para asegurar que, en caso de error durante la realización de una venta o actualización del inventario, la operación se pueda deshacer dejando la base de datos en su estado anterior.

## Tecnologías Utilizadas

- Python
- Flask
- Redis
- HTML/CSS
- Pytest (para pruebas)

## Requisitos Previos

- Python 3.6 o superior
- Redis

## Instalación

1. Clona el repositorio:

   \`\`\`sh
   git clone https://github.com/tu-usuario/xyz_inventory_system.git
   cd xyz_inventory_system
   \`\`\`

2. Crea y activa un entorno virtual:

   \`\`\`sh
   python -m venv venv
   source venv/bin/activate   # En Windows usa: venv\Scripts\activate
   \`\`\`

3. Instala las dependencias:

   \`\`\`sh
   pip install -r requirements.txt
   \`\`\`

4. Asegúrate de que Redis esté instalado y ejecutándose en tu sistema.

## Ejecución de la Aplicación

1. Inicia el servidor Redis:

   \`\`\`sh
   redis-server
   \`\`\`

2. Ejecuta la aplicación Flask:

   \`\`\`sh
   flask run
   \`\`\`

3. Abre tu navegador web y ve a \`http://127.0.0.1:5000\` para interactuar con la aplicación.

## Uso

### Gestión de Inventario

1. Navega a la página de Gestión de Inventario desde la página principal.
2. Usa el formulario para agregar o actualizar productos en el inventario.
3. El inventario actual se mostrará en una tabla en la misma página.

### Registro de Ventas

1. Navega a la página de Registro de Ventas desde la página principal.
2. Usa el formulario para registrar una venta indicando el producto, cantidad, precio de venta y fecha de la transacción.

## Pruebas

Para ejecutar las pruebas, asegúrate de que Redis esté ejecutándose y luego usa **pytest:**


PYTHONPATH=.. pytest   # En sistemas Unix
# o
set PYTHONPATH=.. && pytest   # En Windows


## Estructura del Proyecto

\`\`\`
xyz_inventory_system/
│
├── app.py
├── requirements.txt
├── README.md
├── tests/
│   ├── __init__.py
│   └── test_app.py
├── templates/
│   ├── index.html
│   ├── sales.html
│   └── inventory.html
└── static/
    └── style.css

\`\`\`


