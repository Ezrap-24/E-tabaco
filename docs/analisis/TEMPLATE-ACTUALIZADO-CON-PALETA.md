# Template Polène-Style — Actualizado con Paleta Oficial

## ✅ Cambio Realizado

He actualizado `landing-polene-style.html` con **la paleta de colores oficial** de PURO TABACO y las fuentes correctas.

**Antes:** Colores genéricos (naranja #FF6B35, azul #264653)  
**Ahora:** Paleta oficial premium (verde tabaco, bronce, marfil)

---

## 🎨 Paleta Oficial Aplicada

### Colores Primarios
```
Verde Tabaco        #30483A  → Headers, secciones principales, newsletter
Bronce Envejecido   #8B7355  → CTAs, botones, acentos principales
Tabaco Claro        #C8808A  → Acentos cálidos, hover states
Marfil Vintage      #EFE6D6  → Fondos claros, secciones secundarias
Gris Pizarra        #343A3A  → Textos, cuerpo
```

### Tipografía
```
Playfair Display    → Títulos (H1, H2, H3) - Heritage + Autoridad
Lora                → Cuerpo de texto - Profesional, legible
```

---

## 📐 Mapa de Colores por Sección

| Sección | Color Primario | Color Secundario | Efecto |
|---------|---|---|---|
| **Header** | Verde Tabaco #30483A | Bronce #8B7355 (hover) | Logo bronce, nav links con hover |
| **Hero** | Fondo claro | Bronce CTA | Headline grande, botón bronce |
| **Galería** | Marfil #EFE6D6 | Bronce (tags) | Cards limpias, overlay elegante |
| **Story** | Blanco | Verde Tabaco | Imagen lado izquierdo, copy derecha |
| **Featured** | Blanco | Bronce botones | Cards producto con CTA bronce |
| **Newsletter** | Verde Tabaco #30483A | Bronce botón | Contraste alto, CTA clara |
| **Mayoristas** | Marfil #EFE6D6 | Verde Tabaco borde | Caja discreta pero visible |
| **Footer** | Gris Pizarra #343A3A | Bronce (hover) | Links profesionales |

---

## 🎯 Decisiones de Diseño

### Por qué Bronce para CTAs
El bronce envejecido (#8B7355) es:
- Premium y sofisticado (lujo)
- Cálido y confiable (tabaco)
- Diferenciado (no naranja genérico)
- Elegante sin ser frío

### Por qué Verde Tabaco para Fondos
El verde tabaco (#30483A) es:
- Identidad de la marca (tabaquería premium)
- Sofisticado y premium
- Profesional sin ser corporativo
- Diferenciado en el mercado

### Por qué Marfil para Luz
El marfil vintage (#EFE6D6) es:
- Cálido, no blanco frío
- Premium y vintage
- Contrasta bien con texto oscuro
- Complementa verde y bronce

---

## 📝 Tipografía en Detalle

### Playfair Display (Google Fonts)
```css
font-family: 'Playfair Display', Georgia, serif;
font-weight: 700, 800;
```
**Usos:**
- H1 (hero): 5rem, weight 800
- H2 (secciones): 2.5rem, weight 800
- H3 (cards): 1.3rem, weight 700
- Logo: Playfair Display, weight 700

**Efecto:** Elegancia, autoridad, herencia

### Lora (Google Fonts)
```css
font-family: 'Lora', Georgia, serif;
font-weight: 400, 600, 700;
```
**Usos:**
- Body: 1rem, weight 400
- Acentos: weight 600, 700
- Line-height: 1.6-1.9

**Efecto:** Legibilidad, profesionalismo, warmth

---

## 🔗 Estructura con Colores

```
┌─────────────────────────────────────────────────┐
│  HEADER (Verde Tabaco)                          │
│  Logo Bronce | Nav links | Cart | Login         │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  HERO (Blanco/Marfil)                           │
│  Premium Selection                              │
│  Headline Grande (Playfair Display)             │
│  [Botón Bronce]                                 │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  GALERÍA (Marfil)                               │
│  Nuestras Categorías (tag Bronce)               │
│  [Cards blancas con hover, overlay]             │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  STORY (Blanco)                                 │
│  [Imagen Verde] | Nuestra Historia              │
│                   [CTA outline Verde]           │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  FEATURED (Blanco)                              │
│  Lo Más Vendido (tag Bronce)                    │
│  [Cards producto] [Botón Bronce]                │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  NEWSLETTER (Verde Tabaco)                      │
│  Email input | Botón Bronce                     │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  MAYORISTAS (Marfil)                            │
│  Caja blanca | Borde Verde | Botón Verde       │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  FOOTER (Gris Pizarra)                          │
│  Links | Social | Copyright                     │
└─────────────────────────────────────────────────┘
```

---

## 🎨 Paleta Expandida (Para Futuros Usos)

```
Paleta PURO TABACO
├─ Verde Tabaco      #30483A  (Primary, Heritage)
├─ Bronce Envejecido #8B7355  (CTA, Warmth)
├─ Tabaco Claro      #C8808A  (Accent warm)
├─ Marfil Vintage    #EFE6D6  (Light BG)
└─ Gris Pizarra      #343A3A  (Text)

Derivados (Hover States, Gradients)
├─ Verde Tabaco Dark  #1a2f25  (Dark hover)
├─ Bronce Light       #a8937a  (Light accent)
└─ Marfil Oscuro      #ddd3c0  (Subtle dividers)
```

---

## ✨ Diferenciadores del Design

### vs Competencia Genérica
- ❌ Colores corporativos (azul, rojo, naranja)
- ✅ Paleta premium tabaquera (verde, bronce)

### vs Competencia Premium
- ❌ Diseño estático, sin movimiento
- ✅ Hover effects elegantes, transiciones suaves

### vs Diseño Editorial
- ❌ Mucho texto, poco visual
- ✅ Galería visual, imagenes grandes, espacios blancos

---

## 📱 Responsive con Paleta

El template mantiene la paleta en todos los breakpoints:

```css
@media (max-width: 768px) {
    /* Colores se mantienen igual */
    /* Solo layout se adapta */
}
```

**Esto significa:**
- Mobile: mismo Verde Tabaco, Bronce, Marfil
- Tablet: mismo color scheme
- Desktop: mismo color scheme

Sin perder identidad en ningún device.

---

## 🖼️ Puntos de Inserción de Imágenes (Sin Cambios)

Los placeholders siguen en los mismos lugares, ahora con mejor contexto visual:

| Sección | Elemento | Color Fondo | Nota |
|---------|----------|-------------|------|
| Hero | `.hero-image` | Gradiente Verde-Tabaco | Debajo del texto |
| Galería | `.gallery-item-image` | Marfil | 4 cards |
| Story | `.story-image` | Gradiente Verde-Tabaco | Lado izquierdo |
| Featured | `.featured-card-image` | Marfil | 4 cards |

**Recomendación:** Fotos con fondo natural (madera, ambiente) combinan bien con verde y bronce.

---

## 🔨 Cómo Usar Este Template

### 1. Visualizar
Abre `landing-polene-style.html` en navegador. Verás:
- Colores oficiales (verde, bronce, marfil)
- Tipografía Playfair Display + Lora
- Layout elegante tipo Polène
- Responsive design

### 2. Personalizar Textos
Busca y reemplaza:
- "Los Mejores Tabacos Seleccionados" → Tu headline
- "Nuestra Historia" → Título real
- Textos de categorías, featured, etc.

### 3. Agregar Imágenes
Cambia placeholders (emojis) por fotos reales:
```html
<!-- Antes -->
<div class="hero-image">🚬</div>

<!-- Después -->
<div class="hero-image" style="background: url('/media/hero.jpg') center/cover"></div>
```

### 4. Integrar en Django
```python
# views.py
def home(request):
    categories = Category.objects.all()
    featured = Product.objects.filter(featured=True)
    return render(request, 'landing-polene-style.html', {
        'categories': categories,
        'featured_products': featured,
    })
```

### 5. Testing
- [ ] Colores coinciden con paleta oficial
- [ ] Fuentes (Playfair Display + Lora) cargan
- [ ] Responsive en mobile/tablet/desktop
- [ ] Botones funcionan (hover, click)
- [ ] Imágenes cargan sin lag

---

## 📦 Archivos Finales

| Archivo | Propósito |
|---------|-----------|
| `landing-polene-style.html` | **PRINCIPAL** — Template con paleta oficial |
| `TEMPLATE-ACTUALIZADO-CON-PALETA.md` | Esta guía |
| `TEMPLATE-POLENE-GUIA.md` | Guía original (referencia) |

---

## 🎯 Resumen de Cambios vs. Versión Anterior

```diff
- Colores: Naranja #FF6B35 → Verde Tabaco #30483A
- Tipografía: Inter → Lora + Playfair Display
- Acentos: Azul #264653 → Bronce #8B7355
- Backgrounds: Gris claro → Marfil #EFE6D6
- Identidad: Genérica → Premium Tabaquera
```

---

## ✅ Próximos Pasos

1. **Validar Colores** — ¿Coinciden exactamente con tu paleta de referencia?
2. **Sesión Fotográfica** — Fotos de productos, local, ambientes
3. **Integración Django** — Conectar datos dinámicos
4. **Performance** — Optimizar imágenes, lazy-load
5. **Testing** — Mobile, velocidad, conversión

¿Hay algo que quieras ajustar en los colores, tipografía o estructura?
