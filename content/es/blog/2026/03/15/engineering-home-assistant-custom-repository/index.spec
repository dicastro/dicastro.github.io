Quiero que redactes el post de acuerdo a los requisitos e incluyendo el contenido, no omitas contenido, tampoco te inventes contenido, cíñete exactamente a lo que se menciona en la especificación. Si hay más detalles que quieras conocer para mejorar la redacción, PREGUNTALO, y completo esta especificación para que lo puedas generar de nuevo.

--- Requisitos de Redacción

* Público Objetivo: Personas entusiastas del self-hosting que valoran el equilibrio entre control y tiempo personal
* Tono: Sincero, técnico y reflexivo. Debe transmitir la capacidad crítica, de analizar la solución actual, ver los inconvenientes/mejoras/debilidades y replantearse un cambio con el espíritu de mejorar. Debe transmitir la autoridad de quien sabe montar un sistema complejo (como proxmox, virtualizacion con docker, automatizado con ansible, etc) pero tiene la madurez de elegir la simplicidad y eficiencia
* Estructura: Longitud extensa y exhaustiva. Uso de bloques de advertencia (admonitions) cuando se considere oportuno, por ejemplo: lección aprendida, problema identificado, solución no entendida
* Formato: Markdown compatible con Hugo Blox (Frontmatter YAML con atributos: slug, title, summary). Quiero que me devuelvas directamente un markdown que pueda copiar
* Propósito: Explicar que es lo que he aprendido o decisiones tomadas en el desarrollo de un custom repository de home assistant para acerlo actualizable y lo menos acoplado posible a las aplicaciones de terceros que se incluyen

--- Lista de Elementos a Comentar

- Por qué un custom repo de HomeAssistant?
    - Las aplicaciones ofrecidas en los repositorios de HomeAssistant no cubren mis necesidades
    - Me parece sencillo desarrollarlo y centrarlizar ahí las aplicaciones que necesito
    - Teniendo una rpi5 con HomeAssistant, me parece una forma muy sencilla de añadir servicios a mi solución doméstica sin tener que complicarme con servidores, etc
    - Al estar integrado con HomeAssistant, tengo automáticamente backups de los datos
    - Es muy sencillo hacer actualizaciones de versiones de dichas aplicaciones
    - Además HomeAssistant permite hacer un backup automático antes de una actualización de versión para poder hacer rollback de forma sencilla si algo se rompe con la actualización

- Yo quería ejecutar las siguientes aplicaciones:
    - ActualBudets
    - Tandoor Recipes
    - Mailpit
    - Heimdall
    - CouchDB
        - En realidad no es que quiera ejecutar couchdb en sí mismo, sino que es necesario para utilizar un plugin de sincronización de Obsidian y sincronizar así notas entre distintos dispositivos

- Ha habido recientemente un cambio de conceptos en HomeAssistant, y lo que antes se conocían como "Add-ons" ahora son "Applications"

- La mayoría de estas aplicaciones admiten configuraciones en base a variables de entorno
    - Mi idea inicial era configurar estas aplicaciones a través de la definición del `environment` de HomeAssistant
    - Por no estar claro en la documentación, perdí un tiempo muy valioso intentando hacer que los valores de las variables definidas en `environment` fuesen dinámicos y se tomasen de la configuración que establece el usuario en la UI
    - Tras diversos intentos descubrí que esto no era posible
    - La forma de conseguir definir variables de entorno con valores dinámicos tomados de la configuración del usuario es a través de la creación de una imagen docker "wrapper" con un entrypoint en donde se tiene acceso a la configuración del usuario y en base a la misma se crean las variables de entorno en tiempo de ejecución

- Una recomendación a la hora de elegir una aplicación para cubrir una determinada necesidad es valorar entre las distintas opciones la posibilidad de customización/configuración de la misma mediante variables de entorno

