# Manual de Marca — Puro Tabaco (v2.0)

**Versión:** 2.0 — Versión Robusta  
**Fecha:** 2026-04-20  
**Dominio:** purotabaco.cl  
**Posicionamiento:** Premium / B2B Mayorista  

---

## 🎯 Identidad de Marca (MEJORADA)

### Propósito
**Puro Tabaco es la conexión moderna con la tradición tabacalera mundial.** Somos una mayorista premium que conecta a Chile con las mejores marcas de tabaco desde 1902 (legado histórico). Nos dirigimos a negocios, distribuidores y clientes confiables que valoran la excelencia, la tradición y las relaciones a largo plazo.

### Narrativa clave
> **"Tradición que mueve negocios"**

Conectamos el legado tabacalero de Londres 1900 con el comercio mayorista moderno. Cada producto cuenta historias de generaciones, y cada relación es construida en confianza.

### Valores
- **Tradición:** 120+ años de herencia tabacalera
- **Calidad:** Productos de excelencia bajo altos estándares
- **Confianza:** Relaciones a largo plazo, transparencia y compromiso
- **Eficiencia:** Despachos rápidos, precios competitivos
- **Experiencia:** Conocimiento profundo del sector

### Tono de Voz
- Profesional pero cercano
- Directo y confiable
- Que respete la historia sin ser arcaico
- Que inspire confianza en negocios
- Palabra clave: **Herencia profesional**

---

## 🎨 Identidad Visual (NUEVA PALETA)

### Paleta de Colores Primaria

```
┌─────────────────────────────────────────┐
│ COLOR PRIMARIO: Verde Tabaco            │
│ HEX: #30483A                            │
│ RGB: 48, 72, 58                         │
│ PANTONE: 18-0430 (Hunter Green)         │
│ Uso: Headers, fondos principales       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ COLOR SECUNDARIO: Tabaco Claro          │
│ HEX: #C8B08A                            │
│ RGB: 200, 176, 138                      │
│ PANTONE: 15-1021 (Tan Brown)            │
│ Uso: Acentos, detalles, bordes         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ COLOR TERCIARIO: Marfil Vintage         │
│ HEX: #EFE6D6                            │
│ RGB: 239, 230, 214                      │
│ PANTONE: 11-0605 (Cream)                │
│ Uso: Fondos secundarios, tarjetas      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ COLOR ACENTO: Gris Pizarra              │
│ HEX: #3A3A3A                            │
│ RGB: 58, 58, 58                         │
│ PANTONE: 19-0303 (Dark Gray)            │
│ Uso: Textos, bordes, elementos fuertes │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ COLOR ENFASIS: Bronce Envejecido        │
│ HEX: #8B7355                            │
│ RGB: 139, 115, 85                       │
│ PANTONE: 18-1141 (Bronze)               │
│ Uso: Botones CTA, highlights premium   │
└─────────────────────────────────────────┘
```

### Aplicación de Colores

