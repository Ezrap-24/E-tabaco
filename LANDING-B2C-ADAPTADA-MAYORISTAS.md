# Landing B2C Adaptada con Opción Mayoristas

## Resumen de Cambios

He adaptado la landing `landing-mockup.html` para mantener **foco 100% minorista (B2C)** pero agregando una **sección secundaria discreta para mayoristas** que no interfiere con el flujo principal.

**Resultado:** Una landing que vende agresivamente a minoristas, pero que también abre la puerta a mayoristas sin distraer.

---

## Estructura Final del Landing

```
1. Header (sticky)
2. Hero + CTAs claros (COMPRAR AHORA, VER CATÁLOGO)
3. Categorías Grid (4 categorías, 125+ a 350+ productos)
4. Ofertas del Día (carrusel, precios, badges -20%)
5. Value Props (3 pillars: Envío, Garantía, Pagos)
6. [NUEVO] Sección Mayoristas (discreta, secundaria) ← CAMBIO PRINCIPAL
7. Newsletter (10% descuento, suscripción)
8. Footer (links, contacto, redes)
```

---

## Cambio Principal: Sección Mayoristas

### Ubicación
**Justo después de Value Props (sección 5) y antes de Newsletter (sección 6)**

```html
<!-- MAYORISTAS (SECONDARY CTA) -->
<section class="wholesale">
    <div class="wholesale-content">
        <div class="wholesale-icon">🏢</div>
        <h2>¿Eres Mayorista o Distribuidor?</h2>
        <p>Ofrecemos precios especiales y condiciones adaptadas para negocios, 
           distribuidoras, locales, hoteles y gastronomía. Acceso directo a 
           nuestro equipo de ventas B2B.</p>
        <button class="btn-secondary-outline">Contacta con Ventas →</button>
    </div>
</section>
```

### Diseño de la Sección

