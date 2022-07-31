from bs4 import BeautifulSoup
import requests
import json

from scrappertools.price import *
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
		["bicicletas/monta-a", MTB],
		["bicicletas/urbana", CITY_BIKES],
		["bicicletas/ruta", ROAD_BIKES],
		["162/ciclismo/componentes-de-bicicleta?initialMap=productClusterIds&initialQuery=162&map=productClusterIds", CHAINS]
	]
	
	product_urls = []

	for category_path, local_category in url_extensions:
		if local_category != category:
			continue

		page = 1
		contador = 0
		done = False
		
		while True:
			old_page = page
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
					
discover_category_urls(categoria)
