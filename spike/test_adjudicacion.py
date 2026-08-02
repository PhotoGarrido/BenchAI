"""Tests offline de la adjudicación firmada de discrepancias.

Contratos que protege:
  1. registrar es idempotente y no reabre resueltas
  2. resolver exige razón y no re-resuelve (corrección = entrada nueva)
  3. mientras está pendiente, resolucion() devuelve None (→ INVALIDA)
  4. check() cuenta pendientes (la puerta exige 0)
  5. una sustitución retira la resolución sustituida
"""

import pathlib
import tempfile

import adjudicacion as adj


def main():
    with tempfile.TemporaryDirectory() as d:
        # 1 · registrar + idempotencia
        i1 = adj.registrar("g2", "cadena7/rep2", "interpretacion",
                           {"fuente": "regex", "valor": "SI"},
                           {"fuente": "juez", "valor": "NO"},
                           contexto="paráfrasis ambigua", directorio=d)
        assert i1 == adj.registrar("g2", "cadena7/rep2", "interpretacion",
                                   {}, {}, directorio=d)
        pend, res = adj.cargar(d)
        assert len(pend) == 1 and not res, "idempotencia rota"

        # 3 · pendiente → None (INVALIDA para los análisis)
        assert adj.resolucion("g2", "cadena7/rep2", "interpretacion",
                              directorio=d) is None

        # 4 · la puerta ve la pendiente
        assert adj.check(d) == 1

        # 2 · sin razón no hay resolución
        try:
            adj.resolver(i1, "SI", "   ", "david", directorio=d)
            raise AssertionError("resolvió sin razón")
        except ValueError:
            pass

        fila = adj.resolver(i1, "SI", "el juez ignora la negación elidida",
                            "david", directorio=d)
        assert fila["decisor"] == "david" and fila["decision"] == "SI"
        assert adj.check(d) == 0
        r = adj.resolucion("g2", "cadena7/rep2", "interpretacion",
                           directorio=d)
        assert r and r["decision"] == "SI" and r["razon"]

        # 2b · re-resolver prohibido
        try:
            adj.resolver(i1, "NO", "cambio de opinión", "david", directorio=d)
            raise AssertionError("re-resolvió una resuelta")
        except ValueError:
            pass

        # 1b · registrar de nuevo NO reabre la resuelta
        adj.registrar("g2", "cadena7/rep2", "interpretacion", {}, {},
                      directorio=d)
        assert adj.check(d) == 0, "reabrió una resuelta"

        # 5 · corrección por sustitución: la entrada nueva retira la vieja
        # y pasa a ser la vigente
        adj._anadir(pathlib.Path(d) / "resueltas.jsonl", {
            "id": "corr-" + i1, "sustituye_a": i1, "experimento": "g2",
            "registro": "cadena7/rep2", "medida": "interpretacion",
            "decision": "NO", "razon": "revisión posterior con más contexto",
            "decisor": "david", "fecha_resolucion": "2026-08-02T00:00:00"})
        vigente = adj.resolucion("g2", "cadena7/rep2", "interpretacion",
                                 directorio=d)
        assert vigente and vigente["decision"] == "NO" \
            and vigente["id"] == "corr-" + i1, \
            "la sustitución no desplazó a la resolución original"

    print("test_adjudicacion: 5 contratos OK")


if __name__ == "__main__":
    main()
