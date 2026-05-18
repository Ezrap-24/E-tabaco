# Memoria de trabajo — e-Tabaco

## El proyecto

**e-Tabaco** es una tienda e-commerce para una empresa tabaquera que vende tabaco en paquetes. El objetivo es armar un sitio profesional con catálogo, carrito de compras y checkout, orientado tanto a venta minorista como mayorista.

Stack: **Django + PostgreSQL + Bootstrap + JavaScript**

## Estado actual (2026-04-27)

**El MVP está prácticamente completo.** El proyecto evolucionó de 1 tienda a 3 marcas en monorepo.

- Apps Django implementadas: `productos`, `carrito`, `pedidos`, `paginas`, `cuenta`
- Stripe integrado (PaymentIntent en CLP, webhook, email de confirmación)
- Sistema de cuentas completo (registro, login, perfil, historial de pedidos)
- Docker listo (`Dockerfile` + `docker-compose.yml`)
- Brand Guide Puro Tabaco v2 completo (paleta verde tabaco + B2B mayorista)
- Wireframes y mockups de diseño disponibles en `docs/design/`

## Páginas

| Sección | Estado |
|---------|--------|
| Inicio (landing) | ✅ Implementado |
| Catálogo | ✅ Implementado |
| Ficha de producto | ✅ Implementado |
| Carrito | ✅ Implementado (sesiones Django) |
| Checkout + Pago Stripe | ✅ Implementado |
| Confirmación de pedido | ✅ Implementado |
| Sobre la empresa | ✅ Implementado |
| Contacto | ✅ Implementado |
| FAQ | ✅ Implementado |
| Términos y Privacidad | ✅ Implementado |
| Gate de mayoría de edad | ✅ Implementado (fecha nacimiento + cookie 30 días) |
| Mi cuenta (dashboard, pedidos, dirección) | ✅ Implementado |

## Arquitectura objetivo: Monorepo 3 marcas

Ver `docs/PLAN-MIGRACION-MONOREPO.md`

| Dominio | Marca | Estado |
|---------|-------|--------|
| purotabaco.cl | Puro Tabaco (Premium / B2B) | Brand guide listo, código base listo |
| clubdeltabaco.cl | Club del Tabaco | Pendiente diferenciación |
| zonatabaco.cl | Zona Tabaco | Pendiente diferenciación |

## Próximos hitos

1. Migración a monorepo (`shared/` + 3 instancias Django)
2. CSS personalizado por marca (usar Brand Guide v2)
3. Deploy en Railway
4. Tests completos con pytest
5. Fotos reales de productos

## Decisiones técnicas acordadas

- Validación de mayoría de edad: modal en entrada al sitio
- Imágenes de productos: convención `marca-tipo-peso.jpg`, guardadas en `/media/products/`
- Carrito: implementado con sesiones de Django

## Flujo de trabajo recomendado

1. `/brainstorming` — antes de diseñar cualquier feature nueva
2. `/writing-plans` — para planificar implementación antes de codificar
3. `/executing-plans` — para ejecutar paso a paso
4. `/verification-before-completion` — antes de marcar algo como hecho

## Skills disponibles

| Comando | Cuándo usarlo |
|---------|---------------|
| `/brainstorming` | **Antes de cualquier trabajo creativo** — diseño de features, componentes, flujos |
| `/writing-plans` | Crear un plan de implementación antes de codificar |
| `/executing-plans` | Ejecutar un plan paso a paso |
| `/test-driven-development` | Cuando vayas a escribir código con tests |
| `/systematic-debugging` | Para depurar errores de forma estructurada |
| `/requesting-code-review` | Antes de hacer merge o push |
| `/receiving-code-review` | Al recibir feedback de un code review |
| `/subagent-driven-development` | Para tareas grandes que se pueden paralelizar |
| `/dispatching-parallel-agents` | Ejecutar múltiples agentes en paralelo |
| `/using-git-worktrees` | Trabajar en ramas aisladas con worktrees |
| `/finishing-a-development-branch` | Cerrar una rama de desarrollo limpiamente |
| `/verification-before-completion` | Verificar antes de marcar una tarea como hecha |
| `/using-superpowers` | Integrar herramientas externas (Codex, Gemini, etc.) |
| `/writing-skills` | Crear o mejorar skills de agente |

## Agentes custom

- **code-reviewer** — revisor de código especializado, definido en `.agents/agents/code-reviewer.md`

# Token Efficient Rules

1. Think before acting. Read existing files before writing code.
2. Be concise in output but thorough in reasoning.
3. Prefer editing over rewriting whole files.
4. Do not re-read files you have already read unless the file may have changed.
5. Test your code before declaring done.
6. No sycophantic openers or closing fluff.
7. Keep solutions simple and direct.
8. User instructions always override this file.