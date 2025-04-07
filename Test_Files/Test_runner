# conftest.py
# Place this in your tests directory to configure pytest

import pytest
import os
import sys

# Add parent directory to path so pytest can find the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# test_runner.py
# This file provides a convenient way to run the tests
def run_tests():
    """Run the test suite with verbose output and colorized terminal."""
    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct path to the test file
    test_file = os.path.join(current_dir, 'test_stock_analysis.py')
    
    # Check if the test file exists
    if not os.path.isfile(test_file):
        print(f"Error: Test file not found at {test_file}")
        return False
    
    print(f"Running tests from {test_file}...")
    
    # Run pytest with the specified test file
    # -v for verbose output
    # --color=yes for colorized output
    exit_code = pytest.main(['-v', '--color=yes', test_file])
    
    # Return True if all tests passed, False otherwise
    return exit_code == 0

if __name__ == "__main__":
    # When running this file directly, execute the tests
    success = run_tests()
    
    if success:
        print("\nTest execution completed successfully!")
    else:
        print("\nTest execution completed with failures or errors.")
        
    # Exit with appropriate code (0 for success, 1 for failure)
    sys.exit(0 if success else 1)