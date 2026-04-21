# Normas de Venta de Tabaco en Chile

**Versión:** 1.0  
**Fecha:** 2026-04-20  
**Aplicable a:** purotabaco.cl, clubdeltabaco.cl, zonatabaco.cl  

⚠️ **ADVERTENCIA LEGAL:** Este documento es informativo. **CONSULTA CON UN ABOGADO ESPECIALIZADO** antes de lanzar. Las regulaciones pueden haber cambiado.

---

## 📋 Regulaciones Principales

### 1. ✅ VALIDACIÓN OBLIGATORIA DE MAYORÍA DE EDAD (18+)

**Base legal:** Ley 19.419 sobre Tabaco (modificada)

**Requisito:**
- No se puede vender tabaco a menores de 18 años
- Debe haber verificación de edad ANTES de la compra
- Esto es **OBLIGATORIO** en e-commerce también

**Implementación técnica:**
```
1. MODAL AL ENTRAR AL SITIO:
   ┌────────────────────────────────────┐
   │ RESTRICCIÓN POR EDAD               │
   │                                    │
   │ Debes ser mayor de 18 años para   │
   │ acceder a este sitio.             │
   │                                    │
   │ ¿Tienes 18 años o más?            │
   │                                    │
   │ [ SÍ, TENGO 18+ ]  [ NO, SALIR ]  │
   │                                    │
   │ Al continuar aceptas nuestros    │
   │ términos y condiciones.           │
   └────────────────────────────────────┘

2. La cookie/sesión debe recordar que pasó la validación
3. Si cierra navegador, validar de nuevo

⚠️ IMPORTANTE: NO permitir bypass (ej: "click aquí si tienes 18")
   Debe ser clara, obligatoria, sin trampa
```

**En el checkout:**
```
☑ Certifico que tengo 18 años o más
☑ Acepto los términos legales de venta de tabaco
```

---

### 2. 📢 RESTRICCIONES EN PUBLICIDAD Y MARKETING

**Base legal:** Ley 19.419, Decretos relacionados

**Restricciones comunes:**
- ❌ NO publicitar en redes dirigidas a menores
- ❌ NO usar celebridades menores de edad
- ❌ NO hacer parecer el tabaco como "saludable"
- ❌ NO ofrecerse como alternativa a medicinas
- ⚠️ Debes incluir advertencias sanitarias
- ✅ Puedes informar sobre historia, tradición, calidad

**Para Puro Tabaco:**
```
✅ PERMITIDO:
- "Tabaco premium desde 1902"
- "Tradición que mueve negocios"
- "Para adultos responsables"
- Énfasis en calidad, herencia

❌ NO PERMITIDO:
- "Tabaco saludable" o "sin riesgo"
- "El mejor para tu salud"
- "Recomendado por expertos"
- Dirigir a menores directamente
```

---

### 3. ⚠️ ADVERTENCIAS SANITARIAS OBLIGATORIAS

**Requisito:**
- En producto: Advertencia sanitaria (según normativa)
- En sitio web: Debe indicar los riesgos

**Texto recomendado para sitio:**
```
⚠️ ADVERTENCIA:
El consumo de tabaco es perjudicial para la salud. 
Contiene nicotina que crea adicción.

Su venta está prohibida a menores de 18 años.
```

**Dónde colocar en el sitio:**
1. Footer de cada página (pequeño, pero visible)
2. Antes del checkout (clara, obligatoria)
3. En términos y condiciones (legalmente)

---

### 4. 💼 DOCUMENTACIÓN Y REGISTROS (B2B)

**Para mayorista B2B, necesitas:**

- ✅ RUT registrado como vendedor de tabaco
- ✅ Licencia sanitaria municipal (si aplica)
- ✅ Registro de compradores mayoristas
- ✅ Factura por cada venta (requerimiento fiscal)
- ✅ Documentación del cliente (para B2B):
  - RUT empresa
  - Giro comercial
  - Dirección entrega

**En el sitio:**
```
Para acceso mayorista, solicitamos:
- RUT de empresa
- Giro comercial verificable
- Referencia de negocio anterior
- Domicilio de entrega

Esto es para CUMPLIR normativa fiscal chilena.
```

---

### 5. 📦 IMPUESTOS Y ARANCELES

**Importante saber:**
- Tabaco tiene impuestos específicos en Chile
- El precio debe INCLUIR todos los impuestos
- Debes informar al cliente exactamente qué está pagando

**Estructura de precio recomendada:**
```
Tabaco Brand X - 50g
━━━━━━━━━━━━━━━━━━━━━━━━━
Precio base:           $10.000
Impuesto específico:   $  2.000
Subtotal:             $12.000
IVA (19%):            $ 2.280
━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL:                $14.280
```

**En el sitio:**
- Mostrar precio final claramente
- Detallar componentes de impuestos
- No sorprender al cliente en checkout

---

## 🎯 Implementación en Puro Tabaco

### En la Landing Page (Canva design)

Agregar en footer o sección específica:

