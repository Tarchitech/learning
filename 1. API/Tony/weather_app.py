#!/usr/bin/env python3
"""
Canadian Weather API Client
A command-line application to fetch weather information and forecasts for Canadian cities
using the MSC GeoMet-OGC-API from Environment and Climate Change Canada.
"""

import requests
import json
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import os
import unicodedata
import re
from csv_api_mapping import CSV_TO_API_MAPPING, get_api_identifier


class CanadianWeatherAPI:
    """Client for the Canadian Weather API (MSC GeoMet-OGC-API)"""
    
    BASE_URL = "https://api.weather.gc.ca"
    CITY_LIST_URL = "https://dd.weather.gc.ca/citypage_weather/docs/site_list_en.csv"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'Canadian Weather App/1.0'
        })
        self.city_codes = {}
        self._load_city_codes()
    
    def _load_city_codes(self) -> None:
        """Load city codes from CSV and map to correct API identifiers"""
        try:
            response = self.session.get(self.CITY_LIST_URL)
            response.raise_for_status()
            
            # Handle encoding issues
            text = response.text
            if 'MontrÃ©al' in text:
                text = text.replace('MontrÃ©al', 'Montréal')
            if 'QuÃ©bec' in text:
                text = text.replace('QuÃ©bec', 'Québec')
            
            lines = text.strip().split('\n')
            # Skip header and BOM (first 2 lines)
            for line in lines[2:]:
                if line.strip():
                    # Parse CSV line
                    parts = []
                    current_part = ""
                    in_quotes = False
                    
                    for char in line:
                        if char == '"':
                            in_quotes = not in_quotes
                        elif char == ',' and not in_quotes:
                            parts.append(current_part.strip())
                            current_part = ""
                            continue
                        current_part += char
                    
                    # Add the last part
                    parts.append(current_part.strip())
                    
                    if len(parts) >= 2:
                        csv_code = parts[0].strip().strip('"')
                        city_name = parts[1].strip().strip('"')
                        province = parts[2].strip().strip('"') if len(parts) > 2 else ''
                        
                        # Use comprehensive mapping table
                        api_identifier = get_api_identifier(csv_code)
                        
                        if api_identifier:
                            # Normalize city name and store
                            normalized_name = self._normalize_text(city_name)
                            self.city_codes[normalized_name] = api_identifier
                            
                            # Also store original name if different
                            if normalized_name != city_name.lower():
                                self.city_codes[city_name.lower()] = api_identifier
                        
        except requests.RequestException as e:
            print(f"Warning: Could not load city codes from CSV: {e}")
            # Fallback to some common cities with correct API identifiers
            self.city_codes = {
                'toronto': 'on-143',
                'vancouver': 'bc-74',
                'montreal': 'qc-147',
                'calgary': 'ab-52',
                'ottawa': 'on-79',
                'edmonton': 'ab-50',
                'winnipeg': 'mb-38',
                'halifax': 'ns-40',
                'quebec': 'qc-133',
                'hamilton': 'on-77',
                'gatineau': 'qc-126'
            }
    
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text by removing accents and converting to lowercase"""
        # Remove accents and convert to lowercase
        normalized = unicodedata.normalize('NFD', text.lower())
        normalized = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
        return normalized.strip()
    
    def find_city_code(self, city_name: str) -> Optional[str]:
        """Find city code for a given city name with accent support"""
        city_normalized = self._normalize_text(city_name)
        
        # Direct match (normalized)
        if city_normalized in self.city_codes:
            return self.city_codes[city_normalized]
        
        # Partial match (normalized)
        for city, code in self.city_codes.items():
            if city_normalized in city or city in city_normalized:
                return code
        
        return None
    
    def get_current_weather(self, city_code: str) -> Optional[Dict]:
        """Get current weather for a city using API identifier parameter"""
        url = f"{self.BASE_URL}/collections/citypageweather-realtime/items"
        params = {'identifier': city_code}
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Return the first feature if available
            if data.get('features') and len(data['features']) > 0:
                return data['features'][0]
            return None
            
        except requests.RequestException as e:
            print(f"Error fetching current weather: {e}")
            return None
    
    
    def get_forecast(self, city_code: str, days: int = 5) -> Optional[List[Dict]]:
        """Get weather forecast for a city"""
        weather_data = self.get_current_weather(city_code)
        if not weather_data:
            return None
        
        try:
            forecast_group = weather_data.get('properties', {}).get('forecastGroup', {})
            forecasts = forecast_group.get('forecasts', [])
            return forecasts[:days] if forecasts else []
        except (KeyError, TypeError) as e:
            print(f"Error parsing forecast data: {e}")
            return None
    
    
    def list_available_cities(self, limit: int = 20) -> List[str]:
        """List available cities (for debugging)"""
        return list(self.city_codes.keys())[:limit]


class WeatherDisplay:
    """Handle weather data display formatting"""
    
    @staticmethod
    def format_current_weather(data: Dict) -> str:
        """Format current weather data for display"""
        try:
            props = data.get('properties', {})
            name = props.get('name', {})
            region = props.get('region', {})
            current = props.get('currentConditions', {})
            
            city_name = name.get('en', 'Unknown City')
            province = region.get('en', 'Unknown Province')
            
            temperature = current.get('temperature', {}).get('value', {}).get('en', 'N/A')
            condition = current.get('condition', {})
            if isinstance(condition, dict):
                condition = condition.get('en', 'N/A')
            humidity = current.get('relativeHumidity', {}).get('value', {}).get('en', 'N/A')
            pressure = current.get('pressure', {}).get('value', {}).get('en', 'N/A')
            wind_speed = current.get('wind', {}).get('speed', {}).get('value', {}).get('en', 'N/A')
            wind_direction = current.get('wind', {}).get('direction', {}).get('value', {}).get('en', 'N/A')
            
            output = f"""
