# Análisis Técnico: Smoke Jokers (smokejokers.com)

## Resumen Ejecutivo

**Smoke Jokers** es una tabaquería online chilena con presencia física. Su plataforma está construida sobre **WordPress + WooCommerce**, un stack maduro, probado y fácil de escalar. Es una arquitectura comercial pragmática que prioriza conversión sobre innovación técnica.

---

## Stack Tecnológico Detectado

### Backend & CMS
- **WordPress 6.9.4** — CMS estándar de industria (2 de cada 3 sitios web)
- **WooCommerce 10.5.3** — Plugin de ecommerce número uno para WordPress
- **Base de datos** — Presumiblemente MySQL/MariaDB (estándar en hosting compartido)
- **Servidor** — Hosting tradicional (no detectable sin acceso a cabeceras HTTP)

### Frontend
- **jQuery 3.7.1** — Librería de manipulación DOM (legacy pero funcional)
- **Bootstrap CSS** — Framework responsive (base de componentes UI)
- **Tema personalizado** — `smoke_jokers` (tema propio, no un tema genérico)
- **Librerías de animación:**
  - TweenMax (animaciones JavaScript)
  - Three.js (renderización 3D básica — probablemente para backgrounds)
  - Swiper.js (carruseles/sliders)
  - Animate.css (transiciones CSS)
  - ImagesLoaded (precarga de imágenes)

### Plugins Instalados
| Plugin | Función |
|--------|---------|
| **WooCommerce** | Carrito, checkout, gestión de productos |
| **WooCommerce Memberships** | Programa de suscripción "Ser un Joker" |
| **WooCommerce All Products for Subscriptions** | Integraciones de suscripciones |
| **WC Pickup Store** | Gestión de puntos de retiro |
| **Age Gate** | Validación de mayoría de edad (✓ Obligatorio en tabacaleras) |
| **Google Tag Manager** | Analytics y seguimiento de conversiones |
| **Google Analytics** | Métricas de tráfico |
| **Facebook Pixel** | Retargeting y conversiones en Facebook |
| **Mailchimp for WordPress** | Newsletter y email marketing |
| **Mabel Wheel of Fortune** | Gamificación (rueda de premios) |
| **Brevo SDK** | Email automation (alternativa a Mailchimp) |
| **Metricool** | Social media analytics |

### Integraciones Externas
- **Google Tag Manager (GTM)** — Dos instancias (GTM-MFB2KMF, GTM-MR9W2426)
- **Google Analytics** — Seguimiento de usuarios
- **Facebook Pixel** — Publicidad retargeting
- **Brevo (Sendinblue)** — Email marketing
- **Mailchimp** — Email automation
- **Metricool** — Análisis de redes sociales

### CSS y Estilos
- **Google Fonts** — Poppins (300, 400, 600, 700 weights)
- **Font Awesome 4.7** — Iconografía
- **Magnific Popup** — Modales/lightboxes
- **Swiper.css** — Estilos de carruseles

---

## Arquitectura de Funcionalidades

### 1. **Validación de Edad** ✓
```
Gate Gate Plugin v3.7.2 → Modal en entrada al sitio
Obligatorio antes de acceder al catálogo
```
**Lección para e-Tabaco:** Es la opción estándar. Implementa un modal similar.

### 2. **Modelo de Negocio**

**A. Venta Minorista**
- Carrito de compra tradicional
- Checkout WooCommerce
- Despacho a domicilio (1-3 días hábiles)
- Puntos de retiro asociados (sin costo de envío)

**B. Membresía "Ser un Joker"**
- Suscripción $2.490/mes
- Descuentos tiered (10-15%) en categorías
- Gestión con WooCommerce Memberships
- Tabla de beneficios clara

**C. Venta a Empresas**
- Canal separado (menciona "contacto")
- Probablemente órdenes grandes, términos especiales

**Lección para e-Tabaco:** Considera modelo de suscripción desde el MVP. Es recurrente y aumenta LTV.

### 3. **Catálogo**
| Categoría | Subcategorías |
|-----------|---------------|
| Tabacos | ~8 marca/tipos |
| Puros y Puritos | ~9 marcas |
| Artículos Varios | ~14 (incluyendo cannabis/cultivo) |
| Narguiles | ~1 |
| E-Liquids | Listado completo |

Estructura jerárquica 3 niveles: Categoría → Subcategoría → Producto

**Lección para e-Tabaco:** Necesitas jerarquía de categorías clara. WooCommerce lo soporta nativamente.

### 4. **Ficha de Producto**
- Imagen principal + variaciones
- Descripción (probablemente con especificaciones)
- Precio (con descuentos si es miembro)
- Stock visible
- Botón "Agregar al carrito"
- Posiblemente reviews (no visible en screenshot, pero WooCommerce lo soporta)

