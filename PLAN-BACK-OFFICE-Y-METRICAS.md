# Plan Estratégico: Back Office, Métricas y Escalabilidad

**Fecha:** 2026-04-23  
**Problema:** Hemos enfocado el proyecto en frontend (catálogo, carrito). El back office está vacío y es preocupante delegarlo sin estructura.  
**Solución:** Arquitectura modular del back office que se pueda delegar.

---

## 1. Estado Actual vs. Lo que Falta

### ✓ Lo que Existe (Según CLAUDE.md)

```
Estructura Base:
├── Django setup ✓
├── Apps configuradas ✓
├── PostgreSQL lista ✓
├── Decisiones técnicas documentadas ✓
└── Propuesta de dominio + Deck de presentación ✓

Frontend Planeado:
├── Inicio (landing) ✗ Pendiente
├── Catálogo ✗ Pendiente
├── Ficha de producto ✗ Pendiente
├── Carrito ✗ Pendiente
├── Checkout ✗ Pendiente
├── Sobre la empresa ✗ Pendiente
├── Contacto ✗ Pendiente
├── FAQ ✗ Pendiente
└── Gate de mayoría de edad ✗ Pendiente
```

### ✗ Lo que NO Existe (Back Office)

```
Back Office Administrativo:
├── Dashboard de métricas ✗ NO EXISTE
├── Gestión de productos (agregar/editar/eliminar) ✗ NO EXISTE
├── Gestión de stock/inventario ✗ NO EXISTE
├── Gestión de órdenes/pedidos ✗ NO EXISTE
├── Gestión de usuarios/clientes ✗ NO EXISTE
├── Reportes de ventas ✗ NO EXISTE
├── Integración con Google Analytics ✗ NO EXISTE
├── Sistema de roles y permisos ✗ NO EXISTE
└── Auditoría y logs ✗ NO EXISTE
```

---

## 2. Prioridad: Qué Construir Primero

### Fase 1: MVP Back Office (CRÍTICO - Semanas 3-4)

Esto debe estar ANTES de lanzar, porque sin esto, ¿cómo agregarás 200-500 productos por marca?

#### 1.1 Autenticación y Roles
```
Usuarios:
├── Ezra (Propietario/Admin)
├── Asistente de catálogo (puede agregar/editar productos)
├── Gerente de marca (solo ve su marca)
└── Sistema de permisos granular
```

**Implementación:** Django Admin extendido o panel custom simple

#### 1.2 Gestión de Productos (CRÍTICO)
```
Funcionalidades:
├── Formulario para agregar productos
│   ├── Nombre, descripción
│   ├── Precio, SKU
│   ├── Stock (por variante si aplica)
│   ├── Imágenes (sube desde interfaz)
│   ├── Categoría (selector)
│   └── Marca (selector)
├── Editar producto existente
├── Eliminar producto (soft delete)
├── Importar CSV en lote (⭐ crítico para comenzar)
└── Vista previa (cómo se vería en el sitio)
```

**Por qué CSV:** Cargas 500 productos 1 vez con Excel, no manualmente en formulario.

#### 1.3 Dashboard Mínimo de Ventas
```
Mostrará:
├── Hoy: ingresos, órdenes, visitas
├── Semana: tendencia de ventas
├── Top productos (últimos 7 días)
├── Top marcas (comparativa)
└── Carrito abandonado (cuántas personas dejaron sin comprar)
```

**Integración:** Google Tag Manager / Analytics (sin código extra, ya está)

### Fase 2: Operaciones (Semanas 5-6)

```
├── Gestión de órdenes (ver estado, cambiar estado)
├── Gestión de inventario (alertas de stock bajo)
├── Gestión de usuarios/clientes (ver histórico)
└── Notificaciones (cuando hay nueva orden)
```

### Fase 3: Inteligencia (Opcional, semanas 7+)

```
├── Reportes avanzados (Excel download)
├── Análisis de rentabilidad por marca
├── Segmentación de clientes
└── Predicción de tendencias
```

---

## 3. Arquitectura del Back Office

