# Especificación de Diseño — e-Tabaco E-commerce
**Fecha:** 2026-03-27
**Proyecto:** e-Tabaco — Tienda online de tabaco para liar
**Versión:** 1.0
**Estado:** Aprobado

---

## 1. Resumen del Proyecto

Desarrollo de una tienda online (e-commerce) para una empresa tabaquera que vende tabaco para liar en dos modalidades: por unidad y por caja. El objetivo del MVP es tener una tienda funcional, sobria y profesional que permita al cliente descubrir productos, agregarlos al carrito y completar la compra de forma segura.

**Supuesto clave:** No se contaba con información específica de la empresa al momento del diseño. Los datos reales (nombre, logo, dirección, productos exactos, precios, métodos de envío y normativa aplicable por país) deberán ser completados por el cliente antes del lanzamiento.

---

## 2. Enfoque Elegido

**Opción 1: Estructura Simple y Directa**

Tienda minimalista con foco 100% en funcionalidad y conversión de venta. Sin complejidades innecesarias para el MVP. Permite tener algo funcional rápido y escalar en fases posteriores.

---

## 3. Estructura General del Sitio

### Páginas principales

| Página | Descripción |
|---|---|
| Validación de edad | Primera pantalla obligatoria. Modal que verifica mayoría de edad antes de acceder. |
| Home | Banner principal, productos destacados, breve presentación de la empresa, CTA al catálogo. |
| Catálogo | Listado completo de productos con filtros, búsqueda y paginación. |
| Ficha de producto | Detalle del producto, selector unidad/caja, cantidad, botón agregar al carrito. |
| Carrito | Resumen de items, edición de cantidades, totales automáticos. |
| Checkout | Formulario de datos de envío, facturación y pago. |
| Confirmación | Número de pedido, resumen de compra, info de envío estimado. |
| Sobre nosotros | Historia y valores de la empresa. |
| Contacto | Formulario de contacto + información directa. |
| FAQs | Preguntas frecuentes sobre envíos, productos y devoluciones. |
| Términos y condiciones | Marco legal del sitio. |
| Política de privacidad | Tratamiento de datos personales. |

---

## 4. Flujo de Compra

```
1. Entrada al sitio
   ↓
2. Validación de edad (modal obligatorio — guarda estado en sesión)
   ↓
3. Home: Ve destacados y CTA
   ↓
4. Catálogo: Busca y filtra productos
   ↓
5. Ficha de producto: Lee detalles, elige tipo (unidad/caja) y cantidad
   ↓
6. Agregar al carrito (confirmación visual inmediata con HTMX)
   ↓
7. Continúa comprando O va al carrito
   ↓
8. Carrito: Revisa items, edita o elimina si necesita
   ↓
9. Checkout:
   - Paso 1: Datos de envío
   - Paso 2: Datos de facturación (opción: igual al envío)
   - Paso 3: Método de pago (Stripe)
   ↓
10. Confirmación: Número de pedido en pantalla
    ↓
11. Email automático con resumen del pedido
```

**Reglas del flujo:**
- La validación de edad ocurre una sola vez por sesión
- El carrito persiste en localStorage (no se pierde al cerrar la pestaña)
- El precio se actualiza automáticamente al cambiar entre unidad y caja
- No se requiere crear cuenta para comprar (guest checkout)

---

## 5. Arquitectura Técnica

### Stack tecnológico

| Capa | Tecnología | Nivel |
|---|---|---|
| Frontend | HTML + CSS + Bootstrap | Conocido |
| Interactividad | HTMX | Nuevo |
| Backend | Python + Django | Conocido |
| API REST | Django REST Framework (DRF) | Nuevo |
| Base de datos | PostgreSQL | Conocido |
| Pagos | Stripe (SDK Python) | Nuevo |
| Email | Django email + SMTP / SendGrid | Nuevo |
| Testing | Pytest + pytest-django | Nuevo |
| Contenedores | Docker | Nuevo |
| Deploy | Railway | Nuevo |
| Control de versiones | Git + GitHub | Conocido |

### Diagrama de arquitectura

```
Navegador del cliente
       │
       ▼
HTML + Bootstrap + HTMX
       │
       ▼
Django (Views + URLs + Templates)
       │
       ├──► Django ORM ──► PostgreSQL
       │
       ├──► DRF (API REST) ──► Endpoints JSON
       │
       ├──► Stripe SDK ──► Pasarela de pago
       │
       └──► SMTP/SendGrid ──► Email de confirmación
```

### Orden de aprendizaje recomendado para tecnologías nuevas
1. **HTMX** — Se usa desde el inicio para el carrito dinámico
2. **DRF** — Se incorpora al construir los endpoints de productos y órdenes
3. **Stripe** — Se integra en el módulo de checkout
4. **Docker** — Se configura al preparar el deploy
5. **Pytest** — Se incorpora progresivamente durante el desarrollo

### Nota sobre React
React se descartó para el MVP deliberadamente. La combinación Django + HTMX ofrece la misma experiencia dinámica con mucho menos complejidad. React queda disponible como opción para la Fase 3 si el negocio lo justifica.

---

## 6. Modelo de Datos (PostgreSQL)

### Entidades principales

**Categoria**
```
id              (PK)
nombre          VARCHAR — ej: "Tabaco rubio", "Tabaco negro", "Orgánico"
descripcion     TEXT
```

**Producto**
```
id              (PK)
nombre          VARCHAR — ej: "Tabaco Virginia Gold"
descripcion     TEXT
imagen          ImageField
precio_unidad   DECIMAL
precio_caja     DECIMAL
unidades_por_caja  INTEGER — ej: 10
stock           INTEGER
activo          BOOLEAN — controla visibilidad en el catálogo
categoria_id    FK → Categoria
```