- Crear una imagen docker "wrapper" de la imagen original trae ciertas complicaciones
    - Dichas complicaciones surgen cuando no quieres acoplarte a la imagen base, es decir, quieres saber lo menos posible de la misma
        - no conocer el SO base
        - no tener que instalar ninguna utilidad adicional
        - no saber cómo se arranca la aplicación de la imagen base
    - el sentido de crear una imagen "wrapper" de la original es poder crear un script de entrypoint en el cual poder definir las variables de entorno necesarias para customizar/configurar la aplicación
    - HomeAssistant se encarga de crear un fichero json, que está disponible en el contenedor con la configuración que ha establecido el usuario en la UI
        - para poder crear variables de entorno dinámicas el script entrypoint tiene que ser capaz de parsear el fichero de configuración, crear las variables de entorno y arrancar el servicio igual que la imagen base
    - este script entrypoint de la imagen base tiene que utilizar un determinado lenguaje de scripting (soportado por la imagen base)
    - para que el custom repo sea lo más agnóstico posible (menos acoplado a las diferentes aplicaciones) y fácil de mantener en el tiempo:
        - es preferible utilizar un lenguaje de scripting que esté presente en el mayor número de imágenes docker, como por ejemplo preferir `sh` sobre `bash` o `zsh`
        - es preferible evitar hacer uso de herramientas que no estén presentes en la imagen y hacer uso únicamente de las que son prácticamente universales (`sed`, `grep`, `awk`, etc.)
            - aunque esto complique el script
            - es tentador caer en uso de herramientas como `jq` para parseo de json de configuración de homeassistant, pero eso implica instalar software sobre la imagen base (en la mayoría de caso no viene pre-instalado), y eso implica conocer el sistema de paquetes utilizado en la imagen base, y eso implica acoplarse al SO de la imagen base en un momento dado
        - ha habido excepciones a esto y en una ocasión no me ha quedado más remedio que instalar alguna herramienta como `curl`, ya que necesitaba ejecutar un script de inicialización proporcionado por un tercero (con lógica de negocio), y era mejor en este caso acoplarme a la instalación de curl, que acoplarme al script de inicialización con N configuraciones a hacer, y que es más probable que cambie a lo largo del tiempo, forzándome a actualizar el script de entrypoint
        - en ocasiones he preferido establecer explícitamente variables con el mismo valor que el valor por defecto, ya que puede que en un futuro (aunque lo veo improbable) ese valor por defecto cambie y me rompa algo, al establecerlo explicitamente me evito ese problema
        - hay que prestar mucha atención a donde el contenedor persiste los datos para que estén correctamente mapeados en home assistant y se incluyan en los backups de forma automática
        - he tenido que jugar en ocasiones con como defino el valor de una variable de entorno para que la base de datos se persista donde me interesaba, porque no había una variable de entorno específica y la ruta por defecto no se incluía en los backups
        - también definir puid y guid para evitar problemas de permisos en el futuro si el usuario por defecto cambiase

- Sobre el workflow de actualización de versiones
    - he creado un fichero `upgrade.yaml` (esto es una cosa propia y no de los custom repo de HomeAssistant) con la versión actual y la fuente del servicio (que puede ser una release de GitHub y usará el registry de GH, o un tag de docker y usa el registry de docker hub)
    - hay un action de github actions que ejecuta un workflow cada lunes y en base a los ficheros `update.yaml` comprueba si hay nuevas versiones de las imágenes
    - al detectar una nueva versión, inspecciona los metadatos de la imagen con `skopeo` y obtiene el `ENTRYPOINT` y `CMD` originales y los guarda como argumentos en el `build.yaml` de home assistant
        - esos `ENTRYPOINT` y `CMD` originales se utilizan en el script entrypoint de la imagen docker que actúa como wrapper para arrancar el servicio sin acoplarse al servicio que se despliega
            - se puede arrancar una imagen sin tener que mirar el código a ver cómo se arranca
            - hace el custom repo más independiente y no acoplado a las aplicaciones que contiene
    - también el workflow permite filtrar tags en base a regexp para poder filtrar solo versiones finales
        - esto se define en el `upgrade.yaml`
    - también el workflow está diseñado para no romperse cuando el servicio publica muchos tags en el hub de docker, ya que va paginando y recuperando tags por orden de creación inverso (de más reciente a más antiguos) hasta encontrar un tag que cumpla la regex (eso sí, hay un máximo de páginas que itera para que no sea eterno). Al lanzarse semanalmente es difícil que llegue al final sin encontrar una versión final
    - el workflow se encarga también de actualizar la documentación afectada para que sea todo coherente
    - al haber un cambio de versión, HomeAssistant lo detecta, lo notifica y con 1 click se puede actualizar la app sin complicaciones (incluso haciendo un backup previo automático por si hubiera que hacer rollback)