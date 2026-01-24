#!/usr/bin/env python3
"""
Example usage of the Canadian Weather API Client
This script demonstrates how to use the weather_app.py module programmatically.
"""

from weather_app import CanadianWeatherAPI, WeatherDisplay


def example_usage():
    """Demonstrate the weather API usage"""
    
    # Initialize the API client
    api = CanadianWeatherAPI()
    display = WeatherDisplay()
    
    # Example cities to check
    cities = ['toronto', 'vancouver', 'montreal']
    
    print("🌤️  CANADIAN WEATHER API EXAMPLES")
    print("=" * 60)
    
    for city in cities:
        print(f"\n📍 Checking weather for {city.title()}...")
        
        # Find city code
        city_code = api.find_city_code(city)
        if not city_code:
            print(f"❌ City '{city}' not found")
            continue
        
        print(f"✅ Found city code: {city_code}")
        
        # Get current weather
        current_weather = api.get_current_weather(city_code)
        if current_weather:
            print(display.format_current_weather(current_weather))
        
        # Get 3-day forecast
        forecasts = api.get_forecast(city_code, 3)
        if forecasts:
            print(display.format_forecast(forecasts))
        
        print("\n" + "=" * 60)


def interactive_example():
    """Interactive example"""
    api = CanadianWeatherAPI()
    display = WeatherDisplay()
    
    print("\n🎯 INTERACTIVE EXAMPLE")
    print("=" * 30)
    
    while True:
        city = input("\nEnter a city name (or 'quit' to exit): ").strip()
        
        if city.lower() in ['quit', 'exit', 'q']:
            break
        
        if not city:
            continue
        
        city_code = api.find_city_code(city)
        if not city_code:
            print(f"❌ City '{city}' not found. Try another city.")
            continue
        
        # Get current weather
        current_weather = api.get_current_weather(city_code)
        if current_weather:
            print(display.format_current_weather(current_weather))
        
        # Ask for forecast
        forecast_choice = input("Show forecast? (y/n): ").strip().lower()
        if forecast_choice in ['y', 'yes']:
            days = input("How many days? (3-5): ").strip()
            try:
                days = int(days) if days.isdigit() else 3
                days = max(3, min(5, days))  # Clamp between 3-5
            except ValueError:
                days = 3
            
            forecasts = api.get_forecast(city_code, days)
            if forecasts:
                print(display.format_forecast(forecasts))


if __name__ == "__main__":
    # Run the example
    example_usage()
    
    # Ask if user wants interactive mode
    choice = input("\nWould you like to try interactive mode? (y/n): ").strip().lower()
    if choice in ['y', 'yes']:
        interactive_example()
    
    print("\n👋 Thanks for using the Canadian Weather API!")
