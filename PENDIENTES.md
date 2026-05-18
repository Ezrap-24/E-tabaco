# Pendientes — Puro Tabaco

## Datos reales para reemplazar

### Footer y página de contacto
- [ ] **Teléfono** — reemplazar `+56 9 XXXX XXXX` en `templates/base.html` (footer) y `templates/paginas/contacto.html`
- [ ] **Email** — reemplazar `contacto@purotabaco.cl` en `templates/paginas/contacto.html`
- [ ] **WhatsApp** — reemplazar número en `templates/paginas/contacto.html`
- [ ] **Dirección** — reemplazar `Santiago, Chile` por la dirección completa en `templates/paginas/contacto.html` y footer
- [ ] **Instagram** — agregar URL real del perfil en footer y contacto
- [ ] **Facebook** — agregar URL real del perfil en footer y contacto
- [ ] **Horario de atención** — agregar en footer (ej: Lun–Vie 9:00–18:00)

### Imágenes
- [ ] **Favicon** — reemplazar con versión .ico de la marca (actualmente usa el PNG del logo)
- [ ] **Banners del slider (home)** — preparar 5 imágenes para el carrusel principal:
  - Tamaño recomendado: **1920 × 900 px** (relación 16:5), formato JPG o WebP
  - Guardar en `/static/img/banners/banner-01.jpg` … `banner-05.jpg`
  - Definir el **enlace (href)** de cada banner (ej: catálogo, oferta, contacto mayorista)
  - Definir **título y subtítulo** opcionales por slide (o dejar solo imagen)
  - Mientras no haya imágenes reales, el slider muestra fondos de color de marca
- [ ] **Categorías en home** — reemplazar emojis por imágenes reales de productos cuando estén disponibles
- [ ] **Productos** — subir fotos reales desde `/static/img/Fotos Productos/` al admin de Django

### Contenido
- [ ] **Ticker** — actualizar mensajes con monto real del envío gratis y datos reales de la empresa
- [ ] **Sobre Nosotros / Contacto** — reemplazar "Años de tradición" por el número real de años
- [ ] **FAQ** — revisar y ajustar respuestas con información real (horarios, montos, condiciones)
- [ ] **Términos** — revisar con un abogado antes del lanzamiento real

### Técnico (antes del deploy)
- [ ] **Variables de entorno Railway** — configurar en el dashboard de Railway
- [ ] **Stripe** — cambiar de modo test a producción (clave `STRIPE_SECRET_KEY`)
- [ ] **Email SMTP** — configurar servidor de email real para las confirmaciones de pedido
- [ ] **Dominio** — apuntar `purotabaco.cl` al servidor de Railway
- [ ] **SSL** — verificar que el certificado HTTPS quede activo

---
*Archivo generado el 13/05/2026 — actualizar a medida que se completan los puntos.*
