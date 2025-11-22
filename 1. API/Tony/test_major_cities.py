#!/usr/bin/env python3
"""
Major Canadian Cities Test Script
Tests all major Canadian cities to see which ones are available in the Canadian Weather API
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from weather_app import CanadianWeatherAPI, WeatherDisplay


def test_major_canadian_cities():
    """Test all major Canadian cities"""
    
    # List of major Canadian cities by population and importance
    major_cities = [
        # Ontario
        'toronto', 'ottawa', 'hamilton', 'london', 'kitchener', 'waterloo', 
        'mississauga', 'brampton', 'markham', 'vaughan', 'windsor', 'oshawa',
        
        # Quebec
        'montreal', 'montréal', 'quebec', 'québec', 'quebec city', 'québec city',
        'laval', 'gatineau', 'longueuil', 'sherbrooke', 'trois-rivieres', 'trois rivieres',
        
        # British Columbia
        'vancouver', 'surrey', 'burnaby', 'richmond', 'abbotsford', 'coquitlam',
        
        # Alberta
        'calgary', 'edmonton', 'red deer', 'lethbridge', 'st albert',
        
        # Manitoba
        'winnipeg', 'brandon', 'steinbach',
        
        # Saskatchewan
        'saskatoon', 'regina', 'prince albert', 'moose jaw',
        
        # Nova Scotia
        'halifax', 'sydney', 'dartmouth',
        
        # New Brunswick
        'moncton', 'saint john', 'fredericton',
        
        # Newfoundland and Labrador
        'st johns', 'mount pearl', 'corner brook',
        
        # Prince Edward Island
        'charlottetown', 'summerside',
        
        # Northwest Territories
        'yellowknife', 'hay river',
        
        # Yukon
        'whitehorse', 'dawson city',
        
        # Nunavut
        'iqaluit', 'rankin inlet'
    ]
    
    print("🇨🇦 TESTING MAJOR CANADIAN CITIES")
    print("=" * 60)
    
    api = CanadianWeatherAPI()
    display = WeatherDisplay()
    
    available_cities = []
    unavailable_cities = []
    
    print(f"Testing {len(major_cities)} major Canadian cities...")
    print()
    
    for city in major_cities:
        city_code = api.find_city_code(city)
        if city_code:
            # Test if we can actually get weather data
            try:
                weather_data = api.get_current_weather(city_code)
                if weather_data:
                    city_name = weather_data['properties']['name']['en']
                    available_cities.append((city, city_code, city_name))
                    print(f"✅ {city.title():<20} -> {city_code:<10} ({city_name})")
                else:
                    unavailable_cities.append((city, city_code, "No weather data"))
                    print(f"❌ {city.title():<20} -> {city_code:<10} (No weather data)")
            except Exception as e:
                unavailable_cities.append((city, city_code, f"Error: {str(e)[:30]}"))
                print(f"❌ {city.title():<20} -> {city_code:<10} (Error)")
        else:
            unavailable_cities.append((city, None, "Not found"))
            print(f"❌ {city.title():<20} -> {'N/A':<10} (Not found)")
    
    print()
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"✅ Available cities: {len(available_cities)}")
    print(f"❌ Unavailable cities: {len(unavailable_cities)}")
    print(f"📈 Success rate: {len(available_cities)/len(major_cities)*100:.1f}%")
    
    print()
    print("✅ AVAILABLE CITIES:")
    print("-" * 40)
    for city, code, name in available_cities:
        print(f"  {city.title():<20} ({code}) - {name}")
    
    print()
    print("❌ UNAVAILABLE CITIES:")
    print("-" * 40)
    for city, code, reason in unavailable_cities:
        if code:
            print(f"  {city.title():<20} ({code}) - {reason}")
        else:
            print(f"  {city.title():<20} - {reason}")
    
    return available_cities, unavailable_cities


def test_sample_cities():
    """Test a few sample cities to show the weather data"""
    print()
    print("🌤️  SAMPLE WEATHER DATA")
    print("=" * 60)
    
    api = CanadianWeatherAPI()
    display = WeatherDisplay()
    
    sample_cities = ['toronto', 'vancouver', 'montreal', 'calgary', 'ottawa']
    
    for city in sample_cities:
        city_code = api.find_city_code(city)
        if city_code:
            print(f"\n📍 Testing {city.title()}...")
            try:
                weather_data = api.get_current_weather(city_code)
                if weather_data:
                    print(display.format_current_weather(weather_data))
                else:
                    print(f"❌ No weather data for {city}")
            except Exception as e:
                print(f"❌ Error getting weather for {city}: {e}")
        else:
            print(f"❌ City code not found for {city}")


if __name__ == "__main__":
    available, unavailable = test_major_canadian_cities()
    test_sample_cities()
    
    print()
    print("🎯 RECOMMENDATIONS")
    print("=" * 60)
    if unavailable:
        print("Cities that need further investigation:")
        for city, code, reason in unavailable:
            if not code:  # Only cities not found at all
                print(f"  - {city.title()}: {reason}")
    else:
        print("All major cities are working! 🎉")