### 5. **Carrito y Checkout**
- Carrito flotante en esquina superior derecha
- Muestra items + subtotal
- Link "Ver carrito" (página de carrito completa)
- Checkout probablemente con opciones de envío y pago

**Métodos de envío observados:**
- Despacho a domicilio
- Retiro en punto asociado

---

## Decisiones Arquitectónicas Clave

### ✓ Por qué WordPress/WooCommerce

1. **Velocidad de mercado** — Sitio funcional en semanas, no meses
2. **Bajo costo inicial** — Hosting compartido $20-50/mes suficiente
3. **Escalabilidad pragmática** — Soporta 100+ productos sin problemas
4. **Plugin ecosystem** — Membresías, puntos de retiro, age gate listos
5. **SEO out-of-box** — WordPress es SEO-friendly por defecto
6. **Tema personalizado** — No generic, pero usando base de Bootstrap

### ✗ Limitaciones observadas

1. **JavaScript legacy** — jQuery en 2026 es... funcional pero no moderno
2. **3D experimental** — Three.js cargado (backgrounds 3D), pero uso limited
3. **Sin API REST separada** — Probablemente REST API de WordPress, pero no app mobile
4. **Análisis fragmentado** — 4+ herramientas de analytics (GTM, GA, Facebook, Metricool)

---

## Detalles de Implementación

### Estructura de URLs
```
/categoria/tabaco/           → Listado de categoría
/producto/[nombre-slug]/     → Ficha de producto
/carrito/                    → Página del carrito
/checkout/                   → Página de checkout
/mi-cuenta/                  → Mi cuenta (login/pedidos)
/ser-un-joker/               → Página de membresía
/marcas/                     → Directorio de marcas
```

### SEO y Analytics
- **Meta tags completos** — OG:image, OG:description, etc.
- **Google Site Verification** — Integración con GSC
- **Robots meta** — index, follow (no bloqueos de crawl)
- **Structured data** — Probablemente schema.org para productos (WooCommerce lo genera)

### Performance Observado
- Página carga sin lentitud aparente
- Imágenes optimizadas
- Assets minificados (js.min.js, css.min.css)
- Lazy loading implied (por imagesloaded.js)

---

## Elementos Faltantes o No Detectados

1. **App mobile** — No hay mención. Posiblemente solo web responsive.
2. **Métodos de pago** — No visible en screenshot, pero WooCommerce integra Mercado Pago, PayPal, transferencia bancaria.
3. **Sistema de reviews** — No visible, pero WooCommerce lo soporta.
4. **Chat o soporte en vivo** — No detectado.
5. **Blog/contenido** — No visible en homepage, pero WordPress lo permite.

---

## Recomendaciones para e-Tabaco

### Copiar (porque funciona)
1. **WordPress + WooCommerce** — No reinventar la rueda. Estándar de industria.
2. **Age Gate en entrada** — Obligatorio, Smoke Jokers lo hace bien.
3. **Modelo de membresía** — Aumenta LTV y engagement.
4. **Puntos de retiro** — Si tienes físicas, integra con WooCommerce.
5. **GTM + GA + Facebook Pixel** — Seguimiento de conversiones standard.

### Mejorar (porque tu stack es diferente)
1. **Frontend moderno** — Django + Vue/React es más robusto que WordPress + jQuery.
2. **API REST nativa** — Django REST Framework > WordPress API.
3. **Control de datos** — PostgreSQL tuyo > compartido hosting.
4. **Escalabilidad a la medida** — Django crece con tus 3 ecommerce.

### Evitar
1. **Múltiples herramientas de analytics** — Elige GTM o GA, no ambas.
2. **jQuery para lógica compleja** — Tu frontend moderno es ventaja competitiva.
3. **Tema genérico** — Smoke Jokers pagó por tema personalizado, hazlo bien.

---

## Conclusión

**Smoke Jokers es un ecommerce sólido, profesional y orientado a conversión.** Usa la stack estándar de la industria, sin experimentar. Es la opción correcta para una tabaquería.

Tu decisión de usar Django + PostgreSQL es más ambiziosa, pero te da:
- **Control total** sobre el monorepo de 3 ecommerce
- **Escalabilidad diferenciada** para cada marca
- **Frontend moderno** (vs jQuery)
- **API REST** para futuras integraciones

**La pregunta no es "¿Por qué no WordPress?"** — es "¿Necesito control y escalabilidad para 3 marcas independientes?" Si la respuesta es sí (que lo es), Django es la elección correcta. Solo asegúrate de invertir en:

1. Validación de edad robusto (como Smoke Jokers)
2. Sistema de membresía desde MVP
3. Google Tag Manager para analytics

Smoke Jokers prueba que el problema no es técnico — es comercial. Tu stack es más sofisticado, úsalo a tu favor.
