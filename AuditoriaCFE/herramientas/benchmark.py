"""Benchmark reproducible de carga sintética; mide proceso, no promete SLA."""
import argparse
import ctypes
import json
import os
import platform
import sys
import time
from pathlib import Path

PROJECT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(PROJECT/'src'),str(PROJECT/'tests')]


def metrics():
    if os.name=='nt':
        from ctypes import wintypes
        class Memory(ctypes.Structure):
            _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(n,ctypes.c_size_t) for n in
                      ('PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage',
                       'QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage')]
        class IO(ctypes.Structure):
            _fields_=[(n,ctypes.c_ulonglong) for n in ('ReadOperationCount','WriteOperationCount','OtherOperationCount',
                       'ReadTransferCount','WriteTransferCount','OtherTransferCount')]
        kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        kernel.GetCurrentProcess.restype=wintypes.HANDLE
        process=kernel.GetCurrentProcess();m=Memory();m.cb=ctypes.sizeof(m);io=IO()
        psapi=ctypes.WinDLL('psapi',use_last_error=True)
        psapi.GetProcessMemoryInfo.argtypes=[wintypes.HANDLE,ctypes.POINTER(Memory),wintypes.DWORD]
        kernel.GetProcessIoCounters.argtypes=[wintypes.HANDLE,ctypes.POINTER(IO)]
        if not psapi.GetProcessMemoryInfo(process,ctypes.byref(m),m.cb) or not kernel.GetProcessIoCounters(process,ctypes.byref(io)):
            raise OSError(ctypes.get_last_error(),'No se pudieron medir contadores nativos')
        return dict(rss_pico_bytes=m.PeakWorkingSetSize,lectura_os_bytes=io.ReadTransferCount,escritura_os_bytes=io.WriteTransferCount)
    import resource
    r=resource.getrusage(resource.RUSAGE_SELF)
    return dict(rss_pico_bytes=int(r.ru_maxrss*(1 if sys.platform=='darwin' else 1024)),
                lectura_os_bytes=r.ru_inblock*512,escritura_os_bytes=r.ru_oublock*512)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--filas-xml',type=int,default=1000000)
    parser.add_argument('--elementos',type=int,default=10000)
    args=parser.parse_args(argv)
    if not 1<=args.elementos<=100000 or not args.elementos+1<=args.filas_xml<=1048576:
        parser.error('Requiere 1..100000 elementos y dimension física elementos+1..1048576')
    from support import AuditFixture,xlsx,record
    from auditoriacfe.pipeline import run
    from auditoriacfe.reporting import verify
    from auditoriacfe.util import json_text
    fixture=AuditFixture()
    try:
        path=fixture.path/'entrada/a.xlsx'
        rows=[(i+2,record(route='SINTETICA-'+str(i%14),coord=f'32.{500000+i:06d}N 117.000000W'),False)
              for i in range(args.elementos)]
        created=time.perf_counter()
        xlsx(path,rows=rows,physical_rows=args.filas_xml,dimension='A1:XFD1048576',images=True)
        creation=time.perf_counter()-created
        fixture.save(schema_02=2)
        before=metrics();cpu=time.process_time();clock=time.perf_counter()
        manifest=run(fixture.path,emit=lambda *a:None)
        verify(fixture.path)
        elapsed=time.perf_counter()-clock;cpu=time.process_time()-cpu;after=metrics()
        if manifest['conteos']['filas_csv_00']!=args.elementos:raise AssertionError('Conteos del benchmark no concilian')
        result=dict(python=platform.python_version(),plataforma=platform.platform(),filas_xml=args.filas_xml,
                    componentes=args.elementos,xlsx_bytes=path.stat().st_size,generacion_s=creation,
                    pipeline_y_verificacion_s=elapsed,cpu_s=cpu,rss_pico_proceso_bytes=after['rss_pico_bytes'],
                    lectura_os_delta_bytes=after['lectura_os_bytes']-before['lectura_os_bytes'],
                    escritura_os_delta_bytes=after['escritura_os_bytes']-before['escritura_os_bytes'],
                    io_definicion='Windows: transferencias logicas del proceso; Unix: bloques fisicos reportados por getrusage',
                    estado='OK_SINTETICO_NO_SLA')
        output=PROJECT/'tests/_runtime';output.mkdir(exist_ok=True)
        (output/'benchmark.json').write_text(json_text(result),encoding='utf-8')
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    finally:fixture.close()


if __name__=='__main__':raise SystemExit(main())
