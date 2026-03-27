# Plan de Implementación — e-Tabaco MVP
**Fecha:** 2026-03-27
**Spec base:** docs/superpowers/specs/2026-03-27-etabaco-ecommerce-design.md
**Stack:** Python + Django + PostgreSQL + Bootstrap + HTMX + Stripe

---

## FASE 1: Configuración del entorno y estructura base

### Tarea 1.1 — Estructura del proyecto Django
- Crear proyecto Django: `etabaco`
- Crear apps: `productos`, `carrito`, `pedidos`, `paginas`
- Configurar `settings.py` para PostgreSQL
- Configurar variables de entorno con `python-decouple` o `django-environ`
- Crear archivo `.env.example`

### Tarea 1.2 — Dependencias
Instalar y registrar en `requirements.txt`:
- django
- psycopg2-binary
- pillow (imágenes de productos)
- stripe
- django-htmx
- pytest + pytest-django
- python-decouple

### Tarea 1.3 — Configuración de Bootstrap y estática
- Configurar `STATIC_FILES` en Django
- Integrar Bootstrap 5 vía CDN en template base
- Integrar HTMX vía CDN en template base
- Crear `base.html` con navbar, footer y bloque de contenido

### Tarea 1.4 — Configuración de base de datos
- Crear base de datos PostgreSQL local: `etabaco_db`
- Verificar conexión desde Django
- Ejecutar migraciones iniciales

---

## FASE 2: Modelos de datos

### Tarea 2.1 — App `productos`: Modelos
```python
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/')
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_caja = models.DecimalField(max_digits=10, decimal_places=2)
    unidades_por_caja = models.IntegerField(default=10)
    stock = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
```

### Tarea 2.2 — App `pedidos`: Modelos
```python
class Orden(models.Model):
    ESTADOS = [('pendiente','Pendiente'),('pagado','Pagado'),
               ('enviado','Enviado'),('entregado','Entregado')]
    numero_orden = models.CharField(max_length=20, unique=True)
    cliente_nombre = models.CharField(max_length=200)
    cliente_email = models.EmailField()
    cliente_telefono = models.CharField(max_length=20)
    direccion_envio = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

class DetallePedido(models.Model):
    TIPOS = [('unidad','Unidad'),('caja','Caja')]
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('productos.Producto', on_delete=models.PROTECT)
    tipo_venta = models.CharField(max_length=10, choices=TIPOS)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
```

### Tarea 2.3 — Migraciones y Django Admin
- Crear y aplicar migraciones
- Registrar modelos en admin.py con personalización básica
- Verificar que Django Admin muestre correctamente productos y pedidos

---

## FASE 3: Validación de edad

### Tarea 3.1 — Middleware de verificación de edad
- Crear middleware `AgeVerificationMiddleware`
- Rutas excluidas: `/verificar-edad/`, `/admin/`, archivos estáticos
- Si sesión no tiene `edad_verificada=True` → redirigir a `/verificar-edad/`

### Tarea 3.2 — View y template de verificación
- View `verificar_edad`: GET muestra modal, POST procesa respuesta
- Si respuesta = "si" → `request.session['edad_verificada'] = True` → redirect al home
- Si respuesta = "no" → redirect a `https://www.google.com`
- Template: pantalla completa, diseño sobrio con paleta de colores definida

---

## FASE 4: Catálogo y ficha de producto

### Tarea 4.1 — Views del catálogo
- `CatalogoView` (ListView): lista de productos activos, filtro por categoría
- `ProductoDetailView` (DetailView): ficha de producto individual
- URLs: `/catalogo/` y `/catalogo/<slug>/` o `/catalogo/<pk>/`

### Tarea 4.2 — Templates del catálogo
- `catalogo.html`: grid de productos con Bootstrap, precio unidad y caja
- `producto_detalle.html`: imagen grande, descripción, selector tipo (unidad/caja) con JS básico que actualiza el precio visible, selector de cantidad, botón "Agregar al carrito"
- Advertencia sanitaria visible en cada producto

---

## FASE 5: Carrito de compras (HTMX)

### Tarea 5.1 — Lógica del carrito en sesión Django
- El carrito se almacena en `request.session['carrito']`
- Estructura: `{producto_id: {tipo, cantidad, precio_unitario, subtotal}}`
- Clase helper `Carrito` con métodos: `agregar()`, `eliminar()`, `actualizar()`, `total()`

