# Implementación del Diseño — Puro Tabaco

**Versión:** 1.0  
**Fecha:** 2026-04-20  
**Estado:** Design completado en Canva, listo para implementación  

---

## 📦 Qué recibiste de Canva

```
docs/design/project/
├── Puro Tabaco Landing.html    ← Archivo principal (READ FIRST)
├── wireframes.html              ← Wireframes interactivos
├── wireframes-print.html        ← Wireframes para imprimir
├── design-canvas.jsx            ← Componente React (referencia)
└── README.md                     ← Instrucciones Canva
```

### Archivo Principal: `Puro Tabaco Landing.html`

**Contiene:**
- ✅ HTML/CSS/JS completo (prototipo)
- ✅ Colores exactos en variables CSS
- ✅ Tipografía Playfair Display + Lora
- ✅ Navegación responsive
- ✅ Todas las secciones del landing
- ✅ Media queries para móvil

**Variables CSS (copia estos valores):**
```css
:root {
  --green:   #30483A;    /* Verde tabaco - header */
  --tan:     #C8B08A;    /* Tabaco claro - acentos */
  --cream:   #EFE6D6;    /* Marfil - fondos */
  --slate:   #3A3A3A;    /* Gris pizarra - textos */
  --bronze:  #8B7355;    /* Bronce - botones CTA */
}
```

---

## 🎯 Cómo Implementar

### Opción A: Usar HTML/CSS como Base (Rápido)

1. **Copia el HTML a Django template:**
   ```bash
   cp docs/design/project/"Puro Tabaco Landing.html" \
      purotabaco/templates/purotabaco/index.html
   ```

2. **Extraer CSS a archivo separado:**
   ```bash
   # El CSS del HTML → purotabaco/static/css/purotabaco.css
   ```

3. **Extraer JavaScript a archivo separado:**
   ```bash
   # El JS del HTML → purotabaco/static/js/purotabaco.js
   ```

4. **Reemplazar paths estáticos:**
   ```django
   <!-- De: <link rel="stylesheet" href="style.css"> -->
   <!-- A: <link rel="stylesheet" href="{% static 'css/purotabaco.css' %}"> -->
   ```

5. **Crear variables Django:**
   ```django
   <!-- Reemplazar datos hardcodeados con variables -->
   <h1>{{ BRAND_NAME }}</h1>  <!-- en lugar de PURO TABACO -->
   ```

**Ventaja:** Rápido, el diseño ya está hecho  
**Desventaja:** Mantener HTML + Django mezclado

---

### Opción B: Recrear en Bootstrap (Recomendado)

1. **Estudiar el HTML** de Canva
2. **Recrear con Bootstrap 5** + variables CSS personalizadas
3. **Mantener estructura limpia** (HTML, CSS, JS separados)
4. **Aplicar los colores y tipografía exacta**

**Ventaja:** Código limpio, mantenible, profesional  
**Desventaja:** Más trabajo inicial

**Estructura recomendada:**
```
purotabaco/
├── templates/purotabaco/
│   ├── base.html              (template base)
│   ├── index.html             (landing)
│   ├── producto.html          (ficha de producto)
│   ├── carrito.html           (carrito)
│   └── checkout.html          (checkout)
├── static/css/
│   ├── purotabaco-theme.css   (variables + overwrites)
│   └── bootstrap-custom.css   (si necesitas tweaks)
└── static/js/
    └── purotabaco.js          (interacciones)
```

---

## 📋 Estructura del Diseño (Secciones)

Basándome en el HTML de Canva, el landing tiene estas secciones:

### 1. HEADER/NAVEGACIÓN (Fixed)
```html
<nav id="nav">
  <logo>PURO TABACO - Est. 1902</logo>
  <links>INICIO | CATÁLOGO | MARCAS | CONTACTO | ACCESO MAYORISTAS</links>
  <cta-button>SOLICITAR CATÁLOGO</cta-button>
</nav>
```

