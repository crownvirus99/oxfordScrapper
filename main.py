from bs4 import BeautifulSoup
import requests
import json

from scrappertools.productos import Product
from scrappertools.categorias import MTB, ROAD_BIKES, CHAINS, CITY_BIKES

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
		["143/ciclismo/bicicletas-y-cuadros?initialMap=productClusterIds&initialQuery=143&map=productClusterIds", MTB],
		["152/ciclismo/bicicletas-y-cuadros?initialMap=productClusterIds&initialQuery=152&map=productClusterIds", CITY_BIKES],
		["146/ciclismo/bicicletas-y-cuadros?initialMap=productClusterIds&initialQuery=146&map=productClusterIds", ROAD_BIKES],
		["162/ciclismo/componentes-de-bicicleta?initialMap=productClusterIds&initialQuery=162&map=productClusterIds", CHAINS]
	]
	
	product_urls = []

	for category_path, local_category in url_extensions:
		if local_category != category:
			continue

		page = 1
		contador = 0
		
		while True:
			category_url = "https://www.montenbaik.com/{}&page={}" \
			.format(category_path, page)
			#print(category_url)
			retries = 3
			while retries:
				data = requests.get(category_url).text
				soup = BeautifulSoup(data, 'html.parser')
				json_data = json.loads(soup.findAll(
					"script", {"type" : "application/ld+json"})[1].text)
				if not json_data:
					retries -= 1
				else:
					retries = 0
				print("retries: ", retries, "page: ", page)

			item_list = json_data["itemListElement"]

			if len(item_list) == 0:
				if page == 1:
					print("empty category")
				break
			else:
				for i in item_list:
					if "item" in i:
						contador +=1
						print(contador)
						print(i["item"]["@id"])
						product_urls.append(i["item"]["@id"])
			page += 1

		return("pepo")
					
#discover_category_urls(categoria)

def product_info(cls, url, category=None):
	print (url)
	response = requests.get(url).text
	soup = BeautifulSoup(response, 'html.parser')
	
	json_tags = soup.findAll("script", {'type': 'application/ld+json'})

	if not json_tags:
		return[]

	json_data = json.loads(json_tags[0].text)
	
	#name
	name = json_data["name"]
	print(name)
	
	#sku
	sku = str(json_data["sku"])
	print(sku)

	#stock
	stock = json_data['offers']['offers'][0]['availability']
	if stock == "http://schema.org/InStock":
			stock = -1
	else:
			stock = 0
	print(stock)

	#price
	price = json_data['offers']['offers'][0]['price']
	print(price)

	#descripcion
	description = json_data['description']
	print(description)

	#pictures
	picture_urls = json_data['image']
	print(picture_urls)

	p = Product(
		category,
		cls,
		url,
		name,
		stock,
		price,
		sku,
	)

	p.print_products()
	
	return [p]

#cadena = product_info("montenbaik", "https://www.montenbaik.com/cadena-cn12a-12v-126-eslabones-sunrace/p", "chains")