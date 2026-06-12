Quiero que redactes el post de acuerdo a los requisitos e incluyendo el contenido, no omitas contenido, tampoco te inventes contenido, cíñete exactamente a lo que se menciona en la especificación. Si hay más detalles que quieras conocer para mejorar la redacción, PREGUNTALO, y completo esta especificación para que lo puedas generar de nuevo.

--- Requisitos de Redacción

* Público Objetivo: Personas interesadas por la privacidad y entusiastas del self-hosting
* Tono: Sincero, técnico y reflexivo. Debe transmitir la capacidad crítica, de analizar la solución actual, ver los inconvenientes/mejoras/debilidades y replantearse un cambio con el espíritu de mejorar
* Estructura: Longitud extensa y exhaustiva. Uso de bloques de advertencia (admonitions) cuando se considere oportuno, por ejemplo: lección aprendida, problema identificado, solución no entendida
* Formato: Markdown compatible con Hugo Blox (Frontmatter YAML con atributos: slug, title, summary)
* Proposito: Contextualizar la solución que tengo, cómo ha evolucionado a lo largo de los años, llegando a una situación precaria a nivel hardware (terminando con una resistencia soldada en el qnap), cómo he detectado configuraciones mejorables (que quizás en su día hice sin saber), cómo he llegado a la conclusión de renovarlo haciendo un cambio de enfoque en la solución

--- Lista de Elementos a Comentar

* Hace unos años (unos 8/10 años) comenzó mi interés por la privacidad
* Descubrí que con un NAS podía ser el propietario de mis datos y no depender tanto de terceros
    * Me decidí por el ecosistema de QNAP por diversos motivos
        * proporcionaba aplicaciones tanto para escritorio (multiplataforma) como para dispositivos móviles
        * tenía años de experiencia y parecía que sus aplicaciones estaban mantenidas e iban evolucionando
        * cubría varias de mis necesidades
            * almacenamiento de documentos: reemplazando a dropbox y google drive
                * con una aplicación (de escritorio y móvil) para sincronizar
            * almacenamiento de fotos: reemplazando a google photos
                * con una aplicación para ver las fotos del estilo a google photos: podía identificar caras, las ordenaba en un timeline, identificaba objetos, las posicionaba en un mapa
            * almacenamiento de notas: remplazando a google keep
        * proporcionaba un sistema que me permitía hacer muy fácilmente backups cifrados en la nube
        * proporciona un servicio MyQNAPCloud que permite conectar al NAS desde el exterior a través de los servidores de QNAP
    * Me decanté por un TS-251 con 2xHDD de 2 TB en RAID1 y 2GB de RAM (que era la RAM por defecto)
        * Con el paso de los años se me hacía muy lento su uso y decidí ampliar la RAM al máximo (4GB) para ver si mejoraba el rendimiento
        * En 2 ocasiones se me fastidió 1 HDD, y por precaución cambié los 2 HDD
            * Mi razonamiento era que si se había fastidiado 1 HDD, y ambos habían sido comprados al mismo tiempo, había una alta probabilidad de que se fastidiara el otro, por eso cambiaba los 2
* Un tiempo después descubrí HomeAssistant, que era una solución para domotizar la casa, que no te ataba a una tecnología concreta y que respetaba la privacidad
    * Me decidí a instalarlo y hacer una primera domotización de casa mezclando varias tecnologías
    * Utilicé bombillas Ikea Tradfri para el salón y un relé doble z-wave para las luces de la cocina
    * Aunque iba en contra de la privacidad, decidí conectar un google home para poder dar instrucciones de voz a HomeAssistant
    * Para esto tenía una RaspberryPi (inicialmente no sé cuál era, creo que la 3, y años después la actualicé a la 4B con 8GB de RAM y una SD de 32GB)
    * Como parte de la actualización de la rpi a la version 4B, el dongle usb z-wave que tenía dejó de funcionar
      * parece ser que se debía a un problema con la version de los usb y el firmware del dongle
      * la rpi no detectaba el dongle
      * buscando por internet, encontré que varias personas habían reportado el problema y una de ellas lo había documentado
        * soldando una resistencia en el dongle se arreglaba el problema, y así fue! se arregló!
        * no tuve ningún problema más con el dongle, pero me generaba cierta preocupación
* HomeAssistant no solo era una solución de domótica, sino que me proporcionaba otros servicios adicionales
    * Instalé VaultWarden como gestor de contraseñas y cambié todas las contraseñas que tenía repetidas por contraseñas únicas que no me sabía
    * Instalé WireGuard para tener una VPN que me permitiera conectarme desde el exterior a la red de casa como si estuviera en ella
    * Instalé NGINX Proxy Manager para configurar un dominio con SSL y redirigir el tráfico al propio HomeAssistant
    * Instalé NUT para conectar la rpi a un SAI y que pudiera apagarse de forma controlada si se iba la luz durante un largo periodo de tiempo
    * Como no tenía una IP fija en mi casa, configuré HomeAssistant para que actualizase la IP en el DNS donde tenía el dominio para apuntar a mi IP en cada momento
* Con el paso de los años fui actualizando ambos sistemas de una manera sencilla, era una de las ventajas, tanto QNAP como HomeAssistant permitían actualizar el sistema de forma transparente con un click
    * En el caso de HomeAssistant no fue siempre así, creo que empecé a utilizarlo en una fase bastante inicial y me pillaron varios breaking changes que me obligaron a invertir horas en investigar cómo arreglar/re-configurar lo que se había roto
