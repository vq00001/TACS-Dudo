# TACS-Dudo

[![Tests](https://github.com/vq00001/TACS-Dudo/actions/workflows/tests.yml/badge.svg)](https://github.com/vq00001/TACS-Dudo/actions)
[![Coverage](https://img.shields.io/badge/coverage-check%20latest-blue)](https://github.com/vq00001/TACS-Dudo)

## Grupo 16

- **Javier Torres Ortiz**
- **Valeria Quiroga Carrere** 
- **Joseph Matamala Sepúlveda**

## Instalación y Configuración

### Prerrequisitos

- Python 3.9 o superior
- pip

### Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/vq00001/TACS-Dudo.git
   cd TACS-Dudo
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## Ejecutar el Juego
```bash
python main.py
```
## Resumen de las reglas básicas
### SETUP
- Dos o más jugadores.
- Cada turno se tiran los dados.
- Se tienen 5 dados por jugador al comenzar. Si gana uno extra y ya tiene 5, queda con uno a favor, de modo de reserva a la espera de que pierda alguno para ingresarlo al juego.
- El primer jugador se decide por el mayor numero al tirar un dado, y él decide hacia qué direccion se avanza. 
- El juego termina cuando solo queda un jugador con dados en su cacho.

### JUEGO
Pintas: **1** (As), **2** (Tonto), **3** (Tren), **4** (Cuadra), **5** (Quina), **6** (Sexto). 

- El jugador que pierde o recoja un dado comienza en la siguiente ronda.

#### Tipos de acciones

- Apostar: Solo se puede elevar la apuesta anterior, ya sea en apariciones o pintas. No se puede empezar con As a menos que se tenga un solo dado.

- Dudar: Si existe un número igual o mayor de dados con la pinta especulada en la apuesta, quién dudó pierde un dado, de lo contrario la persona que efectuó la apuesta lo pierde. 

- Calzar: Si el número de apariciones es exactamente el mismo, la persona que calzó gana un dado, de lo contrario pierde un dado. 
> Limitación: Solo se puede calzar cuando queden la mitad o más de los dados en juego, o cuando el jugador que desea calzar tenga solo un dado.</i> 

- Pasar: Si se duda después de que alguien pase, se está dudando el pase. El siguiente jugador apuesta sobre la última apuesta hecha (antes del jugador que pasó). 
>Limitaciones: Solo puede pasar un jugador con <b>"full"</b> (3 dados de igual pinta y los otros 2 dados de igual pinta) o un jugador con los cinco dados iguales. **|** No pueden pasar dos jugadores consecutivos.</i>

#### Ases
Son comodines y siempre se les asigna el valor del la pinta que se esté apostando, <u><i>con la excepción de rondas obligadas.</i></u>

- Rebajar la apuesta: Si la pinta es cualquiera distinta de As, se puede bajar la pinta a As cambiando su cantidad de apariciones a la mitad + 1 si par, o mitad aproximado hacia arriba si impar. 

- Subir la apuesta con As: Si se está apostando con Ases y se quiere cambiar de pinta hacia arriba, debe ser al doble + 1 (o más) de las apariciones.

#### Obligar
Cuando un jugador queda con un solo dado **por primera vez** puede optar por jugar una ronda especial de dos tipos. En esta los ases valen como 1 y no sirven como comodin.    

- Ronda abierta: Los jugadores deben mostrar sus dados y ver los de los demás pero no los propios. 

- Ronda cerrada: Solo el jugador que obliga la ronda puede ver sus propios dados, el resto no ve nada.