```
┌──────────────────────────────────┐
│ ⚠️ AVISO LEGAL IMPORTANTE        │
│                                  │
│ Este sitio está dirigido SOLO a │
│ mayores de 18 años.             │
│                                  │
│ El consumo de tabaco es         │
│ perjudicial para la salud y     │
│ causa adicción.                 │
│                                  │
│ Producto sujeto a regulaciones  │
│ de venta en Chile.              │
│                                  │
│ [Ver términos completos]        │
└──────────────────────────────────┘
```

### En el Carrito/Checkout

```
PASO 1: Validación de edad (OBLIGATORIO)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
¿Tienes 18 años o más?
☑ Sí, tengo 18 años o más

PASO 2: Revisión de carrito
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Producto 1: [Tabaco X] - $14.280
Producto 2: [Tabaco Y] - $12.500
Subtotal: $26.780
Impuestos: $  5.088
TOTAL:    $31.868

PASO 3: Datos de entrega
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Nombre:
Dirección:
Teléfono:
Email:

PASO 4: Confirmación legal
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☑ Certifico que tengo 18+ años
☑ Acepto términos y condiciones
☑ Entiendo los riesgos para la salud

[REALIZAR PAGO]
```

---

## 📄 Documentos legales necesarios

### 1. Términos y Condiciones (Incluir)

```
1. RESTRICCIÓN DE EDAD
   - Sitio solo para mayores de 18 años
   - Usuario certifica su mayoría de edad

2. ADVERTENCIA SANITARIA
   - Consumo de tabaco es perjudicial
   - Causa adicción y problemas de salud

3. RESPONSABILIDAD DEL COMPRADOR
   - Usuario es responsable de cómo usa el producto
   - Puro Tabaco no es responsable de daños a la salud

4. REGULACIONES CHILENAS
   - Cumplimos leyes de venta de tabaco en Chile
   - Nos reservamos derecho de rechazar compras

5. PROHIBICIONES
   - No vendemos a menores
   - No vendemos a jurisdicciones donde es ilegal
```

### 2. Política de Privacidad

```
Incluir cláusula sobre datos de comprador:
- Qué datos recopilamos
- Para qué los usamos
- Cómo los protegemos
```

### 3. Política de devoluciones

```
Para tabaco (normalmente):
- No se aceptan devoluciones de productos abiertos
- Devoluciones solo por defecto de fabricación
- Reembolso o reemplazo del producto dañado
```

---

## ✅ Checklist de Cumplimiento

### Antes de lanzar purotabaco.cl

**En el sitio web:**
- [ ] Modal de mayoría de edad en entrada
- [ ] Advertencia sanitaria en footer
- [ ] Aviso legal claro y visible
- [ ] Términos y condiciones completos
- [ ] Política de privacidad actualizada

**En checkout/carrito:**
- [ ] Validación de edad obligatoria
- [ ] Checkbox de aceptación de términos
- [ ] Confirmación de mayoría de edad
- [ ] Detalles de impuestos visibles

**En base de datos:**
- [ ] Campo para guardar consentimiento de mayoría de edad
- [ ] Fecha de aceptación de términos
- [ ] Log de validación de edad

**En políticas de negocio:**
- [ ] RUT de empresa registrado
- [ ] Licencias sanitarias municipales (si aplica)
- [ ] Registro de compradores mayoristas
- [ ] Documentación clara de proveedores

**En marketing:**
- [ ] Sin publicidad dirigida a menores
- [ ] Sin claims de salud
- [ ] Sin influencers menores de edad
- [ ] Énfasis en "Para adultos"

---

## ⚖️ Recomendaciones Legales

### 1. Consulta con abogado especializado
- Verificar si necesitas licencias adicionales
- Confirmar impuestos específicos aplicables
- Validar términos legales

### 2. Contacta a municipalidad
- Algunos municipios requieren permisos adicionales
- Verifica si tu zona permite venta online de tabaco
- Puede haber restricciones por jurisdicción

### 3. Revisa dirección de Impuestos Internos
- Confirmartipuración de tabaco
- Obligaciones fiscales para mayoristas
- Retención de IVA

### 4. Documentación clara
- Mantén registros de:
  - Quién compra (mayoristas)
  - Cuándo se vende
  - Cuánto se vende
  - Prueba de mayoría de edad (logs)

---

## 🚨 Riesgos Si No Cumples

| Incumplimiento | Consecuencia |
|---|---|
| No validar edad | Multa + cierre de sitio |
| Vender a menor | Delito penal |
| Sin advertencia sanitaria | Multa de SERNAC |
| Publicidad prohibida | Sanción + campaña reversa |
| Sin documentación | Problemas fiscales |

---

## 📞 Próximos pasos

1. **URGENTE:** Consulta con abogado especializado en regulaciones de tabaco en Chile
2. Contacta a municipalidad de operación
3. Verifica con Impuestos Internos
4. Redacta términos legales completos
5. Implementa en sitio antes de lanzar

---

## 🔗 Referencias útiles

- Ley 19.419 sobre Tabaco (búsca en bcn.cl)
- SERNAC - Derechos del consumidor
- Dirección de Impuestos Internos (SII) - Tributación tabaco
- Municipalidad de tu zona

---

**Este documento es informativo, no legal.**  
**Consulta con profesionales legales antes de lanzar.**  
**Última actualización:** 2026-04-20