* Con el paso de los años iba añadiendo a una lista mental una serie de defectos o cosas que se podrían mejorar o nuevas cosas que me gustaría tener
    * El QNAP era muy lento, sobre todo lo notaba con la aplicacion de notas y con la de visualización de fotos, y lo peor es que no se podía mejorar más el hardware
    * La rpi del HomeAssistant, aunque no me había dado problemas con el almacenamiento en la SD, había oído hasta la saciedad a un montón de personas que habían tenido problemas con la SD y habían perdido todo
    * No había entendido bien la solución de HomeAssistant, lo veía como una solución de domótica, y no entendía que tuviera servicios de VPN, gestor de contraseñas, proxy para el propio HomeAssistant
    * Había expuesto los puertos del QNAP en el router de casa para poder acceder desde el exterior directamente
        * De todas formas no había entendido la solución de MyQNAPCloud, y no me di cuenta de que no necesitaba exponer ningún puerto del NAS
        * Hubo unas cuantas cosas de QNAP que no había entendido y las había configurado sin entender, al principio me sentí abrumado con tanta información, tecnologías y opcione. Además no había ninguna IA a la que preguntar tan fácilmente como hoy en día
    * Cada día recibía intentos de login en el QNAP y tenía que configurar bloqueos por intentos fallidos
    * Había expuesto los puertos de HomeAssistant en el router para poder acceder desde el exterior
    * Había activado UPnP en el router para poder abrir puertos para la VPN de WireGuard
    * Finalmente no utilizaba la VPN de WireGuard, al poder acceder desde el exterior no usaba nunca la VPN
    * Tenía un dominio que estaba todo el rato apuntando a la IP de mi casa y no me gustaba
    * Los backups de HomeAssistant los hacía a mano de forma periódica y los subía manualmente al NAS
        * Por aquel entonces HomeAssistant no proporcionaba otro sistema mejor de backups
    * Había empezado a utilizar otros servicios (como por ejemplo ActualBudget) y los tenía localmente en un PC y los arrancaba cada vez que los quería usar
        * No encontraba una forma sencilla de tenerlos corriendo en el QNAP o en HomeAssistant
            * Era factible ejecutarlos en ambos sitios, ya que al ser un contenedor docker, tanto QNAP (con su container station) como HomeAssistant (al basarse en docker) permitía su ejecución
            * Otra cosa sería el mantenimiento, la persistencia de los datos, backups, etc
    * Había otros servicios que me gustaría empezar a usar, pero que no me decicía a hacerlo por la dificultad que tenía con los que ha usaba (ActualBudget)
        * Tandoor Recipes, para guardar recetas de cocina
        * PiHole como bloqueador de anuncios
* También con el paso de los años había ido viendo cómo solventar estos inconvenientes/problemas o como configurarlo de forma mejor
    * Descubrí que había nuevos modelos de QNAP que permitían añadir SSD a modo de caché para mejorar el rendimiento considerablemente
    * Descubrí que ya era posible conectar de forma más sencilla un SSD a la rpi
    * Decidí que no quería tener expuesto ningún puerto en el router
    * Decidí que no quería que mi dominio apuntase a la IP de mi casa
    * Tenía claro que la solución me tenía que permitir acceder desde el exterior
    * Descubrí TailScale que permitía tener una VPN sin exponer ningún puerto en el router
        * La pega es que dependes de un tercero
        * Diría que su código es opensource, así que se puede auditar si lo que venden es cierto

* Hubo una día que el NAS dejó de arrancar, y los HDD estaban correctamente. Buscando por internet llegué a un foro donde una persona reportó que era un fallo del reloj del procesador Celeron y que con una resistencia se podía parchear el problema y "resucitar" el NAS. Esa persona hizo un gran trabajo documentando qué pasaba, y cómo había que soldar la resistencia. Dado que el NAS no me funcionaba decidí probarlo y funcionó!
    * Era un parche y me generaba mucha incertidumbre seguir con el NAS en ese estado, en cualquier momento podía perderlo
    * Me daba tiempo para cambiar la solución, aprovechando para aplicar las mejoras que había detectado
        * No se cubría todo, pero se mejoraba
    * Este fue el detonante que me hizo ponerme con la nueva solución

* Por qué opción opté, por adquirir un MiniPC con Proxmox, y crear máquinas virtuales con Docker
    * Me permitía tener un hardware más potente, mucho mejor procesador, más RAM, poder seguir actualizando en el futuro
    * Proxmox proporcionaba un sistema de backups (Proxmox Backup Server) que en teoría haría que fuese sencillo hacer backups
    * Tener dockerizada la solución me permitía estandarizar la forma de instalar software
    * Podía aprovechar a separar la solución de domótica HomeAssistant del resto de servicios que estaban embebidos y darles independencia: VaultWarden
    * Cambién el proxy NGINX Proxy Manager por Traefik, preparado para docker y que se integraba fácilmente con let's encrypt
    * Había encontrado sustitutos para los servicios proporcionados por QNAP
        * OwnCloud para el almacenamiento de ficheros
        * Immitch para el almacenamiento y consulta de fotos/videos
    * Podía instalar todos los servicios que quisiera de la misma forma que el resto, al ser todo contenedores docker, no debería ser muy complicado
    * Tenía que estar todo automatizado, para que en caso de catástrofe hardware o software fuese replicable la instalación sin grandes manualidades
        * Para ello había decidido usar Ansible ya que había hecho en el pasado algún pinito
    * Tenía control total sobre los servicios que utilizaba, y salvo por TailScale, no dependía ya de ningún tercero, ni siquiera de QNAP

* Así fue como surgió el proyecto [Homelab Personal]({{< ref "personal-homelab" >}})