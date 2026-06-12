Quiero que redactes el post de acuerdo a los requisitos e incluyendo el contenido, no omitas contenido, tampoco te inventes contenido, cíñete exactamente a lo que se menciona en la especificación. Si hay más detalles que quieras conocer para mejorar la redacción, PREGUNTALO, y completo esta especificación para que lo puedas generar de nuevo.

--- Requisitos de Redacción

* Público Objetivo: "Mi yo del futuro" y entusiastas del self-hosting
* Tono: Sincero, técnico y reflexivo. Debe transmitir la capacidad analítica, investigación, comprensión, decisión y configuración de la mejor forma posible
* Estructura: Longitud extensa y exhaustiva. Uso de bloques de advertencia (admonitions) cuando se considere oportuno, por ejemplo: lección aprendida, problema identificado, solución no entendida
* Formato: Markdown compatible con Hugo Blox (Frontmatter YAML con atributos: slug, title, summary)
* Propósito: Documentación técnica exhaustiva del despliegue y configuración del TS-264 para consulta en los próximos años. Quiero que sea una secuencia con las configuraciones que se han realizado y en cada paso quiero que se expliquen los conceptos propios de QNAP o generales de los NAS.

--- Lista de Elementos a Comentar

* La situación de partida es:
  * Tengo un QNAP TS-251 con 2x HDD 2TB en RAID1. De los 2TB de capacidad disponible, tras casi 10 años de uso, se han ocupado entre 100GB y 200GB
  * Dispongo de un PC con un HDD de 1TB que tiene sincronizados todos los datos con qsync
    * Razon:
      * Me sirve como segunda copia en otro dispositivo físico, aunque en la misma ubicación. Por cumplir con la práctica 3-2-1 de backups
      * Desde el PC puedo consultar fotos/videos/documentos localmente y los cambios de replican en el nas
      * Desde este PC es desde donde normalmente creo nuevos documentos
      * Desde este PC puedo importar ciertas fotos que vienen de terceros, como por ejemplo cuando hemos contratado algún fotógrafo para una sesión fotográfica
      * La mayoría de contenido multimedia fotos/videos se sincronizan desde un dispositivo móvil (unidireccional desde el móvil al NAS)

