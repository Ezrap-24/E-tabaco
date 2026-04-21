# Flujo de Carrito y Checkout — Puro Tabaco

**Versión:** 1.0  
**Fecha:** 2026-04-20  
**Aplicable a:** purotabaco.cl, clubdeltabaco.cl, zonatabaco.cl  

---

## 🛒 Arquitectura General

```
Entrada al sitio
        ↓
Validar edad (Modal)
        ↓
Navegar catálogo
        ↓
Ver ficha de producto
        ↓
Agregar al carrito
        ↓
Ver carrito
        ↓
Proceder a checkout
        ↓
Datos de entrega
        ↓
Confirmación legal
        ↓
Pago
        ↓
Orden confirmada
```

---

## 1️⃣ GATE DE MAYORÍA DE EDAD (Entrada)

### Implementación

**Se muestra ANTES de cualquier contenido:**

```
┌────────────────────────────────────┐
│                                    │
│  ⚠️  VERIFICACIÓN DE EDAD          │
│                                    │
│  Este sitio contiene productos    │
│  solo para mayores de 18 años.    │
│                                    │
│  ¿Tienes 18 años o más?           │
│                                    │
│  ┌─────────────┐    ┌─────────┐   │
│  │ SÍ, TENGO   │    │  NO,    │   │
│  │  18 AÑOS    │    │  SALIR  │   │
│  └─────────────┘    └─────────┘   │
│                                    │
│  Al hacer clic aceptas que:       │
│  - Tienes 18 años o más          │
│  - Reconoces los riesgos del     │
│    consumo de tabaco             │
│                                    │
└────────────────────────────────────┘
```

**Comportamiento:**
- Click "SÍ": Se guarda en cookie/sesión, acceso al sitio
- Click "NO": Redirige a página externa (ej: Google)
- Si cookie expira: Pedir validación de nuevo
- Mantener por 30 días máximo

**Código conceptual (Django):**
```python
# views.py
def age_gate_view(request):
    if request.POST.get('confirm_age'):
        response = HttpResponseRedirect('/')
        response.set_cookie('age_verified', 'true', max_age=30*24*60*60)
        return response
    
    if request.COOKIES.get('age_verified') == 'true':
        return redirect('home')
    
    return render(request, 'age_gate.html')

# middleware.py
class AgeGateMiddleware:
    def __call__(self, request):
        if not request.COOKIES.get('age_verified'):
            if not request.path.startswith('/age-gate/'):
                return redirect('age_gate')
        return self.get_response(request)
```

---

## 2️⃣ CATÁLOGO Y FICHA DE PRODUCTO

### Página de Catálogo

```
CATÁLOGO - TABACO PREMIUM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Filtros:    [Marca ▼]  [Tipo ▼]  [Precio ▼]

┌─────────┐  ┌─────────┐  ┌─────────┐
│         │  │         │  │         │
│ Imagen  │  │ Imagen  │  │ Imagen  │
│         │  │         │  │         │
├─────────┤  ├─────────┤  ├─────────┤
│ Dunhill │  │ Mac     │  │Davidoff │
│ Premium │  │ Baren   │  │  Gold   │
│         │  │ Nordic  │  │         │
│$14.280  │  │$12.500  │  │$16.800  │
│★★★★★   │  │★★★★★   │  │★★★★★   │
│         │  │         │  │         │
│[+DETALLES]│[+DETALLES]│[+DETALLES]
└─────────┘  └─────────┘  └─────────┘
```

### Ficha de Producto

```
DUNHILL PREMIUM SELECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Imagen grande de producto]

Marca:          Dunhill
Tipo:           Tabaco Premium
Peso:           50g
Origen:         Reino Unido
Precio:         $14.280

★★★★★ (42 evaluaciones)

DESCRIPCIÓN:
Tabaco premium seleccionado del mejor tabaco mundial.
Cada mezcla ha sido cuidadosamente desarrollada...

CARACTERÍSTICAS:
• Aroma intenso y balanceado
• Quemada lenta y pareja
• Sabor suave y complejo
• Envasado en caja de lujo

INFORMACIÓN LEGAL:
⚠️ Contiene tabaco - puede causar adicción
⚠️ No recomendado para embarazadas
⚠️ Venta solo para mayores de 18 años

[CANTIDAD: 1 ▼]

┌──────────────────┐
│ AGREGAR AL       │
│ CARRITO          │
│ $14.280          │
└──────────────────┘

[VER SIMILARES]
```

---

## 3️⃣ CARRITO (Ver Carrito)

### Page: /carrito/

```
MI CARRITO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Productos en tu carrito: 3

┌─────────────────────────────────────┐
│ DUNHILL PREMIUM - 50g               │
│ Cantidad: [1] [Actualizar] [✕]      │
│ Subtotal: $14.280                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ MAC BAREN NORDIC - 50g              │
│ Cantidad: [2] [Actualizar] [✕]      │
│ Subtotal: $25.000                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ DAVIDOFF GOLD - 40g                 │
│ Cantidad: [1] [Actualizar] [✕]      │
│ Subtotal: $16.800                   │
└─────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Subtotal productos:      $56.080
Impuestos:               $10.655
TOTAL:                   $66.735

⚠️ Recuerda: Solo para mayores de 18 años

┌─────────────────────────────┐
│ CONTINUAR COMPRANDO         │
└─────────────────────────────┘

┌─────────────────────────────┐
│ IR AL CHECKOUT (PAGAR)      │
└─────────────────────────────┘
```

