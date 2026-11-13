// Auditoría de funciones históricas desde COPIAS. Nunca ejecuta MAIN ni genera SCR.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const directory = path.resolve(process.argv[2]);
const allowed = new Set(['STD-MIRADOR.csv', 'STD-OTAY-FLORIDO.csv', 'quoted.csv']);
const libraries = {};
for (const name of ['generar', 'ordenar', 'trayectoria']) {
  const source = fs.readFileSync(path.join(directory, name + '.js'), 'utf8');
  const marker = source.indexOf('// MAIN');
  if (marker < 0) throw new Error('MAIN no localizado inequívocamente');
  const sandbox = {
    require(module) {
      if (module !== 'fs') throw new Error('Módulo no autorizado');
      return Object.freeze({
        readFileSync(file, encoding) {
          if (!allowed.has(file)) throw new Error('Lectura no autorizada');
          return fs.readFileSync(path.join(directory, file), encoding);
        },
        writeFileSync() { throw new Error('Escrituras históricas deshabilitadas'); }
      });
    }
  };
  vm.createContext(sandbox);
  // No se evalúa el fragmento MAIN ni se invoca generarSCR.
  vm.runInContext(source.slice(0, marker), sandbox, {timeout: 5000});
  libraries[name] = sandbox;
}
const result = {node: process.version, libraries: {}};
for (const [name, lib] of Object.entries(libraries)) {
  const cases = {};
  for (const filename of ['STD-MIRADOR.csv', 'STD-OTAY-FLORIDO.csv']) {
    const processed = lib.procesarCSV(filename);
    const points = name === 'generar' ? processed.puntos : processed;
    const filtered = lib.filtrarAislados ? lib.filtrarAislados(points) : points;
    cases[filename] = {
      parsed: points.length, filtered: filtered.length,
      inventory: processed.conteo || null,
      points: filtered,
      removed: points.map((p, i) => filtered.includes(p) ? null : i).filter(i => i !== null)
    };
    if (name !== 'generar') {
      const graph = (lib.construirGrafo || lib.crearGrafo)(filtered);
      const components = (lib.componentes || lib.obtenerComponentes)(graph);
      const routes = components.map(c => name === 'ordenar'
        ? lib.recorrerDFS(graph, lib.encontrarExtremo(c, filtered))
        : lib.ordenarTramo(c, graph));
      cases[filename].components = components.map(c => c.length);
      cases[filename].route_lengths = routes.map(r => r.length);
      cases[filename].non_edges = routes.reduce((n, r) => n + r.slice(1).filter((v, i) => !graph.get(r[i]).includes(v)).length, 0);
      cases[filename].transitions = routes.reduce((n, r) => n + Math.max(0, r.length - 1), 0);
      cases[filename].edges = [...graph.values()].reduce((n, v) => n + v.length, 0) / 2;
    }
  }
  const graph = new Map([[0,[1]], [1,[0,2,3]], [2,[1]], [3,[1]]]);
  cases.branch = name === 'ordenar' ? lib.recorrerDFS(graph, 0)
    : name === 'trayectoria' ? lib.ordenarTramo([0,1,2,3], graph) : null;
  cases.parser = ['32.5N117W', '432.464440N 116.8W', '32..5N 117W', 'junk32.5N 117Wtail'].map(t => lib.parseCoord(t));
  const quoted = lib.procesarCSV('quoted.csv');
  cases.quoted_count = (quoted.puntos || quoted).length;
  cases.thresholds = {
    filter500: lib.filtrarAislados ? lib.filtrarAislados([{x:0,y:0},{x:500,y:0}], 500).length : null,
    filter1000: lib.filtrarAislados ? lib.filtrarAislados([{x:0,y:0},{x:500,y:0}], 1000).length : null,
    colocated: lib.filtrarAislados ? lib.filtrarAislados([{x:0,y:0},{x:0,y:0}]).length : null,
    graph120: name !== 'generar' ? (lib.construirGrafo || lib.crearGrafo)([{x:0,y:0},{x:120,y:0}]).get(0).length : null,
    classifySubstring: name === 'generar' ? lib.clasificar('no-es-un-poste') : null
  };
  cases.projection = [[32.5,-117], [32.52229449,-117.02010997]].map(([lat,lon]) => ({lat,lon,...lib.latLonToUTM(lat,lon)}));
  result.libraries[name] = cases;
}
process.stdout.write(JSON.stringify(result));
