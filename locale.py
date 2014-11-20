import config
import pyowm

class Locale(object):
	class LookupError(Exception):
		pass

	def __init__(self, *args, **kwargs):
		self._coords = None
		self._name = None
		if 'coords' in kwargs.keys():
			self._coords = kwargs.pop('coords')
		if 'name' in kwargs.keys():
			self._name = kwargs.pop('name')
		self.__dict__.update(kwargs)
		self._pyowm_model = None

	@property
	def lat(self):
		if self._coords is not None:
			return self._coords[0]
		return None

	@property
	def long(self):
		if self._coords is not None:
			return self._coords[1]
		return None

	@property
	def name(self):
		return self._name

	@property
	def pyowm_model(self):
		if self._pyowm_model == None:
			if self._coords is not None:
				try:
					self._pyowm_model = config.conn.weather_around_coords(self.lat, self.long)[0]
				except Exception as e:
					raise LookupError()
			elif self._name is not None:
				self._pyowm_model = config.conn.weather_at_place(self._name)
				if self._pyowm_model == None:
					raise LookupError()
			else:
				raise LookupError()
			self._name = self._pyowm_model.get_location().get_name()
			self._coords = (self._pyowm_model.get_location().get_lat(), self._pyowm_model.get_location().get_lon())
		return self._pyowm_model

	_lookup = {
		'day' : u'\u2600',
		'night' : u'\u263E',
		'rain' : u'\u2614',
		'snow' : u'\u2744',
		'cloudy' : u'\u2601',
		'emergency' : u'\u2639'
	}

	@property
	def forecast(self):
		# http://openweathermap.org/weather-conditions
		w = self.pyowm_model.get_weather()
		status = w.get_weather_code()

		group = status / 100
		k = None
		if group in (2, 3, 5):
			k = 'rain'
		elif group == 6:
			k = 'snow'
		elif group == 7:
			if status >= 762:
				k = 'emergency'
		elif group == 8:
			if status >= 802:
				k = 'cloudy'
		elif group == 9:
			if status <= 906 or status >= 957:
				k = 'emergency'
		if k == None:
			k = 'night'
			if w.get_sunrise_time() <= w.get_reference_time() <= w.get_sunset_time():
				k = 'day'
		return Locale._lookup[k]

if __name__ == "__main__":
	chicago = Locale(name="Chicago")
	assert(chicago.name == "Chicago")
	assert(chicago.lat == None)
	assert(chicago.pyowm_model != None)
	assert(chicago.lat != None)
	assert(chicago.forecast)
