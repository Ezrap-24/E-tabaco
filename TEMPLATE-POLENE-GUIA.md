# Template Polène-Style — Guía de Uso

## 📋 Resumen

He creado `landing-polene-style.html` — un template elegante, minimalista y visual, inspirado en Polène Paris pero con **nuestros colores actuales** intactos.

**Colores usados:**
- `#FF6B35` (naranja primario)
- `#264653` (azul secundario)
- `#2A9D8F` (verde agua - acento)
- `#1A1A1A` (texto oscuro)
- `#F8F9FA` (fondo claro)

---

## 🎨 Estructura del Template

### 1. **HEADER** (Fijo en Top)
```
LA TABAQUERÍA | Categorías | Colección | Sobre Nosotros | 🛒 Carrito | 👤 Login
```
- Navbar sticky con backdrop blur
- Minimalista, limpio, moderno
- Responsive (menú hamburguesa en mobile)

### 2. **HERO ÉPICO** (80vh)
```
Premium Selection
Los Mejores Tabacos Seleccionados
Directamente desde nuestro local a tu puerta...
[EXPLORAR AHORA]
```
- Grande, impactante, visual
- Fondo gradiente suave
- Círculo decorativo (placeholder para imagen)
- CTA claro

### 3. **GALERÍA DE CATEGORÍAS** (Grid 4-col)
```
Nuestras Categorías
├─ Tabacos Granel (125+ opciones)
├─ Papelillos (200+ opciones)
├─ Accesorios (350+ opciones)
└─ Esotéricos (180+ opciones)
```
- Grid responsivo
- Hover effects elegantes
- Overlay de información
- Estilo tipo Polène (imágenes grandes)

### 4. **STORY SECTION** (2-col)
```
[Imagen] | Nuestra Historia
          (texto + CTA)
```
- Lado izquierdo: imagen/placeholder
- Lado derecho: storytelling
- Tono editorial, minimalista
- Sección de identidad

### 5. **FEATURED COLLECTION** (Grid 4-col)
```
Lo Más Vendido
├─ Bristol Caramelo - $4.790 - [Agregar]
├─ Ronson Rainbow - $8.990 - [Agregar]
├─ Flandria Virginia - $7.600 - [Agregar]
└─ Wotofo Vape - $7.490 - [Agregar]
```
- Productos destacados
- Precio visible
- Botón agregar al carrito
- Hover effects

### 6. **NEWSLETTER** (Fondo azul secundario)
```
Ofertas Exclusivas
Suscríbete y recibe 10% descuento...
[Email input] [Suscribir]
Respetamos tu privacidad. 0 spam.
```
- Llamada clara a la acción
- Incentivo (10% descuento)
- Note sobre privacidad

### 7. **MAYORISTAS** (CTA Secundaria)
```
🏢
¿Eres Mayorista?
Ofrecemos precios especiales...
[CONTACTA CON VENTAS]
```
- Discreto pero visible
- Borde azul (diferenciado)
- Ubicación baja (no interfiere con flujo minorista)

### 8. **FOOTER** (4-col)
```
Categorías | Compra | Legal | Contacto
Social Links
Copyright
```
- Completo, bien organizado
- Links a todas las secciones
- Contacto directo

---

## 🖼️ Puntos de Inserción de Imágenes

El template está listo para ser llenado con tus imágenes. Aquí están los placeholders:

| Sección | Ubicación | Placeholder | Recomendación |
|---------|-----------|-------------|----------------|
| **Hero** | `.hero-image` | Círculo gradiente | Foto de producto principal o ambiente |
| **Galería 1** | `.gallery-item-image` | 🚬 | Foto categoría Tabacos |
| **Galería 2** | `.gallery-item-image` | 📄 | Foto categoría Papelillos |
| **Galería 3** | `.gallery-item-image` | 🔥 | Foto categoría Accesorios |
| **Galería 4** | `.gallery-item-image` | 🛠️ | Foto categoría Esotéricos |
| **Story** | `.story-image` | 🏪 | Foto del local físico |
| **Featured 1-4** | `.featured-card-image` | 🚬/📄/etc | Fotos productos reales |

---

## 💻 Cómo Cambiar Placeholders por Imágenes Reales

### Opción 1: Reemplazar directamente en HTML
```html
<!-- Antes -->
<div class="hero-image">🚬</div>

<!-- Después -->
<div class="hero-image" style="background: url('/media/products/hero-hero-tabaco.jpg') center/cover"></div>
```

### Opción 2: Agregar etiqueta img
```html
<div class="hero-image">
    <img src="/media/products/hero-tabaco.jpg" alt="Tabacos Premium">
</div>
```

Necesitarás ajustar CSS:
```css
.hero-image {
    ...
    display: flex; → display: block;
    font-size: 4rem; → height: 400px;
}

.hero-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
```

