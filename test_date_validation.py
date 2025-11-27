"""
Unit tests for date validation functions
Run with: python3 test_date_validation.py
"""
import sys
from datetime import date, datetime

# Standalone copies of validation functions for testing
def is_valid_dob(dob_str: str) -> tuple:
    """Validate date of birth (copy from app.py for testing)"""
    if not dob_str:
        return (False, "Date of birth is required.")

    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
    except ValueError:
        return (False, "Invalid date format. Please use YYYY-MM-DD.")

    today = date.today()

    if dob > today:
        return (False, "Date of birth cannot be in the future.")

    eighteen_years_ago = date(today.year - 18, today.month, today.day)
    if dob < eighteen_years_ago:
        return (False, "Date of birth cannot be more than 18 years ago.")

    return (True, None)

def is_valid_academic_date(year: int, month: int) -> tuple:
    """Validate academic date (copy from app.py for testing)"""
    if not year or not month:
        return (False, "Year and month are required.")

    if month < 1 or month > 12:
        return (False, "Month must be between 1 and 12.")

    current_year = date.today().year

    if year < 2000:
        return (False, f"Year cannot be before 2000.")

    if year > current_year:
        return (False, f"Year cannot be in the future.")

    today = date.today()
    record_date = date(year, month, 1)

    if record_date > today:
        return (False, "Academic record date cannot be in the future.")

    return (True, None)

def test_dob_validation():
    """Test Date of Birth validation"""
    print("=" * 60)
    print("Testing Date of Birth Validation")
    print("=" * 60)

    tests = [
        # (dob_string, should_pass, description)
        ("2020-01-15", True, "Valid DOB (5 years old)"),
        ("2099-12-31", False, "Future date (rejected)"),
        ("1900-01-01", False, "Too old (>18 years)"),
        ("2010-06-15", True, "Valid DOB (15 years old)"),
        ("", False, "Empty DOB"),
        ("invalid", False, "Invalid format"),
        ("2025-12-31", False, "Future date"),
    ]

    passed = 0
    failed = 0

    for dob_str, should_pass, description in tests:
        is_valid, error_msg = is_valid_dob(dob_str)

        if is_valid == should_pass:
            print(f"✓ PASS: {description}")
            passed += 1
        else:
            print(f"✗ FAIL: {description}")
            print(f"  Expected: {'Valid' if should_pass else 'Invalid'}")
            print(f"  Got: {'Valid' if is_valid else f'Invalid - {error_msg}'}")
            failed += 1

    print(f"\nDOB Tests: {passed} passed, {failed} failed\n")
    return failed == 0

def test_academic_date_validation():
    """Test Academic Date validation"""
    print("=" * 60)
    print("Testing Academic Date Validation")
    print("=" * 60)

    current_year = date.today().year

    tests = [
        # (year, month, should_pass, description)
        (2024, 6, True, "Valid date (June 2024)"),
        (2000, 1, True, "Valid date (January 2000)"),
        (1999, 6, False, "Year before 2000"),
        (3000, 6, False, "Future year (3000)"),
        (current_year + 1, 1, False, "Next year"),
        (2024, 13, False, "Invalid month (13)"),
        (2024, 0, False, "Invalid month (0)"),
        (None, 6, False, "Missing year"),
        (2024, None, False, "Missing month"),
    ]

    passed = 0
    failed = 0

    for year, month, should_pass, description in tests:
        is_valid, error_msg = is_valid_academic_date(year, month)

        if is_valid == should_pass:
            print(f"✓ PASS: {description}")
            passed += 1
        else:
            print(f"✗ FAIL: {description}")
            print(f"  Expected: {'Valid' if should_pass else 'Invalid'}")
            print(f"  Got: {'Valid' if is_valid else f'Invalid - {error_msg}'}")
            failed += 1

    print(f"\nAcademic Date Tests: {passed} passed, {failed} failed\n")
    return failed == 0

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("DATE VALIDATION TEST SUITE")
    print("=" * 60 + "\n")

    dob_pass = test_dob_validation()
    academic_pass = test_academic_date_validation()

    print("=" * 60)
    if dob_pass and academic_pass:
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
