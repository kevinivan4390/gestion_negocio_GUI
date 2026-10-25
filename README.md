# Sistema de Gestión de Negocio (Desktop GUI)

Software de escritorio desarrollado en Python con interfaz gráfica (Tkinter) y persistencia en base de datos relacional (MySQL) para el control comercial integral de stock, clientes, ventas, compras y caja.

## 🚀 Tecnologías y Arquitectura

* **Lenguaje:** Python
* **Interfaz Gráfica:** Tkinter
* **Base de Datos:** MySQL
* **Patrón de Diseño:** MVC (Modelo - Vista - Controlador / Capas)

### 📁 Estructura del Proyecto

* `database/`: Conexiones y consultas SQL para cada entidad (caja, clientes, empleados, productos, proveedores, ventas).
* `models/`: Clases de dominio del sistema (Caja, Cliente, Empleado, Producto, Proveedor, Venta).
* `views/`: Interfaz de usuario dividida por módulos (Caja, Clientes, Empleados, Productos, Proveedores, Ventas).
* `resources/`: Archivos multimedia, iconos, facturas y reportes.
* `utils/`: Funciones auxiliares y scripts de utilidad.

---

## ⚙️ Funcionalidades Principales

* **Control de Stock y Productos:** Alta, modificación, catálogo y búsqueda filtrada.
* **Gestión de Clientes y Proveedores:** Registro, modificación y detalle comercial.
* **Punto de Venta y Caja:** Registro de transacciones, historial de ventas y flujo de caja.
* **Gestión de Empleados:** Administración del personal del negocio.
* **Reportes y Facturación:** Generación de comprobantes y gestión de reportes.

---

## 🛠️ Instalación y Configuración

1. **Clonar el repositorio:**

   git clone https://github.com/kevinivan4390/gestion_negocio_GUI.git
   cd gestion_negocio_GUI

2. **Crear y activar el entorno virtual**

python -m venv venv
venv\Scripts\activate

3. **Instalar dependencias**

pip install -r requirements.txt

4. **Configurar la base de datos**

 - Importar el archivo gestion_negocio_GUI.sql en tu servidor MySQL (usando DBeaver, MySQL Workbench, phpMyAdmin, etc.).
 - Revisar las credenciales de conexión en database/conexion.py si tus datos locales de MySQL varían.

## Ejecutar la aplicación

python main.py