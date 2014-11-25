import config
import pyowm

class Locale(object):
	class LookupError(Exception):
		pass

	def __init__(self, *args, **kwargs):
		self._coords = None
		self._name = None
		self._id = None
		if 'coords' in kwargs.keys():
			self._coords = kwargs.pop('coords')
		if 'name' in kwargs.keys():
			self._name = kwargs.pop('name')
		if 'id' in kwargs.keys():
			self._name = kwargs.pop('id')
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
	def id(self):
		if self._name == '':
			return 'Unknown'
		return self._id

	@property
	def name(self):
		if self._name == '':
			return 'Unknown'
		return self._name

	@property
	def country(self):
		return self.pyowm_model.get_location().get_country()

	@property
	def pyowm_model(self):
		if self._pyowm_model == None:
			try:
				if self._coords is not None:
					self._pyowm_model = config.conn.weather_at_coords(self.lat, self.long)
				elif self.id is not None:
					self._pyowm_model = config.conn.weather_at_id(self.id)
				elif self.name is not None:
					self._pyowm_model = config.conn.weather_at_place(self.name)
				else:
					raise LookupError()
			except Exception as e:
				raise LookupError()
			if self._pyowm_model == None:
				raise LookupError()

			self._name = self._pyowm_model.get_location().get_name()
			self._coords = (self._pyowm_model.get_location().get_lat(), self._pyowm_model.get_location().get_lon())
			self._id = int(self._pyowm_model.get_location().get_ID())
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
	def temp(self):
		return str(self.pyowm_model.get_weather().get_temperature()['temp'] - 273.15)

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

def forecast(arg, t=False, verbose=True):
	instance = None
	if isinstance(arg, str):
		instance = Locale(name=arg)
	elif isinstance(arg, tuple):
		instance = Locale(coords=arg)
	elif isinstance(arg, int):
		instance = Locale(id=arg)
	f = instance.forecast
	if t:
		f += '  ' + str(int(float(instance.temp))) + u'\u00b0' + 'C'
	f += '  (%s, %s)' % (instance.name, instance.country)
	if verbose:
		print f
	return f

def test():
	chicago = Locale(name='Chicago')
	assert(chicago.name == 'Chicago')
	assert(chicago.id == None)
	assert(chicago.lat == None)
	assert(chicago.pyowm_model != None)
	assert(chicago.lat != None)
	assert(chicago.id == 4887398)
	assert(chicago.forecast)
	assert(forecast('Chicago', verbose=False) == chicago.forecast)

if __name__ == '__main__':
	from sys import argv
	if len(argv) == 2:
		arg = argv[1]
		if arg == 'test':
			test()
		else:
			try:
				forecast(arg, t=True)
			except Exception:
				exit(-1)
	else:
		print('usage: %s (test|city|coords|id)' % argv[0])
