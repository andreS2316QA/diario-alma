import streamlit as st
import random
import datetime
import base64

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Mi Diario del Alma 🌸", page_icon="🌸", layout="centered")

# --- FUNCIÓN PARA LA MÚSICA (COMPATIBLE CON IPHONE) ---
def cargar_musica(archivo_mp3):
    try:
        with open(archivo_mp3, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            # HTML para reproductor invisible que inicia al interactuar
            md = f"""
                <audio id="audioTag" autoplay loop>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                <script>
                    var audio = document.getElementById("audioTag");
                    audio.volume = 0.4;
                </script>
            """
            st.markdown(md, unsafe_allow_html=True)
    except:
        st.error("⚠️ No se encontró 'la_reina.mp3' en GitHub.")

# --- ESTILOS CSS ---
def local_css(mood_color="#FF0055", accent_color="#00F7FF"):
    st.markdown(f'<link rel="apple-touch-icon" href="https://raw.githubusercontent.com/andreS2316QA/diario-alma/main/icono.png">', unsafe_allow_html=True)
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {mood_color}; color: white; }}
        .stButton>button {{
            width: 100%; border-radius: 15px; height: 60px;
            background-color: rgba(255, 255, 255, 0.2); color: white;
            border: 2px solid {accent_color}; font-weight: bold; font-size: 1.1rem;
        }}
        .mensaje-box {{
            padding: 20px; border-radius: 20px; background: rgba(0, 0, 0, 0.3);
            text-align: center; font-style: italic; font-size: 1.2rem;
            border-left: 5px solid {accent_color}; margin: 20px 0px;
        }}
        h1, h2, h3 {{ text-align: center; color: white !important; }}
        </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS (RESUMIDA A 10 POR CATEGORÍA PARA ESTE BLOQUE, PERO PUEDES COPIAR LAS 400 AQUÍ) ---