### Tarea 5.2 — Views del carrito con HTMX
- `agregar_al_carrito`: POST, retorna fragmento HTML del carrito actualizado
- `eliminar_del_carrito`: POST, retorna fragmento HTML actualizado
- `actualizar_cantidad`: POST, retorna fragmento HTML actualizado
- `ver_carrito`: GET, página completa del carrito
- Usar `django-htmx` para detectar requests HTMX y retornar fragmentos vs páginas completas

### Tarea 5.3 — Templates del carrito
- `carrito.html`: página completa con resumen de items
- `carrito_fragment.html`: fragmento que se intercambia con HTMX (tabla de items + total)
- Navbar muestra contador de items del carrito (actualizado con HTMX)

---

## FASE 6: Checkout y pagos

### Tarea 6.1 — Formulario de checkout
- `CheckoutForm`: campos de envío y facturación
- View `checkout`: GET muestra formulario, POST valida y crea sesión de pago Stripe
- Template `checkout.html`: formulario Bootstrap de 3 pasos (envío, facturación, pago)

### Tarea 6.2 — Integración Stripe
- Configurar claves Stripe en `.env`
- View `crear_payment_intent`: crea PaymentIntent con el total del carrito
- View `stripe_webhook`: escucha evento `payment_intent.succeeded`
  - Crea la Orden y DetallePedido en la base de datos
  - Limpia el carrito de la sesión
  - Envía email de confirmación
- Template `checkout.html`: incluye Stripe.js para procesar pago

### Tarea 6.3 — Confirmación de pedido
- View `confirmacion_pedido`: muestra número de orden y resumen
- Template `confirmacion.html`: número de orden, productos comprados, info de envío estimado

---

## FASE 7: Email de confirmación

### Tarea 7.1 — Configuración de email
- Configurar SMTP en `settings.py` (usar Gmail SMTP para desarrollo)
- Template HTML de email: `email/confirmacion_pedido.html`

### Tarea 7.2 — Envío automático
- Función `enviar_email_confirmacion(orden)` llamada desde el webhook de Stripe
- Contenido: número de orden, detalle de productos, total, info de envío

---

## FASE 8: Páginas estáticas y Home

### Tarea 8.1 — App `paginas`
- View y template `home.html`: banner + productos destacados (los 4 más recientes activos) + bloque "Sobre nosotros"
- View y template `sobre_nosotros.html`
- View y template `contacto.html` con formulario simple
- View y template `faqs.html` con acordeón Bootstrap
- View y template `terminos.html`
- View y template `privacidad.html`

---

## FASE 9: Diseño visual

### Tarea 9.1 — CSS personalizado
- Archivo `static/css/etabaco.css` con:
  - Variables CSS de la paleta de colores definida
  - Fuentes Google: Playfair Display + Inter
  - Estilos personalizados del navbar, footer, botones, cards de producto

### Tarea 9.2 — Responsive y polish
- Verificar todas las páginas en mobile (Bootstrap breakpoints)
- Navbar hamburguesa funcional en mobile
- Carrito visible con contador en todo momento

---

## FASE 10: Testing

### Tarea 10.1 — Configuración de Pytest
- Crear `pytest.ini` y `conftest.py`
- Configurar `pytest-django` con `DJANGO_SETTINGS_MODULE`

### Tarea 10.2 — Tests críticos
- Test: validación de edad (acceso bloqueado sin verificar, acceso permitido verificado)
- Test: agregar producto al carrito (unidad y caja)
- Test: cálculo correcto de totales del carrito
- Test: creación de Orden con DetallePedido correcto
- Test: modelo Producto (campos, precios, stock)

---

## FASE 11: Docker y Deploy

### Tarea 11.1 — Docker
- `Dockerfile` para la app Django
- `docker-compose.yml` con servicios: `web` (Django) + `db` (PostgreSQL)
- `.dockerignore`
- Verificar que `docker-compose up` levanta el proyecto completo

### Tarea 11.2 — Deploy en Railway
- Crear cuenta en Railway (si no existe)
- Conectar repositorio GitHub
- Configurar variables de entorno en Railway
- Configurar PostgreSQL como servicio en Railway
- Ejecutar migraciones en producción
- Verificar que el sitio corre correctamente en la URL de Railway

---

## Criterios de verificación final

- [ ] Validación de edad bloquea el sitio correctamente
- [ ] El catálogo muestra todos los productos activos
- [ ] Se puede agregar/quitar productos del carrito sin recargar la página (HTMX)
- [ ] El checkout completa una compra en modo test de Stripe
- [ ] Se envía email de confirmación al completar la compra
- [ ] Django Admin permite gestionar productos y ver pedidos
- [ ] El sitio es responsive en mobile
- [ ] Todos los tests pasan con `pytest`
- [ ] El proyecto corre con `docker-compose up`