### Opción A: Django Admin Extendido (RECOMENDADO PARA DELEGACIÓN)

**Ventaja:** Fácil de usar, sin código requerido del asistente.

```python
# admin.py - Modelo a seguir
from django.contrib import admin
from .models import Product, Brand, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'stock', 'created_at')
    list_filter = ('brand', 'category', 'created_at')
    search_fields = ('name', 'sku')
    actions = ['mark_as_active', 'mark_as_inactive']
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'description', 'sku', 'brand', 'category')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'sale_price', 'stock', 'low_stock_threshold')
        }),
        ('Imágenes', {
            'fields': ('image_main', 'image_gallery')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
```

**Interfaz:** Parecida a Smoke Jokers / La Tabaquería internamente.

**Delegación:** Un asistente puede aprender en 30 minutos a agregar productos.

### Opción B: Panel Custom (Más Trabajo, Más Control)

```
├── Dashboard personalizado
├── Gestión de productos con React/Vue
├── Importador de CSV visual
└── Reportes embebidos (Chart.js)
```

**Ventaja:** Más control, mejor UX.  
**Desventaja:** 3-4 semanas extra de desarrollo.

### Decisión
**Comienza con Opción A (Django Admin extendido).**  
Si después quieres migrar a Opción B, es viable. Django Admin es suficiente para delegar.

---

## 4. Cómo Verás Métricas (Integración con GTM + Analytics)

### Datos que Ya Tendrás (sin extra código)

Smoke Jokers y La Tabaquería usan Google Tag Manager + Google Analytics. Tú ya lo tienes (decisión técnica).

**GTM proporciona:**
```
├── Página vistas
├── Usuarios únicos
├── Tasa de rebote
├── Tiempo en sitio
├── Fuente de tráfico (orgánico, directo, publicidad)
└── Embudos de conversión (visita → carrito → checkout)
```

### Datos que Necesitas Construir (Back Office)

```
├── Ingresos (solo en DB, no visible en Analytics)
├── Órdenes completadas (solo en DB)
├── Productos más vendidos (solo en DB)
├── Performance por marca (desglose en DB)
└── Margen de rentabilidad (cálculo en backend)
```

### Arquitectura de Reporte

```
Back Office Dashboard (Fase 1)
├── Google Analytics Widget (embebido)
│   └── Visitas, usuarios, tráfico
├── Base de Datos Query (custom)
│   ├── SELECT SUM(total) FROM orders WHERE date >= today
│   ├── SELECT product, SUM(qty) FROM order_items GROUP BY product
│   ├── SELECT brand, SUM(total) FROM orders GROUP BY brand
│   └── Carrito abandonado (sessions sin compra)
└── Tabla simple (HTML table)
    └── Últimas 10 órdenes, estado, total
```

**Código conceptual:**

```python
# back_office/views.py
from django.shortcuts import render
from django.db.models import Sum, Count
from .models import Order, Product

def dashboard(request):
    # Google Analytics (iframe embebido)
    ga_embed_url = "https://analytics.google.com/..."
    
    # Datos de DB
    today_revenue = Order.objects.filter(
        created_at__date=today()
    ).aggregate(Sum('total'))['total__sum']
    
    top_products = Product.objects.annotate(
        total_sold=Sum('orderitem__quantity')
    ).order_by('-total_sold')[:5]
    
    top_brands = Brand.objects.annotate(
        brand_revenue=Sum('product__orderitem__order__total')
    ).order_by('-brand_revenue')
    
    context = {
        'today_revenue': today_revenue,
        'top_products': top_products,
        'top_brands': top_brands,
        'ga_embed_url': ga_embed_url
    }
    return render(request, 'back_office/dashboard.html', context)
```

---

## 5. Flujo para Agregar Productos

### Escenario Actual (Tú manualmente)

```
1. Toma foto de producto en el local
2. Edita nombre, precio, descripción en Excel
3. Carga imagen a carpeta /media/products/
4. En el back office: agregar formulario
5. Repite 500 veces 😅
```

