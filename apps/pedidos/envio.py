"""Cálculo del costo de despacho. El envío NUNCA es gratis.

- Región Metropolitana de Santiago: $2.500 fijo, se cobra dentro del pedido
  (se agrega al total y se incluye como ítem en la preferencia de Mercado Pago).
- Cualquier otra región: se despacha por Starken "por pagar" — el cliente
  paga directamente al courier al recibir. No se cobra nada por el sitio.
"""
from decimal import Decimal

REGION_METROPOLITANA = 'Región Metropolitana de Santiago'

COSTO_ENVIO_RM = Decimal('2500')

# Las 16 regiones de Chile, para el select del checkout.
REGIONES_CHILE = [
    ('Región de Arica y Parinacota', 'Región de Arica y Parinacota'),
    ('Región de Tarapacá', 'Región de Tarapacá'),
    ('Región de Antofagasta', 'Región de Antofagasta'),
    ('Región de Atacama', 'Región de Atacama'),
    ('Región de Coquimbo', 'Región de Coquimbo'),
    ('Región de Valparaíso', 'Región de Valparaíso'),
    (REGION_METROPOLITANA, REGION_METROPOLITANA),
    ("Región del Libertador Gral. Bernardo O'Higgins", "Región del Libertador Gral. Bernardo O'Higgins"),
    ('Región del Maule', 'Región del Maule'),
    ('Región de Ñuble', 'Región de Ñuble'),
    ('Región del Biobío', 'Región del Biobío'),
    ('Región de la Araucanía', 'Región de la Araucanía'),
    ('Región de Los Ríos', 'Región de Los Ríos'),
    ('Región de Los Lagos', 'Región de Los Lagos'),
    ('Región de Aysén del Gral. Carlos Ibáñez del Campo', 'Región de Aysén del Gral. Carlos Ibáñez del Campo'),
    ('Región de Magallanes y de la Antártica Chilena', 'Región de Magallanes y de la Antártica Chilena'),
]


def es_rm(region: str) -> bool:
    return (region or '').strip() == REGION_METROPOLITANA


def calcular_envio(region: str) -> Decimal:
    """Costo de despacho cobrado en el sitio para esa región."""
    return COSTO_ENVIO_RM if es_rm(region) else Decimal('0')


def descripcion_envio(region: str) -> str:
    """Texto explicando cómo se despacha, para mostrar al cliente."""
    if es_rm(region):
        return f'Despacho Región Metropolitana: ${COSTO_ENVIO_RM:,.0f}'.replace(',', '.')
    return 'Despacho por Starken, por pagar: el courier cobra el envío al recibir el pedido.'
