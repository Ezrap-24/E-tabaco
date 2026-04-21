# 🚀 Inicio Rápido — E-Tabaco Monorepo

**Estado actual:** 📋 Documentación & Planning completados  
**Próxima acción:** Generar diseño visual en Canva  
**Fecha:** 2026-04-20  

---

## ✅ Qué ya está hecho

### 1. ✅ Arquitectura definida (Monorepo)
- 3 instancias Django independientes
- Código compartido en `shared/`
- Decisiones técnicas documentadas

**Archivo:** `docs/PLAN-MIGRACION-MONOREPO.md`

### 2. ✅ README profesional
- Instrucciones de setup
- Cómo correr cada instancia
- Convenciones de desarrollo
- Troubleshooting

**Archivo:** `README.md`

### 3. ✅ Manual de Marca para Puro Tabaco
- Identidad visual completa
- Paleta de colores (5 colores definidos en HEX)
- Tipografía (Georgia + Segoe UI)
- Componentes de UI (botones, cards, etc)
- CSS base listo para implementar

**Archivo:** `docs/BRAND-GUIDE-PUROTABACO.md`

### 4. ✅ Prompt profesional para Canva Design
- Especificación visual detallada
- Todas las secciones de la landing
- Paleta de colores exacta
- Instrucciones de uso y variantes

**Archivo:** `docs/PROMPT-CANVA-PUROTABACO.md`

---

## 🎨 PRÓXIMO PASO: Generar Diseño en Canva

### ¿Qué hacer ahora?

1. Abre **Canva Design:** https://claude.ai/design
2. Copia el prompt completo de: `docs/PROMPT-CANVA-PUROTABACO.md`
3. Pégalo en el chat de Claude
4. Espera a que genere opciones de diseño
5. Selecciona la que más te guste
6. Descarga/exporta el resultado

**Tiempo estimado:** 5-10 minutos

---

## 📂 Estructura de Documentos

```
docs/
├── 00-INICIO-RAPIDO.md           ← TÚ ESTÁS AQUÍ
├── PLAN-MIGRACION-MONOREPO.md    ← Arquitectura técnica
│
├── 🎨 MARCA PURO TABACO (v2.0 - MEJORADA)
├── BRAND-GUIDE-PUROTABACO-v2.md  ← ✅ Manual robusto (USAR ESTE)
├── PROMPT-CANVA-PUROTABACO-v2.md ← ✅ Prompt mejorado (USAR ESTE)
├── RESUMEN-CAMBIOS-v2.md         ← Qué cambió y por qué
│
├── 📚 VERSIÓN ANTERIOR (v1.0 - Para referencia)
├── BRAND-GUIDE-PUROTABACO.md     ← v1.0 (guardar en historia)
└── PROMPT-CANVA-PUROTABACO.md    ← v1.0 (guardar en historia)

(futuro)
├── BRAND-GUIDE-CLUBDELTABACO.md
└── BRAND-GUIDE-ZONATABACO.md
```

---

## 🎯 Línea de tiempo estimada

| Fase | Qué | Tiempo | Estado |
|------|-----|--------|--------|
| **1. Planning** | Decisiones, documentación | ✅ Hecho | COMPLETO |
| **2. Diseño Visual** | Landing page Puro Tabaco en Canva | Hoy | EN PROGRESO |
| **3. Migración código** | Reorganizar a estructura monorepo | 1-2 días | PENDIENTE |
| **4. Implementación** | Crear pages, templates, URLs | 3-5 días | PENDIENTE |
| **5. Deploy local** | Correr 3 instancias en localhost | 1 día | PENDIENTE |
| **6. Producción** | Docker, nginx, dominio real | 1-2 días | PENDIENTE |

**Estimado total:** 2 semanas para Puro Tabaco en producción

---

## 📊 Paleta de Colores Puro Tabaco (para referencia rápida)

```
Negro Profundo     #1A1A1A  ■■■■■■  (Headers, fondos principales)
Oro Clásico        #C4A17A  ■■■■■■  (Acentos, botones)
Crema Marfil       #F4EDE4  ■■■■■■  (Fondos secundarios)
Borgoña Oscuro     #5C2E2E  ■■■■■■  (Botones CTA)
Gris Charcoal      #4A4A4A  ■■■■■■  (Textos secundarios)
```

---

## 🔤 Tipografía (para referencia)

| Uso | Fuente | Peso | Tamaño |
|-----|--------|------|--------|
| Títulos (H1) | Georgia, serif | 700 | 48px |
| Títulos (H2) | Georgia, serif | 700 | 36px |
| Párrafos | Segoe UI, sans | 400 | 16px |
| Botones | Segoe UI, sans | 600 | 14px |

---

## ✏️ Checklist de Próximos Pasos

### Hoy (2026-04-20)
- [ ] Generar diseño en Canva Design (5-10 min)
- [ ] Revisar y hacer feedback (10-15 min)
- [ ] Exportar como PNG (1 min)
- [ ] Guardar proyecto en Canva (1 min)

### Mañana (2026-04-21)
- [ ] Comenzar migración a estructura monorepo
- [ ] Crear directorios shared/, purotabaco/, etc
- [ ] Mover código existente

### Esta semana
- [ ] Crear settings.py para Puro Tabaco
- [ ] Crear urls.py y wsgi.py
- [ ] Implementar Brand Guide (CSS, colores)
- [ ] Crear templates base con marca

### Semana próxima
- [ ] Probar que corre localmente
- [ ] Crear docker-compose.yml
- [ ] Setup de producción

---

## 📚 Documentos importantes

**Para entender la arquitectura:**
→ `docs/PLAN-MIGRACION-MONOREPO.md`

**Para implementar el diseño:**
→ `docs/BRAND-GUIDE-PUROTABACO.md`

**Para generar landing en Canva:**
→ `docs/PROMPT-CANVA-PUROTABACO.md`

**Para instrucciones de desarrollo:**
→ `README.md`

---

## 💡 Tips

1. **Brand Guide es tu "biblia"** — refiere a él siempre que diseñes
2. **CSS está listo** — copia el archivo `purotabaco-theme.css` en `static/css/`
3. **Colores en HEX exactos** — no redonees #1A1A1A a #1A1A1B
4. **Typography matters** — Georgia en títulos es CLAVE para elegancia
5. **Whitespace es lujo** — no aprietes los elementos

---

## 🆘 Si tienes dudas

- **"¿Cómo sé qué colores usar?"** → Ver `BRAND-GUIDE-PUROTABACO.md` sección "Paleta de Colores"
- **"¿Cómo estructuro la BD?"** → Ver `PLAN-MIGRACION-MONOREPO.md` sección "Decisiones Arquitectónicas"
- **"¿Qué prompt pasarle a Canva?"** → Copiar `PROMPT-CANVA-PUROTABACO.md` completo
- **"¿Cómo corro 3 instancias a la vez?"** → Ver `README.md` sección "Cómo trabajar en cada instancia"

---

## 🎯 Objetivo de hoy

**Generar un diseño visual profesional en Canva que sea:**
✓ Minimalista y elegante
✓ Premium y sofisticado
✓ Fácil de navegar
✓ Con los colores exactos definidos
✓ Listo para implementar en Django

**Tiempo:** 20-30 minutos  
**Responsable:** Tú + Canva AI

---

## 📞 Próxima sesión

Cuando tengas el diseño de Canva, te ayudaré con:
1. Implementación en HTML/CSS
2. Integración en Django
3. Responsive design
4. Optimización

---

**¿Listo para crear el diseño en Canva?** 🚀