**Visual:**
- Fondo gris muy claro (`#f5f5f5` → `#fafafa` gradient) — Diferente al resto
- Caja blanca centrada con borde izquierdo azul (#264653) — Marca como "secundaria"
- Ícono grande: 🏢 (edificio/empresa)
- Tipografía clara pero no invasiva

**Funcionalmente:**
- No compite con minorista (colores diferentes, ubicación baja)
- CTA claro pero discreto (botón outline azul, no naranja)
- Mensaje directo: "Si eres mayorista, aquí estamos"

### Estilos CSS Añadidos

```css
/* MAYORISTAS (SECONDARY CTA) */
.wholesale {
    padding: 4rem 2rem;
    background: linear-gradient(135deg, #f5f5f5 0%, #fafafa 100%);
    text-align: center;
}

.wholesale-content {
    max-width: 700px;
    margin: 0 auto;
    padding: 3rem;
    background: white;
    border-radius: 12px;
    border-left: 4px solid var(--secondary);  /* Borde azul = secundario */
}

.wholesale-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.wholesale h2 {
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: var(--text-dark);
}

.wholesale p {
    font-size: 1rem;
    color: var(--text-light);
    margin-bottom: 1.5rem;
    line-height: 1.7;
}

.btn-secondary-outline {
    padding: 0.9rem 2rem;
    border: 2px solid var(--secondary);      /* Azul = diferente al primario */
    background: white;
    color: var(--secondary);
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.btn-secondary-outline:hover {
    background: var(--secondary);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(38, 70, 83, 0.2);
}
```

**Clave:** El borde azul `border-left: 4px solid` marca visualmente que es una sección diferente, secundaria.

---

## Flujo de Usuario: Comparación

### Minorista (Flujo Principal)
```
Entra
  ↓ (ve hero con CTAs claros)
Elige categoría o producto
  ↓ (compra rápida)
Checkout
  ↓
Éxito
```

### Mayorista (Flujo Secundario)
```
Entra como minorista
  ↓ (scrollea viendo todo el contenido B2C)
Llega a sección "¿Eres Mayorista?"
  ↓ (se siente identificado)
Clickea "Contacta con Ventas"
  ↓ (va a formulario de contact o WhatsApp)
Equipo de ventas toma control
```

**Ventaja:** No interrumpe el flujo minorista. Solo aparece cuando el usuario ya vio todo lo demás.

---

## Archivos Generados

| Archivo | Propósito |
|---------|-----------|
| `landing-b2c-minorista.html` | **PRINCIPAL** — Landing adaptada con sección mayoristas |
| `landing-mockup.html` | Original (mantenido para referencia) |
| `LANDING-PAGE-MODERNA-PROPUESTA.md` | Especificaciones originales |
| `ANALISIS-COMPARATIVO-LANDING.md` | Análisis vs landing anterior |

**Recomendación:** Usa `landing-b2c-minorista.html` como la versión oficial.

---

## Integración en Django

### Opción A: Reemplazar Home Actual

```python
# e_tabaco/apps/pages/views.py

def home(request):
    # Datos dinámicos para la landing
    categories = Category.objects.all()[:4]
    featured_products = Product.objects.filter(featured=True)[:4]
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'paginas/landing-b2c-minorista.html', context)
```

```html
<!-- templates/paginas/landing-b2c-minorista.html -->
<!-- Guardar landing-b2c-minorista.html aquí y adaptar dinámicamente -->

<!-- CATEGORÍAS (dinámicas) -->
<section class="categories" id="categorias">
    <h2 class="section-title">Nuestras Categorías</h2>
    <div class="categories-grid">
        {% for category in categories %}
        <div class="category-card">
            <div class="category-icon">{{ category.icon }}</div>
            <h3>{{ category.name }}</h3>
            <p>{{ category.description }}</p>
            <div class="category-count">{{ category.product_count }}+ opciones</div>
        </div>
        {% endfor %}
    </div>
</section>

<!-- OFERTAS (dinámicas) -->
<section class="top-products" id="ofertas">
    <h2 class="section-title">Ofertas del Día</h2>
    <div class="products-grid">
        {% for product in featured_products %}
        <div class="product-card">
            <div class="product-image">
                <img src="{{ product.image.url }}" alt="{{ product.name }}">
                {% if product.discount %}
                <div class="product-badge">-{{ product.discount }}%</div>
                {% endif %}
            </div>
            <div class="product-info">
                <div class="product-brand">{{ product.brand }}</div>
                <div class="product-name">{{ product.name }}</div>
                <div class="product-price">
                    {% if product.original_price %}
                    <span class="original">${{ product.original_price }}</span>
                    {% endif %}
                    ${{ product.price }}
                </div>
                <button class="btn-sm" onclick="addToCart({{ product.id }})">
                    Agregar
                </button>
            </div>
        </div>
        {% endfor %}
    </div>
</section>

<!-- MAYORISTAS: Botón dinámico a contacto -->
<section class="wholesale">
    <div class="wholesale-content">
        <div class="wholesale-icon">🏢</div>
        <h2>¿Eres Mayorista o Distribuidor?</h2>
        <p>Ofrecemos precios especiales y condiciones adaptadas para negocios, 
           distribuidoras, locales, hoteles y gastronomía. Acceso directo a 
           nuestro equipo de ventas B2B.</p>
        <a href="{% url 'pages:contact' %}?ref=wholesale" class="btn-secondary-outline">
            Contacta con Ventas →
        </a>
    </div>
</section>
```

### Opción B: Mantener Separadas (Recomendado)

Si aún tienes la landing anterior como mayorista pura:

```
/                          → landing-b2c-minorista.html (nueva)
/mayorista/                → home.html actual (la antigua)
/contacto-mayorista/       → formulario especializado
```

```python
# urls.py
path('', views.home_b2c, name='home'),              # Nueva landing minorista
path('mayorista/', views.home_mayorista, name='home_mayorista'),  # Landing antigua B2B
path('contacto-mayorista/', views.contact_mayorista, name='contact_mayorista'),
```

**Ventaja:** Puedes A/B test. Medir qué landing convierte más.

---

## Flujo del Botón "Contacta con Ventas"

El botón debe redirigir a uno de estos:

### Opción 1: Formulario de Contacto (Recomendado)
```html
<a href="{% url 'pages:contact' %}?ref=wholesale" class="btn-secondary-outline">
    Contacta con Ventas →
</a>
```

En el formulario, pre-llenar:
- Campo "Asunto": "Consulta mayorista"
- Mostrar campos extras: "Tipo de negocio", "Volumen estimado"

### Opción 2: WhatsApp Directo
```html
<a href="https://wa.me/56950895853?text=Hola, soy mayorista y quisiera consultar precios" 
   class="btn-secondary-outline" target="_blank">
    Contacta con Ventas →
</a>
```

### Opción 3: Email Pre-redactado
```html
<a href="mailto:mayoristas@latabaqueria.cl?subject=Consulta%20Mayorista" 
   class="btn-secondary-outline">
    Contacta con Ventas →
</a>
```

---

## Próximos Pasos

### Inmediatos (Esta semana)
1. ✅ Review de landing-b2c-minorista.html en navegador
2. ✅ Feedback visual: ¿La sección mayorista está bien equilibrada?
3. ✅ Decidir: ¿Reemplazar home.html o mantener dos versiones?

### Corto plazo (Próximas 2 semanas)
1. Integrar en Django (templates dinámicos con categorías, productos reales)
2. Conectar botones:
   - "Comprar Ahora" → Catálogo
   - "Ver Catálogo" → Catálogo
   - "Agregar" → Carrito
   - "Contacta con Ventas" → Formulario B2B
3. Optimizar imágenes (lazy-load, tamaños responsivos)
4. Testing mobile (iPhone, Android)

### Mediano plazo (Mes 1-2)
1. A/B Testing: Landing minorista vs antigua mayorista
2. Métricas:
   - CTR por botón
   - Bounce rate
   - Conversion rate (compra vs contacto mayorista)
3. Refinar basado en datos

---

## Checklist Visual

Cuando veás la landing en el navegador, verifica:

### Landing Minorista (Secciones 1-5, 7-8)
- [ ] Hero atractivo con CTAs claros
- [ ] Categorías en grid 4-col, hover effects
- [ ] Productos con badges de descuento
- [ ] Value props claras (Envío, Garantía, Pagos)
- [ ] Newsletter signup visible
- [ ] Footer con contacto

### Sección Mayoristas (Sección 6)
- [ ] Aparece después de Value Props
- [ ] Caja blanca con borde azul (marca como secundaria)
- [ ] Ícono 🏢 visible
- [ ] Texto claro pero breve (máx 3 líneas)
- [ ] Botón blue outline (diferente al orange primario)
- [ ] No interfiere con flujo minorista

### Responsive (Mobile)
- [ ] Header sticky funciona
- [ ] Categorías en 2-col en mobile
- [ ] Productos en 2-col en mobile
- [ ] Botones tocan bien (48px mín)
- [ ] Sección mayoristas legible en mobile

---

## Diferencia vs Landing Anterior

| Aspecto | Anterior (home.html) | Nueva (landing-b2c-minorista.html) |
|---------|----------------------|--------------------------------------|
| **Público** | Mayorista puro | Minorista + opción mayorista |
| **Tipografía** | Serif (formal) | Sans-serif (moderno) |
| **Colores** | Marrón/tostado | Naranja/blanco/azul |
| **Estructura** | Editorial larga | Funnel comprimido |
| **CTAs** | 1 (solicitar mayorista) | 5+ (comprar, categorías, etc) |
| **Categorías** | No visible | Grid 4-col |
| **Ofertas** | No | Carrusel visible |
| **Value Props** | 6 cards B2B | 3 pillars simples |
| **Mayoristas** | Enfoque principal | Opción secundaria |
| **Mobile** | Denso | Optimizado |

---

## Conclusión

La landing está lista para:
1. **Vender minorista agresivamente** (categorías, ofertas, urgencia)
2. **Captar mayoristas sutilmente** (sección discreta, CTA clara)
3. **Mantener enfoque visual** (no compiten, colores diferentes)

**Recomendación final:** Usa `landing-b2c-minorista.html` como landing principal. Integra con Django. Mide conversión. Optimiza.

Si necesitas ajustes en la sección mayoristas (mensaje, ubicación, diseño), avísame.
