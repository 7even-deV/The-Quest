# The Quest (Pygame)


## Descripción

Este es el repositorio de código `The-Quest` para el __proyecto final Bootcamp Zero de KeepCoding__.

El juego consiste en la búsqueda de nuevos planetas para colonizarlos.
Durante el transcurso del viaje aparecerán desafíos, ya sean naves enemigas u oleadas de meteoritos.
Cada nivel constará de 1 minuto más de viaje y cada desafío aumentará en número y velocidad.
El jugador dispondrá de munición de balas y carga de misiles para afrontar los desafíos durante el viaje.
Propulsor que reducirá el tiempo de viaje a la mitad aunque no podrá moverme mientras esté activo.
Y una barra de salud más 3 vidas extra. Si consume todas las vidas perderá la partida.

#
## Informacion del repositorio

Realizado por:

| Nombre | Email |
| ---- | ---- |
| [Sergio Fuentes (Seven)](https://www.linkedin.com/in/sergio-fuentes/)  | Seven-z01@outlook.com |


En el transcurso de las 3 semanas para realizar el proyecto final del curso he completado The Quest v1.0.
Utilicé varias herramientas objeto prediseñados para una funcionalidad mejorada y eficiente durante el desarrollo del juego. De los más útiles a destacar fue el objeto Sprite sheet que me facilitó la descarga de cualquier imagen y la creación de instancias heredando todas sus características como objeto base. Un objeto con 4 tipos diferentes de temporizadores múltiples. Un algoritmo muy reducido que me permitía moverme entre las escenas del juego en cualquier sentido. Un objeto que controla consultas CRUD con SQLite registrando los datos de cada jugador en todo momento. También creé botones, barras, tablero y teclado entre otros para facilitar y mejorar la interactividad del usuario. Y múltiples ideas que preferí mostrar y sorprender durante la experiencia del juego.

Para abrir el juego, hay que lanzar `run.pyw`, teniendo previamente descargados todos los archivos del repositorio.

#
## Estructura del repositorio

- `Assets`: Carpeta que contiene todos los activos del juego.

  - `Audio`: Contiene la música de cada escena y los sonidos fx del juego en formato __.ogg__.
  - `Data`: Contiene __.db__ como base de datos de jugadores. La tabla almacena estilo y modelo de barco, último nivel y nivel máximo, último puntaje y puntaje máximo.
  - `Fonts`: Diferentes __.ttf__ para los estilos de fuente proporcionados por el juego.
  - `Images`: Tiene las imágenes __.png__ y __.jpg__ tipo hojas de sprite.
  - `Scripts`: Aquí están todos los códigos __.py__ que utiliza el juego para generar los datos del código del juego.

    - `controller`: Controla todas las escenas a través de sus bucles principales. Les da los atributos que a su vez recoge de la escena anterior.
    - `database`: Clase DataBase donde conecta los datos del juego a la base de datos a través de las funciones CRUD.
    - `documents`: Guarda los documentos credits, history y guide en forma de string, se muestran en el menú principal del juego.
    - `enemies`: Clase Enemy que estructura todas las características de los enemigos. Hay 3 tipos de IA: patrulleros, velocistas y kamikazes.
    - `environment`: Contiene las clases Foreground, Background, Farground, Planet y Portal. Se encargan de la ambientación y acompañan el movimiento del jugador.
    - `manager`: Importador de todas las cargas de música, sonidos e imágenes del juego.
    - `obstacles`: Clase Meteor que estructura toda la funcionalidad de los meteoros.
    - `players`: Clase Player que estructura todas las características y funcionalidades del jugador según el estilo que elijas. Hay 3 estilos: Daño, Defensa y Curación.
    - `scenes`: Contiene las clases Main, Menu, Game y Record que heredan de la clase Scene. Se encargan de controlar el comportamiento del juego en cada escena.
    - `settings`: Guarda todas las constantes del juego. Los ajustes se especifican desde aquí.
    - `tools`: Contiene las clases Timer, Sprite_sheet, Button, Board, Bar, Keyboard, Canvas, Icon, HealthBar y Screen_fade. Se utilizan como herramientas y componentes accesorios.
    - `weapons`: Contiene las clases Bullet, Missile y Explosion. Tipos de armas que puede utilizar cualquier personaje. Explosion es una extensión de Missile.

  - `main`: Archivo __.py__ como lanzador alternativo del juego.

- `commits`: Archivo __.md__ registra todos los commits del repositorio.
- `requirements`: Archivo __.txt__ registra los requisitos para abrir el juego: pygame v2.0.2.
- `run`: Archivo __.pyw__ es el lanzador principal del juego.
