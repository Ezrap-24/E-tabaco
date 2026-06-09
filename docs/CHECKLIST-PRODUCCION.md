# Checklist de Producción — Puro Tabaco

> Panorama final antes de salir a producción real (`purotabaco.cl`).
> Actualizado: 04/06/2026 · Incluye notas de la reunión de hoy.

---

## ✅ Lo que ya está listo

**Funcionalidad (MVP completo)**
- [x] Apps Django: `productos`, `carrito`, `pedidos`, `paginas`, `cuenta`
- [x] Catálogo + ficha de producto
- [x] Carrito (sesiones Django, drawer, agregar/quitar/actualizar)
- [x] Checkout + pago **Stripe** (PaymentIntent en CLP, webhook, email de confirmación)
- [x] Cuentas de usuario (registro, login, dashboard, mis pedidos, dirección)
- [x] Gate de mayoría de edad (fecha de nacimiento + cookie 30 días)
- [x] Páginas: Inicio, Sobre Nosotros, Contacto, FAQ, Términos, Privacidad
- [x] Hero con video + carrusel de banners (optimizados a WebP, fix móvil iOS)
- [x] Sección de trust badges (pago, despacho, envíos, calidad)

**Infraestructura y diseño**
- [x] Docker (`Dockerfile` + `docker-compose.yml`) y `railway.toml` listos
- [x] Brand Guide Puro Tabaco v2 (paleta verde tabaco + B2B mayorista)
- [x] Wireframes, mockups y documentación técnica

---

## 🆕 Cambios de la reunión (hoy) — CONTENIDO

- [ ] **Agregar 2 productos** que faltan al catálogo (cargar en el admin con precio, descripción, stock, foto)
- [ ] **Banners de otras marcas** — generar/incorporar al carrusel del home (seguir `docs/ESPECIFICACIONES-BANNERS.md`: 21:9, centrado, < 400 KB WebP)
- [ ] **Mejorar mensaje de envío ("línea negra" / ticker):**
  - Quitar el texto **"48 hr"**
  - Reemplazar por: **"Si compras antes de las 12:01 PM, el envío es el mismo día"**
  - Agregar: **"Repartimos de lunes a sábado"**
- [ ] **"Herencia"** — reemplazar el placeholder *"Años de tradición"* por **25 años de tradición en la industria** (en Sobre Nosotros y/o Contacto)
- [ ] **Revisar Preguntas Frecuentes (FAQ)** — ajustar respuestas con la info real conversada (horarios, montos de envío, condiciones)

---

## 📋 Datos reales pendientes (reemplazar placeholders)

**Contacto y footer** (`templates/base.html`, `templates/paginas/contacto.html`)
- [ ] Teléfono real (hoy: `+56 9 XXXX XXXX`)
- [ ] Email de contacto real
- [ ] WhatsApp
- [ ] Dirección completa (hoy: "Santiago, Chile")
- [ ] Instagram y Facebook (URLs reales)
- [ ] Horario de atención

**Imágenes**
- [ ] Favicon `.ico` de la marca (hoy usa el PNG del logo)
- [ ] Fotos reales de productos (convención `marca-tipo-peso.jpg`)
- [ ] Reemplazar emojis de categorías del home por imágenes reales

**Legal**
- [ ] Revisar **Términos** con un abogado antes del lanzamiento
- [ ] Verificar cumplimiento normativo tabaco Chile (`docs/NORMAS-VENTA-TABACO-CHILE.md`)

---

## ⚙️ Técnico — antes del deploy

- [ ] **Stripe a modo producción** — cambiar `STRIPE_SECRET_KEY` (de test a live) + clave pública + webhook de producción
- [ ] **Email SMTP real** — configurar servidor de correo para confirmaciones
  - ⚠️ Si usas Gmail, usar una **contraseña de aplicación** de Google, NO tu clave personal
- [ ] **Variables de entorno en Railway** — Stripe, email, `DATABASE_URL`, `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`
- [ ] **Base de datos PostgreSQL** en Railway (hoy el repo trae `db.sqlite3`) — correr migraciones y cargar productos
- [ ] **Archivos estáticos/media** — verificar Whitenoise / storage para fotos de productos en producción
- [ ] **Smoke test completo** — edad gate → catálogo → carrito → checkout → Stripe → email → cuenta

---

## 🔐 Seguridad de la información

**Ya resuelto en el código** (verificado en `etabaco/settings.py`)
- [x] `SECRET_KEY` y todas las claves se leen de variables de entorno (no están en el código)
- [x] `.env` está en `.gitignore` (no se sube al repo)
- [x] `DEBUG=False` por defecto
- [x] Validadores de contraseña de Django activos
- [x] En producción: `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_CONTENT_TYPE_NOSNIFF`, `X_FRAME_OPTIONS=DENY`
- [x] `CSRF_TRUSTED_ORIGINS` configurable por entorno
- [x] Webhook de Stripe con verificación de firma (`STRIPE_WEBHOOK_SECRET`)