### Funcionalidades:
- Actualizar cantidad
- Eliminar producto
- Calcular impuestos automáticamente
- Guardar carrito en sesión/BD
- Permitir abandonar y volver después (72 horas)

---

## 4️⃣ CHECKOUT (Pago)

### Step 1: Datos de Entrega

```
CHECKOUT - PASO 1 de 3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DATOS DE ENTREGA

Nombre completo:
[_____________________________]

Email:
[_____________________________]

Teléfono:
[_____________________________]

Tipo de comprador: ○ Persona  ○ Empresa

Si es empresa:
RUT Empresa:
[_____________________________]

Giro comercial:
[_____________________________]

DIRECCIÓN DE ENTREGA

Calle:
[_____________________________]

Número:
[_____] Apto/Casa: [_____]

Ciudad:
[_____________________________]

Región:
[_____________________________]

Código postal:
[_____________________________]

Instrucciones especiales (opcional):
[________________________________]

Método de entrega:
○ Retiro en local (gratis - 1 a 2 días)
○ Despacho a domicilio ($5.000 - 2 a 3 días)
○ Despacho acelerado ($12.000 - Día siguiente)

┌─────────────┐  ┌─────────────┐
│ ATRÁS       │  │ CONTINUAR   │
└─────────────┘  └─────────────┘
```

### Step 2: Confirmación Legal

```
CHECKOUT - PASO 2 de 3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONFIRMACIÓN Y TÉRMINOS LEGALES

⚠️ ADVERTENCIA SANITARIA:
El consumo de tabaco es perjudicial para la salud
y causa adicción. Se vende solo a mayores de 18 años.

CONFIRMACIONES NECESARIAS (requeridas):

☑ Certifico que tengo 18 años o más
   (Requerido) *

☑ Acepto los Términos y Condiciones
   [Ver términos] (Requerido) *

☑ Entiendo que el consumo de tabaco es perjudicial
   para la salud y puede causar adicción
   (Requerido) *

☑ Autorizo el envío del producto a la dirección
   indicada en mi pedido
   (Requerido) *

☑ Deseo recibir promociones y actualizaciones
   por email (Opcional)
   ☐

RESUMEN DEL PEDIDO:

Productos:
• Dunhill Premium - 50g (1)     $14.280
• Mac Baren Nordic - 50g (2)    $25.000
• Davidoff Gold - 40g (1)       $16.800

Subtotal:                        $56.080
Impuestos:                       $10.655
Despacho (domicilio):            $ 5.000
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL A PAGAR:                   $71.735

┌─────────────┐  ┌──────────────┐
│ ATRÁS       │  │ CONTINUAR    │
└─────────────┘  │ A PAGO       │
                 └──────────────┘
```

### Step 3: Seleccionar Método de Pago

```
CHECKOUT - PASO 3 de 3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MÉTODO DE PAGO

Selecciona cómo quieres pagar:

○ Tarjeta de crédito/débito
  (Visa, Mastercard, American Express)
  [Completar datos...]
  
○ Transferencia bancaria
  Datos de cuenta serán enviados por email
  
○ PayPal
  Serás redirigido a PayPal
  
○ Pago contra entrega (COD)
  Paga cuando recibas el producto
  (Disponible solo para despacho domicilio)

TOTAL A PAGAR: $71.735

┌──────────────────────┐
│ CONFIRMAR PAGO       │
│ (PROCESAR PEDIDO)    │
└──────────────────────┘

Por seguridad, usamos encriptación SSL.
Tus datos están protegidos.
```

---

## 5️⃣ CONFIRMACIÓN (Post-Pago)

### Página de Éxito

```
✅ PEDIDO CONFIRMADO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Número de orden: #PT-2026-04-001234

Gracias por tu compra. Tu pedido ha sido procesado exitosamente.

RESUMEN DEL PEDIDO:

Cliente:           Juan García
Email:             juan@email.com
Teléfono:          +56 9 1234 5678

PRODUCTOS:
• Dunhill Premium - 50g (1)     $14.280
• Mac Baren Nordic - 50g (2)    $25.000
• Davidoff Gold - 40g (1)       $16.800

TOTAL PAGADO: $71.735

ENTREGA:
Domicilio: Calle Principal 123, Apt 4B
           Santiago, Región Metropolitana
Método: Despacho (2 a 3 días hábiles)
Estimado: 2026-04-23

ESTADO DEL PEDIDO: En preparación

┌────────────────────────────────┐
│ VER MI PEDIDO EN DETALLE       │
└────────────────────────────────┘

┌────────────────────────────────┐
│ DESCARGAR RECIBO (PDF)         │
└────────────────────────────────┘

📧 Un email de confirmación ha sido enviado a:
   juan@email.com

Puedes rastrear tu pedido aquí:
www.purotabaco.cl/seguimiento/PT-2026-04-001234

¿Necesitas ayuda? Contáctanos:
WhatsApp: +56 9 1234 5678
Email: soporte@purotabaco.cl
```

