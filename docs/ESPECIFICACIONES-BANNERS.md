# Especificaciones de Banners — Puro Tabaco

Guía para generar banners del carrusel del inicio con Gemini (u otra IA de imágenes)
que calcen exactos con el sitio.

---

## 1. Cómo se muestran en el sitio

El carrusel es una **banda a ancho completo**, fondo negro, imagen recortada con
`object-fit: cover` centrado e `opacity: 0.92`. La altura es fija pero el ancho cambia
según la pantalla, así que **la imagen se recorta distinto en cada dispositivo**:

| Dispositivo        | Banda visible (aprox.) | Lo que se ve         |
|--------------------|------------------------|----------------------|
| PC (~1440 px)      | 1440 × 500 px          | ~2.9 : 1 (panorámico)|
| Tablet / móvil grande | ~768 × 420 px       | ~1.8 : 1             |
| Móvil chico (≤480) | ~390 × 360 px          | ~1.1 : 1 (casi cuadrado) |

**Regla de oro:** todo lo importante (producto, logo, texto) va en el **centro**.
Los bordes laterales se cortan en celular.

---

## 2. Qué pedirle a la IA

- **Proporción:** 2.36 : 1 (21:9) — igual que tus banners buenos actuales.
- **Resolución:** **3168 × 1344 px** (o múltiplo de 21:9, ej. 2400 × 1018).
- **Zona segura:** contenido clave dentro del **60 % central horizontal** y
  **70 % central vertical**.
- **Formato de generación:** PNG o JPG.

### ⚠️ Comprimir antes de subir
Los banners actuales pesan **6–8 MB** (PNG) — demasiado, ralentizan el móvil.
Antes de subirlos al sitio: convertir a **WebP o JPG calidad ~80 %**, objetivo
**< 400 KB** cada uno. (Esto lo puedo hacer yo cuando los tengas.)

---

## 3. Identidad de marca (para el estilo)

- Tienda **premium** de tabaco. Estética **sobria, elegante, editorial**.
- Iluminación **cálida, con sombras suaves**, mood oscuro tipo bodegón de lujo
  (combina con la banda negra del carrusel).
- **Paleta:** verde tabaco `#30483A` · crema `#EFE6D6` · bronce `#8B7355` ·
  tan `#C8B08A`.
- Tipografía de la marca (si va texto): serif elegante estilo *Playfair Display*.

---

## 4. Plantilla A — Imagen LIMPIA (recomendada)

> La IA genera solo fondo/producto. El título y precio se ponen con HTML encima:
> texto perfecto y editable.

```
Crea un banner publicitario panorámico para una tienda premium de tabaco
llamada "Puro Tabaco".

FORMATO:
- Relación de aspecto 21:9 (panorámico ancho), resolución 3168x1344 px.
- Sujeto principal CENTRADO, con aire a los lados (los bordes se recortan en móvil).

PRODUCTO / TEMA:
- [describe el producto: marca, sabor, color, formato del paquete].

ESTILO:
- Sobrio, elegante, editorial, premium. Iluminación cálida, sombras suaves,
  fondo oscuro que combine con una banda negra.
- Paleta: verde tabaco #30483A, crema #EFE6D6, bronce #8B7355, tan #C8B08A.
- SIN texto en la imagen.
- Sin logos de terceros ajenos al producto.
```

---

## 5. Plantilla B — Con TEXTO incrustado

> Más rápido, pero la IA suele deformar letras. **Revisa cada palabra** y, si sale
> mal, vuelve a generar o usa la Plantilla A.

```
Crea un banner publicitario panorámico para una tienda premium de tabaco
llamada "Puro Tabaco".

FORMATO:
- Relación de aspecto 21:9 (panorámico ancho), resolución 3168x1344 px.
- Sujeto y texto CENTRADOS, con aire a los lados (los bordes se recortan en móvil).

PRODUCTO / TEMA:
- [describe el producto: marca, sabor, color, formato del paquete].

TEXTO (en el centro, tipografía serif elegante, alto contraste, legible):
- Titular: "[TU TITULAR]"
- Bajada (opcional): "[texto secundario corto]"

ESTILO:
- Sobrio, elegante, editorial, premium. Iluminación cálida, sombras suaves,
  fondo oscuro que combine con una banda negra.
- Paleta: verde tabaco #30483A, crema #EFE6D6, bronce #8B7355, tan #C8B08A.
- Sin logos de terceros ajenos al producto.
```

---

## 6. Ejemplo rellenado (marca Mantra)

```
Crea un banner publicitario panorámico para una tienda premium de tabaco
llamada "Puro Tabaco".

FORMATO:
- Relación de aspecto 21:9, resolución 3168x1344 px.
- Producto CENTRADO, con aire a los lados.

PRODUCTO:
- Paquetes de tabaco para armar marca "Mantra", presentación premium,
  dos o tres pouches de pie sobre una superficie de madera oscura, con hebras
  de tabaco sueltas al frente.

ESTILO:
- Sobrio, elegante, editorial. Iluminación cálida lateral, sombras profundas,
  fondo oscuro degradado a negro en los bordes.
- Acentos en bronce #8B7355 y crema #EFE6D6.
- SIN texto en la imagen.
```

---

## 7. Checklist antes de subir al sitio

- [ ] Proporción 21:9 y contenido centrado (probar recorte en móvil).
- [ ] Texto (si lo hay) sin errores de IA.
- [ ] Comprimido a WebP/JPG < 400 KB.
- [ ] Nombre de archivo claro: `marca-tema.webp` (ej. `mantra-frambuesa.webp`).
- [ ] Guardar en `static/img/banners/` y agregar al carrusel en `home.html`.
```
