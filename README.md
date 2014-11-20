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
print locale.Locales(name="Chicago").forecast
```