MENSAJES = {
    "feliz": [
        "¡Tu sonrisa ilumina todo el lugar! 😊", "Hoy es un día perfecto porque tú estás en él. ✨", "La felicidad te queda increíble, nunca la sueltes. 💖", 
        "Eres el rayito de sol de cada mañana. ☀️", "Sigue brillando, el mundo necesita tu luz. 🌟", "Tu alegría es contagiosa y mágica. 🌈", 
        "Que nada apague esa chispa que tienes en los ojos. 🔥", "Eres magia pura cuando ríes a carcajadas. 🪄", "Hoy el universo conspira a tu favor. 🌌", 
        "Disfruta este momento, te lo mereces más que nadie. 🏆", "Tu energía positiva es un regalo para el mundo. 🎁", "Eres la definición de un día bonito. 🌻", 
        "Sonríe, hoy es un regalo de la vida para ti. 🎈", "La felicidad es un camino, y tú lo caminas con gracia. 👠", "Tu paz mental es tu mayor éxito hoy. 🧘‍♀️",
        "Eres el color en un día gris para muchos. 🎨", "Que tu risa sea siempre tu mejor medicina. 💊", "Hoy todo saldrá mejor de lo que esperas. 🍀", 
        "Eres capaz de lograr todo lo que te propongas. 🚀", "Tu felicidad es mi parte favorita del día. 🥰", "Qué lindo es verte así de radiante y plena. 💎",
        "Sigue coleccionando momentos felices, princesa. 📸", "Eres luz, eres amor, eres alegría pura. 🕯️", "Hoy el sol salió solo para verte sonreír. 🌤️",
        "Tu buen humor cambia el ambiente de cualquier lugar. 🎊", "No dejes de ser esa persona tan especial. ⭐", "Eres un imán de cosas maravillosas. 🧲",
        "Disfruta las pequeñas cosas que pasen hoy. 🍭", "Tu alma brilla con luz propia, sin filtros. ✨", "Eres la razón por la que alguien sonríe hoy. 💌",
        "Quédate con quien te haga sentir así de feliz. 🫂", "La vida es bella, y más si tú estás presente. 🌍", "Eres una bendición para quienes te rodean. 🙌",
        "Tu entusiasmo es verdaderamente inspirador. 🌬️", "Hoy es un gran día para simplemente ser tú misma. 👑", "Nada es más bonito que tu paz interior. 🕊️",
        "Eres el éxito hecho persona, nunca lo dudes. 🎓", "Tu corazón alegre es un imán de milagros. 🎋", "Sigue cultivando esa alegría interna. 🌱",
        "Eres un ser maravilloso por dentro y por fuera. 🦄", "Que tu día sea tan lindo como tu alma. 🌷", "Hoy brillas más que cualquier estrella. 🌠", 
        "La alegría es el lenguaje de tu corazón. 🗣️", "Eres el tesoro más grande que existe. 💰", "Disfruta cada segundo de este día único. ⏳",
        "Tu sonrisa es lo que más me gusta del mundo. 😍", "Eres pura inspiración para los demás. 💡", "Que la vida te devuelva toda la alegría que das. 🔄",
        "Hoy es un día para celebrar quién eres. 🍾", "Eres simplemente espectacular y única. 🎬"
    ],
    "triste": [
        "Se vale estar mal, date permiso de sentirlo. 🌧️", "Esta tormenta también pasará, te lo prometo. ⛈️", "Mañana el sol volverá a salir para ti. 🌅", 
        "Eres fuerte, incluso cuando tus lágrimas caen. 💧", "No estás sola en esto, aquí estoy. 🤝", "Tu tristeza no define quién eres. 👤", 
        "Un mal día no significa una mala vida. 🗓️", "Está bien no poder con todo hoy. ⚓", "Tómate el tiempo que necesites para sanar. 🩹", 
        "Después de la lluvia siempre sale el arcoíris. 🌈", "Tu corazón es más resiliente de lo que crees. 🛡️", "Permítete descansar y procesar lo que sientes. 🛌", 
        "Eres valiente por enfrentar tus sombras. 🌑", "Abraza tu vulnerabilidad hoy, es fuerza. 🫂", "Mañana será una nueva oportunidad de empezar. 🆕",
        "Incluso las flores necesitan lluvia para crecer. 🌻", "No te presiones, ve un paso a la vez. 🚶‍♀️", "Tu dolor es válido y merece ser escuchado. 📣",
        "Eres más fuerte de lo que te imaginas ahora. 💪", "Cuidar de ti es tu única prioridad hoy. 🧖‍♀️", "Escucha a tu alma, ella sabe cómo sanar. 🧘‍♀️",
        "No tienes que sonreír si no lo sientes. 🎭", "El tiempo acomoda todas las piezas del rompecabezas. 🧩", "Confía en el proceso de tu vida. 🌊",
        "Eres una guerrera, pronto estarás de pie. ⚔️", "Permite que tus lágrimas limpien tu alma. 🚿", "Tus sentimientos importan mucho para mí. 💎",
        "Eres amada, incluso en tus momentos más oscuros. 🕯️", "No te compares con los demás hoy. 🚫", "Cada lágrima es un paso hacia la paz. 🕊️",
        "Tú puedes con esto, aunque hoy parezca difícil. 🧗‍♀️", "El descanso es sagrado en días así. 💤", "Eres luz, aunque ahora te sientas sombra. 🕯️",
        "Mañana tendrás más fuerzas que hoy. 🔋", "Rodéate de cosas que te den calma y silencio. 🍃", "Eres valiosa, pase lo que pase fuera. 🏷️",
        "Este sentimiento es solo temporal. ⏳", "Ámate un poquito más hoy que estás triste. ❤️", "Tu paz volverá, te lo aseguro. 🌊",
        "Eres importante y necesaria en este mundo. 🌎", "No te rindas, el sol te está esperando. ⛅", "Respira profundo, solo es un mal momento. 🌬️",
        "Eres una persona increíble atravesando algo difícil. 🎢", "Date un abrazo fuerte de mi parte. 🤗", "Tu sensibilidad es una virtud, no un error. 🎻",
        "Pronto volverás a brillar como siempre. ✨", "Busca la calma en los pequeños detalles. 🐚", "Eres mucho más que tus problemas actuales. 🏔️",
        "No cargues con todo tú sola hoy. 🎒", "Estoy muy orgulloso de ti por seguir adelante. 🏅"
    ],
    "ansiosa": [
        "Todo va a estar bien, respira profundo. 🌬️", "Estás a salvo aquí y ahora, nada te pasará. 🏠", "No tienes que resolver el futuro hoy. 📅", 
        "Inhala calma, exhala todos tus miedos. 🧘‍♀️", "Tus pensamientos no son la realidad. 🧠", "Suelta lo que no puedes controlar ahora mismo. 🎈", 
        "Un paso a la vez, no hace falta correr. 🐢", "Confía en que todo se acomodará solo. 🧘", "Eres capaz de manejar lo que sea que venga. 🌊", 
        "Enfócate en tu respiración, siente el aire entrar. 🫁", "Este sentimiento pasará más pronto de lo que crees. ⏳", "Tu mente es poderosa, úsala para la paz. ☮️", 
        "No te adelantes al mañana, quédate conmigo hoy. 📍", "El presente es el único lugar donde estás a salvo. 🎁", "Eres más grande que cualquier miedo. 🏔️",
        "Relaja tus hombros, suelta toda la tensión. 💆‍♀️", "Todo tiene una solución, no te agobies. 💡", "Eres una mujer fuerte y centrada. 🎯",
        "Confía en tu capacidad de resiliencia. 🛡️", "No permitas que la prisa te robe la paz. 🛑", "Tus preocupaciones son solo nubes pasando. ☁️",
        "Siente tus pies en la tierra, estás presente. 👣", "Eres el capitán de tu propia calma. ⚓", "Date permiso de desconectar del ruido. 🔇",
        "La respuesta llegará en el momento justo. 🔑", "No tienes que ser perfecta, solo sé tú. 🌸", "Tu paz interior es tu refugio sagrado. 🕍",
        "Eres amada y profundamente protegida. 👼", "Toma un poco de agua y respira de nuevo. 💧", "Todo está fluyendo correctamente. 🌊",
        "Eres suficiente, tal como eres en este instante. ✅", "No escuches a la voz del miedo, es mentirosa. 🚫", "Confía en la vida, ella te sostiene. 🌍",
        "Eres un remanso de tranquilidad en la tormenta. 🏝️", "Sigue adelante, pero siempre a tu propio ritmo. 🥁", "Nada es tan grave como parece en tu mente ahora. 🔍",
        "Eres dueña de tu destino y de tu calma. 🧭", "Relájate, el universo te sostiene con amor. 🌌", "Busca un lugar tranquilo en tu interior. 🕯️",
        "Tus miedos se disuelven ante tu valentía. 🦁", "Eres paz, eres luz, eres equilibrio. ⚖️", "No dejes que el ruido exterior te afecte. 🎧",
        "Eres sabia y sabrás qué hacer llegado el momento. 📖", "Todo está en perfecto orden divino. ✨", "Descansa tu mente unos minutos, se lo merece. 🧠",
        "Eres una persona capaz y muy valiente. 🎖️", "El control es una ilusión, suéltalo con amor. 🪁", "Respira, solo respira una vez más. 🌬️",
        "Eres protegida por el universo entero. 🪐", "Mañana todo será mucho más claro. 👓"
    ],
    "cansada": [
        "El descanso es un acto de amor propio. 🛌", "Hoy te mereces desconectar de todo el mundo. 🔌", "Tu cuerpo te pide calma, escúchalo. 👂", 
        "Dormir es productivo también, recupérate. 💤", "No tienes que poder con todo hoy, suelta. ⚓", "Está bien poner una pausa en el camino. ⏸️", 
        "Tu energía es sagrada, recárgala con mimos. 🔋", "Mañana tendrás fuerzas nuevas y brillantes. 🌅", "Cierra los ojos y respira paz profunda. 😌", 
        "Te has esforzado mucho, descansa con orgullo. 🏅", "Eres humana, no una máquina, trátate con amor. 🌸", "Permítete no hacer nada por un rato. 🍵", 
        "Un baño caliente y a descansar, te lo ganaste. 🛁", "Tu bienestar es lo primero de la lista hoy. 📝", "Suelta las cargas del día al pie de la cama. 🎒",
        "Mañana el mundo seguirá ahí, ahora duerme. 🌎", "Eres valiente por reconocer tus límites. 🚧", "El sueño repara lo que el día desgasta. 🛠️",
        "Regálate un momento de silencio absoluto. 🤫", "Te mereces un premio por todo tu trabajo. 🎁", "Apaga el celular y descansa de las pantallas. 📱",
        "Tu mente necesita un respiro urgente. 🌬️", "Eres fuerte, pero también necesitas apoyo. 🤝", "No te sientas culpable por descansar hoy. 🚫",
        "El descanso trae la claridad que te falta. 💡", "Mañana verás las cosas con otros ojos. 👓", "Tu almohada te espera con mucho cariño. ☁️",
        "Duerme tranquila, todo está bajo control. ✅", "Eres luz, incluso cuando estás agotada. 🕯️", "Un buen descanso cambia tu perspectiva. 🎡",
        "Hoy el sofá es tu mejor amigo. 🛋️", "No hay prisa por llegar a ningún lado hoy. 🐢", "Tu cuerpo es tu templo, cuídalo con sueño. 🏛️",
        "Mañana despertarás con el alma renovada. 🦋", "Eres una guerrera que necesita reponerse. ⚔️", "Disfruta de tu propia compañía en silencio. 🕯️",
        "La vida espera, tu descanso no. 🛑", "Recupera tu magia mientras duermes. 🪄", "Eres valiosa, estés haciendo algo o no. 💎",
        "Date el lujo de dormir un poco más. ⏰", "Tu sonrisa volverá con más fuerza mañana. 😊", "Descansar es parte del éxito. 📈",
        "Eres única, cuida de tu energía vital. ✨", "Que tus sueños sean dulces y tranquilos. 🍬", "Suelta el estrés, abraza la sábana. 🤗",
        "Eres una mujer increíble, ahora descansa. 👑", "Paz para tus pensamientos agotados. 🕊️", "Recarga tu corazón de serenidad. ❤️",
        "Mañana será un día lleno de energía. 🔋", "Duerme, princesa, el mundo te espera mañana. 👸"
    ],
    "motivada": [
        "¡El cielo no es el límite, es solo el inicio! 🚀", "Tu fuego interno es totalmente imparable. 🔥", "Naciste para brillar con luz propia. 🌟", 
        "La meta te está esperando, ¡ve por ella! 🏁", "Eres pura energía positiva en movimiento. ⚡", "Cree en ti tanto como yo creo en ti. 💖", 
        "Nada puede detener a un alma decidida. 🛡️", "Hoy es el día perfecto para conquistar tus sueños. 🏆", "Tu esfuerzo de hoy es el éxito de mañana. 📈", 
        "Eres la arquitecta de tu propio destino. 🏗️", "¡Tú puedes con todo y más! 💪", "Sigue adelante, lo estás haciendo increíble. 👏", 
        "Tu potencial es infinito, no te pongas techos. 🌌", "Cada paso cuenta, no dejes de caminar. 👣", "Eres una mujer de acción y resultados. 🎯",
        "El éxito te busca porque no te rindes. 🔍", "Eres inspiración pura para quienes te miran. 💡", "Convierte tus obstáculos en escalones. 🪜",
        "Tu determinación es tu mejor herramienta. 🛠️", "Hoy vas a brillar más que nunca antes. ✨", "Confía en tu talento, es único en el mundo. 💎",
        "Eres la protagonista de tu propia historia. 🎬", "No sueñes tu vida, vive tus sueños hoy. 🌈", "Tu coraje es más grande que tus dudas. 🦁",
        "¡Haz que las cosas sucedan hoy mismo! 💥", "Eres una ganadora por naturaleza. 🥇", "Sigue alimentando esa ambición sana. 🍎",
        "El mundo es tuyo, sal a reclamarlo. 🌍", "Eres fuerte, inteligente y muy capaz. 🧠", "Tu disciplina te llevará a donde quieras. 🛣️",
        "No te detengas hasta que te sientas orgullosa. 😤", "Hoy es un nuevo lienzo para tu éxito. 🎨", "Eres luz en el camino hacia la cima. 🏔️",
        "Sigue vibrando alto, atraes lo que eres. 📡", "Tu visión es clara y tu camino está listo. 🗺️", "Eres un motor de cambios positivos. ⚙️",
        "Cree en la magia de los nuevos comienzos. 🪄", "Tu persistencia es tu superpoder. 🦸‍♀️", "Hoy vas a dar lo mejor de ti. 💯",
        "Eres la definición de resiliencia y éxito. 👑", "No dejes que nadie apague tu ambición. 🚭", "El futuro pertenece a quienes creen en sí mismos. 🔮",
        "Eres una fuerza de la naturaleza imparable. 🌪️", "Sigue adelante con esa frente en alto. ⬆️", "Tu pasión es el combustible de tus logros. ⛽",
        "Hoy vas a sorprender al mundo entero. 😲", "Eres capaz de crear cosas maravillosas. 🧶", "Tu actitud determina tu altitud hoy. ✈️",
        "¡Ve con todo, sin miedo al éxito! 🤘", "Eres simplemente la mejor en lo que haces. 🌟"
    ],
    "tranquila": [
        "Tu paz no tiene precio, protégela siempre. 🕊️", "Eres el remanso de calma de muchos. 🌊", "Disfruta este silencio sagrado que te rodea. 🤫", 
        "La tranquilidad es tu superpoder más grande. ✨", "Respira la quietud de este momento perfecto. 🌬️", "Tu serenidad es un bálsamo para el alma. 🌿", 
        "Quédate en este estado de paz total. 🧘‍♀️", "Eres como un lago en calma bajo el sol. 🌅", "Nada perturba tu equilibrio interno hoy. ⚖️", 
        "Disfruta del aquí y el ahora, sin prisa. 🎁", "Tu corazón late al ritmo de la naturaleza. 🍃", "La armonía te envuelve como un abrazo. 🫂", 
        "Eres paz en un mundo lleno de ruido. 🎧", "Siente la suavidad de este día tranquilo. ☁️", "Tu mente está en calma, como un cielo despejado. 🌤️",
        "Eres la dueña de tu propio tiempo hoy. ⏰", "Fluye con la vida, como el agua en el río. 💧", "Tu presencia transmite mucha seguridad. 🛡️",
        "Regálate este espacio de no hacer nada. 🍵", "Eres equilibrio puro en cada respiración. 🌬️", "La calma es la cuna de las buenas ideas. 💡",
        "Disfruta de la belleza de lo simple. 🐚", "Tu alma está en casa hoy, descansa. 🏠", "Eres luz suave que ilumina sin quemar. 🕯️",
        "La paciencia es tu mejor compañera hoy. ⏳", "Nada te falta, todo está en orden aquí. ✅", "Eres el silencio que precede al milagro. 🤫",
        "Camina despacio, disfruta del paisaje. 🌳", "Tu mirada refleja la paz de tu interior. 👁️", "Eres un oasis en medio del desierto. 🏝️",
        "Siente la libertad de estar en calma. 🕊️", "Hoy no hay batallas que pelear. ⚔️", "Tu energía es estable y reconfortante. 🔋",
        "Confía en la armonía del universo. 🌌", "Eres un refugio de paz para ti misma. 🏰", "Disfruta de tu propia compañía en paz. 👤",
        "La vida es dulce cuando se vive tranquilo. 🍭", "Eres la calma después de cualquier tormenta. 🌈", "Tu voz es suave y llena de sabiduría. 🗣️",
        "Relájate en el fluir de la existencia. 🌊", "Eres un ser de luz en estado puro. ✨", "Que tu paz interior sea inquebrantable. 💎",
        "Hoy el tiempo se detiene para tu calma. 🛑", "Eres serenidad caminante, princesa. 👸", "Disfruta del aire fresco en tu rostro. 🍃",
        "Tu espíritu está en reposo y sanación. ⛪", "Eres armonía en cada palabra que dices. 🎶", "La paz es el lenguaje de tu alma hoy. 🕊️",
        "Sigue cultivando este jardín de calma. 🌸", "Eres simplemente paz, y eso basta. ❤️"
    ],
    "enojada": [
        "Tu fuego es válido, úsalo para crear. 🔥", "Después del tornado siempre llega la paz. 🌪️", "Protege tus límites con firmeza y amor. 🛡️", 
        "Exhala el humo de la ira poco a poco. 🌬️", "El mar también tiene tormentas necesarias. 🌊", "Tu enojo es energía, transfórmala en algo útil. ⚡", 
        "No permitas que la rabia nuble tu visión. 🌫️", "Respira hondo antes de actuar, tú puedes. 🧘‍♀️", "Eres dueña de tus reacciones, no dejes que te dominen. 🧭", 
        "Está bien sentir rabia, pero no te quedes ahí. 🛑", "Tu fuerza es inmensa, canalízala bien. 🌊", "Suelta lo que te quema por dentro. ☄️", 
        "Eres más grande que cualquier provocación. 🏔️", "Busca la calma en medio del incendio. 🚒", "Tu paz vale más que tener la razón siempre. 🕊️",
        "Cuenta hasta diez y deja que el calor baje. 🔟", "Eres una mujer sabia, no actúes por impulso. 📖", "El enojo pasará, pero tus palabras quedan. ✍️",
        "Protege tu corazón de la amargura. 🖤", "Eres fuego que ilumina, no que destruye. 🕯️", "Saca esa energía haciendo algo productivo. 🔨",
        "No dejes que otros manejen tus emociones. 🎮", "Tu equilibrio volverá pronto, confía. ⚖️", "Escribe lo que sientes y luego quémalo. 📝",
        "Eres valiente por reconocer tu molestia. 🦁", "No te castigues por estar enojada. 🚫", "El perdón es para tu propia paz, no para el otro. 🗝️",
        "Busca un lugar donde puedas gritar y soltar. 🗣️", "Tu calma es tu mejor respuesta ante el caos. 🤫", "No le des poder a lo que te molesta. 🔋",
        "Eres un ser de luz atravesando una sombra. 🕯️", "Mañana verás esto con más frialdad. ❄️", "Tus sentimientos son una brújula, escúchalos. 🧭",
        "No dejes que el sol se ponga sobre tu enojo. 🌅", "Eres capaz de perdonar y seguir adelante. ✨", "La ira es una nube negra que se irá pronto. ☁️",
        "Mantén tu dignidad por encima de tu rabia. 👑", "Eres fuerte y sabrás resolver esto con calma. 💪", "Respira paz donde otros ponen conflicto. 🕊️",
        "No te rebajes al nivel de lo que te enoja. 🪜", "Tu sonrisa es más poderosa que tu ceño fruncido. 😊", "Libérate de la carga del resentimiento. 🎒",
        "Eres una reina, no pierdas tu corona por ira. 👸", "Busca la solución, no el culpable. 💡", "Tu energía es demasiado valiosa para perderla así. 💎",
        "Siente el enojo y déjalo ir como el viento. 🌬️", "Eres paz, aunque hoy te sientas volcán. 🌋", "Todo se aclarará cuando baje la marea. 🌊",
        "Confía en tu capacidad de autocontrol. 🧠", "Eres luz, siempre luz, incluso ahora. ✨"
    ],
    "enamorada": [
        "El amor te hace brillar de una forma especial. 💕", "Tu corazón es un jardín en plena floración. 🌹", "Tienes mariposas bailando en tu interior. 🦋", 
        "Qué lindo es verte amar de esa manera. 🥰", "Tu amor es el lenguaje más bello que existe. 💖", "Eres la musa de tu propia historia de amor. 📝", 
        "Tu sonrisa tiene el nombre de alguien especial. 😊", "El amor es la mejor medicina para el alma. 💊", "Disfruta de este sentimiento tan mágico. 🪄", 
        "Eres una mujer que ama con todo el corazón. ❤️", "Que el amor sea siempre tu brújula. 🧭", "Tu brillo delata lo que siente tu alma. ✨", 
        "Amar te hace más fuerte y valiente. 🦁", "Eres el sueño de alguien hecho realidad. 💭", "Vive este romance con toda tu intensidad. 🔥",
        "Tu corazón late al ritmo de la felicidad. 💓", "Eres pura dulzura cuando estás enamorada. 🍭", "El amor te sienta mejor que cualquier joya. 💎",
        "Quédate con quien te haga sentir así de plena. 🫂", "Tu amor es una luz que ilumina a los demás. 🕯️", "Disfruta de cada detalle de este sentimiento. 🎀",
        "Eres la definición de un corazón contento. 😊", "El amor es el arte de tu alma. 🎨", "Cada suspiro lleva una dosis de alegría. 🌬️",
        "Eres correspondida por el universo entero. 🌌", "Vive tu amor sin miedos ni medidas. 🌊", "Tu felicidad es el reflejo de tu amor. 🪞",
        "Eres una bendición en la vida de quien amas. 🙌", "El amor es tu estado natural, disfrútalo. 🌸", "Qué hermoso es el mundo cuando se ama. 🌍",
        "Tu mirada brilla con una luz diferente hoy. 👁️", "Eres el poema más lindo jamás escrito. 📜", "El amor es la música de tu corazón. 🎶",
        "Sigue cultivando ese amor tan puro. 🌱", "Eres magia cuando hablas de lo que amas. 🪄", "Que este sentimiento crezca cada día más. 📈",
        "Eres el regalo más lindo que alguien puede tener. 🎁", "Tu amor no tiene fronteras ni límites. 🗺️", "Vive este cuento de hadas con alegría. 🏰",
        "Eres amada tal como eres, ¡celébralo! 🥂", "Tu corazón es un refugio de ternura. 🧸", "El amor te hace ver la belleza en todo. 🌻",
        "Eres la chispa que enciende el romance. ✨", "Disfruta de la compañía de tu persona especial. 🫂", "Tu amor es tu mayor tesoro hoy. 💰",
        "Eres una reina en el reino del amor. 👸", "Que tu vida esté siempre llena de besos y risas. 💋", "El amor es el motor de tus días. ⚙️",
        "Eres luz y amor en cada poro de tu piel. ✨", "Simplemente, déjate amar y ama mucho. ❤️"
    ]
}