**Estilos:**
- Fondo: Verde #30483A
- Texto: Crema #EFE6D6
- CTA Button: Tan #C8B08A
- Responsive: Hamburger en móvil

---

### 2. HERO SECTION
```html
<hero>
  <titulo>TRADICIÓN QUE MUEVE NEGOCIOS</titulo>
  <descripcion>Desde 1902, conectando empresas confiables con tabaco premium</descripcion>
  <botones>
    <btn-primary>SOLICITAR CATÁLOGO</btn-primary>
    <btn-secondary>VER MARCAS</btn-secondary>
  </botones>
</hero>
```

**Estilos:**
- Fondo: Verde #30483A (o imagen)
- Titulo: Playfair Display 52px, Tan #C8B08A
- Botones: Bronce #8B7355 + Tan border

---

### 3. SOBRE PURO TABACO
```html
<about>
  <titulo>SOBRE PURO TABACO</titulo>
  <descripcion>Mayorista de tabaco premium desde 1902...</descripcion>
  <valores>
    <valor-card>Herencia</valor-card>
    <valor-card>Confianza</valor-card>
    <valor-card>Calidad</valor-card>
    <valor-card>Eficiencia</valor-card>
  </valores>
</about>
```

**Estilos:**
- Fondo: Blanco o Crema #EFE6D6
- Cards: Crema con borde Tan izquierdo

---

### 4. MARCAS LÍDERES
```html
<marcas>
  <titulo>DISTRIBUIDORES CERTIFICADOS DE MARCAS LÍDERES</titulo>
  <logos>
    <logo>Dunhill</logo>
    <logo>Mac Baren</logo>
    <logo>Davidoff</logo>
    <logo>Marlboro</logo>
    <logo>Pueblo</logo>
  </logos>
</marcas>
```

**Estilos:**
- Fondo: Verde oscuro #30483A
- Logos: Blanco o Crema
- Text: Crema #EFE6D6

---

### 5. VENTAJAS MAYORISTA
```html
<ventajas>
  <card>Stock Permanente</card>
  <card>Precios Mayoristas</card>
  <card>Despachos Rápidos</card>
  <card>Atención Personalizada</card>
  <card>Garantía Autenticidad</card>
</ventajas>
```

**Estilos:**
- Fondo: Crema #EFE6D6
- Cards: Crema con borde Tan izquierdo
- Iconos: Tan o Slate

---

### 6. CÓMO COMPRAR
```html
<como-comprar>
  <paso>1. SELECCIONA - Explora catálogo</paso>
  <paso>2. COMPRA - Carrito simple</paso>
  <paso>3. RECIBE - Despacho rápido</paso>
</como-comprar>
```

**Estilos:**
- Fondo: Blanco
- Números grandes: Bronze #8B7355
- Líneas divisoras: Tan #C8B08A

---

### 7. CTA FINAL
```html
<cta-final>
  <titulo>¿LISTO PARA LLEVAR TU NEGOCIO AL SIGUIENTE NIVEL?</titulo>
  <boton>SOLICITAR ACCESO MAYORISTA</boton>
  <whatsapp>+56 9 1234 5678</whatsapp>
</cta-final>
```

**Estilos:**
- Fondo: Verde #30483A
- Texto: Crema #EFE6D6
- Botón: Bronze #8B7355

---

### 8. FOOTER
```html
<footer>
  <links>Sobre Nosotros | Catálogo | Contacto | Términos</links>
  <redes>Instagram | Facebook | LinkedIn</redes>
  <copyright>© 2026 Puro Tabaco</copyright>
</footer>
```

**Estilos:**
- Fondo: Verde muy oscuro #243830 o #1a2b22
- Texto: Crema #EFE6D6
- Acentos: Tan #C8B08A

---

## 🔧 Pasos de Implementación

### 1. Setup Inicial
```bash
cd /sessions/lucid-keen-cannon/mnt/e-Tabaco

# Leer el HTML de Canva
cat docs/design/project/"Puro Tabaco Landing.html"

# Ver wireframes
open docs/design/project/wireframes.html
```

