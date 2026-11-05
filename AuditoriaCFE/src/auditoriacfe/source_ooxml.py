"""Solo ZIP/XML de celdas; nunca abre medios, dibujos, macros ni enlaces.

Memoria: una fila XML + sharedStrings (límite explícito de 16 MiB XML).
Los registros operativos posteriores sí se retienen para consolidación.
"""
import posixpath
import re
import zipfile
from xml.etree import ElementTree as ET

from .util import PipelineError

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
MAX_META = 16 * 1024 * 1024


def small_xml(book, name):
    if book.getinfo(name).file_size > MAX_META:
        raise PipelineError(f"Metadatos OOXML exceden límite de {MAX_META} bytes: {name}")
    return ET.fromstring(book.read(name))


class Workbook:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.book = zipfile.ZipFile(self.path, "r")
        try:
            if len(self.book.namelist()) != len(set(self.book.namelist())):
                raise PipelineError("Partes ZIP duplicadas: libro ambiguo")
            rels = small_xml(self.book, "xl/_rels/workbook.xml.rels")
            targets = {}
            for rel in rels:
                if rel.get("TargetMode") == "External":
                    continue
                target = rel.get("Target", "")
                target = posixpath.normpath(target.lstrip("/") if target.startswith("/")
                                             else posixpath.join("xl", target))
                if not target.startswith("xl/") or "\\" in target:
                    raise PipelineError("Relación OOXML fuera de xl/")
                targets[rel.get("Id")] = target
            wb = small_xml(self.book, "xl/workbook.xml")
            self.sheets = [(s.get("name"), targets[s.get(REL)], s.get("state", "visible"))
                           for s in wb.findall(f"{NS}sheets/{NS}sheet")]
            names = [s[0] for s in self.sheets]
            if len(names) != len(set(names)):
                raise PipelineError("Nombres de hoja duplicados")
            self.strings = []
            if "xl/sharedStrings.xml" in self.book.namelist():
                sst = small_xml(self.book, "xl/sharedStrings.xml")
                self.strings = ["".join(t.text or "" for t in si.iter(NS + "t")) for si in sst]
            self.media_count = sum(n.startswith("xl/media/") and not n.endswith("/")
                                   for n in self.book.namelist())
            return self
        except BaseException:
            self.book.close()
            raise

    def __exit__(self, *args):
        self.book.close()

    def rows(self, part, stats):
        stats.update(filas_xml=0, filas_con_valor=0, formulas=0, formulas_sin_cache=0)
        previous = 0
        with self.book.open(part, "r") as stream:
            # Eliminar cada row del padre evita retener un millón de nodos vacíos.
            stack = []
            for event, node in ET.iterparse(stream, events=("start", "end")):
                if event == "start":
                    stack.append(node)
                    continue
                if node.tag == NS + "row":
                    rownum = int(node.get("r", "0"))
                    if rownum <= previous:
                        raise PipelineError("Filas OOXML sin orden ascendente inequívoco")
                    previous = rownum
                    stats["filas_xml"] += 1
                    cells = {}
                    for cell in node.findall(NS + "c"):
                        address = cell.get("r", "")
                        match = re.fullmatch(r"([A-Z]+)([0-9]+)", address)
                        if not match or int(match[2]) != rownum or match[1] in cells:
                            raise PipelineError(f"Referencia de celda ambigua: {address}")
                        typ = cell.get("t", "n")
                        raw = cell.findtext(NS + "v", "")
                        formula = cell.find(NS + "f")
                        value = raw
                        if typ == "s" and raw:
                            index = int(raw)
                            if not 0 <= index < len(self.strings):
                                raise PipelineError(f"Índice sharedString inválido: {address}")
                            value = self.strings[index]
                        elif typ == "inlineStr":
                            value = "".join(t.text or "" for t in cell.iter(NS + "t"))
                        if formula is not None:
                            stats["formulas"] += 1
                            stats["formulas_sin_cache"] += not bool(value)
                        if value or formula is not None:
                            cells[match[1]] = dict(valor=value, valor_xml=raw, tipo_celda=typ,
                                                  formula_xml=formula.text if formula is not None else None,
                                                  formula_atributos=dict(formula.attrib) if formula is not None else None,
                                                  es_formula=formula is not None)
                    hidden = node.get("hidden") in ("1", "true")
                    stack[-2].remove(node)
                    node.clear()
                    if cells:
                        stats["filas_con_valor"] += any(c["valor"] for c in cells.values())
                        yield rownum, cells, hidden
                stack.pop()


def value(cells, column):
    return cells.get(column, {}).get("valor", "") if column else ""
