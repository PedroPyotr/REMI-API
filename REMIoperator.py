while True:
    #importación de bibliotecas
    import telegram
    import telebot as tb
    import os
    import threading
    from dotenv import load_dotenv

    #configuración identificador ("token") del bot
    load_dotenv()
    REMItoken=os.getenv("REMItoken")
    bot=tb.TeleBot(REMItoken)

    #administración de mensajes:
    def inicio(message):
        bot.send_message(message.chat.id, "Bienvenido a la interfaz de ensayo del sistema Rapid Encrypted Messaging Interface (R.E.M.I.)")

    @bot.message_handler(commands=['iniciar', 'asistencia'])
    def bienvenida(message): #mensaje de bienvenida
        bot.reply_to(message, "Bienvenido a la interfaz de control del Sistema R.E.M.I., Usuario.")

    #Ensayo de laboratorio: Respuesta ante texto
    @bot.message_handler(func=lambda message: message.text in ["sc?"])
    def stratcom(message):
        bot.send_message(message.chat.id, "StratCom  A C T I V E")

    @bot.message_handler(func=lambda message: message.text in ["pik"])
    def pik(message):
        bot.send_message(message.chat.id, "PIKMIN")

    @bot.message_handler(func=lambda message: True)
    def eco(message):
        bot.reply_to(message, "Eco: " + message.text)

    #Ensayo Multimedia
    #
    #@bot.message_handler(commands=["visual"])
    @bot.message_handler(func=lambda message: message.text in ["Visual"])
    def visual(message):
        photo=open('trans.jpg','rb')
        bot.send_photo(message.chat.id, photo)

    @bot.message_handler(commands=["acustica"])
    def acustica(message):
        audio=open('aud.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)


    @bot.message_handler(commands=["sticker"])
    def estiquer(message):
        estiquer=open('estiquer', 'rb')
        bot.send_message(message.chat.id, estiquer)

    #creación del menú de acciones:
    @bot.message_handler(commands=["menu"])
    def menu(message):
        data=["iniciar","asistencia","sc","Pik","visual","acustica","sticker"]
        teclado=ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        botones=[KeyboardButton(str(comandos)) for comandos in data]
        teclado.add(*botones)
        bot.send_message(message.chat.id, "Seleccione un Comando: ", reply_markup=teclado)

    bot.infinity_polling()