### Opción 3: Usar en Django Template
```html
<div class="gallery-item-image">
    {% if category.image %}
        <img src="{{ category.image.url }}" alt="{{ category.name }}">
    {% else %}
        {{ category.icon }}
    {% endif %}
</div>
```

---

## 🎯 Características Clave del Template

### Minimalismo (Estilo Polène)
- Mucho espacio en blanco
- Tipografía limpia (Inter)
- Animaciones suaves (0.3s a 0.6s)
- Pocos elementos, mucha respiración

### Visual-Heavy
- Imágenes grandes en hero
- Galería con hover overlay
- Cards con aspectos ratios mantenidos
- Featured products destacados

### Conversión-Friendly
- CTAs claros (botones, links)
- Newsletter visible
- Carrito siempre accesible
- Mayoristas no interfieren

### Responsive
- Header adaptive
- Grids que se ajustan (4-col → 2-col → 1-col)
- Touch targets amplios (48px+)
- Formularios mobile-friendly

---

## 📐 Dimensiones de Imágenes Recomendadas

| Sección | Dimensión | Peso | Notas |
|---------|-----------|------|-------|
| Hero | 1920x1080 (16:9) | <300KB | Full width, puede estar en BG |
| Galería | 400x400 (1:1) | <100KB | Aspect ratio 1:1, zoom on hover |
| Story | 600x750 (4:5) | <150KB | Portrait orientation |
| Featured | 300x350 (6:7) | <80KB | Portrait, product cards |

**Optimización:**
- Usar WebP cuando sea posible
- Lazy-load imágenes bajo the fold
- Compresión máxima sin perder calidad
- Nombres descriptivos: `tabaco-bristol-caramelo.jpg`

---

## 🔧 Personalización Rápida

### Cambiar Colores
Edita `:root` en `<style>`:
```css
:root {
    --primary: #FF6B35;      /* Naranja principal */
    --secondary: #264653;    /* Azul secundario */
    --accent: #2A9D8F;       /* Verde agua */
    --text-dark: #1A1A1A;    /* Texto oscuro */
    --text-light: #666;      /* Texto gris */
}
```

### Cambiar Textos
Busca y reemplaza directamente:
- "Los Mejores Tabacos Seleccionados" → Tu headline
- "Premium Selection" → Tu tagline
- "Nuestra Historia" → Tu story

### Cambiar Links de CTAs
```html
<!-- Hero CTA -->
<a href="/catalogo" class="hero-cta">Explorar Ahora</a>

<!-- Mayoristas CTA -->
<button class="wholesale-btn" onclick="window.location.href='/contacto-mayorista'">
    Contacta con Ventas
</button>
```

---

## 📱 Testing Responsive

Verifica en:
- Desktop (1920px)
- Tablet (768px)
- Mobile (375px)

Key elements to check:
- [ ] Header funciona en todos los tamaños
- [ ] Imágenes se cargan sin deformarse
- [ ] CTAs son clickeables (48px+ height)
- [ ] Texto es legible (16px+ size)
- [ ] Galería adapta grid (4col → 2col → 1col)

---

## 🚀 Próximos Pasos

1. **Sesión fotográfica** (fotos productos, local, etc)
2. **Reemplazar placeholders** con imágenes reales
3. **Integrar en Django templates** (datos dinámicos)
4. **Conectar botones:**
   - "Explorar Ahora" → `/catalogo/`
   - "Agregar al Carrito" → JS add-to-cart
   - "Contacta con Ventas" → `/contacto-mayorista/`
   - "Suscribir" → Newsletter signup
5. **Performance optimization:**
   - Lazy-load images
   - Minify CSS/JS
   - PageSpeed > 90

---

## ✅ Checklist Antes de Publicar

- [ ] Todas las imágenes cargadas
- [ ] Todos los textos editados
- [ ] CTAs linkan a URLs correctas
- [ ] Mobile responsive verificado
- [ ] Footer con contacto correcto
- [ ] Newsletter funciona
- [ ] Colores mantienen identidad
- [ ] Performance optimizado
- [ ] SEO: títulos, meta descriptions
- [ ] Analytics configurado

---

## Conclusión

Este template es:
- ✅ **Elegante y visual** (estilo Polène)
- ✅ **Conversion-focused** (CTAs estratégicos)
- ✅ **Modular** (fácil de llenar con imágenes)
- ✅ **Minimalista** (limpio, sin clutter)
- ✅ **Responsive** (funciona en todos los devices)
- ✅ **Con nuestros colores intactos** (naranja, azul, verde)

**Próximo paso:** Sesión fotográfica y luego integración en Django.

¿Necesitas cambiar algo del design o agregar alguna sección?
