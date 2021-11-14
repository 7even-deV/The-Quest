# The Quest (Pygame)


## Descripción

Este es el repositorio de código `The-Quest` para el __proyecto final Bootcamp Zero de KeepCoding__.

El juego está desarrollado en 2D, con perspectiva top-down. Su temática es apocalíptica, futurista y alienígena.
Consiste en la búsqueda de nuevos planetas para colonizarlos.
Los desafíos aparecerán durante el transcurso del viaje, ya sean naves enemigas u olas de meteoritos.
Cada amenaza obtendrá un lote de ítem aleatorio que, dependiendo de su dificultad (escala),
dará una probabilidad de generarlo o no, la variedad de ítems supera actualmente los 10.
Cada nivel constará de 1 minuto más de viaje y sus desafíos aumentarán en número y velocidad.
La nave del jugador dispondrá de munición de balas y carga de misiles, para afrontar los retos durante el viaje.
También un propulsor, que reducirá a la mitad el tiempo de viaje transcurrido. Y una barra de salud más 3 vidas extra.
Hay 3 tipos diferentes de modelos de naves, cada uno con una mejora específica,
pudiendo potenciar cualquier habilidad durante el juego,
algunos de estos serán cancelados si ocurre una colisión y otros si destruyen la nave.
Si consume todas las vidas, perderá en el juego.

#
## Informacion del repositorio

Realizado por:

| Nombre | Email |
| ---- | ---- |
| [Sergio Fuentes (Seven)](https://www.linkedin.com/in/sergio-fuentes/)  | Seven-z01@outlook.com |


En el transcurso de las primeras 3 semanas para completar la primera entrega del proyecto final del curso, completé The Quest v1.0.
Posteriormente, durante las próximas 3 semanas para la segunda entrega, completé The Quest v2.0.
Utilicé varias herramientas objeto prediseñados para una funcionalidad mejorada y eficiente durante el desarrollo del juego. De los más útiles a destacar fue el objeto Sprite sheet que me facilitó la descarga de cualquier imagen y la creación de instancias heredando todas sus características como objeto base. Un objeto con 4 tipos diferentes de temporizadores múltiples. Un algoritmo muy reducido que me permitía moverme entre las escenas del juego en cualquier sentido. Un objeto que controla consultas CRUD con SQLite registrando los datos de cada jugador en todo momento. También desarrollé objetos de clase para botones, barras, tablero, teclado y partículas, entre otros, para facilitar y mejorar la interactividad del usuario. Y múltiples ideas que preferí mostrar y sorprender durante la experiencia del juego.

Para abrir el juego, debes ejecutar `run.exe`, habiendo descargado previamente este archivo junto con su carpeta __Assets__ del repositorio.
No requiere dependencias externas ya que dicho archivo lleva compilado todos los requisitos para abrir el juego: pygame v2.1.0, válido para cualquier sistema operativo.

#
## Estructura del repositorio

- `Assets`: Carpeta que contiene todos los activos del juego.

  - `Audio`: Contiene la música de cada escena y los sonidos fx del juego en formato __.ogg__.
  - `Data`: Contiene __.db__ como base de datos de jugadores. La tabla almacena todos los registros de cada jugador creado.
  - `Fonts`: Diferentes __.ttf__ para los estilos de fuente proporcionados por el juego.
  - `Images`: Tiene las imágenes __.png__ y __.jpg__ tipo hojas de sprite.
  - `Scripts`: Aquí están todos los códigos __.py__ que utiliza el juego para generar los datos del código del juego.

    - `controller`: Controla todas las escenas a través de sus bucles principales. Les da los atributos que a su vez recoge de la escena anterior.
    - `database`: Clase DataBase donde conecta los datos del juego a la base de datos a través de las funciones CRUD.
    - `documents`: Guarda los documentos credits, history y guide en forma de string, se muestran en el menú principal del juego.
    - `enemies`: Clase Enemy que estructura todas las características de los enemigos. Hay 3 tipos de IA: patrulleros, velocistas y kamikazes.
    - `environment`: Contiene las clases Foreground, Background, Farground, Planet y Portal. Se encargan de la ambientación y acompañan el movimiento del jugador.
    - `items`: Contiene la clase Item que genera la lista aleatoria de cada tipo de ítem, más la clase Freeze como funcionalidad si se obtiene.
    - `manager`: Importador de todas las cargas de música, sonidos e imágenes del juego.
    - `obstacles`: Clase Meteor que estructura toda la funcionalidad de los meteoros.
    - `players`: Clase Player que estructura todas las características y funcionalidades del jugador según el estilo que elijas. Hay 3 estilos: Daño, Defensa y Velocidad.
    - `scenes`: Contiene las clases Main, Menu, Load, Game y Record que heredan de la clase Scene. Se encargan de controlar el comportamiento del juego en cada escena.
    - `settings`: Guarda todas las constantes del juego. Los ajustes se especifican desde aquí.
    - `tools`: Contiene las clases Timer, View, Sprite_sheet, Logo, Button, Keyboard, Bar, Board, Canvas, Icon, Health_bar, Screen_fade y Particles. Se utilizan como herramientas y componentes accesorios.
    - `weapons`: Contiene las clases Bullet, Missile y Explosion. Tipos de armas que puede utilizar cualquier personaje. Explosion es una extensión de Missile.

  - `main`: Archivo __.py__ como lanzador alternativo del juego, (requiere dependencias del requirements.txt).
  - `template`: Archivo __.py__ probador de funcionalidad del mismo juego. "Me pareció útil dejarlo para aumentar su alternativa experiencia".

- `commits`: Archivo __.md__ registra todos los commits del repositorio.
- `requirements`: Archivo __.txt__ registra los requisitos para abrir el juego: pygame v2.1.0.
- `run`: Archivo __.exe__ es el lanzador principal del juego.
- `setup`: Archivo __.py__ registra los datos relacionados con el juego y el desarrollador.
