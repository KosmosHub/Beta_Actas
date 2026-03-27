from fpdf import FPDF
import re

def generar_acta(establecimiento, datos, folio=1):
    datos_filtrados = datos[(datos["cantidad"].notnull()) & (datos["cantidad"] > 0)]
    if datos_filtrados.empty:
        print(f"⚠️ No se generó acta para {establecimiento} (sin productos con cantidad).")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, f"Acta de Entrega - Folio {folio}", ln=True, align="C")
    pdf.cell(200, 10, f"Establecimiento: {establecimiento}", ln=True, align="L")
    pdf.ln(10)

    pdf.set_font("Arial", size=10)
    pdf.cell(100, 10, "Producto", 1)
    pdf.cell(30, 10, "Cantidad", 1)
    pdf.cell(40, 10, "Total", 1)
    pdf.ln()

    for _, fila in datos_filtrados.iterrows():
        producto = str(fila["producto"])
        cantidad = str(fila["cantidad"])
        total = str(fila["total"]) if fila["total"] is not None else ""

        x = pdf.get_x()
        y = pdf.get_y()

        pdf.multi_cell(100, 5, producto, border=1)
        altura_producto = pdf.get_y() - y

        pdf.set_xy(x + 100, y)
        pdf.cell(30, altura_producto, cantidad, border=1, align="C")
        pdf.cell(40, altura_producto, total, border=1, align="C")

        pdf.set_xy(x, y + altura_producto)

    safe_name = re.sub(r'[\\/*?:"<>|]', "_", establecimiento)
    safe_name = safe_name.replace("\n", "_").replace(" ", "_")

    # 🔎 nombre único por folio
    nombre_archivo = f"acta_{folio}_{safe_name}.pdf"
    pdf.output(nombre_archivo)
    print(f"✅ Acta generada: {nombre_archivo}")
