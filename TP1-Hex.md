# Trabajo Práctico 1: Engine de Hex


## Introducción

[Hex](https://es.wikipedia.org/wiki/Hex_(board_game)) es un juego de estrategia en el que dos jugadores colocan fichas en un tablero hexagonal con el objetivo de conectar lados opuestos con una cadena ininterrumpida de sus fichas. Un jugador juega con fichas rojas y debe conectar los lados superior e inferior, mientras que el otro juega con fichas azules y debe conectar los lados izquierdo y derecho.
## Objetivo

El objetivo de este trabajo práctico es desarrollar un agente inteligente capaz de jugar al Hex. Se evaluará la eficiencia del agente en términos de su rendimiento durante las partidas de prueba y su habilidad para implementar estrategias de juego avanzadas.

## Rating

Para evaluar el desempeño de los agentes, utilizaremos el sistema de rating [Trueskill](https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/). Este sistema asigna una puntuación a cada agente en base a los enfrentamientos de cada agente contra los demás participantes.

## Recomendaciones

Antes de comenzar con la implementación de su agente, recomendamos realizar pruebas con un tablero más pequeño para facilitar la identificación y corrección de errores.

## Forma de trabajo

La forma de trabajo para este trabajo práctico será la siguiente:

1. Hacer un fork del repositorio del trabajo práctico en GitHub. Esto creará una copia del repositorio en tu cuenta de GitHub.
1. Clonar el repositorio _forked_ en tu entorno local.
1. Desarrollar el código del agente en tu entorno local.
1. Realizar commits y pushs frecuentes a tu repositorio forked para mantener un registro de tus cambios.
1. Cuando hayas terminado, crear una rama (_branch_) para esa entrega, realizar un pull request desde tu repositorio forked hacia el repositorio original. Esto enviará tu código para su revisión y evaluación.

**Nota:**  La rama que se intente _mergear_ mediante el pull request debe contener exclusivamente el código fuente del agente y ningún otro archivo más. Cualquier _merge conflict_ o archivo extra será calificado negativamente.

## Entregables

El entregable para cada fase será el código del agente desarrollado en Python 3.11 . Asegúrese de que su código esté bien comentado y sea fácil de entender. No es necesario un informe, pero se espera que cualquier decisión de diseño o implementación importante esté claramente explicada en los docstrings y comentarios del código.

### Checkpoint 0: Comprendiendo las interfaces del juego

Para el checkpoint, es necesario demostrar que se han entendido las interfaces de juego provistas por la cátedra. Su agente deberá ser capaz de interactuar con la interfaz de juego de [OpenAI Gym/Gymnasium](https://gymnasium.farama.org/) para realizar movimientos válidos en el tablero, es decir, movimientos que no impliquen poner una ficha en una posición ocupada. La estrategia de este agente puede ser cualquiera, incluso random. El agente se debe ajustar al tamaño del tablero que se esté utilizando en el momento de la ejecución.

**Fecha de control**: Domingo 16 de Marzo a las 23:59

### Entrega Final: Agente Avanzado

Para la entrega final se espera un agente que tenga comportamientos avanzados y como mínimo sea capaz de ganarle a todos los agentes de ejemplo provistos por la cátedra sin problemas.
**Fecha de entrega**: Domingo 13 de Abril a las 23:59

### Entregas continuas

Durante el desarrollo del trabajo práctico, el repositorio estará disponible para hacer entregas continuas de los agentes mediante PRs para que sean evaluados periódicamente contra los demás agentes. Esto permitirá evaluar el desempeño de los agentes y realizar ajustes en el código para mejorar su rendimiento.

## Especificaciones

### Interfaz de juego

Se debe crear una carpeta con el apellido del alumno, por ejemplo para el alumno de apellido "turing" sería `scripts/agents/turing`. Dentro de esta carpeta se debe crear un archivo `turingAgent.py` que contenga la implementación del agente descrita a continuación. En esa misma carpeta se pueden agregar otros archivos que contengan código auxiliar.

Se debe implementar una clase con al menos los siguientes métodos:

```python
agent.action(obs)
agent.name() # Diccionario con nombre apellido y legajo del alumno
agent.__str__() # Nombre del agente (elija lo que quiera)
agent.reset() # Reinicia el estado del agente 
```

Estos métodos se utilizarán de la siguiente manera:

```python
import gymnasium as gym
import hex_udesa
from agents.turing.turingAgent import TuringAgent # remplazar turing por SU apellido

env = gym.make('hex_udesa/Hex-v0', render_mode='human')
board,info = env.reset()
agent = TuringAgent()
print(agent.name())
print(str(agent))
```

```sh
>> {nombre:'Alan', apellido:'Turing', legajo:123456}
>> Hex-Runner 2049
```

```python
agent.reset()
terminated, truncated = False, False
while not terminated and not truncated:
    action = agent.action(board)
    board, reward, terminated, truncated, info = env.step(action)
```
### Requerimientos
- Límite de tiempo de ejecución de cada movimiento: **2 segundos**
- Límite de creación del objeto agente: **2 segundos**
- El agente debe correr en un solo hilo de ejecución (no multithreading)
- No está permitido el uso de librerías de aceleración como Numba o Cython
- No se deben exceder los **20Mb de datos pre-computados**, (en ningun momento puede haber mas de 20 Mb en la carpeta con su apellido)
- No se deben exceder los **500Mb de RAM**


## Evaluación

El trabajo será evaluado en un torneo organizado por la cátedra, donde se asignará un rating a los agentes basado en su desempeño. El rating será calculado utilizando el sistema TrueSkill en un torneo de tipo suizo en tablero de 13x13.


El primer checkpoint debe estar aprobado para poder entregar el TP. Si no lo cumplieran en tiempo se restará entre 0 y 1 punto de la nota final. 

Para aprobar, el agente debe tener un **rating superior al de todos los agentes de prueba provistos por la cátedra**.

La nota final se calculará de la siguiente forma:
- **2 puntos** por claridad y legibilidad del código
- **8 puntos** por la implementación y uso correcto de las técnicas vistas en clase

Y si el agente obtiene una nota aprobada:
- **puntos bonus** calculados con la siguiente fórmula:

$`
Bonus = \min \left\{\frac{(\text{Rating} - \text{Rating\_min})}{5} + 0.5 * \text{bounty}, 4 \right\}
`$

Donde `Rating` es el rating del su agente, `Rating_min` es el rating del mejor agente de ejemplo provisto por la cátedra, `bounty` es la cantidad de issues del repositorio de github resueltos por el alumno luego de coordinar con los profesores. 

Este trabajo debe ser realizado individualmente. ¡Buena suerte!