COLORES = {
    "feliz": ("#F9A825", "#FFF5E1"), "triste": ("#7E57C2", "#EDE7F6"),
    "ansiosa": ("#43A047", "#E8F5E9"), "cansada": ("#42A5F5", "#E3F2FD"),
    "motivada": ("#EC407A", "#FCE4EC"), "tranquila": ("#26A69A", "#E0F2F1"),
    "enojada": ("#EF5350", "#FFEBEE"), "enamorada": ("#F06292", "#FCE4EC"),
}

EMOJIS = {
    "feliz": "😊", "triste": "😢", "ansiosa": "😰", "cansada": "😴",
    "motivada": "💪", "tranquila": "😌", "enojada": "😤", "enamorada": "🥰",
}

# --- INICIALIZACIÓN DE SESIÓN ---
if 'page' not in st.session_state:
    st.session_state.page = "bienvenida"
if 'historial' not in st.session_state:
    st.session_state.historial = []
if 'musica_activa' not in st.session_state:
    st.session_state.musica_activa = False

# --- NAVEGACIÓN ---

# 1. PANTALLA DE BIENVENIDA (Para activar audio en iOS)
if st.session_state.page == "bienvenida":
    local_css("#FF0055", "#00F7FF")
    st.markdown("<h1>🌸</h1>", unsafe_allow_html=True)
    st.title("Bienvenida, Princesa")
    st.subheader("Tu lugar seguro está listo ✨")
    st.write("Presiona el botón para entrar con música:")
    if st.button("🎵 ENTRAR AL DIARIO"):
        st.session_state.musica_activa = True
        st.session_state.page = "inicio"
        st.rerun()