### Email de Confirmación

```
ASUNTO: Tu pedido #PT-2026-04-001234 ha sido confirmado

Hola Juan,

Tu pedido ha sido confirmado y está en proceso de preparación.

Número de orden: #PT-2026-04-001234
Fecha: 2026-04-20
Total: $71.735

Detalles:
- Dunhill Premium - 50g (1) ........... $14.280
- Mac Baren Nordic - 50g (2) .......... $25.000
- Davidoff Gold - 40g (1) ............ $16.800
- Despacho a domicilio ............... $ 5.000
- Impuestos .......................... $10.655
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL PAGADO ......................... $71.735

Tu entrega está estimada para:
2026-04-23 (martes)

Puedes rastrear tu pedido aquí:
https://purotabaco.cl/seguimiento/PT-2026-04-001234

¿Preguntas? Contáctanos:
WhatsApp: +56 9 1234 5678
Email: soporte@purotabaco.cl

Gracias por tu confianza en Puro Tabaco.

---
⚠️ Recordatorio: El consumo de tabaco es perjudicial para la salud
```

---

## 🗄️ Base de Datos (Modelos Django)

### Modelo: Carrito

```python
from django.db import models
from django.contrib.auth.models import User

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    sesion_id = models.CharField(max_length=100)  # Para usuarios no registrados
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    def total(self):
        return sum(item.subtotal() for item in self.items.all())

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    
    def subtotal(self):
        return self.producto.precio * self.cantidad
```

### Modelo: Pedido (Orden)

```python
class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente de pago'),
        ('procesando', 'En proceso'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    numero = models.CharField(max_length=20, unique=True)  # PT-2026-04-001234
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.SET_NULL, null=True)
    
    # Datos de entrega
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    tipo_comprador = models.CharField(max_length=20, choices=[('persona', 'Persona'), ('empresa', 'Empresa')])
    rut_empresa = models.CharField(max_length=20, null=True, blank=True)
    
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    
    # Pago
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)  # tarjeta, transferencia, etc
    estado_pago = models.CharField(max_length=20)
    transaccion_id = models.CharField(max_length=100, null=True, blank=True)
    
    # Estado
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    
    # Confirmación legal
    confirma_edad = models.BooleanField()  # 18+
    acepta_terminos = models.BooleanField()
    acepta_advertencia_salud = models.BooleanField()
    
    # Timestamps
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    fecha_entrega_estimada = models.DateField()
    
    def __str__(self):
        return self.numero
```

---

## 🔐 Consideraciones de Seguridad

### 1. Validación de Edad
- ✅ Guardar en BD cuándo se validó edad
- ✅ Revalidar si cookie expira
- ✅ No permitir bypass o trampas
- ✅ Log de intentos

### 2. Datos Sensibles
- ✅ HTTPS/SSL obligatorio
- ✅ No guardar números completos de tarjeta
- ✅ Usar procesador de pagos certificado (Stripe, Mercado Pago)
- ✅ Encriptar información personal en BD

### 3. Prevención de Fraude
- ✅ Verificar dirección de entrega
- ✅ Comparar email de envío con email de registro
- ✅ Limitar número de pedidos por día/usuario
- ✅ Verificar patrones sospechosos

### 4. Cumplimiento Legal
- ✅ Registrar aceptación de mayoría de edad
- ✅ Guardar consentimiento de términos con timestamp
- ✅ Mantener logs de compra
- ✅ Auditoría de acceso a datos sensibles

---

## 📱 Responsive Design

El carrito y checkout deben funcionar perfectamente en:
- Desktop (1024px+)
- Tablet (768px - 1023px)
- Móvil (320px - 767px)

**En móvil:**
- Botones grandes y fáciles de tocar
- Campos de formulario claros
- Menos columnas (1 columna en móvil)
- Resumen del pedido siempre visible

---

## 🚀 MVP vs Fase 2

### MVP (Inicial)
- ✅ Gate de edad
- ✅ Catálogo básico
- ✅ Carrito simple
- ✅ Checkout básico
- ✅ Pago con Stripe/Mercado Pago
- ✅ Email de confirmación

### Fase 2 (Futuro)
- Cuentas de usuario registradas
- Historial de pedidos
- Wishlist/Favoritos
- Seguimiento en tiempo real
- Recomendaciones personalizadas
- Sistema de puntos/rewards

---

## 📞 Próximos pasos

1. ✅ Documentar flujo de carrito (HECHO)
2. 📋 Documentar normas legales (HECHO)
3. 🎨 Agregar carrito al design de Canva
4. 💻 Implementar modelos Django
5. 🧪 Probar flujo completo
6. ✔️ Validar con usuarios

---

**Versión 1.0 — Flujo Completo**  
**Listo para implementación**  
**Última actualización:** 2026-04-20
