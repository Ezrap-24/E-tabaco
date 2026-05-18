# Tasks — e-Tabaco

> **🗓 Deadline: Viernes 15 de mayo de 2026**
> Proyecto principal activo: **Puro Tabaco** (purotabaco.cl) — MVP funcional, entregar versión desplegada y con datos reales.

---

## 🔴 Crítico (debe estar antes del viernes)

- [ ] **Cargar productos reales al admin de Django** — Ingresar SKUs con precio, descripción, marca y stock. Depende de tener las fotos y el catálogo definido.
- [ ] **Subir y organizar fotos de productos** — Renombrar según convención `marca-tipo-peso.jpg`, guardar en `/media/products/`. *(Sesiones de fotos: 31-mar y 02-abr — verificar si se hizo)*
- [ ] **CSS de marca Puro Tabaco** — Aplicar paleta Brand Guide v2 (verde tabaco #30483A + tabaco claro #C8B08A + marfil #EFE6D6). Actualmente usa Bootstrap genérico.
- [ ] **Deploy en Railway** — Docker listo. Configurar variables de entorno en Railway (Stripe, email SMTP, DB). Primera marca: purotabaco.cl.
- [ ] **Smoke test completo del flujo** — Verificar de extremo a extremo: edad gate → catálogo → carrito → checkout → Stripe → email confirmación → cuenta.

## 🟡 Importante (si hay tiempo antes del viernes)

- [ ] **Optimizar experiencia móvil** — Revisar todo el flujo en celular. Bootstrap cubre lo básico pero hay que revisar el carrito drawer y checkout.
- [ ] **Tests críticos con pytest** — Al menos cubrir: modelos de producto, lógica de carrito, y creación de orden. Cobertura parcial ya existe.
- [ ] **Revisar normativa tabaco en Chile** — Verificar que el gate de edad, los avisos y el flujo cumplen `docs/NORMAS-VENTA-TABACO-CHILE.md`.

## 🔵 Backlog post-entrega

- [ ] **Migración a monorepo** — Arquitectura shared/ + clubdeltabaco/ + purotabaco/ + zonatabaco/ (ver `docs/PLAN-MIGRACION-MONOREPO.md`)
- [ ] **Diferenciación CSS marca Club del Tabaco** — Pendiente definición de identidad
- [ ] **Diferenciación CSS marca Zona Tabaco** — Pendiente definición de identidad
- [ ] **HTMX en templates** — Verificar si está integrado o sigue siendo JS vanilla
- [ ] **Tests completos** — Cobertura mayor al 80% con pytest

---

## ✅ Completadas

- [x] **Propuesta inicial de dominio** — Nombres evaluados (`docs/propuesta-nombres-dominio.md`)
- [x] **Presentación de propuesta (.pptx)** — Deck para el cliente
- [x] **Estructura base del proyecto Django** — Apps, configuración, requirements
- [x] **App `productos`** — Modelos, views, templates (catálogo + ficha de producto)
- [x] **App `carrito`** — Sesiones Django, agregar/quitar/actualizar, drawer
- [x] **App `pedidos`** — Checkout, Stripe PaymentIntent CLP, webhook, email de confirmación
- [x] **App `paginas`** — Home, sobre nosotros, contacto, FAQ, términos, privacidad
- [x] **App `cuenta`** — Login, registro, dashboard, mis pedidos, dirección, cambio de contraseña
- [x] **Gate de mayoría de edad** — Verificación por fecha de nacimiento + cookie 30 días
- [x] **Docker** — Dockerfile + docker-compose.yml listos
- [x] **Brand Guide Puro Tabaco v2** — Paleta, tipografía, posicionamiento B2B
- [x] **Wireframes y mockups** — Disponibles en `docs/design/`
- [x] **Documentación técnica** — Flujo carrito/checkout, normativa, arquitectura monorepo