### 2. Crear estructura Django
```bash
# Crear templates
mkdir -p purotabaco/templates/purotabaco

# Crear static files
mkdir -p purotabaco/static/css
mkdir -p purotabaco/static/js
mkdir -p purotabaco/static/img
```

### 3. Crear base template
**purotabaco/templates/purotabaco/base.html:**
```django
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PURO TABACO — Mayorista de Tabaco Premium</title>
    
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/purotabaco-theme.css' %}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% include 'purotabaco/components/header.html' %}
    
    {% block content %}{% endblock %}
    
    {% include 'purotabaco/components/footer.html' %}
    
    <script src="{% static 'js/purotabaco.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### 4. Copiar CSS y variables
**purotabaco/static/css/purotabaco-theme.css:**
```css
:root {
  --green:   #30483A;
  --green-d: #243830;
  --tan:     #C8B08A;
  --cream:   #EFE6D6;
  --slate:   #3A3A3A;
  --bronze:  #8B7355;
}

body {
  font-family: 'Lora', Georgia, serif;
  color: var(--slate);
  background: var(--white);
}

h1, h2, h3, h4 {
  font-family: 'Playfair Display', Georgia, serif;
}

/* Copiar todo el CSS del HTML de Canva */
```

### 5. Implementar componentes
```
purotabaco/templates/purotabaco/components/
├── header.html
├── hero.html
├── about.html
├── marcas.html
├── ventajas.html
├── cta.html
└── footer.html
```

### 6. Crear landing.html
```django
{% extends 'purotabaco/base.html' %}
{% load static %}

{% block content %}
    {% include 'purotabaco/components/hero.html' %}
    {% include 'purotabaco/components/about.html' %}
    {% include 'purotabaco/components/marcas.html' %}
    {% include 'purotabaco/components/ventajas.html' %}
    {% include 'purotabaco/components/cta.html' %}
{% endblock %}
```

---

## ✅ Checklist de Implementación

### Diseño Visual
- [ ] Colores exactos implementados (5 colores principales)
- [ ] Tipografía Playfair Display cargada
- [ ] Tipografía Lora cargada
- [ ] Logo con "EST. 1902" visible
- [ ] Navegación responsive (hamburger en móvil)
- [ ] Hover effects en botones y links
- [ ] Media queries para móvil/tablet/desktop

### Secciones
- [ ] Header/Navegación
- [ ] Hero Section
- [ ] Sobre Puro Tabaco
- [ ] Marcas Líderes
- [ ] Ventajas Mayorista
- [ ] Cómo Comprar
- [ ] CTA Final
- [ ] Footer

### Responsive
- [ ] Móvil (320px)
- [ ] Tablet (768px)
- [ ] Desktop (1024px+)
- [ ] Imágenes optimizadas
- [ ] Touch targets > 44px

### Funcionalidad
- [ ] Links de navegación funcionan
- [ ] Botones CTAs funcionan
- [ ] WhatsApp link correcto
- [ ] Formularios (si aplica)
- [ ] Scroll smooth
- [ ] No errores en consola

---

## 🚀 Próximos Pasos

1. ✅ Diseño completado en Canva
2. ✅ Archivos exportados a `/docs/design/`
3. 📋 **Implementar en Django** (próximo)
4. 🧪 Probar responsive
5. ✔️ Validar con Brand Guide
6. 🚀 Deploy

---

## 📞 Referencia Rápida

- **Archivo principal:** `docs/design/project/Puro Tabaco Landing.html`
- **Colores:** Variables CSS en el HTML
- **Tipografía:** Playfair Display (titles) + Lora (body)
- **Brand Guide:** `docs/BRAND-GUIDE-PUROTABACO-v2.md`
- **Flujo de compra:** `docs/FLUJO-CARRITO-CHECKOUT.md`

---

**Status:** Diseño completado, listo para implementación  
**Próxima acción:** Comenzar implementación en Django  
**Última actualización:** 2026-04-20
