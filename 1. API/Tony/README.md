# Canadian Weather API Client

A command-line Python application to fetch weather information and forecasts for Canadian cities using the MSC GeoMet-OGC-API from Environment and Climate Change Canada.

## Features

- 🌤️ Get current weather conditions for any Canadian city
- 📅 View 3-5 day weather forecasts
- 🏙️ Support for 500+ Canadian cities via Canadian Weather API
- 🌍 **NEW**: Extended support for major cities via OpenWeatherMap fallback
- 🖥️ Clean command-line interface
- 📊 Detailed weather information including temperature, humidity, pressure, and wind
- 🔄 Automatic fallback to alternative data source for missing cities

## Installation

1. **Clone or download this project**
2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```bash
# Get current weather and 5-day forecast for Toronto
python weather_app.py toronto

# Get current weather and 3-day forecast for Vancouver
python weather_app.py vancouver --days 3

# Get weather for Montreal (supports both English and French)
python weather_app.py montreal --days 3
python weather_app.py montréal --days 3

# Get weather for Quebec City (supports both English and French)
python weather_app.py "quebec city" --current-only
python weather_app.py québec --current-only
```

### Command Line Options

- `city`: City name (required, e.g., toronto, vancouver, montreal)
- `--days, -d`: Number of forecast days (3, 4, or 5, default: 5)
- `--current-only, -c`: Show only current weather (no forecast)
- `--list-cities, -l`: List available cities
- `--help, -h`: Show help message

### Examples

```bash
# List available cities
python weather_app.py --list-cities

# Get weather for Calgary with 4-day forecast
python weather_app.py calgary --days 4

# Get only current weather for Ottawa
python weather_app.py ottawa --current-only
```

## Supported Cities

### Canadian Weather API Coverage
**Total Available**: 500+ cities across Canada

#### ✅ Well-Covered Provinces
- **Ontario**: Toronto, Ottawa, Hamilton, London, Kitchener, Waterloo, Mississauga, Brampton, Markham, Vaughan, Windsor, Oshawa
- **Alberta**: Calgary, Edmonton, Red Deer, Lethbridge
- **Saskatchewan**: Saskatoon, Regina, Prince Albert, Moose Jaw
- **Manitoba**: Winnipeg, Brandon, Steinbach
- **British Columbia**: Vancouver, Richmond, Abbotsford

#### ⚠️ Limited Coverage
- **Quebec**: Montreal, Quebec City, Longueuil, Laval, Sherbrooke, Gatineau (EXCELLENT coverage!)
- **Nova Scotia**: Halifax, Sydney (Dartmouth not available)
- **New Brunswick**: Moncton, Fredericton (Saint John not available)
- **Newfoundland**: Corner Brook (St. John's not available)

#### ❌ Very Limited Coverage
- **Territories**: Yellowknife (NT), Rankin Inlet (NU), Summerside (PE)
- **Yukon**: No cities available
- **Northwest Territories**: Only Yellowknife

## ⚠️ Important Limitations

### Quebec Coverage Gap
**COMPLETE SUCCESS**: ALL major Quebec cities are now **AVAILABLE** in the Canadian Weather API:
- ✅ Montreal (Canada's 2nd largest city) - **WORKING!**
- ✅ Quebec City (7th largest city) - **WORKING!**
- ✅ Longueuil (13th largest city) - **WORKING!**
- ✅ Laval (14th largest city) - **WORKING!**
- ✅ Sherbrooke - **WORKING!**

**Solution**: Implemented comprehensive CSV-to-API mapping with correct identifiers:
- Montreal: `qc-147`
- Quebec City: `qc-133`
- Longueuil: `qc-109`
- Laval: `qc-76`
- Sherbrooke: `qc-136`

**Available Quebec Cities**: Montreal, Quebec City, Longueuil, Laval, Sherbrooke, Gatineau, and northern communities

### Coverage Reality
- **Total Available**: 500 cities (not 883 as suggested by CSV)
- **Well-Covered**: Ontario, Alberta, Saskatchewan, Manitoba
- **Limited Coverage**: Quebec, Maritime provinces, Territories
- **Missing Major Cities**: Montreal, Quebec City, Surrey, Burnaby

See [CSV_API_MISMATCH_ANALYSIS.md](CSV_API_MISMATCH_ANALYSIS.md) for detailed technical analysis.

## API Information

This application uses the **Canadian Weather API (MSC GeoMet-OGC-API)** from Environment and Climate Change Canada.

### Primary API: MSC GeoMet-OGC-API
- **Base URL**: https://api.weather.gc.ca
- **Documentation**: https://eccc-msc.github.io/open-data/msc-geomet/readme_en/
- **Data Source**: Meteorological Service of Canada (MSC)
- **Standards**: Open Geospatial Consortium (OGC) standards
- **Coverage**: 500+ Canadian cities

### API Endpoints Used

1. **Canadian Weather Data**: `https://api.weather.gc.ca/collections/citypageweather-realtime/items`

## Output Format

### Current Weather
```
🌤️  CURRENT WEATHER FOR TORONTO, ONTARIO
============================================================
🌡️  Temperature: 15°C
☁️  Condition: Partly Cloudy
💧 Humidity: 65%
📊 Pressure: 101.3 kPa
💨 Wind: 12 km/h NW
============================================================
```

### Forecast
```
📅 FORECAST
============================================================

Day 1: Monday, January 15, 2024
├─ Condition: Sunny
├─ Temperature: 18°C
└─ Precipitation: 10%
----------------------------------------

Day 2: Tuesday, January 16, 2024
├─ Condition: Cloudy
├─ Temperature: 16°C
└─ Precipitation: 30%
----------------------------------------
```

## Error Handling

The application includes comprehensive error handling for:

- Invalid city names
- Network connectivity issues
- API rate limiting
- Malformed data responses
- Missing data fields

## Technical Details

### Architecture

- **CanadianWeatherAPI**: Main API client class
- **WeatherDisplay**: Data formatting and display logic
- **Command-line interface**: Using argparse for user interaction

### Dependencies

- `requests`: HTTP client for API calls
- `argparse`: Command-line argument parsing
- `datetime`: Date/time formatting
- `typing`: Type hints for better code quality

## Troubleshooting

### Common Issues

1. **"City not found" error**
   - Use `--list-cities` to see available cities
   - Try different spellings or abbreviations
   - Check if the city is supported by the Canadian Weather Service

2. **Network errors**
   - Check your internet connection
   - The API might be temporarily unavailable
   - Try again in a few minutes

3. **Installation issues**
   - Ensure Python 3.6+ is installed
   - Use `pip install -r requirements.txt` to install dependencies
   - Check if you have the required permissions

### Debug Mode

For debugging, you can modify the code to add more verbose output or check the raw API responses.

## License

This project is for educational purposes. The weather data is provided by Environment and Climate Change Canada and is subject to their terms of use.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application.

## Resources

- [MSC GeoMet Documentation](https://eccc-msc.github.io/open-data/msc-geomet/readme_en/)
- [Canadian Weather Service](https://weather.gc.ca/)
- [Environment and Climate Change Canada](https://www.canada.ca/en/environment-climate-change.html)