**Header/Footer:** Verde tabaco (#30483A)
**Acentos principales:** Tabaco claro (#C8B08A)
**Fondos:** Marfil vintage (#EFE6D6) o blanco
**Textos:** Gris pizarra (#3A3A3A) para títulos, gris más claro para body
**Botones CTA:** Bronce envejecido (#8B7355) con texto tabaco claro
**Líneas divisoras:** Tabaco claro (#C8B08A)

### Ejemplo de uso

```html
<!-- Header -->
<header style="background-color: #30483A; color: #EFE6D6;">
    <h1>Puro Tabaco</h1>
    <p>Mayorista de Tabaco Premium</p>
</header>

<!-- Botón CTA -->
<button style="background-color: #8B7355; color: #EFE6D6; border: 2px solid #C8B08A;">
    Solicitar Catálogo
</button>

<!-- Card de producto -->
<div style="background-color: #EFE6D6; border-left: 4px solid #C8B08A;">
    <h3 style="color: #3A3A3A;">Marca Premium</h3>
    <p style="color: #666;">Descripción y detalles...</p>
</div>

<!-- Línea divisora -->
<hr style="border: none; border-top: 2px solid #C8B08A;">
```

---

## 🔤 Tipografía (MEJORADA)

### Tipografía Primaria (Títulos y Headings)
**Nombre:** Playfair Display  
**Fallback:** Georgia, serif  
**Pesos:** 400 (regular), 700 (bold)  
**Tamaños:**
- H1: 52px / 60px (bold)
- H2: 40px / 48px (bold)
- H3: 32px / 38px (bold)
- H4: 24px / 30px (regular/bold)

**Uso:** Títulos de página, nombres de marcas, encabezados principales  
**Personalidad:** Clásica, elegante, histórica, atemporal

```html
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap');
    
    h1, h2, h3, h4 {
        font-family: 'Playfair Display', Georgia, serif;
        font-weight: 700;
        letter-spacing: 1px;
        color: #3A3A3A;
    }
    
    h1 { font-size: 52px; line-height: 60px; }
    h2 { font-size: 40px; line-height: 48px; }
    h3 { font-size: 32px; line-height: 38px; }
</style>
```

### Tipografía Secundaria (Body y UI)
**Nombre:** Lora  
**Fallback:** 'Segoe UI', Tahoma, sans-serif  
**Pesos:** 400 (regular), 600 (semi-bold)  
**Tamaños:**
- Body: 16px / 26px (regular)
- Descripción: 14px / 22px (regular)
- Pequeño: 12px / 18px (regular)
- Button: 14px / 18px (600 semi-bold)

**Uso:** Textos de descripción, párrafos, UI, botones  
**Personalidad:** Clásica, legible, con carácter

```html
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;600&display=swap');
    
    body {
        font-family: 'Lora', Georgia, serif;
        font-size: 16px;
        line-height: 26px;
        color: #3A3A3A;
    }
    
    .description {
        font-size: 14px;
        line-height: 22px;
        color: #666;
    }
    
    button {
        font-family: 'Lora', Georgia, serif;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
</style>
```

---

## 🎭 Logo y Sistema de Identidad

### Logo Histórico (Marca de Autoridad)

```
┌────────────────────┐
│  EST.              │
│     [P]            │  ← Escudo geométrico clásico
│  1902              │
│                    │
│  PURO TABACO       │
│  MAYORISTA         │
└────────────────────┘
```

**Variantes:**
- Versión horizontal: Logo + Texto a lado
- Versión solo icono: Solo el escudo (para favicon, app)
- Versión sello: Circular con "Est. 1902"

### Sistema Visual

- **Iconos:** Líneas finas, estilo vintage minimalista
- **Líneas y divisores:** Tabaco claro (#C8B08A), grosor 2px
- **Detalles clásicos:** Pequeños ornamentos, pero sin exceso
- **Sombras:** Muy sutiles (box-shadow: 0 2px 6px rgba(0,0,0,0.08))
- **Esquinas:** Border-radius: 2px (casi rectas, muy clásico)

---

## 🖼️ Estilo Visual

### Fotografía y Moodboard
- **Estilo:** Fotografía vintage/clásica con toque moderno
- **Referencia:** Londres años 1900-1920, carros de tabaco, tiendas históricas
- **Colores:** Tonalidades cálidas, sepia ligera, no saturado
- **Elementos:** Tabaco enrollado, marquillas, cajas vintage, herramientas
- **Tono:** Nostálgico pero profesional, histórico pero accesible

### Fotografía de Productos
- Fondo: Marfil (#EFE6D6) o neutro
- Iluminación: Suave, profesional, estilo vintage
- Ángulos: Frontal con detalle (mostrar textura)
- Presentación: Productos con packaging visible

---

## 📑 Estructura de Página (MEJORADA)

### Header Ejecutivo
```
┌──────────────────────────────────────────────────────┐
│  [PT Logo] PURO TABACO          [INICIO] [CATÁLOGO]  │
│            MAYORISTA DE TABACO  [MARCAS] [CONTACTO]  │
│                                 [ACCESO MAYORISTAS]   │
└──────────────────────────────────────────────────────┘
```

### Hero Section (Narrativa Histórica)
```
┌─────────────────────────────────────────────────┐
│ [Imagen vintage: Big Ben + carro de tabaco]    │
│                                                │
│ TRADICIÓN QUE MUEVE NEGOCIOS                  │
│                                                │
│ Desde 1902, conectando empresas               │
│ confiables con tabaco premium.                │
│                                                │
│ [SOLICITAR CATÁLOGO] [VER MARCAS]             │
└─────────────────────────────────────────────────┘
```

### Sección de Marcas (Social Proof)
```
┌─────────────────────────────────────────────────┐
│ MARCAS LÍDERES QUE CONFIAMOS                   │
│                                                │
│ [Dunhill] [Mac Baren] [Davidoff] [Marlboro]   │
│ [Pueblo] ... [más marcas]                     │
│                                                │
│ Distribuidores certificados en toda Chile     │
└─────────────────────────────────────────────────┘
```

### Sección de Ventajas B2B
```
┌────────┬────────┬────────┬────────┐
│ STOCK  │ PRECIOS│DESPACHO│ATENCIÓN│
│PERM.   │ MAYO- │ RÁPIDO │PERSONAL│
│        │ RISTA │ A TODO │        │
└────────┴────────┴────────┴────────┘
```

### Sección FAQ/Preguntas
```
¿LISTO PARA LLEVAR TU NEGOCIO AL SIGUIENTE NIVEL?

Somos mayoristas con 120+ años de experiencia.
Pregúntanos sobre volúmenes, plazos y condiciones.

[CONTÁCTANOS VÍA WHATSAPP] +56 9 1234 5678
```

### Footer Profesional
```
┌──────────────────────────────────────────────────┐
│ © 2026 Puro Tabaco — Mayorista de Tabaco Premium│
│ www.purotabaco.cl                               │
│                                                 │
│ [Sobre Nosotros] [Catálogo] [Contacto]         │
│ [Términos] [Privacidad]                        │
│                                                 │
│ [Instagram] [Facebook] [LinkedIn]              │
└──────────────────────────────────────────────────┘
```

---

## 🎨 Componentes UI (MEJORADOS)

### Botón Primario (CTA Mayorista)
```css
background-color: #8B7355;
color: #EFE6D6;
border: 2px solid #C8B08A;
padding: 14px 36px;
font-size: 14px;
font-weight: 600;
border-radius: 2px;
text-transform: uppercase;
letter-spacing: 1.5px;
font-family: 'Lora', serif;
```

Hover: `background-color: #6B5545` (más oscuro)

### Botón Secundario
```css
background-color: transparent;
color: #3A3A3A;
border: 2px solid #C8B08A;
padding: 14px 36px;
```

Hover: `background-color: #EFE6D6;`

### Tarjetas (Cards)
```css
background-color: #EFE6D6;
border-left: 4px solid #C8B08A;
padding: 28px;
border-radius: 2px;
box-shadow: 0 2px 6px rgba(0,0,0,0.08);
```

### Inputs y Formularios
```css
border: 1px solid #C8B08A;
border-radius: 2px;
padding: 12px 16px;
font-family: 'Lora', serif;
font-size: 14px;
color: #3A3A3A;
background-color: #FAFAF8;
```

Focus: `border-color: #8B7355; outline: none;`

---

## 💻 CSS Base (archivo: static/css/purotabaco-v2-theme.css)

```css
/* Variables de color */
:root {
    --primary-green: #30483A;
    --secondary-tan: #C8B08A;
    --tertiary-cream: #EFE6D6;
    --dark-gray: #3A3A3A;
    --accent-bronze: #8B7355;
    --border-radius: 2px;
    --transition: all 0.3s ease;
}

/* Typography */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Lora:wght@400;600&display=swap');

body {
    font-family: 'Lora', Georgia, serif;
    color: var(--dark-gray);
    background-color: white;
    line-height: 1.625;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Playfair Display', Georgia, serif;
    color: var(--dark-gray);
    font-weight: 700;
    letter-spacing: 1px;
}

h1 { font-size: 52px; line-height: 60px; }
h2 { font-size: 40px; line-height: 48px; }
h3 { font-size: 32px; line-height: 38px; }
h4 { font-size: 24px; line-height: 30px; }

/* Header */
header {
    background-color: var(--primary-green);
    color: var(--tertiary-cream);
    padding: 20px 0;
    border-bottom: 2px solid var(--secondary-tan);
}

/* Footer */
footer {
    background-color: var(--primary-green);
    color: var(--tertiary-cream);
    padding: 40px 0;
}

/* Buttons */
.btn-primary {
    background-color: var(--accent-bronze);
    color: var(--tertiary-cream);
    border: 2px solid var(--secondary-tan);
    padding: 14px 36px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    border-radius: var(--border-radius);
    cursor: pointer;
    transition: var(--transition);
}

.btn-primary:hover {
    background-color: #6B5545;
}

/* Cards */
.card {
    background-color: var(--tertiary-cream);
    border-left: 4px solid var(--secondary-tan);
    padding: 28px;
    border-radius: var(--border-radius);
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}

/* Separadores */
.divider {
    border: none;
    border-top: 2px solid var(--secondary-tan);
    margin: 40px 0;
}

/* Input focus */
input:focus, textarea:focus {
    border-color: var(--accent-bronze);
    outline: none;
    box-shadow: 0 0 0 3px rgba(139, 115, 85, 0.1);
}
```

---

## ✅ Checklist de Aplicación

- [ ] Importar Google Fonts (Playfair Display + Lora)
- [ ] Aplicar CSS base `purotabaco-v2-theme.css`
- [ ] Colores en variables CSS (:root)
- [ ] Tipografía Playfair en headings
- [ ] Tipografía Lora en body
- [ ] Botones con estilo Bronce + Tabaco claro
- [ ] Cards con borde tabaco claro izquierdo
- [ ] Separadores en color tabaco claro
- [ ] Paleta verde + crema (NO negro + oro)
- [ ] Header verde oscuro con navegación
- [ ] Footer verde oscuro
- [ ] Logo con "EST. 1902"
- [ ] Narrativa "Tradición que mueve negocios"
- [ ] Marcas líderes como social proof
- [ ] Secciones enfocadas en B2B/mayorista
- [ ] Espacios generosos, elegancia profesional

---

## 📸 Referencias Visuales (MEJORADAS)

**Inspiración estética:**
- Tiendas vintage de tabaco londinenses (1900-1920)
- Identidades heritage (Dunhill, Mac Baren)
- E-commerce B2B premium (minimalismo, autoridad)
- Paleta: Verdes oscuros + bronces + crema (elegancia clásica)

---

## 🔄 Próximos pasos

1. ✅ Crear brand guide robusto (completado)
2. 📋 Generar nuevo prompt para Canva (próximo)
3. 🎨 Crear mockups en Canva con nueva paleta
4. 💻 Implementar CSS en templates
5. ✔️ Validar en navegadores y dispositivos
6. 🚀 Deploy

---

**Versión 2.0 — Versión Robusta con Narrativa Histórica**  
**Aprobado para uso**  
**Última actualización:** 2026-04-20