**Orden**
```
id              (PK)
numero_orden    VARCHAR — ej: "ORD-2026-0001"
cliente_nombre  VARCHAR
cliente_email   EmailField
cliente_telefono VARCHAR
direccion_envio TEXT
estado          ENUM: pendiente / pagado / enviado / entregado
total           DECIMAL
metodo_pago     VARCHAR
fecha_creacion  DateTimeField
fecha_actualizacion DateTimeField
```

**DetallePedido**
```
id              (PK)
orden_id        FK → Orden
producto_id     FK → Producto
tipo_venta      ENUM: unidad / caja
cantidad        INTEGER
precio_unitario DECIMAL — precio histórico al momento de la compra
```

### Diagrama de relaciones
```
Categoria ──< Producto >──< DetallePedido >── Orden
```

**Nota:** `precio_unitario` en DetallePedido guarda el precio al momento de la compra para preservar el historial correcto aunque el precio del producto cambie después.

---

## 7. Validación de Edad y Cumplimiento Normativo

### Pantalla de validación
- Modal obligatorio que aparece antes de cualquier contenido del sitio
- Dos opciones: "Sí, soy mayor de 18" o "No"
- Si responde "No" → redirige a Google u otra página externa
- Si responde "Sí" → se guarda en la sesión Django (no persiste indefinidamente por seguridad legal)

### Requisitos normativos implementados
- Advertencia sanitaria visible en cada producto: *"El tabaco es perjudicial para la salud"*
- Términos y condiciones con cláusula explícita de mayoría de edad
- Política de privacidad (tratamiento de datos del cliente)
- Declaración de no venta a menores en el proceso de checkout
- Restricciones de envío documentadas en FAQs

### Importante
El cumplimiento normativo exacto (leyes de tabaco, restricciones de publicidad, impuestos especiales) varía según el país de operación. Debe validarse con asesoría legal antes del lanzamiento real.

---

## 8. Diseño Visual y Estética

### Paleta de colores
| Rol | Color | Código HEX |
|---|---|---|
| Principal | Negro profundo | `#1A1A1A` |
| Secundario | Dorado/tabaco | `#8B6914` |
| Fondo | Crema suave | `#F5F0E8` |
| Texto | Gris oscuro | `#2C2C2C` |
| CTA / Botones | Rojo vino | `#C0392B` |

### Tipografía
- **Títulos:** Playfair Display (serif, elegante, evoca tradición artesanal)
- **Cuerpo:** Inter (sans-serif, limpia, muy legible)
- Fuente: Google Fonts (gratuitas)

### Principios de diseño
- Mucho espacio en blanco — no saturar la pantalla
- Imágenes de producto sobre fondo claro y bien iluminadas
- Iconografía simple y minimalista
- Botones con esquinas levemente redondeadas
- Transiciones suaves, sin animaciones exageradas
- Mobile-first (responsive con Bootstrap)

### Navegación
```
[ Logo e-Tabaco ]   Inicio | Catálogo | Sobre Nosotros | Contacto   [🛒 (2)]
```
- Header fijo (sticky) visible en todo momento
- Carrito siempre visible con contador de items
- Menú hamburguesa en mobile

### Estructura del Home
```
┌──────────────────────────────────────┐
│  BANNER PRINCIPAL                    │
│  Headline + CTA "Ver Catálogo"       │
├──────────────────────────────────────┤
│  PRODUCTOS DESTACADOS (3-4 items)    │
├──────────────────────────────────────┤
│  SOBRE NOSOTROS (texto breve)        │
├──────────────────────────────────────┤
│  FOOTER: Links | Contacto | Legal    │
└──────────────────────────────────────┘
```

---

## 9. MVP y Evolución por Etapas

### Fase 1 — MVP (6 a 8 semanas)
**Entregable:** Tienda funcional que permite comprar tabaco online

- Validación de mayoría de edad
- Catálogo de productos (tabaco para liar, unidad y caja)
- Ficha de producto con selector de cantidad y tipo
- Carrito de compras funcional con HTMX
- Checkout con datos de envío y pago Stripe
- Email automático de confirmación de pedido
- Django Admin para gestionar productos y pedidos
- Secciones estáticas: Sobre nosotros, Contacto, FAQs
- Diseño responsive con Bootstrap
- Deploy en Railway con Docker

### Fase 2 — Mejoras (4 a 6 semanas adicionales)
- Registro y login de clientes
- Historial de pedidos
- Sistema de descuentos y cupones
- Filtros avanzados en catálogo
- Reseñas de productos
- API REST completa (DRF)
- Dashboard de ventas para el administrador
- Alertas de stock bajo

### Fase 3 — Escala (a definir)
- Frontend con React (si el negocio lo justifica)
- Múltiples marcas o proveedores
- Integración con sistemas de logística
- SEO avanzado y blog
- App móvil (React Native)
- Analytics avanzado

---

## 10. Criterios de Éxito del MVP

- Un cliente puede entrar, validar su edad, navegar el catálogo, agregar productos al carrito y completar una compra sin necesidad de crear una cuenta
- El administrador puede gestionar productos, ver pedidos y actualizar su estado desde Django Admin
- El sitio funciona correctamente en móvil y desktop
- El proceso de pago con Stripe opera en modo test sin errores
- Los emails de confirmación se envían automáticamente al completar una compra
- La validación de edad bloquea el acceso antes de mostrar cualquier contenido

---

*Especificación aprobada por: Ezra*
*Fecha de aprobación: 2026-03-27*