* Sobre el almacenamiento
  * El nuevo NAS, el TS-264, al contrario del TS-251, tiene soporte para discos SSD. Igual que el TS-251, el TS-264 tiene 2 ranuras para HDD
    * Encontré 2 opciones para los discos SSD:
      * Utilizarlos para instalar el SO
      * Utilizarlos como caché (teniendo que instalar el SO en los HDD)
    * Decidí utilizarlos para instalar el SO e instalar las aplicaciones de QNAP
      * Ventajas:
        * De esta forma la ejecución de las aplicaciones va a ser muy rápida, y las bases de datos internas que se creen también se alojarán en el SSD, siendo también muy rápido su acceso
        * Un ejemplo sería qumagie, que crea una base de datos con miniaturas de imágenes, rostros identificados, y toda la información que necesita. Al estar alojado todo esto en el SSD, el funcionamiento de qumaggie es muy rápido
    * Para asegurarme de que todo se instalaba en los discos SSD
      * inicialmente instalé en el NAS los discos SSD, SIN INSTALAR los HDD
      * con los SSD instalados
        * arranqué el NAS
        * seguí el wizard de configuración inicial
        * configuré el conjunto de almacenamiento (storage pool) para los 2 SSD disponiéndolos en RAID1
        * configuré un espacio para snapshots (que diría que se hace a nivel de storage pool)
        * a nivel de storage pool se configura también un % de aviso sobre la capacidad
        * creo que había un tercer parámetro que se configuraba no recuerdo cuál es
        * después creé un volumen thick (teniendo que elegir entre thick, thin y static) en el cual hay que elegir el tamaño para el mismo (no recuerdo cuánto puse aquí, pero era teniendo en cuenta la capacidad total, el % de aviso que lo dejé en 80% y el 20% de reserva para snapshots)
        * cuando el sistema está listo y arranca instalé todas las aplicaciones que iba a necesitar para asegurarme que se instalaban en el SSD
        * al instalarse el SO QTS sobre el SSD, este volumen se considera como volumen de sistema
        * instalé todas las aplicaciones
          * tanto las que estaba seguro que iba a usar como las que creía que iba a usar en un futuro
          * por ejemplo instalé container station para que se instale en el SSD y los contenedores vayan más rápido. No tengo pensado ejecutar ningún contenedor por el momento, pero es para estar preparado para el futuro
          * también instalé plex, para que se instale en el ssd, no tengo pensado utilizarlo en el corto plazo, pero si a medio/largo plazo: para la música que tengo y para alguna peli/serie que pudiese tener puntualmente
        * una vez instaladas todas las aplicaciones procedí a la instalación de los HDD y configuración de los mismos (mismos pasos que para los SSD)
    * Sobre el almacenamiento
      * Quiero que se expliquen todos los conceptos: conjunto de almacenamiento `SDDSystem` (storage pool), cómo funciona la reserva de espacio para snapshots, qué son los snapshots, para qué son útiles los snapshots (borrado accidental, malware, etc)
      * Sobre el tema de reserva de espacio de almacenamiento, quiero ejemplo detallado de tamaños:
        * Para los SSD
          * Mis 2 SSD eran de 500GB
          * Quiero que se explique que realmente eso equivale a 4xx GiB, que es lo que muestra QNAP
          * Que de los 4xx GiB, un 20% se reserva para snapshots, calculando lo que realmente queda disponible para el volumen
            * Que este espacio reservado de cara al uso del storage pool se considera como usado y se tiene en cuenta en el % de aviso
          * Para el caso de los SSD (no para los HDD) se configura un % de sobreaprovisionamiento para garantizar el rendimiento de los SSD, parece ser que si se llenan mucho rinden peor o se vuelven inutilizables
            * En mi caso he configurado un 10%
          * Que el % de aviso va (si no estoy equivocado) sobre el total de 4xx GiB
          * Que para determinar el tamaño del volumen (en mi caso thick) tuve en cuenta los 4xx GiB, menos el 20% de reserva para snapshots, y el 80% de aviso, entonces puse el tamaño máximo de tal forma que no me saltara directamente el aviso del 80%
        * Para los HDD el proceso es similar a los SSD pero con otros tamaños
          * Creo un storage pool `HDDData` están en RAID1 con una capacidad de 4TB, que equivale a 3'x TiB
          * También dejé un 20% para snapshots (lo que sea en TiB o GiB)
          * También dejé la alerta de capacidad en 80%
          * También creé un volumen thick y para el cálculo del tamaño lo hice siguiendo la misma lógica que para los SSD pero con los números de capacidad de los HDD
      * Quiero que se expliquen todos los conceptos relacionados sobre este tema, si hay alguno tratado en la conversación que no he incluido aquí añádelo, eso sí, no te inventes nada
      * Numeros reales y concretos sobre los discos
        * SSD
          * 500GB son 465GiB
          * Sobreaprovisionamiento 10% 45GiB
          * RAID1 consume espacio, y teniendo en cuenta el sobreaprovisionamiento del 10%, los 465GiB se quedan en 410GiB disponibles
          * 20% (para snapshots) son 82GiB, esto se calcula sobre los 410GiB disponibles
          * 80% (alerta) son 328GiB, esto se calcula sobre los 410GiB disponibles
          * finalmente asigno 220GiB al volumen, ya que así 220GiB (del volumen) + 82GiB (de snapshots) = 302GiB, que está por debajo del 80% (328GiB)
       * HDD
          * 4TB son 3'64TiB
          * Aquí no hay sobreaprovisionamiento (esto es para que los SSD funcionen mejor, si se llenan a tope funcionan mal)
          * RAID1 consume espacio y los 3'64TiB se quedan en 3'63TiB disponibles
          * 20% (para snapshots) son 0'73TiB, esto se calcula sobre los 3'63TiB disponibles
          * 80% (alerta) son 2'9TiB, , esto se calcula sobre los 3'63TiB disponibles
          * finalmente asigno 2'1TiB al volumen, ya que así 2'1TiB (del volumen) + 0'73TiB (de snapshots) = 2'83TiB, que está por debajo del 80% (2'9TiB)

* Carpetas compartidas
  * Documents (HDDData)
    * Aquí es donde guardo todos mis documentos: facturas, contratos, excels, etc. Cualquier tipo de documento
  * Downloads (SDDSystem)
    * Aquí es donde se guardan las descargas de QGet
    * Se ha seleccionado el SDD porque las descargas son poco a poco y para minimizar múltiples escrituras en HDD
    * Para mi las posibles descargas de QGet serán temporales, para consumir en un tiempo prudencial y borrar
    * Esta carpeta no se incluye en el backup de los datos
  * HomeAssistantBackups (HDDData)
    * Exclusivamente para los full backps de homeassistant
  * ManualBackups (HDDData)
    * Para backups que yo haga manualmente y de forma puntual
  * MediaArchive (HDDData)
    * Contenido multimedia que provenga de terceros o que sea mío pero no se haya realizado con un dispositivo móvil (ej: cámara reflex)
    * Este contenido está en formato raw o sin una gran compresión, la idea es guardarlo. No está preparado para ser consumido/visualizado
    * Esta carpeta compartida no forma parte de la fuente de contenido multimedia (configurado en el multimedia console)
  * MediaGallery (HDDData)
    * Contenido multimedia que provenga de terceros o que sea mío pero no se haya realizado con un dispositivo móvil (ej: cámara reflex)
    * Este contenido sí está procesado y comprimido para ser consumido/visualizado
    * Esta carpeta compartida sí forma parte de la fuente de contenido multimedia (configurado en el multimedia console)
  * MediaLibrary (HDDData)
    * Carpeta compartida pensada para alojar a más largo plazo las descargas realizadas con QGet
    * En principio no se usará inicialmente
    * Esta carpeta compartida no se incluye en el backup de los datos
  * MediaMobile (HDDData)
    * Carpeta compartida donde se sincroniza el contenido multimedia (fotos/videos) de mis dispositivos móviles
    * Esta carpeta compartida sí forma parte de la fuente de contenido multimedia (configurado en el multimedia console)
    * Dentro de esta carpeta voy creando carpetas por cada dispositivo móvil que tengo
      * Por cada dispositivo móvil creo 2 carpetas:
        * Una para sincronizar la cámara del dispositivo móvil
        * Otra para sincronizar otra carpeta del dispositivo móvil
          * Las fotos/videos que me llegan de terceros al dispositivo móvil (via apps de mensajería) y que me interesa conservar, las muevo a esta carpeta para que se guarden en el nas
          * Esta selección es manual y consciente
      * En el móvil utilizo la aplicación QFile para configurar la sincronización de ambas carpetas
  * Music (HDDData)
    * Carpeta donde guardo mi música, que tengo de hace un porrón de años, antes de que surgieran las plataformas de streamming

* Usuarios
  * Actualmente QTS en el wizard de configuración inicial te propone crear un usuario administrador, al hacerlo, automáticamente se desactiva el usuario `admin`
    * Esto no sé cuándo se cambió, porque cuando configuré el TS-251 no era así, y tenía el usuario admin, y yo me tuve que crear un usuario propio para no usar directamente `admin`
  * Para mejorar la seguridad se configura para el usuario principal el uso de inicio de sesión sin contraseña a través de QNAP Authenticator
  * Además he creado otros 2 usuarios adicionales
    * Un usuario `homeassistantbackups` que será utilizado por homeassistant para subir las copias de seguridad al NAS
      * Este usuario únicamente tendrá permisos sobre la carpeta compartida `HomeAssistantBackups`
    * Un usuario `homeassistantmonitor` que será utilizado por homeassistant para la integración con QNAP y poder tener el NAS monitorizado
      * Para que funcione hay que delegarle permisos de "Monitorización del sistema"

* Notas sobre MyQNAPCloud y notificaciones
  * Para que las notificaciones de QNAP funcionen hay que utilizar MyQNAPCloud
  * Yo he decidido no utilizarlo
    * En ninguna aplicación móvil de QNAP tengo configurado MyQNAPCloud
  * Para conectar al NAS desde el exterior
    * Me conecto a la VPN con Tailscale
    * Hago uso de la URL del NAS gracias al DNS local AdGuard Home y al proxy NGINX Proxy Manager (que tengo en HomeAssistant)
  * Esto me imposibilita el uso de las notificaciones de QNAP
  * Para poder tener un mínimo de monitorización y saber si algo va mal, he configurado en HomeAssistant la integración con QNAP (utilizando el usuario `homeassistantmonitor`)
    * Con la integración con QNAP configurada se puede crear una automatización en HomeAssistant para recibir una notificación al móvil si el sistema no está bien
    * Es más limitado que todas las opciones de notificación que ofrece QNAP, pero prefiero no usar MyQNAPCloud y las notificaciones era algo que tampoco usaba antes en el TS-251

* Instantáneas (Snapshots)
  * Para cada conjunto de almacenamiento he programado la creación de instantáneas
    * SSDSystem
      * Ejecución diaria a las 04:00
      * Se conservan 7 instantáneas
    * HDDData
      * Ejecución diaria a las 04:15
      * Se concervan 30 instantáneas
  * Aquí quiero explicar cómo funcionan los snapshots explicando
    * cuánto espacio utilizan
      * diferencia entre snapshot inicial y sucesivos
      * cuánto ocupa el inicial
      * qué se guarda en el snapshot
    * el hecho de que sean incrementales
    * que pasa si no cambia la información
    * que pasa si se llega al máximo número de snapshots configurados
    * cualquier otra cosa que te haya preguntado en la conversación y no enumere aquí

* Copias de seguridad (Backups)
  * Backup del sistema
    * Anteriormente, cuando configuré el TS-251, no era posible automatizar el backup del sistema (toda la configuración del NAS)
      * Se podía hacer una backup manual y se generaba un fichero
    * Ahora se puede automatizar y programar
    * Yo lo tengo de ejecución diaria a las 00:30 y que se almacene en la carpeta compartida `ManualBackups` en una subcarpeta `qnap/ts264`
      * Este backup está cifrado con una clave
  * Backup de datos en el cloud
    * Para cumplir con la buena práctica 3-2-1 de backups que recomienda tener una copia en una ubicación distinta, realizo una copia de seguridad de los datos en un proveedor cloud, en este caso onedrive
      * Esta copia de seguridad también está cifrada con una clave (distinta a la de la copia del sistema)
    * Hybrid Backup System 3 (HBS3) facilita mucho la creación de copias de seguridad y el envío de las mismas a un cloud
      * Tengo configurada una copia diaria a las 05:00
      * incluye las carpetas compartidas
        * Documents, HomeAssistantBackups, ManualBackups, MediaArchive, MediaGallery, MediaMobile, Music, homes
      * Se retienen 30 copias
      * Está programada una comprobación rápida cada Domingo a las 07:00
      * Está programada una comprobación de contenido el día 1 de cada mes a las 08:00
      * Está configurado QuDedup
    * Quiero que se explique:
      * qué es QuDedup, cómo funciona y cómo optimiza el almacenamiento
      * también quiero que se explique cómo es cada copia en el cloud, si es incremental, cuánta información se genera, qué pasaría al restaurar, hace falta tener todas las incrementales? y cualquiero otra cosa que haya preguntado en la conversación al respecto

* Capa de Red y Seguridad (Invisible):
  * Reserva de IP estática en el router (configuración DHCP a través de MAC address)
  * Tailscale como único punto de entrada (instalado fuera del NAS)
  * Nginx Proxy Manager: se encarga de los certificados SSL (con let's encrypt) y el flujo DNS local
    * La conexión entre el proxy y el NAS no está cifrada, va por el puerto HTTP del NAS
    * Lo más correcto sería que fuera también cifrada, pero esto me requeriría configurar un certificado en el NAS
      * Creo que el NAS está preparado para generar certificados de let's encrypt, pero no sé que dominio utilizaría, y no sé si requeriría MyQNAPCloud
      * Esto requiere de más tiempo de investigación y no le veo un gran beneficio
      * No hay nada expuesto directamente al exterior, se accede a través de VPN, y si alguien entrase en la red loca, tendría un problema mayor, y no que el proxy y el nas van por http
  * En NGINX Proxy Manager hay un DNS para el NAS, y lo utilizo en las aplicaciones móviles o si me quiero conectar al nas desde el PC a través de un navegador, sin embargo traté de usarlo para configurar en el PC qsync, y no fue buena idea, tenía muchos problemas de reconexión
    * No lo sé a ciencia cierta pero me da que era por problemas con tamaños de los ficheros y falta de configuración en el proxy host del NGINX Proxy Manager
    * Para no complicarme la vida, y como la IP está reservada en el router, para qsync he configurado la IP del NAS
  * En las aplicaciones móviles (QFile y QSync) que también suben ficheros tengo configurado el DNS y no he experimentado problemas
    * Si tuviera problemas subiendo algún fichero tendría que optar por la misma solución y no pasar a través del proxy
  * Quizá una mejor solución para poder seguir utilizando DNS y saltarse el proxy sería configurar en AdGuard Home una entrada específica para el DNS del NAS que apunte directamente al nas
    * Ahora mismo tengo una entrada wildcard para el dominio que utilizo y todos los subdominios apuntan al proxy
    * La pega de esto es que la conexión ya no podría ser cifrada con mi configuración actual
      * Para que fuese cifrada tendría que configurar un certificado en el NAS lo que me requeriría de más tiempo de investigación y configuración

* Carga inicial de datos en TS-264
  * Dado que ya había un PC que tenía todos los datos
  * Se ha utilizado qsync en el PC para subir los datos al nuevo NAS
    * En lugar de copiar de un nas a otro
  * Se pausó en el pc la sincronización con el NAS anterior (TS-251)
  * Se configuro la sincronización del nuevo NAS (TS-264) y se pausó esta sincronización
  * Se movio el contenido de las carpetas sincronizadas del nas viejo a las del nuevo nas
  * Se fue reanudando la sincronización con el nuevo nas carpeta a carpeta
  * Como ya se ha explicado anteriormente qsync en el PC no pasa por el proxy sino que conecta directamente con el NAS a través de IP y por conexion no cifrada

* Contenido Multimedia
  * En Multimedia Console tengo configuradas como fuentes de contenido multimedia las carpetas compartidas
    * MediaMobile
    * MediaGallery

* El Plan de Desastre (Kit de Emergencia):
  * Había un problema latente
    * Los backups de HomeAssistant van cifrados, se almacenan en el NAS. La clave de cifrado está en el gestor de contraseñas
    * El backup del sistema del TS264 va cifrado, se almacena en el NAS. La clave de cifrado está en el gestor de contraseñas
    * El backup de los datos del NAS (que incluye los backups de HomeAssistant y del sistema del TS264) va cifrada, se almacena en OneDrive. La clave de cifrado está en el gestor de contraseñas
    * He hecho un backup del gestor de contraseñas, en formato JSON cifrado, se almacena en el NAS
    * Si hubiese una catastrofe total y solo tuviera acceso al OneDrive, no podría hacer nada porque está cifrado y no tengo la clave ni la conozco, estaría en el gestor de contraseñas, pero al ser desastre total no habría dicho gestor
    * Si hubiese una catástrofe casi total y tuviese acceso al OneDrive y siguiese funcionando el PC, no podría hacer nada. El backup de onedrive sería inaccesible porque no tengo la clave de cifrado. Al tener los datos del NAS accesisbles en el PC (gracias a qsync) tendría acceso al backup del gestor de contraseñas, pero está cifrado y tampoco tengo la clave
    * Para eso he creado un kit de emergencia
      * Es un fichero zip con clave (que sí conozco) usando AES-256
      * Contiene un TXT con las diferentes claves de cifrado
      * Está almacenado en el PC y en OneDrive (en la raiz, fuera de los backups del NAS)
      * Esto me permitiría descifrar lo necesario y empezar a recuperar cosas

* Configuración de aplicaciones móviles
  * En el móvil tengo:
    * QManager: para consultar el estado general y realizar alguna tarea de administración, como actualizar el firmware
    * QFile: para consultar documentos, puntualmente subir algun documento desde el teléfono y para configurar la sincronización de las fotos de la cámara del móvil y de una carpeta preestablecida
    * QMaggie: para consultar las fotos/videos del NAS
    * Authenticator: para la autenticación en el sistema
      * Esta es la única aplicación que tengo configurada con MyQNAPCloud, no es posible que funcione sin esto
    * Todas las aplicaciones (excepto Authenticator) están configuradas sin uso de MyQNAPCloud por lo que necesitan conexion directa con el NAS, bien porque estoy en la misma red local o bien porque estoy conectado con una VPN
    * Todas las aplicaciones están protegidas con pin

Creo que esto ya incluye todas las configuraciones realizadas y más o menos en la secuencia en que han sido realizadas. Si hay algo en la conversación que se ha discutido y es relevante o bien lo incluyes directamente o me preguntas para darte más conexto y ver si procede o no incluirlo