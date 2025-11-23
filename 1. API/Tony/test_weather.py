#!/usr/bin/env python3
"""
Test script for the Canadian Weather API Client
This script tests the basic functionality of the weather application.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from weather_app import CanadianWeatherAPI, WeatherDisplay


def test_city_codes():
    """Test city code loading and lookup"""
    print("🧪 Testing city code functionality...")
    
    api = CanadianWeatherAPI()
    
    # Test known cities
    test_cities = ['toronto', 'vancouver', 'montreal', 'calgary', 'ottawa']
    
    for city in test_cities:
        city_code = api.find_city_code(city)
        if city_code:
            print(f"✅ {city.title()}: {city_code}")
        else:
            print(f"❌ {city.title()}: Not found")
    
    print(f"\n📊 Total cities loaded: {len(api.city_codes)}")
    return True


def test_api_connection():
    """Test API connection with a known city"""
    print("\n🌐 Testing API connection...")
    
    api = CanadianWeatherAPI()
    display = WeatherDisplay()
    
    # Test with Toronto (should always work)
    city_code = api.find_city_code('toronto')
    if not city_code:
        print("❌ Could not find Toronto city code")
        return False
    
    print(f"📍 Testing with Toronto (code: {city_code})")
    
    # Test current weather
    current_weather = api.get_current_weather(city_code)
    if current_weather:
        print("✅ Current weather API call successful")
        print(display.format_current_weather(current_weather))
    else:
        print("❌ Current weather API call failed")
        return False
    
    # Test forecast
    forecasts = api.get_forecast(city_code, 3)
    if forecasts:
        print("✅ Forecast API call successful")
        print(display.format_forecast(forecasts))
    else:
        print("❌ Forecast API call failed")
        return False
    
    return True


def test_error_handling():
    """Test error handling"""
    print("\n🛡️  Testing error handling...")
    
    api = CanadianWeatherAPI()
    
    # Test invalid city
    invalid_city = api.find_city_code('nonexistentcity123')
    if invalid_city is None:
        print("✅ Invalid city handling works correctly")
    else:
        print("❌ Invalid city handling failed")
        return False
    
    # Test invalid city code
    invalid_weather = api.get_current_weather('invalid-code-123')
    if invalid_weather is None:
        print("✅ Invalid city code handling works correctly")
    else:
        print("❌ Invalid city code handling failed")
        return False
    
    return True


def main():
    """Run all tests"""
    print("🚀 CANADIAN WEATHER API CLIENT - TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("City Code Loading", test_city_codes),
        ("API Connection", test_api_connection),
        ("Error Handling", test_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        try:
            if test_func():
                print(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print(f"\n📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The weather app is ready to use.")
        print("\n💡 Try running: python weather_app.py toronto")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
