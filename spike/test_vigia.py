"""Tests offline de la lógica de decisión del vigía de baterías."""

from vigia import decidir


def main():
    # Batch cerrado: el manifest manda, haya o no proceso.
    assert decidir({"fin": "2026-08-01T14:00:00", "completo": True},
                   hay_proceso=False, segundos_sin_senal=9999) == "terminada"
    assert decidir({"fin": "2026-08-01T14:00:00", "completo": False,
                    "fallos": [["m", "asch"]]},
                   hay_proceso=False,
                   segundos_sin_senal=0) == "terminada_con_fallos"

    # Proceso vivo → nunca relanzar (aunque la señal sea vieja: un
    # experimento largo puede tardar en escribir).
    assert decidir({}, hay_proceso=True, segundos_sin_senal=99999) == "activa"

    # Sin proceso ni cierre: margen dentro del umbral, reanudar después.
    assert decidir({}, hay_proceso=False, segundos_sin_senal=30,
                   umbral=600) == "esperar"
    assert decidir({}, hay_proceso=False, segundos_sin_senal=601,
                   umbral=600) == "reanudar"

    # El umbral es parametrizable (launchd con pasadas espaciadas).
    assert decidir({}, hay_proceso=False, segundos_sin_senal=61,
                   umbral=60) == "reanudar"

    print("test_vigia: decisiones OK")


if __name__ == "__main__":
    main()
