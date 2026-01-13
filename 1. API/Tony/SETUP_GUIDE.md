# Setup Guide for Enhanced Weather App

## 🔑 OpenWeatherMap API Key Setup (Optional)

To access weather data for major Canadian cities like Vancouver, Montreal, and Quebec City that are not available in the Canadian Weather API, you can set up a free OpenWeatherMap API key.

### Steps:

1. **Sign up for a free account** at [OpenWeatherMap](https://openweathermap.org/api)
2. **Get your API key** from the API keys section
3. **Set the environment variable**:

   **On macOS/Linux:**
   ```bash
   export OPENWEATHER_API_KEY="your_api_key_here"
   ```

   **On Windows:**
   ```cmd
   set OPENWEATHER_API_KEY=your_api_key_here
   ```

   **Or add to your shell profile** (e.g., `~/.bashrc`, `~/.zshrc`):
   ```bash
   echo 'export OPENWEATHER_API_KEY="your_api_key_here"' >> ~/.bashrc
   source ~/.bashrc
   ```

### Benefits:

- ✅ Access to Vancouver, Montreal, Quebec City, Hamilton, and 20+ other major cities
- ✅ More comprehensive city coverage
- ✅ Backup weather data source
- ✅ Free tier includes 1,000 calls/day

### Without API Key:

The app will still work with the Canadian Weather API for cities like Toronto, Ottawa, Calgary, Edmonton, Winnipeg, and Halifax.

## 🚀 Usage Examples

```bash
# Works with Canadian API (no key needed)
python weather_app.py toronto
python weather_app.py ottawa

# Works with fallback API (requires API key)
python weather_app.py vancouver
python weather_app.py montreal
python weather_app.py "quebec city"
```
