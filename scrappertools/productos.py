import validators

#implementacion de clase producto:

class Product:
	def __init__(self, category, store, url, name, stock, price, sku=None, picture_urls=None):
	
		assert len(name) <= 256
		assert isinstance(stock, int)

		if picture_urls:
			for picture_url in picture_urls:
				assert validators.url(picture_url), picture_url

		self.category = category
		self.store = store
		self.url = url
		self.name = name
		self.sku = sku
		self.stock = stock
		self.price = price
		self.picture_urls = picture_urls

	def print_products(self):
		print("Producto: ", self.name, self.category, self.store, self.url, self.name, self.sku, self.stock, self.price, self.picture_urls)
