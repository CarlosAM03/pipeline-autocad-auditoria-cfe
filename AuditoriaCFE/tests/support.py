"""Fixtures OOXML mínimos generados en runtime; no se versionan XLSX."""
import sys
import json
import shutil
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "src"))
from auditoriacfe.config import AUDITS
from auditoriacfe.util import within

NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
HEADERS = {
    1: {"A": "Nombre", "B": "elemento", "C": "coordenandas completas", "D": "Coordenadas N", "E": "Coordenadas W"},
    2: {"A": "Ruta ", "B": "Elemento de Red ", "C": "Coordenadas", "D": "Foto"},
    3: {"A": "Numero", "B": "Nombre ruta", "C": "Elemento de red", "D": "Coordenadas", "E": "Fotos"},
    4: {"B": "Ruta", "C": "Elemento de red", "D": "Coordenadas", "E": "Foto"},
}
GEO = dict(lat_min="32", lat_max="33", lon_min="-118", lon_max="-116", aprobada=True,
           evidencia="FIXTURE SINTÉTICO; no acredita perímetro operativo")


def xml_row(number, cells, hidden=False):
    result = [f'<row r="{number}" hidden="{int(hidden)}">']
    for col, item in cells.items():
        if isinstance(item, dict):
            typ = item.get("tipo", "n")
            formula = ""
            if "formula" in item:
                attrs = "".join(f" {k}={quoteattr(str(v))}" for k, v in item.get("attrs", {}).items())
                formula = f'<f{attrs}>{escape(item["formula"])}</f>'
            val = f'<v>{escape(str(item["valor"]))}</v>' if item.get("valor") is not None else ""
            result.append(f'<c r="{col}{number}" t="{typ}">{formula}{val}</c>')
        else:
            result.append(f'<c r="{col}{number}" t="inlineStr"><is><t xml:space="preserve">{escape(str(item))}</t></is></c>')
    return "".join(result) + "</row>"


def xlsx(path, family=3, rows=None, blank_d=False, empty=False, images=False, dimension=None, physical_rows=0, sheets=None, shared=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    header = dict(HEADERS[family])
    if blank_d:
        del header["D"]
    if rows is None:
        rows = [(2, record(family), False)]
    if sheets is None:
        sheets = [("Datos", [] if empty else [(1, header, False)] + rows)]
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("xl/workbook.xml", f'<workbook xmlns="{NS}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>' + "".join(f'<sheet name={quoteattr(n)} sheetId="{i}" r:id="r{i}"/>' for i, (n, _) in enumerate(sheets, 1)) + '</sheets></workbook>')
        z.writestr("xl/_rels/workbook.xml.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(f'<Relationship Id="r{i}" Target="worksheets/sheet{i}.xml" Type="worksheet"/>' for i in range(1, len(sheets) + 1)) + '</Relationships>')
        if shared is not None:
            z.writestr("xl/sharedStrings.xml", f'<sst xmlns="{NS}">' + "".join(f'<si><t>{escape(s)}</t></si>' for s in shared) + '</sst>')
        for i, (name, data) in enumerate(sheets, 1):
            with z.open(f"xl/worksheets/sheet{i}.xml", "w") as stream:
                stream.write(f'<worksheet xmlns="{NS}">'.encode())
                if dimension:
                    stream.write(f'<dimension ref="{dimension}"/>'.encode())
                stream.write(b'<sheetData>')
                for num, cells, hidden in data:
                    stream.write(xml_row(num, cells, hidden).encode())
                start = max((r[0] for r in data), default=0) + 1
                for start_batch in range(start, physical_rows + 1, 4096):
                    stream.write("".join(f'<row r="{n}" s="1"/>' for n in range(start_batch, min(start_batch + 4096, physical_rows + 1))).encode())
                stream.write(b'</sheetData></worksheet>')
        if images:
            z.writestr("xl/media/image1.png", b"THIS IS NOT AN IMAGE; MUST NEVER BE DECODED" * 1000)
            z.writestr("xl/drawings/drawing1.xml", b"DRAWING MUST NOT BE OPENED")
    return path


def record(family=3, route="Ruta", typ="poste", coord="32.500000N 117.000000W", extras=None):
    columns = ("A", "B", "C") if family in (1, 2) else ("B", "C", "D")
    return {**dict(zip(columns, (route, typ, coord))), **(extras or {})}


class AuditFixture:
    def __init__(self):
        AUDITS.mkdir(exist_ok=True)
        self.path = Path(tempfile.mkdtemp(prefix="TestProceso1_", dir=AUDITS))
        (self.path / "entrada").mkdir()
        self.cfg = dict(auditoria=self.path.name, fuentes_en_orden=["a.xlsx"], geografia_permitida=GEO)

    def save(self, **changes):
        self.cfg.update(changes)
        (self.path / "configuracion.json").write_text(json.dumps(self.cfg, ensure_ascii=False), encoding="utf-8")
        return self

    def close(self):
        path = within(self.path, AUDITS)
        if not path.name.startswith("TestProceso1_"):
            raise RuntimeError("No borrar una auditoría operativa")
        shutil.rmtree(path)
