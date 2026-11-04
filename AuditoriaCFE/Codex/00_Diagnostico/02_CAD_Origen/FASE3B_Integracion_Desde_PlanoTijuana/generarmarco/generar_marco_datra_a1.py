"""Generador DATRA A1 v0.2 — identidad corporativa en atributos editables.

Fuentes de identidad (consultadas 2026-11-04): https://datra.mx/
- DATRA: nombre comercial exhibido en sitio, no razón social acreditada.
- Teléfono (664) 941-8515; info@datra.mx; Blvd. Cuauhtémoc Sur
  9784-C, Col. Revolución, Tijuana, B.C.; https://datra.mx

El logotipo oficial NO se inventa ni se descarga de imágenes de otra DATRA.
Opcional: --logo C:/ruta/logo_datra.png (PNG/JPG real y autorizado).
La imagen se copia junto al DXF con ruta relativa; conservarla al crear la DWT.

Genera SOLO DXF de Paper Space en milímetros; no incluye mapa ni rutas.
Dependencia: python -m pip install ezdxf
Si se usa --logo: python -m pip install pillow
"""
from pathlib import Path
import argparse
import shutil
import ezdxf

PARSER = argparse.ArgumentParser(description="Generar marco A1 editable DATRA / CFE")
PARSER.add_argument("--logo", help="Ruta local del logotipo OFICIAL DATRA (PNG/JPG)")
PARSER.add_argument("--output", help="Ruta del DXF de salida")
ARGS = PARSER.parse_args()
OUT = Path(ARGS.output).expanduser().resolve() if ARGS.output else Path(__file__).with_name("MARCO_DATRA_A1_EMPRESA_v0_2.dxf")
OUT.parent.mkdir(parents=True, exist_ok=True)
LOGO_INPUT = Path(ARGS.logo).expanduser().resolve() if ARGS.logo else (Path(__file__).with_name("logo_datra.png") if Path(__file__).with_name("logo_datra.png").is_file() else None)

# Identidad comercial consultada en sitio oficial, no equivale a datos legales CFE.
DATRA = {
    "telefono": "(664) 941-8515",
    "correo": "info@datra.mx",
    "domicilio": "Blvd. Cuauhtemoc Sur 9784-C, Col. Revolucion, Tijuana, B.C.",
    "sitio": "datra.mx",
}

doc = ezdxf.new("R2013", setup=True)
doc.header["$INSUNITS"] = 4             # unidades DXF de la lámina: milímetros
doc.header["$MEASUREMENT"] = 1

LAYERS = [
    ("DATRA_A1_MARCO", 7, 35),
    ("DATRA_A1_TITULOS", 5, 25),
    ("DATRA_A1_TEXTO", 7, 18),
    ("DATRA_A1_SIMBOLOS", 1, 25),
    ("DATRA_A1_ATRIBUTOS", 7, 25),
    ("DATRA_A1_GUIAS_NO_PLOT", 8, 13),
    ("DATRA_A1_LOGO", 7, 25),
]
for name, color, lw in LAYERS:
    if name not in doc.layers:
        doc.layers.new(name, dxfattribs={"color": color, "lineweight": lw})
doc.layers.get("DATRA_A1_GUIAS_NO_PLOT").dxf.plot = 0

layout = doc.layout("Layout1")
doc.layouts.rename("Layout1", "DATRA_A1")
layout = doc.layout("DATRA_A1")
layout.page_setup(size=(841, 594), margins=(5, 5, 5, 5), units="mm", rotation=0,
                  scale=16, name="ISO A1 horizontal - DATRA", device="DWG To PDF.pc3")

BORDER="DATRA_A1_MARCO"
TXT="DATRA_A1_TEXTO"
HEAD="DATRA_A1_TITULOS"
SYM="DATRA_A1_SIMBOLOS"
GUIDE="DATRA_A1_GUIAS_NO_PLOT"

def ln(space, x1,y1,x2,y2,layer=BORDER):
    return space.add_line((x1,y1),(x2,y2),dxfattribs={"layer":layer})

def rect(space, x1,y1,x2,y2,layer=BORDER):
    return space.add_lwpolyline([(x1,y1),(x2,y1),(x2,y2),(x1,y2)], close=True,
        dxfattribs={"layer": layer})

