#!/usr/bin/env python3
"""
Comprehensive Test Suite for Canadian Weather App
Tests all supported cities to ensure they work correctly
"""

import sys
import os
import time
from typing import List, Dict, Tuple
from weather_app import CanadianWeatherAPI, WeatherDisplay
from csv_api_mapping import CSV_TO_API_MAPPING, get_api_identifier

class WeatherAppTester:
    """Comprehensive test suite for the weather application"""
    
    def __init__(self):
        self.api = CanadianWeatherAPI()
        self.display = WeatherDisplay()
        self.test_results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'errors': []
        }
    
    def test_city_code_lookup(self, city_name: str) -> Tuple[bool, str]:
        """Test if a city code can be found for a given city name"""
        try:
            city_code = self.api.find_city_code(city_name)
            if city_code:
                return True, f"Found code: {city_code}"
            else:
                return False, "City code not found"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def test_weather_data_fetch(self, city_code: str) -> Tuple[bool, str]:
        """Test if weather data can be fetched for a given city code"""
        try:
            weather_data = self.api.get_current_weather(city_code)
            if weather_data:
                city_name = weather_data['properties']['name']['en']
                return True, f"Weather data fetched for {city_name}"
            else:
                return False, "No weather data returned"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def test_forecast_data_fetch(self, city_code: str) -> Tuple[bool, str]:
        """Test if forecast data can be fetched for a given city code"""
        try:
            forecast_data = self.api.get_forecast(city_code, 3)
            if forecast_data and len(forecast_data) > 0:
                return True, f"Forecast data fetched: {len(forecast_data)} days"
            else:
                return False, "No forecast data returned"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def test_major_cities(self) -> Dict[str, Dict]:
        """Test all major Canadian cities"""
        major_cities = [
            # Quebec
            'montreal', 'montréal', 'quebec', 'québec', 'longueuil', 'laval', 'sherbrooke',
            # Ontario  
            'toronto', 'ottawa', 'hamilton', 'london', 'kitchener', 'waterloo', 'windsor',
            # British Columbia
            'vancouver', 'richmond', 'abbotsford',
            # Alberta
            'calgary', 'edmonton', 'red deer', 'lethbridge',
            # Manitoba
            'winnipeg', 'brandon', 'steinbach',
            # Saskatchewan
            'saskatoon', 'regina', 'prince albert', 'moose jaw',
            # Nova Scotia
            'halifax', 'sydney',
            # New Brunswick
            'moncton', 'fredericton',
            # Newfoundland
            'corner brook',
            # Territories
            'yellowknife', 'rankin inlet'
        ]
        
        results = {}
        print("Testing major Canadian cities...")
        print("=" * 60)
        
        for city in major_cities:
            print(f"Testing {city}...", end=" ")
            
            # Test city code lookup
            code_success, code_msg = self.test_city_code_lookup(city)
            
            if code_success:
                city_code = self.api.find_city_code(city)
                
                # Test weather data fetch
                weather_success, weather_msg = self.test_weather_data_fetch(city_code)
                
                # Test forecast data fetch
                forecast_success, forecast_msg = self.test_forecast_data_fetch(city_code)
                
                results[city] = {
                    'code_lookup': code_success,
                    'weather_fetch': weather_success,
                    'forecast_fetch': forecast_success,
                    'city_code': city_code,
                    'messages': {
                        'code': code_msg,
                        'weather': weather_msg,
                        'forecast': forecast_msg
                    }
                }
                
                if weather_success:
                    print("✅ PASS")
                else:
                    print("❌ FAIL")
                    print(f"    Weather fetch failed: {weather_msg}")
            else:
                results[city] = {
                    'code_lookup': False,
                    'weather_fetch': False,
                    'forecast_fetch': False,
                    'city_code': None,
                    'messages': {
                        'code': code_msg,
                        'weather': 'Not tested',
                        'forecast': 'Not tested'
                    }
                }
                print("❌ FAIL")
                print(f"    Code lookup failed: {code_msg}")
            
            # Small delay to avoid overwhelming the API
            time.sleep(0.1)
        
        return results
    
    def test_mapping_table_coverage(self) -> Dict[str, int]:
        """Test the coverage of the mapping table"""
        print("\nTesting mapping table coverage...")
        print("=" * 60)
        
        # Get all CSV codes from mapping table
        mapped_codes = list(CSV_TO_API_MAPPING.keys())
        
        # Test a sample of mapped cities
        sample_size = min(50, len(mapped_codes))  # Test up to 50 cities
        sample_codes = mapped_codes[:sample_size]
        
        working_codes = 0
        failed_codes = 0
        
        print(f"Testing {sample_size} cities from mapping table...")
        
        for csv_code in sample_codes:
            api_id = CSV_TO_API_MAPPING[csv_code]
            success, msg = self.test_weather_data_fetch(api_id)
            
            if success:
                working_codes += 1
                print(f"  {csv_code} -> {api_id}: ✅")
            else:
                failed_codes += 1
                print(f"  {csv_code} -> {api_id}: ❌ ({msg})")
            
            time.sleep(0.1)  # Small delay
        
        coverage_stats = {
            'total_mapped': len(mapped_codes),
            'tested': sample_size,
            'working': working_codes,
            'failed': failed_codes,
            'success_rate': (working_codes / sample_size * 100) if sample_size > 0 else 0
        }
        
        return coverage_stats
    
    def test_accent_support(self) -> Dict[str, bool]:
        """Test accent support for French cities"""
        print("\nTesting accent support...")
        print("=" * 60)
        
        accent_tests = [
            ('montreal', 'montréal'),
            ('quebec', 'québec'),
            ('montreal', 'Montréal'),
            ('quebec', 'Québec'),
        ]
        
        results = {}
        
        for english_name, french_name in accent_tests:
            print(f"Testing {english_name} vs {french_name}...", end=" ")
            
            # Test both versions
            eng_code = self.api.find_city_code(english_name)
            fr_code = self.api.find_city_code(french_name)
            
            if eng_code and fr_code and eng_code == fr_code:
                results[f"{english_name}/{french_name}"] = True
                print("✅ PASS")
            else:
                results[f"{english_name}/{french_name}"] = False
                print("❌ FAIL")
                print(f"    English: {eng_code}, French: {fr_code}")
        
        return results
    
    def run_comprehensive_test(self) -> Dict:
        """Run all tests and return comprehensive results"""
        print("🌤️  COMPREHENSIVE WEATHER APP TEST SUITE")
        print("=" * 60)
        print(f"Testing {len(CSV_TO_API_MAPPING)} mapped cities...")
        print()
        
        # Run all test suites
        major_cities_results = self.test_major_cities()
        mapping_coverage = self.test_mapping_table_coverage()
        accent_results = self.test_accent_support()
        
        # Calculate overall statistics
        total_major_tests = len(major_cities_results)
        passed_major_tests = sum(1 for result in major_cities_results.values() 
                               if result['weather_fetch'])
        
        total_accent_tests = len(accent_results)
        passed_accent_tests = sum(1 for result in accent_results.values() if result)
        
        # Compile final results
        final_results = {
            'major_cities': {
                'total': total_major_tests,
                'passed': passed_major_tests,
                'failed': total_major_tests - passed_major_tests,
                'success_rate': (passed_major_tests / total_major_tests * 100) if total_major_tests > 0 else 0,
                'details': major_cities_results
            },
            'mapping_coverage': mapping_coverage,
            'accent_support': {
                'total': total_accent_tests,
                'passed': passed_accent_tests,
                'failed': total_accent_tests - passed_accent_tests,
                'success_rate': (passed_accent_tests / total_accent_tests * 100) if total_accent_tests > 0 else 0,
                'details': accent_results
            },
            'overall_stats': {
                'total_cities_mapped': len(CSV_TO_API_MAPPING),
                'major_cities_success_rate': (passed_major_tests / total_major_tests * 100) if total_major_tests > 0 else 0,
                'mapping_success_rate': mapping_coverage['success_rate'],
                'accent_success_rate': (passed_accent_tests / total_accent_tests * 100) if total_accent_tests > 0 else 0
            }
        }
        
        return final_results
    
    def print_test_summary(self, results: Dict):
        """Print a comprehensive test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        # Major cities summary
        major = results['major_cities']
        print(f"Major Cities Test: {major['passed']}/{major['total']} passed ({major['success_rate']:.1f}%)")
        
        # Mapping coverage summary
        mapping = results['mapping_coverage']
        print(f"Mapping Coverage: {mapping['working']}/{mapping['tested']} working ({mapping['success_rate']:.1f}%)")
        
        # Accent support summary
        accent = results['accent_support']
        print(f"Accent Support: {accent['passed']}/{accent['total']} passed ({accent['success_rate']:.1f}%)")
        
        # Overall stats
        overall = results['overall_stats']
        print(f"\nOverall Statistics:")
        print(f"  Total Cities Mapped: {overall['total_cities_mapped']}")
        print(f"  Major Cities Success Rate: {overall['major_cities_success_rate']:.1f}%")
        print(f"  Mapping Success Rate: {overall['mapping_success_rate']:.1f}%")
        print(f"  Accent Support Success Rate: {overall['accent_success_rate']:.1f}%")
        
        # Failed tests details
        print(f"\nFailed Major Cities:")
        for city, result in major['details'].items():
            if not result['weather_fetch']:
                print(f"  ❌ {city}: {result['messages']['weather']}")
        
        print(f"\nFailed Accent Tests:")
        for test, passed in accent['details'].items():
            if not passed:
                print(f"  ❌ {test}")

def main():
    """Main test runner"""
    tester = WeatherAppTester()
    
    try:
        results = tester.run_comprehensive_test()
        tester.print_test_summary(results)
        
        # Save results to file
        import json
        with open('test_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nDetailed results saved to test_results.json")
        
        # Return exit code based on success rate
        overall_success = results['overall_stats']['major_cities_success_rate']
        if overall_success >= 90:
            print(f"\n🎉 EXCELLENT! {overall_success:.1f}% success rate")
            sys.exit(0)
        elif overall_success >= 70:
            print(f"\n✅ GOOD! {overall_success:.1f}% success rate")
            sys.exit(0)
        else:
            print(f"\n⚠️  NEEDS IMPROVEMENT! {overall_success:.1f}% success rate")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nTest failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
