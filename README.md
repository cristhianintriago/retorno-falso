# 🐉 Retorno Falso: RPG de Texto Modular

> **Un juego de exploración y combate por turnos basado en lógica pura.**

![Estado del Proyecto](https://img.shields.io/badge/Estado-En_Desarrollo-yellow)
![Lenguaje](https://img.shields.io/badge/Lenguaje-Python-blue)

## 📖 Descripción

**Retorno Falso** es un RPG de consola diseñado para demostrar el manejo de lógica de programación, estructuras de datos y trabajo colaborativo modular. 

El jugador se enfrenta al reto de navegar un **mapa invisible de 5x5**, gestionando recursos limitados y combatiendo enemigos aleatorios. El objetivo es simple pero peligroso: encontrar la **Llave** y escapar con vida.

## ⚙️ Mecánicas del Juego

El juego se basa en una matriz de coordenadas $(x, y)$ donde cada movimiento es una decisión estratégica.

* **Mapa:** Una matriz 5x5 oculta al jugador.
* **Encuentros:** Cada casilla puede contener:
    * 👾 **Monstruo:** Inicia el bucle de combate.
    * 💰 **Tesoro:** Otorga ítems (pociones, armas).
    * 🗝️ **La Llave:** Objeto necesario para ganar.
    * 💨 **Nada:** Un respiro momentáneo.

---

## 🚀 Instalación y Uso

Sigue estos pasos para probar el juego en tu terminal:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/retorno-falso.git](https://github.com/tu-usuario/retorno-falso.git)
    ```
2.  **Navegar a la carpeta:**
    ```bash
    cd retorno-falso
    ```
3.  **Ejecutar el juego:**
    ```bash
    python main.py
    ```

## 📂 Estructura del Proyecto

```text
retorno-falso/
├── main.py           # El Narrador (Punto de entrada)
├── mapa.py           # El Cartógrafo
├── combate.py        # El Maestro de Combate
├── inventario.py     # El Inventario
└── README.md         # Documentación
