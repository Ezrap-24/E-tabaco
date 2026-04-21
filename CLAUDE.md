# Memoria de trabajo — e-Tabaco

## El proyecto

**e-Tabaco** es una tienda e-commerce para una empresa tabaquera que vende tabaco en paquetes. El objetivo es armar un sitio profesional con catálogo, carrito de compras y checkout, orientado tanto a venta minorista como mayorista.

Stack: **Django + PostgreSQL + Bootstrap + JavaScript**

## Estado actual (2026-03-31)

- Estructura base de Django lista (apps, config, requirements)
- Propuesta de dominio documentada (`docs/propuesta-nombres-dominio.md`)
- Deck de presentación para el cliente listo (`propuesta-dominio-tabaqueria.pptx`)
- **Próximo hito: sesión fotográfica en el local (2026-03-31)**

## Páginas planificadas

| Sección | Estado |
|---------|--------|
| Inicio (landing) | Pendiente |
| Catálogo | Pendiente |
| Ficha de producto | Pendiente |
| Carrito | Pendiente |
| Checkout | Pendiente |
| Sobre la empresa | Pendiente |
| Contacto | Pendiente |
| FAQ | Pendiente |
| Gate de mayoría de edad | Pendiente |

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