# 2. PANTALLA DE INICIO (ESTADOS)
elif st.session_state.page == "inicio":
    if st.session_state.musica_activa:
        cargar_musica("la_reina.mp3")
        
    local_css("#FF0055", "#00F7FF")
    st.markdown("<h1>🌸</h1>", unsafe_allow_html=True)
    st.title("Mi Diario del Alma")
    st.subheader("¿Cómo te sientes hoy? ✨")
    
    col1, col2 = st.columns(2)
    estados = list(EMOJIS.keys())
    for i, estado in enumerate(estados):
        with col1 if i % 2 == 0 else col2:
            if st.button(f"{EMOJIS[estado]} {estado.capitalize()}"):
                st.session_state.mood = estado
                st.session_state.msg = random.choice(MENSAJES[estado])
                st.session_state.page = "mensaje"
                st.rerun()

# 3. PANTALLA DE MENSAJE Y DIARIO
elif st.session_state.page == "mensaje":
    if st.session_state.musica_activa:
        cargar_musica("la_reina.mp3")
        
    mood = st.session_state.mood
    color_accent, color_bg = COLORES[mood]
    local_css(color_accent, "#FFFFFF")
    
    st.markdown(f"<h1>{EMOJIS[mood]}</h1>", unsafe_allow_html=True)
    st.markdown(f"## Hoy te sientes {mood.upper()}")
    st.markdown(f'<div class="mensaje-box">{st.session_state.msg}</div>', unsafe_allow_html=True)
    
    if st.button("✨ Ver otro mensaje"):
        st.session_state.msg = random.choice(MENSAJES[mood])
        st.rerun()

    st.divider()
    st.subheader("Escribiendo memorias... ✍️")
    texto_diario = st.text_area("Cuéntamelo todo...", placeholder="Escribe aquí tus pensamientos del día...")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("💾 Guardar"):
            if texto_diario:
                ahora = datetime.datetime.now().strftime('%H:%M')
                fecha = datetime.date.today().strftime('%d/%m/%Y')
                st.session_state.historial.insert(0, f"📅 {fecha} [{ahora}] - Mood: {mood.upper()}\n{texto_diario}")
                st.success("Guardado en tu diario ✨")
            else:
                st.warning("Escribe algo primero.")
    with col_b:
        if st.button("← Volver"):
            st.session_state.page = "inicio"
            st.rerun()

    st.divider()
    with st.expander("🔍 Ver mi diario"):
        if st.session_state.historial:
            for entrada in st.session_state.historial:
                st.info(entrada)
        else:
            st.write("Aún no hay notas hoy. 📖")
