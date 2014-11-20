pydrizzle
====

Silly Project Returning Current Weather in Unicode

dependencies
====
* [OpenWeatherMap API key](http://openweathermap.org/appid)
* [pyowm](https://github.com/csparpa/pyowm)

installation
====

```bash
pip install pyowm
```

usage
====

```python
import locale
print locale.Locale(name="Chicago").forecast
print locale.Locale(name="Mt. Rushmore").forecast
print locale.Locale(coords=(-22.57, -43.12)).forecast

# wrapper function
f = locale.forecast('Chicago', verbose=False)
assert(f == locale.Locale(name='Chicago').forecast)
```
