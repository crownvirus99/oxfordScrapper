from bs4 import BeautifulSoup
import requests
from categorias import MTB, ROAD_BIKES, CHAINS, CITY_BIKES

blacklist = ['CLP$', 'CLP', 'precio', 'internet', 'normal',
                 '$', '.', ',', '&nbsp;', '\r', '\n', '\t', '\xa0']

categoria = "Chains"

def categories(cls):
	return [
		MTB,
		ROAD_BIKES,
		CHAINS,
		CITY_BIKES
	]
	
#discover urls
def discover_category_urls(category):
	url_extensions = [
		["bicicletas/monta-a", MTB],
		["bicicletas/urbana", CITY_BIKES],
		["bicicletas/ruta", ROAD_BIKES],
		["componentes/transmision/cadenas", CHAINS]
	]
	
	product_urls = []

	for category_path, local_category in url_extensions:
		if local_category != category:
			continue
	
		done = False
		page = 1
		contador = 0
		
		while not done:
			category_url = "https://www.oxfordstore.cl/{}.html?p={}" \
		                    .format(category_path, page)
			print(category_url)
			data = requests.get(category_url).text
			soup = BeautifulSoup(data, 'html.parser')
			product_containers = soup.findAll("li", "item product product-item")
			
			if not product_containers:
				if page == 1:
					raise Exception('Empty category: ' + category_path)
					break
				if page != 1:
					done = True
					break
			
			for container in product_containers:
				product_url = container.find('a')['href']
				print("product: ", product_url)
				product_urls.append(product_url)
				contador += 1
				
			print("Contador: ", contador, "Page: ", page, "Done: ", done)
			page += 1
			
	return(product_urls)

discover_category_urls(categoria)

#products:
def product_info(url):
    response = requests.get(url).text

    soup = BeautifulSoup(response, 'html.parser')
    name = soup.find("h1", "page-title").text.strip()
    print(name)

    sku = soup.find("div", "value").text.strip()
    print(sku)

    stock = soup.find("div", "availability in-stock")
    if stock.find("en tienda web") == -1:
        stock = "No Disponible"
    else:
        stock = "Disponible"
    print(stock)

    price = soup.find("span", "price").text.strip()
    for word in blacklist:
    	price = price.replace(word, '')
    print(price)

    #descripcion

    picture_urls = [tag['src'] for tag in
										soup.findAll('img', 'gallery-placeholder__image')]
    #picture_urls = soup.find('img', 'gallery-placeholder__image')
    print(picture_urls)

    return("Producto terminado")