🌤️  CURRENT WEATHER FOR {city_name.upper()}, {province.upper()}
{'='*60}
🌡️  Temperature: {temperature}°C
☁️  Condition: {condition}
💧 Humidity: {humidity}%
📊 Pressure: {pressure} kPa
💨 Wind: {wind_speed} km/h {wind_direction}
{'='*60}
"""
            return output
            
        except Exception as e:
            return f"Error formatting current weather: {e}"
    
    @staticmethod
    def format_forecast(forecasts: List[Dict]) -> str:
        """Format forecast data for display"""
        if not forecasts:
            return "No forecast data available."
        
        output = "\n📅 FORECAST\n" + "="*60 + "\n"
        
        for i, forecast in enumerate(forecasts, 1):
            try:
                period = forecast.get('period', {})
                period_name = period.get('textForecastName', {}).get('en', f'Day {i}')
                
                # Get temperature
                temperatures = forecast.get('temperatures', {})
                temp_summary = temperatures.get('textSummary', {}).get('en', 'N/A')
                
                # Get condition
                abbreviated = forecast.get('abbreviatedForecast', {})
                condition = abbreviated.get('textSummary', {}).get('en', 'N/A')
                
                # Get precipitation info
                precipitation = forecast.get('precipitation', {})
                precip_info = "N/A"
                if precipitation.get('precipPeriods'):
                    precip_periods = precipitation['precipPeriods']
                    if precip_periods:
                        precip_info = precip_periods[0].get('value', {}).get('en', 'N/A')
                
                output += f"""
Day {i}: {period_name}
├─ Condition: {condition}
├─ Temperature: {temp_summary}
└─ Precipitation: {precip_info}
{'-'*40}
"""
            except Exception as e:
                output += f"Day {i}: Error parsing forecast data - {e}\n"
        
        return output


def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description='Canadian Weather App - Get weather info and forecasts for Canadian cities',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python weather_app.py toronto
  python weather_app.py vancouver --days 3
  python weather_app.py montreal --days 5
  python weather_app.py --list-cities
        """
    )
    
    parser.add_argument('city', nargs='?', help='City name (e.g., toronto, vancouver)')
    parser.add_argument('--days', '-d', type=int, default=5, choices=[3, 4, 5],
                       help='Number of forecast days (3, 4, or 5)')
    parser.add_argument('--list-cities', '-l', action='store_true',
                       help='List available cities')
    parser.add_argument('--current-only', '-c', action='store_true',
                       help='Show only current weather (no forecast)')
    
    args = parser.parse_args()
    
    # Initialize API client
    api = CanadianWeatherAPI()
    display = WeatherDisplay()
    
    # List cities if requested
    if args.list_cities:
        print("Available cities (sample):")
        cities = api.list_available_cities(30)
        for city in cities:
            print(f"  - {city.title()}")
        return
    
    # Validate city input
    if not args.city:
        print("Error: Please provide a city name.")
        print("Use --help for usage information.")
        print("Use --list-cities to see available cities.")
        sys.exit(1)
    
    # Find city code
    city_code = api.find_city_code(args.city)
    if not city_code:
        print(f"Error: City '{args.city}' not found.")
        print("Use --list-cities to see available cities.")
        sys.exit(1)
    
    print(f"Fetching weather data for {args.city.title()}...")
    
    # Get current weather
    current_weather = api.get_current_weather(city_code)
    if current_weather:
        print(display.format_current_weather(current_weather))
    else:
        print("Error: Could not fetch current weather data.")
        sys.exit(1)
    
    # Get forecast if requested
    if not args.current_only:
        forecasts = api.get_forecast(city_code, args.days)
        if forecasts:
            print(display.format_forecast(forecasts))
        else:
            print("Error: Could not fetch forecast data.")


if __name__ == "__main__":
    main()