def text(space, x,y,s,h=2.5,layer=TXT):
    return space.add_text(s, dxfattribs={"insert":(x,y),"height":h,"layer":layer, "style":"Standard"})

def circle(space,x,y,r,layer=SYM):
    space.add_circle((x,y),r,dxfattribs={"layer":layer})

# Área segura: 13mm respecto a los bordes físicos del papel A1.
rect(layout, 11,11,830,583)
rect(layout, 14,14,827,580)
# Panel izquierdo y central: cajetín derecho mantiene geometría independiente.
rect(layout, 14,14,139,580)
rect(layout, 143,14,695,580)
rect(layout, 699,14,827,580)

# Columna de detalles técnicos: no inventar herrajes ni detalles de cable CFE.
ln(layout, 14,554,139,554)
text(layout,20,564,"TIPOS DE ESTRUCTURA",4,HEAD)
text(layout,25,557,"DETALLES APROBADOS",2.7,HEAD)
for i,(hi,lo,head) in enumerate([
    (554,446,"DETALLE 01 - TENSION"),
    (446,338,"DETALLE 02 - SUSPENSION"),
    (338,230,"DETALLE 03 - DERIVACION"),
    (230,122,"DETALLE 04 - EMPALME"),
    (122,14,"DETALLE 05 - OTROS"),
]):
    if i: ln(layout,14,hi,139,hi)
    text(layout,20,hi-8,head,2.6,HEAD)
    text(layout,23,lo+51,"IMPORTAR DETALLE VALIDADO",2.3,GUIDE)
    text(layout,23,lo+45,"DE LA BASE CFE / DATRA",2.3,GUIDE)
    # marcas vectoriales simples de posición - solo guías no ploteables
    ln(layout,27,lo+26,126,lo+26,GUIDE)
    circle(layout,77,lo+26,3,GUIDE)

# Panel de mapa: NO insertar cartografía aún ni dibujar rutas.
text(layout,150,572,"AREA DE MAPA - VIEWPORT DE AUDITORIA",3.1,GUIDE)
text(layout,150,567,"VALIDAR CRS / ESCALA ANTES DE ACTIVAR VENTANA",2.1,GUIDE)

# Columna derecha: orientación.
ln(layout,699,502,827,502)
text(layout,729,573,"ORIENTACION",3.2,HEAD)
circle(layout,763,539,13)
ln(layout,763,519,763,561,SYM)
ln(layout,744,539,782,539,SYM)
layout.add_lwpolyline([(763,562),(760,551),(766,551)], close=True, dxfattribs={"layer":SYM})
text(layout,759,567,"N",3.3,SYM)
text(layout,758,513,"NORTE",2.7)

# Croquis sin inventar delimitaciones administrativas.
ln(layout,699,415,827,415)
text(layout,718,492,"UBICACION DE ZONA",3.2,HEAD)
rect(layout,708,427,818,484)
text(layout,720,454,"CROQUIS DE UBICACION",2.5,GUIDE)
text(layout,737,448,"PENDIENTE",2.5,GUIDE)

# Leyenda de red con símbolos provisionales acordados.
ln(layout,699,315,827,315)
text(layout,741,406,"SIMBOLOGIA",3.3,HEAD)
legend=[
    (391,"POSTE - SIMBOLO GENERICO","P"),
    (374,"CAJA DE EMPALME","C"),
    (357,"EXCEDENTE DE FIBRA","E"),
    (340,"RUTA CONFIRMADA","R"),
    (323,"RAMAL CONFIRMADO","B"),
]
for y,lab,typ in legend:
    if typ=='P':circle(layout,713,y,3)
    elif typ=='C':rect(layout,710,y-3,716,y+3,layer=SYM)
    elif typ=='E':
        layout.add_lwpolyline([(713,y+3),(716,y-3),(710,y-3)],close=True,dxfattribs={"layer":SYM})
    elif typ=='R': ln(layout,707,y,719,y,SYM)
    elif typ=='B':
        ln(layout,707,y,713,y,SYM);ln(layout,713,y,719,y+4,SYM)
    text(layout,723,y-1,lab,2.5)

