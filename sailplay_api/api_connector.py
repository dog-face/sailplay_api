from urllib import urlencode as encode
from urllib2 import urlopen as open
import logging
import json


class api_connector(object):
	def __init__(self, store_department_id, store_department_key, pin_code):
		self.dep_id = store_department_id
		self.dep_key = store_department_key
		self.pin_code = pin_code
		self.token = None
		
		self.sailplay_domain = "https://sailplay.net"
	
	def login(self):
		url_params = encode({
			'store_department_id': self.dep_id,
			'store_department_key': self.dep_key,
			'pin_code': self.pin_code
		})
		data = open("%s/api/v2/login/?%s" % (self.sailplay_domain, url_params)).read().decode("utf-8")
		response_json = json.loads(data)
		
		if response_json[u'status'] == u'ok':
			logging.info("sp_api_connector: login: success: [%s]" % (response_json))
			self.token = response_json[u'token']
			return self.token
		else:
			logging.error(
				"sp_api_connector: login: failure: [%s: %s] " % (response_json[u'status'], response_json[u'message']))
			return False
	
	# method is of the form "/api/vX/path/to/method/", params are a dictionary
	def api_call(self, method, params, internal=False):
		try:
			url_params = params
			
			# add token and dep id
			url_params['token'] = self.token
			url_params['store_department_id'] = self.dep_id
			
			url_params = encode(url_params)
			
			request = "%s%s?%s" % (self.sailplay_domain, method, url_params)
			data = open(request).read().decode("utf-8")
			response_json = json.loads(data)
			if internal:
				return request, response_json
			
			if response_json[u'status'] == u'ok':
				logging.info("api_call: success: [%s] " % request)
				return response_json
			else:
				logging.error("api_call: Error: [%s] [%s: %s]" %
							  (request, response_json[u'status'], response_json[u'message']))
				return False
		except Exception as e:
			logging.critical("api_call: Exception: [%s] [%s] " % (e, request))
			return False
	
	def users_info(self, origin_user_id=None, phone=None, email=None):
		try:
			url_params = {}
			if origin_user_id is not None:
				url_params['origin_user_id'] = origin_user_id
			elif email is not None:
				url_params['email'] = email
			elif phone is not None:
				url_params['phone'] = phone
			
			url_params = encode(url_params)
			
			request, response_json = self.api_call("/api/v2/users/info/", url_params, internal=True)
			
			if response_json[u'status'] == u'ok':
				logging.info("users_info: [%s] found" % request)
				return response_json
			else:
				logging.error("users_info: Error: [%s] not found: [%s: %s]" %
							  (request, response_json[u'status'], response_json[u'message']))
				return False
		except Exception as e:
			logging.critical("users_info: Exception: [%s]" % e)
			return False
	
	def users_add(self, origin_user_id=None, phone=None, email=None, first_name=None, middle_name=None, last_name=None,
				  birth_date=None, sex=None):
		try:
			
			url_params = {}
			
			if origin_user_id is not None:
				url_params['origin_user_id'] = origin_user_id
			if phone is not None:
				url_params['phone'] = phone
			if email is not None:
				url_params['email'] = email
			if first_name is not None:
				url_params['first_name'] = first_name
			if middle_name is not None:
				url_params['middle_name'] = middle_name
			if last_name is not None:
				url_params['last_name'] = last_name
			if birth_date is not None:
				url_params['birth_date'] = birth_date
			if sex is not None:
				url_params['sex'] = sex
			
			request, response_json = self.api_call("/api/v2/users/add/", url_params, internal=True)
			
			if response_json[u'status'] == u'ok':
				logging.info("users_add: created [%s]" % request)
				return response_json
			else:
				logging.error("users_add: Error: [%s] not created: [%s: %s]" % (
					request, response_json[u'status'], response_json[u'message']))
				return False
		
		except Exception as e:
			logging.critical("users_add: Exception: [%s]" % e)
			return False
		
	def users_update(self, origin_user_id=None, phone=None, email=None, first_name=None, middle_name=None, last_name=None,
				  birth_date=None, sex=None, add_phone=None, add_email=None, new_phone=None, new_email= None):
		try:
			
			url_params = {}
			
			if origin_user_id is not None:
				url_params['origin_user_id'] = origin_user_id
			if phone is not None:
				url_params['phone'] = phone
			if email is not None:
				url_params['email'] = email
			if first_name is not None:
				url_params['first_name'] = first_name
			if middle_name is not None:
				url_params['middle_name'] = middle_name
			if last_name is not None:
				url_params['last_name'] = last_name
			if birth_date is not None:
				url_params['birth_date'] = birth_date
			if sex is not None:
				url_params['sex'] = sex
			if add_phone is not None:
				url_params['add_phone'] = add_phone
			if add_email is not None:
				url_params['add_email'] = add_email
			if new_phone is not None:
				url_params['new_phone'] = new_phone
			if new_email is not None:
				url_params['new_email'] = new_email
			
			request, response_json = self.api_call("/api/v2/users/update/", url_params, internal=True)
			
			if response_json[u'status'] == u'ok':
				logging.info("users_update: updated [%s]" % request)
				return response_json
			else:
				logging.error("users_update: Error: [%s] not updated: [%s: %s]" % (
					request, response_json[u'status'], response_json[u'message']))
				return False
		
		except Exception as e:
			logging.critical("users_update: Exception: [%s]" % e)
			return False
		
		
	#  Provide tags as a list
	def users_tags_add(self, tags, origin_user_id=None, phone=None, email=None, language=None):
		try:
			url_params = {
				'tags': ",".join(tags)
			}
			
			if origin_user_id is not None:
				url_params['origin_user_id'] = origin_user_id
			if phone is not None:
				url_params['phone'] = phone
			if email is not None:
				url_params['email'] = email
			if language is not None:
				url_params['language'] = language
			
			request, response_json = self.api_call("/api/v2/users/tags/add/", url_params, internal=True)
			
			if response_json[u'status'] == u'ok':
				logging.info("users_tags_add: updated [%s]" % request)
				return response_json
			else:
				logging.error("users_tags_add: Error: [%s] not updated: [%s: %s]" % (
					request, response_json[u'status'], response_json[u'message']))
				return False
		
		except Exception as e:
			logging.critical("users_tags_add: Exception: [%s]" % e)
			return False
			
	#  Provide tags as a list
	def users_tags_delete(self, tags, origin_user_id=None, phone=None, email=None, language=None):
		try:
			
			url_params = {
				'tags': ",".join(tags)
			}
			
			if origin_user_id is not None:
				url_params['origin_user_id'] = origin_user_id
			if phone is not None:
				url_params['phone'] = phone
			if email is not None:
				url_params['email'] = email
			if language is not None:
				url_params['language'] = language
			
			request, response_json = self.api_call("/api/v2/users/tags/delete/", url_params, internal=True)
			
			if response_json[u'status'] == u'ok':
				logging.info("users_tags_delete: updated [%s]" % request)
				return response_json
			else:
				logging.error("users_tags_delete: Error: [%s] not updated: [%s: %s]" % (
					request, response_json[u'status'], response_json[u'message']))
				return False
		
		except Exception as e:
			logging.critical("users_tags_delete: Exception: [%s]" % e)
			return False
		
		
	def purchases_new(self, order_num, cart, origin_user_id=None, phone=None, email=None):
		try:
			url_params = {
				'pin_code': self.pin_code,
				'order_num': order_num,
				'cart': cart
			}
			
			if origin_user_id is not None:
				url_params['origin_user_id'] = origin_user_id
			elif phone is not None:
				url_params['phone'] = phone
			elif email is not None:
				url_params['email'] = email

			request, response_json = self.api_call("/api/v2/purchases/new/", url_params, internal=True)
			
			if response_json[u'status'] == u'ok':
				logging.info("purchases_new: [%s] purchase added [%s]" % (order_num, request))
				return response_json
			else:
				logging.error("purchases_new: Error: [%s] purchase not added: [%s: %s]" % (
					request, response_json[u'status'], response_json[u'message']))
				return False
		
		
		except Exception as e:
			logging.critical("purchases_new: Exception: [%s]" % e)
			return False
	
	def points_add(self, points, origin_user_id=None, phone=None, email=None, comment=None, order_num=None):
		try:
			url_params = {
				'points': points
			}
			
			if origin_user_id is not None:
				url_params['origin_user_id'] = origin_user_id
			elif phone is not None:
				url_params['phone'] = phone
			elif email is not None:
				url_params['email'] = email
			if comment is not None:
				url_params['comment'] = comment
			if order_num is not None:
				url_params['order_num'] = order_num
			
			request, response_json = self.api_call("/api/v2/points/add/", url_params, internal=True)
			
			if response_json[u'status'] == u'ok':
				logging.info("points_add: [%s] points added [%s]" % (points, request))
				return response_json
			else:
				logging.error("points_add: Error: [%s] points not added: [%s: %s]" % (
					request, response_json[u'status'], response_json[u'message']))
				return False
		
		except Exception as e:
			logging.critical("points_add: Exception: [%s]" % e)
			return False
		
	def products_add(self, sku, name=None, price=None, category_sku=None, points_rate=None):
		try:
			url_params = {
				'sku': sku
			}
			
			if name is not None:
				url_params['name'] = name
			if price is not None:
				url_params['price'] = price
			if category_sku is not None:
				url_params['category_sku'] = category_sku
			if points_rate is not None:
				url_params['points_rate'] = points_rate
			
			request, response_json = self.api_call("/api/v2/basket/products/add/", url_params, internal=True)
			
			if response_json[u'status'] == u'ok':
				logging.info("products_add: [%s] product added [%s]" % (sku, request))
				return response_json
			else:
				logging.error("products_add: Error: [%s] product not added: [%s: %s]" % (
					request, response_json[u'status'], response_json[u'message']))
				return False
		
		except Exception as e:
			logging.critical("products_add: Exception: [%s]" % e)
			return False
		
	def products_edit(self, sku, name=None, price=None, category_sku=None, points_rate=None):
		try:
			url_params = {
				'sku': sku
			}
			
			if name is not None:
				url_params['name'] = name
			if price is not None:
				url_params['price'] = price
			if category_sku is not None:
				url_params['category_sku'] = category_sku
			if points_rate is not None:
				url_params['points_rate'] = points_rate
			
			request, response_json = self.api_call("/api/v2/basket/products/edit/", url_params, internal=True)
			
			if response_json[u'status'] == u'ok':
				logging.info("products_edit: [%s] product edited [%s]" % (sku, request))
				return response_json
			else:
				logging.error("products_edit: Error: [%s] product not edited: [%s: %s]" % (
					request, response_json[u'status'], response_json[u'message']))
				return False
		
		except Exception as e:
			logging.critical("products_edit: Exception: [%s]" % e)
			return False
		
	def products_attributes_add(self, sku, attribute_sku, value_sku):
		try:
			url_params = {
				'sku': sku,
				'attribute_sku': attribute_sku,
				'value_sku': value_sku
			}
			
			request, response_json = self.api_call("/api/v2/basket/products/attributes/add/", url_params, internal=True)
			
			if response_json[u'status'] == u'ok':
				logging.info("products_attributes_add: [%s] product attribute added [%s]" % (sku, request))
				return response_json
			else:
				logging.error("products_attributes_add: Error: [%s] product attribute not added: [%s: %s]" % (
					request, response_json[u'status'], response_json[u'message']))
				return False
		
		except Exception as e:
			logging.critical("products_attributes_add: Exception: [%s]" % e)
			return False
		
	def products_attributes_edit(self, sku, attribute_sku, value_sku_from, value_sku_to):
		try:
			url_params = {
				'sku': sku,
				'attribute_sku': attribute_sku,
				'value_sku_from': value_sku_from,
				'value_sku_to': value_sku_to
			}
			
			request, response_json = self.api_call("/api/v2/basket/products/attributes/edit/", url_params, internal=True)
			
			if response_json[u'status'] == u'ok':
				logging.info("products_attributes_edit: [%s] product attribute edited [%s]" % (sku, request))
				return response_json
			else:
				logging.error("products_attributes_edit: Error: [%s] product attribute not edited: [%s: %s]" % (
					request, response_json[u'status'], response_json[u'message']))
				return False
		
		except Exception as e:
			logging.critical("products_attributes_edit: Exception: [%s]" % e)
			return False
		
	def products_categories_add(self, sku, parent_sku=None, name=None, pic=None, points_rate=None):
		try:
			url_params = {
				'sku': sku
			}
			
			if parent_sku is not None:
				url_params['parent_sku'] = parent_sku
			if name is not None:
				url_params['name'] = name
			if pic is not None:
				url_params['pic'] = pic
			if points_rate is not None:
				url_params['points_rate'] = points_rate
			
			request, response_json = self.api_call("/api/v2/basket/categories/add/", url_params, internal=True)
			
			if response_json[u'status'] == u'ok':
				logging.info("products_categories_add: [%s] product category added [%s]" % (sku, request))
				return response_json
			else:
				logging.error("products_categories_add: Error: [%s] product category not added: [%s: %s]" % (
					request, response_json[u'status'], response_json[u'message']))
				return False
		
		except Exception as e:
			logging.critical("products_categories_add: Exception: [%s]" % e)
			return False
		
	def products_categories_edit(self, sku, parent_sku=None, name=None, pic=None, points_rate=None):
		try:
			url_params = {
				'sku': sku
			}
			
			if parent_sku is not None:
				url_params['parent_sku'] = parent_sku
			if name is not None:
				url_params['name'] = name
			if pic is not None:
				url_params['pic'] = pic
			if points_rate is not None:
				url_params['points_rate'] = points_rate
	
			request, response_json = self.api_call("/api/v2/basket/categories/edit/", url_params, internal=True)
			
			if response_json[u'status'] == u'ok':
				logging.info("products_categories_edit: [%s] product category edited [%s]" % (sku, request))
				return response_json
			else:
				logging.error("products_categories_edit: Error: [%s] product category not edited: [%s: %s]" % (
					request, response_json[u'status'], response_json[u'message']))
				return False
		
		except Exception as e:
			logging.critical("products_categories_edit: Exception: [%s]" % e)
			return False
		
	#Convert a dictionary of the form {sku: {quantity, price}, sku: {quantity, price}, ...} into a valid cart string
	def to_cart(self, cart_dict):
		index = 1
		cart_string = "{"
		for sku in cart_dict:
			this_item = cart_dict[sku]
			cart_string += "\"" + str(index) + "\":{\"sku\":\"" + str(sku) + "\",\"quantity\":" + \
						   str(this_item['quantity']) + ",\"price\":" + str(this_item['price']) + "},"
			index += 1
		cart_string = cart_string[:-1] + "}" # Trim last "," and close braces
		return cart_string