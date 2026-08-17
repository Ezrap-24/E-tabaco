"""Generación de comprobante PDF con código de barras para órdenes pagadas."""
import io

import barcode
from barcode.writer import ImageWriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


# Paleta Puro Tabaco
VERDE = colors.HexColor('#30483A')
CREMA = colors.HexColor('#EFE6D6')
BRONCE = colors.HexColor('#C8B08A')
GRIS = colors.HexColor('#888888')


def generar_barcode_png(valor: str) -> io.BytesIO:
    """Genera un Code128 como PNG en memoria y retorna el BytesIO."""
    buf = io.BytesIO()
    code128 = barcode.get('code128', valor, writer=ImageWriter())
    code128.write(buf, options={
        'module_width': 0.3,
        'module_height': 8,
        'font_size': 7,
        'text_distance': 2,
        'quiet_zone': 3,
        'dpi': 150,
        'write_text': True,
        'background': 'white',
        'foreground': 'black',
    })
    buf.seek(0)
    return buf


def generar_comprobante(orden) -> io.BytesIO:
    """Retorna un BytesIO con el PDF del comprobante de la orden."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    ancho, alto = A4

    # ── ENCABEZADO ────────────────────────────────────────────────
    c.setFillColor(VERDE)
    c.rect(0, alto - 45*mm, ancho, 45*mm, fill=1, stroke=0)

    c.setFillColor(CREMA)
    c.setFont('Helvetica-Bold', 18)
    c.drawString(20*mm, alto - 18*mm, 'PURO TABACO')

    c.setFont('Helvetica', 9)
    c.setFillColor(BRONCE)
    c.drawString(20*mm, alto - 25*mm, 'TABACO PREMIUM · MAYORISTA')

    # Folio en encabezado (derecha)
    c.setFillColor(CREMA)
    c.setFont('Helvetica-Bold', 14)
    folio = orden.folio
    c.drawRightString(ancho - 20*mm, alto - 18*mm, folio)

    c.setFont('Helvetica', 8)
    c.setFillColor(BRONCE)
    c.drawRightString(ancho - 20*mm, alto - 25*mm, 'COMPROBANTE DE PEDIDO')

    # ── CÓDIGO DE BARRAS ──────────────────────────────────────────
    try:
        barcode_buf = generar_barcode_png(orden.codigo_barras)
        img = ImageReader(barcode_buf)
        # Centrado bajo el encabezado
        bar_w, bar_h = 70*mm, 18*mm
        bar_x = (ancho - bar_w) / 2
        bar_y = alto - 70*mm
        c.drawImage(img, bar_x, bar_y, width=bar_w, height=bar_h, preserveAspectRatio=True)
    except Exception:
        # Si falla el barcode, igual generamos el PDF sin él
        pass

    # ── DATOS DE LA ORDEN ─────────────────────────────────────────
    y = alto - 80*mm

    def linea_datos(etiqueta, valor, y_pos):
        c.setFont('Helvetica-Bold', 8)
        c.setFillColor(GRIS)
        c.drawString(20*mm, y_pos, etiqueta.upper())
        c.setFont('Helvetica', 9)
        c.setFillColor(colors.black)
        c.drawString(65*mm, y_pos, str(valor))
        return y_pos - 6*mm

    y = linea_datos('Folio', folio, y)
    y = linea_datos('Fecha', orden.fecha_pago.strftime('%d/%m/%Y %H:%M') if orden.fecha_pago else orden.fecha_creacion.strftime('%d/%m/%Y'), y)
    y = linea_datos('Cliente', orden.cliente_nombre, y)
    y = linea_datos('Email', orden.cliente_email, y)
    if orden.cliente_telefono:
        y = linea_datos('Teléfono', orden.cliente_telefono, y)
    y = linea_datos('Dirección', orden.direccion_envio, y)

    # ── TABLA DE PRODUCTOS ────────────────────────────────────────
    y -= 6*mm
    # Cabecera tabla
    c.setFillColor(VERDE)
    c.rect(20*mm, y - 6*mm, ancho - 40*mm, 7*mm, fill=1, stroke=0)
    c.setFillColor(CREMA)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(22*mm, y - 4*mm, 'PRODUCTO')
    c.drawRightString(ancho - 65*mm, y - 4*mm, 'CANT.')
    c.drawRightString(ancho - 40*mm, y - 4*mm, 'P. UNIT.')
    c.drawRightString(ancho - 20*mm, y - 4*mm, 'SUBTOTAL')
    y -= 6*mm

    # Filas
    for i, detalle in enumerate(orden.detalles.all()):
        fila_y = y - 6*mm
        if i % 2 == 0:
            c.setFillColor(colors.HexColor('#F8F6F0'))
            c.rect(20*mm, fila_y, ancho - 40*mm, 6*mm, fill=1, stroke=0)
        c.setFillColor(colors.black)
        c.setFont('Helvetica', 8)
        nombre = detalle.producto_nombre or str(detalle.producto)
        if len(nombre) > 45:
            nombre = nombre[:42] + '...'
        c.drawString(22*mm, fila_y + 1.5*mm, nombre)
        c.drawRightString(ancho - 65*mm, fila_y + 1.5*mm, str(detalle.cantidad))
        c.drawRightString(ancho - 40*mm, fila_y + 1.5*mm, f'${detalle.precio_unitario:,.0f}')
        c.drawRightString(ancho - 20*mm, fila_y + 1.5*mm, f'${detalle.subtotal():,.0f}')
        y -= 6*mm

    # ── DESPACHO Y TOTAL ─────────────────────────────────────────
    y -= 4*mm
    c.setStrokeColor(VERDE)
    c.setLineWidth(0.5)
    c.line(20*mm, y, ancho - 20*mm, y)
    y -= 6*mm

    if orden.costo_envio and orden.costo_envio > 0:
        c.setFont('Helvetica', 9)
        c.setFillColor(colors.black)
        c.drawString(20*mm, y, 'Subtotal productos')
        c.drawRightString(ancho - 20*mm, y, f'${orden.subtotal_productos:,.0f}')
        y -= 5.5*mm
        c.drawString(20*mm, y, 'Despacho (Región Metropolitana)')
        c.drawRightString(ancho - 20*mm, y, f'${orden.costo_envio:,.0f}')
        y -= 6.5*mm
    else:
        c.setFont('Helvetica', 8)
        c.setFillColor(GRIS)
        c.drawString(20*mm, y, 'Despacho por Starken, por pagar al recibir')
        y -= 6.5*mm

    c.setFont('Helvetica-Bold', 11)
    c.setFillColor(VERDE)
    c.drawString(20*mm, y, 'TOTAL')
    c.drawRightString(ancho - 20*mm, y, f'${orden.total:,.0f}')

    # ── PIE DE PÁGINA ─────────────────────────────────────────────
    c.setFont('Helvetica', 7)
    c.setFillColor(GRIS)
    c.drawCentredString(ancho / 2, 18*mm, 'Puro Tabaco — purotabaco.cl')
    c.drawCentredString(ancho / 2, 13*mm, 'El tabaco es perjudicial para la salud.')

    c.save()
    buf.seek(0)
    return buf