# CAJETIN como bloque editable (atributos con nombres estables para SCR 02).
blk=doc.blocks.new("DATRA_CAJETIN_A1_V02")
rect(blk,0,0,128,301)
# Identidad DATRA: datos públicos en ATTRIB editables (sin inventar razón social).
# Se conservan los 13 TAG anteriores; se versiona nombre de bloque V02 para
# evitar colisión con cajetín v0.1 al importar el nuevo layout.
# Los cuatro TAG CORP_* son editables con EATTEDIT/ATTEDIT.
rect(blk,2,263,126,298)
text(blk,6,288.5,"DATRA",8.0,HEAD)
text(blk,6,282.5,"CONECTIVIDAD EMPRESARIAL | FIBRA OPTICA",2.1,HEAD)
# Las guías de logo no se imprimen; logo auténtico opcional x=91..124.
rect(blk,91,279,124,297,GUIDE)
text(blk,95,287,"AREA LOGO",2.2,GUIDE)
text(blk,95,283,"OFICIAL",2.0,GUIDE)
for tag, value, yy, hh in [
    ("CORP_TEL", "Tel. " + DATRA["telefono"], 277.2, 2.1),
    ("CORP_EMAIL", DATRA["correo"], 273.2, 2.2),
    ("CORP_DOMICILIO", DATRA["domicilio"], 269.3, 1.85),
    ("CORP_WEB", DATRA["sitio"], 265.4, 2.0),
]:
    blk.add_attdef(tag=tag,insert=(5,yy),text=value,height=hh,
        dxfattribs={"layer":"DATRA_A1_ATRIBUTOS","prompt":tag})

def field(label,tag,top,height=20,pref="PENDIENTE"):
    bot=top-height
    ln(blk,2,bot,126,bot)
    text(blk,5,top-6,label,2.35,HEAD)
    blk.add_attdef(tag=tag,insert=(5,bot+5),text=pref,height=3.2,
                   dxfattribs={"layer":"DATRA_A1_ATRIBUTOS","prompt":label})
    return bot

start=263
for label,tag,h,default in [
    ("NOMBRE DEL PLANO", "NOMBRE_PLANO", 28, "PENDIENTE"),
    ("AUDITORIA / SUBRUTA", "AUDITORIA", 25, "PENDIENTE"),
    ("ZONA", "ZONA", 20, "TIJUANA, B.C."),
    ("FECHA DE AUDITORIA", "FECHA", 20, "PENDIENTE"),
    ("ELABORO", "ELABORO", 20, "PENDIENTE"),
    ("REVISO", "REVISO", 20, "PENDIENTE"),
    ("CRS VALIDADO", "CRS", 20, "POR VALIDAR"),
]:
    start=field(label,tag,start,h,default)
# start = 110.
text(blk,5,103,"RESUMEN DE ELEMENTOS UNICOS",2.6,HEAD)
ln(blk,2,98,126,98)
for i,(tag,label) in enumerate([("TOTAL_POSTES","POSTES"),("TOTAL_CAJAS","CAJAS"),("TOTAL_EXCEDENTES","EXCEDENTES")]):
    top=98-i*20;bot=top-20
    ln(blk,2,bot,126,bot)
    text(blk,5,top-6,label,2.4,HEAD)
    blk.add_attdef(tag=tag,insert=(83,bot+6),text="--",height=4.1,
                   dxfattribs={"layer":"DATRA_A1_ATRIBUTOS","prompt":label})
# y=38 after counts
ln(blk,2,18,126,18)
text(blk,5,31,"ESTADO DE REVISION",2.2,HEAD)
blk.add_attdef(tag="ESTADO",insert=(55,30),text="PRELIMINAR",height=3,
               dxfattribs={"layer":"DATRA_A1_ATRIBUTOS","prompt":"Estado"})
text(blk,5,22,"ESCALA / No. PLANO",2.2,HEAD)
blk.add_attdef(tag="ESCALA",insert=(53,21),text="S/E",height=2.8,
               dxfattribs={"layer":"DATRA_A1_ATRIBUTOS","prompt":"Escala"})
blk.add_attdef(tag="NUM_PLANO",insert=(94,21),text="01/01",height=2.8,
               dxfattribs={"layer":"DATRA_A1_ATRIBUTOS","prompt":"No. plano"})
text(blk,6,7,"DATRA - PLANO DE AUDITORIA CFE",2.0)