**Por reforzar antes de salir a producción**
- [ ] **`SECRET_KEY` nueva y exclusiva de producción** — no reutilizar la de desarrollo
- [x] **Forzar HTTPS / HSTS** — ✅ aplicado en `settings.py` (bloque `if not DEBUG`): `SECURE_SSL_REDIRECT`, `SECURE_PROXY_SSL_HEADER`, `SECURE_HSTS_SECONDS` (1 año) + subdominios + preload, `CSRF_COOKIE_HTTPONLY`. Verificado con `manage.py check --deploy` (sin advertencias de HTTPS/cookies).
- [ ] **Almacenamiento persistente para `/media`** — ⚠️ en Railway el disco es efímero: las fotos que se suban por el admin **se borran en cada redeploy**. Solución: volumen de Railway montado en `/media` **o** object storage (Cloudflare R2 / AWS S3)
- [ ] **Backups automáticos** de la base PostgreSQL
- [ ] **Proteger el panel `/admin`** — superusuario con contraseña fuerte (idealmente URL distinta y/o limitar acceso)
- [ ] **Revisar el historial de git** — confirmar que nunca se subió `.env` ni claves en commits viejos
- [ ] **Cambiar la clave de Gmail** que se compartió en el chat y usar una **contraseña de aplicación** de Google para el SMTP
- [ ] *(Opcional, recomendado)* monitoreo de errores (Sentry) y límite de intentos de login (`django-axes`)

---

## 🖥️ Hosting / Infraestructura de producción

> **Decisión (junio 2026): Railway como host + Cloudflare por delante (DNS, CDN y SSL).**
> Sin lock-in: la app está dockerizada, así que se puede migrar a Render o un VPS más adelante si conviene.

**Host: Railway** — el proyecto ya está preparado para esto:
`Dockerfile` + `railway.toml` + `start.sh` (migraciones → fixtures → collectstatic → gunicorn), con `whitenoise` (estáticos) y `dj-database-url` (PostgreSQL).

Componentes a levantar en Railway:
- [ ] **Servicio web** — deploy desde el repo con el Dockerfile (ya configurado)
- [ ] **PostgreSQL** — agregar el plugin de base de datos (genera `DATABASE_URL` automáticamente)
- [ ] **Volumen para `/media`** — para que las fotos de productos persistan (ver sección de seguridad)
- [ ] **Variables de entorno** en el dashboard: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=purotabaco.cl,www.purotabaco.cl`, `CSRF_TRUSTED_ORIGINS=https://purotabaco.cl,https://www.purotabaco.cl`, claves de Stripe (live), SMTP, `DATABASE_URL` (automática)
- [ ] **Dominio en Railway** — agregar `purotabaco.cl` y `www.purotabaco.cl` como custom domains (Railway te entrega el destino CNAME)
- [ ] **SSL en Railway** — se emite automáticamente; verificar que quede activo
- [ ] **Healthcheck** — ya configurado en `/health/` (`railway.toml`)

### Cloudflare (DNS + CDN + SSL por delante)
- [x] **Dominio `purotabaco.cl` comprado en NIC.cl** ✅
- [ ] **Crear cuenta y agregar el dominio** `purotabaco.cl` en Cloudflare
- [ ] **Cambiar los nameservers en el panel de NIC.cl** a los 2 que indique Cloudflare (la propagación puede tardar de minutos a horas)
- [ ] **Registros DNS** — apuntar `@` y `www` al destino que dio Railway, con el **proxy activado (nube naranja)**
- [ ] ⚠️ **Modo SSL/TLS = "Full (strict)"** — NO usar "Flexible". Con Flexible hay **bucle de redirección** porque la app ya fuerza HTTPS (`SECURE_SSL_REDIRECT`). Railway entrega un certificado válido, así que "Full (strict)" es lo correcto y seguro.
- [ ] **Activar "Always Use HTTPS"** en Cloudflare
- [ ] **Confirmar `CSRF_TRUSTED_ORIGINS` y `ALLOWED_HOSTS`** con el dominio final (ya contemplado en variables de entorno)
- [ ] *(Opcional)* activar caché de estáticos, Brotli y reglas de caché en Cloudflare para acelerar el móvil

> Nota: el host ya estaba decidido a nivel de código (Railway). No falta elegir proveedor, solo **aprovisionarlo**: crear el proyecto, agregar PostgreSQL + volumen, cargar variables, conectar el dominio y poner Cloudflare por delante.

---

## 🚀 Deploy y go-live

- [ ] Deploy en **Railway**
- [ ] Apuntar dominio **purotabaco.cl** al servidor
- [ ] Verificar **SSL/HTTPS** activo
- [ ] Probar flujo completo en el dominio real (desktop **y** móvil)
- [ ] Pago de prueba real en producción con tarjeta verdadera (monto chico)

---

## 🔵 Post-lanzamiento (backlog)

- [ ] Tests con pytest (modelos, carrito, creación de orden) → meta >80%
- [ ] Migración a monorepo (`shared/` + 3 marcas)
- [ ] Diferenciación de marca: Club del Tabaco y Zona Tabaco

---

### Resumen del panorama

| Bloque | Estado |
|--------|--------|
| Funcionalidad del sitio | ✅ Completa |
| Cambios de la reunión (contenido) | 🟡 5 ítems |
| Datos reales / placeholders | 🟡 ~12 ítems |
| Seguridad de la información | 🟡 base ✅ + 7 a reforzar |
| Técnico pre-deploy | 🔴 6 ítems (bloquean go-live) |
| Hosting (Railway + Cloudflare) | 🔴 aprovisionar |
| Deploy y dominio | 🔴 5 ítems |
| Post-lanzamiento | 🔵 Backlog |

**Lo que realmente bloquea salir a producción:** aprovisionar **Railway** (web + PostgreSQL + volumen para `/media`), cargar los productos reales (incl. los 2 nuevos), datos de contacto reales, Stripe en modo live, SMTP real, reforzar HTTPS/HSTS y conectar dominio + SSL. El resto del sitio ya funciona.
