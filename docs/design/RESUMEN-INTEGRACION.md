# Integración de Diseño Canva al Proyecto

**Status:** Diseño completado y listo para implementar  
**Fecha:** 2026-04-20  
**Próxima acción:** Implementar en Django  

---

## ✅ Lo que ya está hecho

- ✅ Diseño generado en Canva Design
- ✅ Archivos exportados a `/docs/design/project/`
- ✅ README.md actualizado con referencias al diseño
- ✅ Documentación de implementación creada
- ✅ Estructura Django lista para recibir templates

---

## 📂 Archivos de Diseño

```
docs/design/
├── project/
│   ├── Puro Tabaco Landing.html     ← ARCHIVO PRINCIPAL
│   ├── wireframes.html
│   ├── wireframes-print.html
│   ├── design-canvas.jsx
│   └── README.md
├── IMPLEMENTACION-DESIGN.md         ← Guía de integración
├── RESUMEN-INTEGRACION.md           ← Este archivo
└── README.md                        ← Original de Canva
```

---

## 🎯 Próximos Pasos (Orden)

### 1️⃣ LEER EL DISEÑO (10 minutos)

```bash
# Abre y lee el archivo HTML principal
cat docs/design/project/"Puro Tabaco Landing.html"

# O en navegador (si tienes acceso local)
open docs/design/project/"Puro Tabaco Landing.html"
```

**Qué buscar:**
- Estructura HTML
- Variables CSS (colores exactos)
- Secciones principales
- Responsive breakpoints

---

### 2️⃣ IMPLEMENTAR TEMPLATES (2-3 días)

**Crear estructura:**

```bash
# 1. Crear carpeta de templates
mkdir -p purotabaco/templates/purotabaco/components

# 2. Crear base template
touch purotabaco/templates/purotabaco/base.html

# 3. Crear componentes
touch purotabaco/templates/purotabaco/components/header.html
touch purotabaco/templates/purotabaco/components/hero.html
touch purotabaco/templates/purotabaco/components/about.html
touch purotabaco/templates/purotabaco/components/marcas.html
touch purotabaco/templates/purotabaco/components/ventajas.html
touch purotabaco/templates/purotabaco/components/cta.html
touch purotabaco/templates/purotabaco/components/footer.html

# 4. Crear landing
touch purotabaco/templates/purotabaco/index.html
```

**Copiar CSS:**

```bash
# 1. Crear carpeta CSS
mkdir -p purotabaco/static/css

# 2. Crear archivo de tema (copiar variables del HTML de Canva)
touch purotabaco/static/css/purotabaco-theme.css
```

**Copiar JS:**

```bash
# 1. Crear carpeta JS
mkdir -p purotabaco/static/js

# 2. Copiar funciones del HTML de Canva
touch purotabaco/static/js/purotabaco.js
```

---

### 3️⃣ GUÍA RÁPIDA POR SECCIÓN

Lee `docs/design/IMPLEMENTACION-DESIGN.md` que contiene:
- ✅ Estructura de cada sección
- ✅ Estilos CSS específicos
- ✅ Clases y estructura HTML
- ✅ Variables de color y tipografía
- ✅ Checklist de implementación

---

## 🎨 Referencia de Colores

Copia estos valores exactos del HTML de Canva a tu CSS:

```css
:root {
  --green:   #30483A;    /* Verde tabaco - principal */
  --green-d: #243830;    /* Verde oscuro - footer */
  --tan:     #C8B08A;    /* Tabaco claro - acentos */
  --cream:   #EFE6D6;    /* Marfil - fondos */
  --slate:   #3A3A3A;    /* Gris - textos */
  --bronze:  #8B7355;    /* Bronce - botones */
  --white:   #FDFAF5;    /* Off-white */
}
```

---

## 🔤 Tipografía

```html
<!-- Agregar a <head> -->
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,900;1,400;1,700&family=Lora:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
```

```css
/* En CSS */
.playfair { font-family: 'Playfair Display', Georgia, serif; }
.lora { font-family: 'Lora', Georgia, serif; }

body { font-family: 'Lora', Georgia, serif; }
h1, h2, h3, h4, h5, h6 { font-family: 'Playfair Display', Georgia, serif; }
```

---

## 📋 Checklist de Implementación

### [ ] Estructura Base
- [ ] Base template creado
- [ ] Componentes divididos en archivos separados
- [ ] CSS separado del HTML
- [ ] JS separado del HTML