### Escenario Mejorado (Con importador CSV)

```
1. Toma fotos de productos
2. Renombra: marca-tipo-peso.jpg (convención acordada)
3. Crea Excel con columnas: name, price, brand, category, sku, stock
4. En back office: click en "Importar CSV" + sube archivo
5. Sistema crea 500 productos en 2 minutos
6. Revisa, corrige si hay errores, publica
```

**Archivo Excel:**
```
name,sku,brand,category,price,stock,image_url
Tabaco Bristol Caramelo,BST-CAR,Bristol,Tabaco Granel,5000,50,bristol-caramelo.jpg
Tabaco Flandria Virginia,FLA-VIR,Flandria,Tabaco Granel,7600,30,flandria-virginia.jpg
...
```

**Código para el importador:**

```python
# back_office/forms.py
from django import forms
from django.contrib.auth.models import User
import csv

class CSVImportForm(forms.Form):
    csv_file = forms.FileField(label='Subir CSV de productos')
    
    def clean_csv_file(self):
        file = self.cleaned_data['csv_file']
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('Debe ser archivo CSV')
        return file

# back_office/views.py
def import_products_csv(request):
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            reader = csv.DictReader(csv_file)
            
            for row in reader:
                Product.objects.create(
                    name=row['name'],
                    sku=row['sku'],
                    brand=Brand.objects.get(name=row['brand']),
                    category=Category.objects.get(name=row['category']),
                    price=int(row['price']),
                    stock=int(row['stock']),
                    image_url=row['image_url']
                )
            
            return render(request, 'success.html', {
                'count': len(reader)
            })
    else:
        form = CSVImportForm()
    
    return render(request, 'import.html', {'form': form})
```

---

## 6. Delegación en el Futuro

### Escenario: Contratas Asistente de Catálogo

**Lo que necesitas documentar:**

```
1. MANUAL DE USUARIO (15 minutos de lectura)
   ├── Cómo loguear en back office
   ├── Cómo agregar producto (formulario)
   ├── Cómo importar CSV (archivo Excel)
   ├── Cómo editar producto existente
   ├── Cómo ver stock bajo
   └── Qué hacer si algo falla (contactar a Ezra)

2. PLANTILLA DE EXCEL (descargable)
   └── Columnas pre-rellenadas, solo agrega datos

3. CONVENCIÓN DE NOMBRES
   ├── Imágenes: marca-tipo-peso.jpg
   ├── SKU: BRAND-PRODUCT-CODE
   ├── Categorías: solo valores predefinidos

4. LISTA DE VALIDACIÓN
   ├── Producto tiene nombre ✓
   ├── Producto tiene precio ✓
   ├── Producto tiene imagen ✓
   ├── Stock >= 0 ✓
   └── Categoría es válida ✓
```

**Requisitos del Asistente:**
- NO necesita saber código
- Necesita ser ordenado (nombres consistentes)
- Necesita atención al detalle (validación)
- Preferible: alguien con experiencia en Excel

**Tiempo de Onboarding:** 2-3 horas

---

## 7. Plan de Implementación (RECOMENDADO)

### Semana 1-2: Frontend MVP
```
├── Estructura HTML/CSS del sitio
├── Menú de categorías
├── Listado de productos
├── Ficha de producto
├── Carrito (básico)
└── Gate de edad (modal)
```

### Semana 3-4: Back Office MVP (CRÍTICO)
```
├── Autenticación Django Admin
├── Modelo Product + Admin extendido
├── Modelo Order + Admin
├── Importador CSV
└── Dashboard mínimo (últimas órdenes + hoy revenue)
```

### Semana 5-6: Checkout + Pagos
```
├── Integración Mercado Pago / PayPal
├── Página de checkout
├── Confirmación de orden
└── Email de confirmación
```

### Semana 7+: Operaciones
```
├── Gestión de inventario
├── Notificaciones de stock bajo
├── Dashboard de métricas completo
└── Reportes (Excel download)
```

---

## 8. Respuesta a Tus Dudas Específicas

