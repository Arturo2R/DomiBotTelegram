import os
import logging
import telegram
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
import calculos

data = {
  'To_Address': '',
  'From_Address': '',
  'To_Name': '',
  'From_Name': '',
  'Distance': 0,
  'Total_Price': 0,
  'Phone_Number': 0
}

Update = telegram.Update
my_secret = os.environ['TELEGRAM_TOKEN']

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

FROM_NAME, FROM_ADDRESS, TO_NAME, TO_ADDRESS, PRICE, ACCEPT, ERROR = range(7)

mensaje_bienvenida = "Hola! 👋 gracias por comunicarte con MENSAJERIA AA, tu domicilio de confianza 🏍💨. Si deseas un servicio por favor regalanos los siguientes datos: \n🔲📍Dirección de origen(Barrio, casa o edificio/apto)\nDirección de entrega(Barrio, casa o edificio/apto)\n🔲👤Nombre y de las personas que entregan y reciben(Especifica quien paga el servicio)\n🔲📦Tipo de producto que desea transportar\n✔El precio del servicio te lo facilitaremos de inmediato he iniciaremos luego de su confirmación. Si te equivocas en algún momento porfavor escribe /cancel para empezar de nuevo"

def start(update: Update, _: CallbackContext) -> int:
  print(update.effective_chat.id)
  update.message.reply_text(mensaje_bienvenida)
  update.message.reply_text('Para proceder con el pedido porfavor envianos tu nombre')

  return FROM_NAME

def from_name(update: Update, _: CallbackContext) -> int:
  #user = update.message.from_user
  logger.info("Nombre Completo del usuario of %s", update.message.text)
  update.message.reply_text(
    'Ahora Enviame la dirección de salida',
  )
  

  data['From_Name'] = update.message.text
  return FROM_ADDRESS

def from_address(update: Update, _: CallbackContext) -> int:
  

  while True:
    validation_address = calculos.regeValidation(update.message.text, 'address')
    if validation_address:
      data['From_Address'] = update.message.text
      logger.info("Dirección de salida es %s", update.message.text)
      update.message.reply_text(
      'Ahora Enviame el nombre de la persona que recibira el paquete')
      break  
    else:
        update.message.reply_text(
          'Esta mal escrito por favor intente de nuevo')
        return FROM_ADDRESS

  

    

  return TO_NAME

def to_name(update: Update, _: CallbackContext) -> int:
  logger.info("Dirección del destino es %s", update.message.text)
  update.message.reply_text(
    'Ahora Enviame la dirección de la persona que recibira el paquete')
  data['To_Name'] = update.message.text


  return TO_ADDRESS

def to_address(update: Update, _: CallbackContext) -> int:
  
  data['To_Address'] = update.message.text
  #Calcular el Precio Y Decirlo




  while True:
    validation_address = calculos.regeValidation(update.message.text, 'address')
    if validation_address:
      data['TO_ADDRESS'] = update.message.text
      
      break  
    else:
        update.message.reply_text(
          'Esta mal escrito por favor intente de nuevo')
        return TO_ADDRESS


  km = calculos.address_and_distance(data['From_Address'], data['To_Address'])
  data['Distance'] = km
  pesos = calculos.precio_total(km)
  data['Total_Price'] = pesos

  # = #Distancia
  update.message.reply_text(f'El precio es de {pesos} , diga si para aceptar')
  # = #Precio
  return ACCEPT

def accept(update: Update, _: CallbackContext) -> int:
  user = update.message.from_user
  respuesta = str.lower(update.message.text)

  logger.info("%s, pidio exitosamente", user.first_name)

  if respuesta == 'si' :
    #Guardar en La Base De Datos
    # Ejecutar el Webhook
    # Escribir en el grupo de telegram


    update.message.reply_text(
      'Ok Su Pedido Se Ha Procesado y  llegara lo más pronto posible'
    )
  else:
    update.message.reply_text(
      'Ok Aqui estaremos siempre para usted'
    )
  

  return ConversationHandler.END

def cancel(update: Update, _: CallbackContext) -> int:
  user = update.message.from_user
  logger.info("User %s canceled the conversation.", user.first_name)
  update.message.reply_text(
      'Bye! I hope we can talk again some day.'
  )

  return ConversationHandler.END

def main() -> None:
  updater = Updater(my_secret)

  dispatcher = updater.dispatcher

  conv_handler = ConversationHandler(
    entry_points= [CommandHandler('start', start)],
    states={
      FROM_NAME: [MessageHandler(Filters.text, from_name)],
      FROM_ADDRESS: [MessageHandler(Filters.text, from_address)],
      TO_NAME: [MessageHandler(Filters.text, to_name)],
      TO_ADDRESS: [MessageHandler(Filters.text, to_address)],      
      ACCEPT: [MessageHandler(Filters.text, accept)],
      
    },
    fallbacks=[CommandHandler('cancelar', cancel)]
  )

  dispatcher.add_handler(conv_handler)

  updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
  updater.idle()

if __name__ == '__main__':
  main()