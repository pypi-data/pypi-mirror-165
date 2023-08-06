"""Модуль функций библиотеки"""

import requests, json, time, random
from . import __version__

def safe_request(mode, url, headers=None, body=None, try_number=1):
	"""Функция безопасного запроса на timeout

    :param mode: метод запроса (get,post,patch,delete)
    :type mode: str
    :param url: адрес запроса
    :type url: str
    :param headers: заголовки запроса
    :type headers: dict
    :param body: тело запроса (если предусмотрено)
    :type body: dict
    :param try_number: номер попытки передачи запроса
    :type try_number: int
    :return: результат запроса
    :rtype: dict
    """

	try:
		if mode == 'post': response = requests.post(url, data=body, headers=headers).json()
		if mode == 'put': response = requests.put(url, data=body, headers=headers).json()
		if mode == 'get': response = requests.get(url, headers=headers).json()
		if mode == 'patch': response = requests.patch(url, data=body, headers=headers).json()
		if mode == 'delete': response = requests.delete(url, headers=headers).json()

	except (requests.exceptions.ConnectionError, json.decoder.JSONDecodeError):
		time.sleep(2**try_number + random.random()*0.01)
		return safe_request(mode, url, headers, body, try_number=try_number+1)

	else:
		return response