### ❓ "¿Cómo veremos las métricas?"

**Respuesta:**
1. **Google Analytics** (embebido en back office): Visitas, usuarios, tráfico
2. **Dashboard personalizado:** Ventas, órdenes, productos top (los que tú construyes)
3. **Reportes en Excel** (descarga manual cada mes)

**No necesitas hacer nada especial.** GTM ya está configurado.

### ❓ "¿Cómo agregaremos nuevos productos?"

**Respuesta:**
1. **Al inicio (Tú):** Importador CSV (500 productos en 2 minutos)
2. **Mantenimiento (Asistente):** Formulario web simple o CSV incremental

**Modelo sugerido:**
- Lanzamiento: CSV inicial
- Semanal: Asistente agrega 10-20 productos nuevos via formulario
- Mensual: Restock masivo via CSV

### ❓ "¿Cómo delegamos el back office?"

**Respuesta:**
1. Usa Django Admin (la interfaz estándar de Django)
2. Documenta manual de usuario (1-2 páginas)
3. Entrena asistente (2-3 horas)
4. Mira el trabajo la primera semana
5. Delega con confianza

**El riesgo es bajo** porque Django Admin limita lo que pueden romper.

### ❓ "¿Qué pasa con las 3 marcas?"

**Respuesta:**
```
Opción A (Simple): Separar back offices
├── clubdeltabaco.cl: Asistente 1
├── purotabaco.cl: Asistente 2
└── zonatabaco.cl: Asistente 3

Opción B (Integrada): Un solo back office con filtros
├── Dashboard con selector de marca
├── Un asistente ve solo su marca (por rol/permiso)
└── Reportes comparativos (3 marcas en 1 gráfico)
```

**Recomendación:** Opción B (más eficiente, un equipo, múltiples marcas).

---

## 9. Arquitectura Recomendada (Resumen)

```
e-Tabaco (Monorepo)
├── Frontend (Django templates + JavaScript)
│   ├── Inicio / Landing
│   ├── Catálogo con filtros
│   ├── Ficha de producto
│   ├── Carrito
│   ├── Checkout (Mercado Pago)
│   └── Gate de edad
├── Back Office (Django Admin extendido)
│   ├── Autenticación + Roles
│   ├── Gestión de productos (formulario + CSV)
│   ├── Gestión de órdenes
│   ├── Dashboard de métricas
│   ├── Reportes (PDF/Excel)
│   └── Inventario y alertas
├── APIs (Django REST Framework)
│   ├── /api/products/ (GET, POST, PUT, DELETE)
│   ├── /api/orders/ (GET, POST)
│   └── /api/inventory/ (GET, PUT)
└── Integraciones Externas
    ├── Google Tag Manager (Analytics)
    ├── Mercado Pago (Pagos)
    └── Email (Notificaciones)
```

---

## 10. Conclusión: Qué Construir Ahora

### Prioridad Inmediata (Semanas 3-4)

```
HACER PRIMERO (antes del frontend):
1. Modelos de BD (Product, Order, Brand, Category)
2. Django Admin extendido
3. Importador CSV
4. Dashboard básico

POR QUÉ: Sin esto, no puedes:
- Agregar 500 productos
- Ver ventas
- Delegar el negocio
```

### Después (Semanas 5-6)

```
DESPUÉS (una vez que tengas productos):
1. Checkout con Mercado Pago
2. Email de confirmación
3. Gestión de órdenes
```

### Calma

No estás atrasado. **Pero sí,** descuidar el back office desde el inicio es error común. Ahora que lo viste, arreglarlo cuesta 3-4 semanas de desarrollo, que es perfectamente factible en tu timeline.

---

## Próximos Pasos

1. **Leer este documento** (lo hiciste)
2. **Decidir:** ¿Django Admin extendido o Panel custom?
3. **Planificar modelos de BD** (Product, Order, Brand, etc.)
4. **Construir Fase 1** (semanas 3-4)
5. **Documentar para delegación** (manual + plantillas)

¿Preguntas sobre el plan?