ins=layout.add_blockref("DATRA_CAJETIN_A1_V02",(699,14),dxfattribs={"layer":BORDER})
ins.add_auto_attribs({
    "NOMBRE_PLANO":"PENDIENTE", "AUDITORIA":"PENDIENTE", "ZONA":"TIJUANA, B.C.",
    "FECHA":"PENDIENTE", "ELABORO":"PENDIENTE", "REVISO":"PENDIENTE",
    "CRS":"POR VALIDAR", "TOTAL_POSTES":"--", "TOTAL_CAJAS":"--",
    "TOTAL_EXCEDENTES":"--", "ESTADO":"PRELIMINAR", "ESCALA":"S/E",
    "NUM_PLANO":"01/01",
    "CORP_TEL":"Tel. " + DATRA["telefono"],
    "CORP_EMAIL":DATRA["correo"],
    "CORP_DOMICILIO":DATRA["domicilio"],
    "CORP_WEB":DATRA["sitio"],
})

# Logotipo opcional ORIGINAL, enlazado con ruta relativa y copiado junto al DXF.
# No se genera un logo inventado ni se añade una imagen de empresa homónima.
if LOGO_INPUT is not None:
    if not LOGO_INPUT.is_file():
        raise FileNotFoundError(f"Logotipo no encontrado: {LOGO_INPUT}")
    if LOGO_INPUT.suffix.lower() not in (".png", ".jpg", ".jpeg"):
        raise ValueError("El logotipo debe ser PNG, JPG o JPEG; convertir SVG a PNG previamente")
    try:
        from PIL import Image
    except ImportError as exc:
        raise SystemExit("Para agregar logo: python -m pip install pillow") from exc
    from hashlib import sha256
    logo_ext = LOGO_INPUT.suffix.lower()
    final_logo = OUT.parent / ("logo_datra_oficial" + logo_ext)
    if LOGO_INPUT.resolve() != final_logo.resolve():
        shutil.copyfile(LOGO_INPUT, final_logo)
    with Image.open(final_logo) as im:
        w_px, h_px = im.size
        if w_px <= 0 or h_px <= 0:
            raise ValueError("Dimensiones del logotipo no válidas")
    max_w, max_h = 31.5, 16.5
    scale = min(max_w / w_px, max_h / h_px)
    w_mm, h_mm = w_px * scale, h_px * scale
    x_mm = 699 + 91 + (33 - w_mm)/2
    y_mm = 14 + 279 + (18 - h_mm)/2
    logo_def = doc.add_image_def(filename=final_logo.name, size_in_pixel=(w_px, h_px))
    layout.add_image(image_def=logo_def, insert=(x_mm, y_mm),
                     size_in_units=(w_mm, h_mm),
                     dxfattribs={"layer":"DATRA_A1_LOGO"})
    print("LOGO:", final_logo, "SHA-256:", sha256(final_logo.read_bytes()).hexdigest())
else:
    print("LOGO: sin imagen oficial local; se conserva DATRA como texto CAD editable.")


# No insertar VIEWPORT: todavía no se validaron el CRS ni los puntos de control.
doc.modelspace().add_text(
    "ARTEFACTO DE MARCO: ABRIR LAYOUT DATRA_A1 (NO HAY CARTOGRAFIA EN MODEL).",
    dxfattribs={"layer":"DATRA_A1_GUIAS_NO_PLOT", "height":8}
)

# Validación de entidades antes del guardado.
# Sólo sobreescribir el DXF objetivo; no tocar el DWG original.
doc.saveas(OUT)
re=ezdxf.readfile(OUT)
aud=re.audit()
if aud.has_errors:
    raise RuntimeError(f"Errores DXF: {len(aud.errors)}")
pp=re.layout("DATRA_A1")
print("DXF:",OUT)
print("Layout:",pp.name,"Entidades en Paper Space:",len(pp))
tags = [x.dxf.tag for x in re.blocks.get('DATRA_CAJETIN_A1_V02').query('ATTDEF')]
required = {"NOMBRE_PLANO","AUDITORIA","ZONA","FECHA","ELABORO","REVISO",
            "CRS","TOTAL_POSTES","TOTAL_CAJAS","TOTAL_EXCEDENTES","ESTADO",
            "ESCALA","NUM_PLANO","CORP_TEL","CORP_EMAIL","CORP_DOMICILIO","CORP_WEB"}
assert set(tags) == required, ("TAG faltantes", required - set(tags))
print("Cajetin: DATRA_CAJETIN_A1_V02, atributos:", tags)
print("Page:",pp.get_paper_limits())
