while True:
    #importación de bibliotecas
    import telebot as tb
    import os
    from dotenv import load_dotenv
    from telebot.types import ReplyKeyboardMarkup, KeyboardButton

    #configuración identificador ("token") del bot
    load_dotenv()
    REMItoken=os.getenv("REMItoken")
    bot=tb.TeleBot(REMItoken)

    #administración de mensajes:

    usuarios_en_modo_transmision={}

    @bot.message_handler(commands=['start'])
    def bienvenida(message): #mensaje de bienvenida
        bot.reply_to(message, "Bienvenido a la interfaz de control del Sistema R.E.M.I., Usuario. Envía el comando /help para ayuda.")


    @bot.message_handler(commands=['help'])
    def ayuda(message):  # mensaje de bienvenida
        bot.reply_to(message,"Bienvenido a la sección de ayuda. Nuestros comandos son: ")
        bot.send_message(message.chat.id, "Para recibir una imagen usa /visual. Para recibir audio usa /acustica. Para recibir un sticker usa /sticker. Para acceder al menú usa /menu. Para iniciar el trabajo de transmisión remota de mensajes escritos con cifrado, usa /transmision.")



    #Ensayo de laboratorio: Respuesta ante texto
    @bot.message_handler(func=lambda message: message.text in ["sc?"])
    def stratcom(message):
        bot.send_message(message.chat.id, "StratCom  A C T I V E")

    @bot.message_handler(func=lambda message: message.text in ["pik"])
    def pik(message):
        bot.send_message(message.chat.id, "PIKMIN")


    #Ensayo Multimedia
    #
    #@bot.message_handler(commands=["visual"])
    @bot.message_handler(commands=["visual"])
    def visual(message):
        bot.reply_to(message, "Aquí está tu foto: ")
        photo=open('trans.jpg','rb')
        bot.send_photo(message.chat.id, photo)

    @bot.message_handler(commands=["acustica"])
    def acustica(message):
        bot.reply_to(message, "Aquí está tu audio: ")
        audio=open('aud.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)


    @bot.message_handler(commands=["sticker"])
    def estiquer(message):
        bot.reply_to(message, "Aquí está tu sticker: ")
        estiquer=open('estiquer.webp', 'rb')
        bot.send_sticker(message.chat.id, estiquer)

    #creación del menú de acciones:
    @bot.message_handler(commands=["menu"])
    def menu(message):
        data=["/start","/help","sc?","pik","/visual","/acustica","/sticker"]
        teclado=ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        botones=[KeyboardButton(str(comandos)) for comandos in data]
        teclado.add(*botones)
        bot.send_message(message.chat.id, "Seleccione un Comando: ", reply_markup=teclado)


    @bot.message_handler(commands=["transmision"])
    def transmision(message):
        user_id = message.from_user.id
        usuarios_en_modo_transmision[user_id] = True
        bot.send_message(message.chat.id,
                         "Perfecto, envíanos el mensaje que deseas transmitir. Escribe 'stop' cuando termines para salir del modo transmisión.")


    @bot.message_handler(func=lambda message: True)
    def recepcion(message):
        user_id = message.from_user.id
        texto = message.text.strip()

        if usuarios_en_modo_transmision.get(user_id):
            if texto.lower() == "stop":
                usuarios_en_modo_transmision[user_id] = False
                bot.reply_to(message, "Modo de transmisión finalizado. Puedes seguir usando los comandos normalmente.")
            else:
                nombre_archivo = "comunicado.json"
                with open(nombre_archivo, 'a', encoding='utf-8') as f:
                    f.write(texto + '\n')

                bot.reply_to(message, "Listo. Tu mensaje a transmitir es:")
                bot.send_message(message.chat.id, texto)
                bot.reply_to(message,
                             "Esta es una copia para que verifiques que todo está en orden. Tu mensaje se ha añadido a la fila y se transmitirá pronto. Muchas gracias por usar R.E.M.I.")
        else:
            bot.reply_to(message, "Usa el comando /transmision para enviar un nuevo mensaje al sistema R.E.M.I.")
            #bot.reply_to(update,"Esta es una copia para que verifiques que todo está en orden. Tu mensaje se ha añadido a la fila y se transmitirá pronto. Muchas gracias por usar R.E.M.I.")

    bot.infinity_polling()