### [ ] Estilos
- [ ] Variables CSS importadas
- [ ] Playfair Display cargada
- [ ] Lora cargada
- [ ] Colores exactos aplicados
- [ ] Media queries (móvil, tablet, desktop)

### [ ] Secciones
- [ ] Header/Navegación
- [ ] Hero
- [ ] Sobre Puro Tabaco
- [ ] Marcas Líderes
- [ ] Ventajas
- [ ] Cómo Comprar
- [ ] CTA Final
- [ ] Footer

### [ ] Responsive
- [ ] Hamburger menu en móvil
- [ ] Imágenes responsive
- [ ] Grid responsive
- [ ] Touch targets > 44px

### [ ] Funcionalidad
- [ ] Links de navegación funcionan
- [ ] Botones sin errores
- [ ] WhatsApp link funciona
- [ ] Scroll smooth
- [ ] Sin errores en consola

### [ ] Integración Django
- [ ] {% static %} usado correctamente
- [ ] {% load static %} en templates
- [ ] Variables Django (si aplica)
- [ ] Collected static files

---

## 🚀 Comandos Útiles

```bash
# Ver el HTML de Canva
cat docs/design/project/"Puro Tabaco Landing.html" | head -100

# Crear carpetas de un tiro
mkdir -p purotabaco/templates/purotabaco/components
mkdir -p purotabaco/static/{css,js,img}

# Ejecutar servidor Django
export DJANGO_SETTINGS_MODULE=purotabaco.settings
python manage.py runserver

# Verificar archivos static
python manage.py collectstatic --noinput

# Ver estructura creada
tree purotabaco/ -I '__pycache__'
```

---

## 📚 Documentación Relacionada

| Documento | Para |
|-----------|------|
| `docs/BRAND-GUIDE-PUROTABACO-v2.md` | Referencia de marca (colores, tipografía, componentes) |
| `docs/FLUJO-CARRITO-CHECKOUT.md` | Flujo de compra (no está en el landing, será después) |
| `docs/NORMAS-VENTA-TABACO-CHILE.md` | Requerimientos legales (validación edad, etc) |
| `docs/design/IMPLEMENTACION-DESIGN.md` | Detalles técnicos de cada sección |
| `README.md` | Overview del proyecto |

---

## ⚠️ Puntos Críticos

1. **Colores exactos:** #30483A (NO aproximado)
2. **Tipografía:** PLAYFAIR DISPLAY para títulos (NO Georgia)
3. **Responsive:** Probar en 320px, 768px, 1024px+
4. **Static files:** Usar {% static %} en Django
5. **Funcionalidad:** Sin errores en consola del navegador

---

## 🎯 Resultado Final

Después de implementar tendrás:

```
purotabaco/
├── templates/purotabaco/
│   ├── base.html              ✅ Template base
│   ├── index.html             ✅ Landing
│   └── components/
│       ├── header.html        ✅ Navegación
│       ├── hero.html          ✅ Hero section
│       ├── about.html         ✅ Sobre nosotros
│       ├── marcas.html        ✅ Marcas líderes
│       ├── ventajas.html      ✅ Ventajas
│       ├── cta.html           ✅ CTA final
│       └── footer.html        ✅ Footer
│
├── static/css/
│   ├── purotabaco-theme.css   ✅ Variables + overwrites
│   └── bootstrap-custom.css   ✅ Si necesitas tweaks
│
└── static/js/
    └── purotabaco.js          ✅ Interacciones
```

---

## 📞 Si tienes dudas

**Pregunta:** ¿Cómo extraigo CSS del HTML de Canva?  
**Respuesta:** Copia todo lo que está entre `<style>` y `</style>`

**Pregunta:** ¿Cómo hago que funcione en Django?  
**Respuesta:** Reemplaza rutas de CSS/JS con `{% static %}`

**Pregunta:** ¿Dónde pongo el contenido dinámico?  
**Respuesta:** En variables Django: `{{ nombre_variable }}`

---

## ✨ Estado del Proyecto

```
✅ Arquitectura definida (Monorepo)
✅ Brand Guide completado (v2.0)
✅ Diseño visual completado (Canva)
✅ Documentación de integración lista
⏳ Implementación en Django (próximo - 2-3 días)
⏳ Testing responsive (1 día)
⏳ Deploy local (1 día)
```

---

**Listo para implementar** 🚀

Próxima acción: Leer `docs/design/IMPLEMENTACION-DESIGN.md` y comenzar con templates Django.

**Última actualización:** 2026-04-20
