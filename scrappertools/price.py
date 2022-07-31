#Utilidades para el manejo de los precios

#Lista negra para borrar palabras en los precios
blacklist = ['CLP$', 'CLP', 'precio', 'internet', 'normal',
                 '$', '.', ',', '&nbsp;', '\r', '\n', '\t', '\xa0']

#funcion para borrar palabras de los precios:
def price_cleaner(price):
	for word in blacklist:
			price = price.replace(word, '')
	return(price)