#!/usr/bin/env python3
"""
Test script for form validation logic
Run this to verify validation works before deploying
"""

import sys
import os

# Add current directory to path to import submit_form
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from submit_form import validate_form_data

def test_empty_submission():
    """Test that empty submissions are rejected"""
    print("\n🧪 Test 1: Empty submission")
    form_data = {}
    is_valid, error_msg, field_errors = validate_form_data(form_data)
    assert not is_valid, "Empty submission should be rejected"
    print(f"   ✅ Correctly rejected: {error_msg}")

def test_missing_required_fields():
    """Test that submissions with missing fields are rejected"""
    print("\n🧪 Test 2: Missing required fields")
    form_data = {
        'company': 'Test Company',
        'email': 'test@example.com'
        # Missing: phone, contact_person, inquiry_content, cargo_type, referral_source, consents
    }
    is_valid, error_msg, field_errors = validate_form_data(form_data)
    assert not is_valid, "Submission with missing fields should be rejected"
    assert len(field_errors) > 0, "Should have field errors"
    print(f"   ✅ Correctly rejected with {len(field_errors)} field errors")

def test_invalid_email():
    """Test that invalid email is rejected"""
    print("\n🧪 Test 3: Invalid email format")
    form_data = {
        'company': 'Test Company',
        'email': 'invalid-email',  # Invalid format
        'phone': '123456789',
        'phone_prefix': '+86',
        'contact_person': 'John Doe',
        'inquiry_content': 'Test inquiry',
        'cargo_type': 'container',
        'referral_source': 'google',
        'privacy_consent': True,
        'terms_consent': True,
        'cross_border_consent': True
    }
    is_valid, error_msg, field_errors = validate_form_data(form_data)
    assert not is_valid, "Invalid email should be rejected"
    assert 'email' in field_errors, "Should have email field error"
    print(f"   ✅ Correctly rejected invalid email")

def test_missing_consents():
    """Test that missing consent checkboxes are rejected"""
    print("\n🧪 Test 4: Missing consent checkboxes")
    form_data = {
        'company': 'Test Company',
        'email': 'test@example.com',
        'phone': '123456789',
        'phone_prefix': '+86',
        'contact_person': 'John Doe',
        'inquiry_content': 'Test inquiry',
        'cargo_type': 'container',
        'referral_source': 'google',
        'privacy_consent': False,  # Not accepted
        'terms_consent': False,
        'cross_border_consent': False
    }
    is_valid, error_msg, field_errors = validate_form_data(form_data)
    assert not is_valid, "Missing consents should be rejected"
    assert 'privacy_consent' in field_errors, "Should have consent errors"
    print(f"   ✅ Correctly rejected missing consents")

def test_valid_submission():
    """Test that a valid submission is accepted"""
    print("\n🧪 Test 5: Valid submission")
    form_data = {
        'company': 'Test Company Ltd.',
        'email': 'john.doe@testcompany.com',
        'phone': '123456789',
        'phone_prefix': '+86',
        'contact_person': 'John Doe',
        'inquiry_content': 'I would like to inquire about shipping options from Shanghai to Gdansk.',
        'cargo_type': 'container',
        'referral_source': 'google',
        'privacy_consent': True,
        'terms_consent': True,
        'cross_border_consent': True
    }
    is_valid, error_msg, field_errors = validate_form_data(form_data)
    assert is_valid, f"Valid submission should be accepted, but got error: {error_msg}"
    assert len(field_errors) == 0, f"Valid submission should have no errors, but got: {field_errors}"
    print(f"   ✅ Correctly accepted valid submission")

def test_custom_phone_prefix():
    """Test custom phone prefix validation"""
    print("\n🧪 Test 6: Custom phone prefix validation")

    # Test missing custom prefix
    form_data = {
        'company': 'Test Company',
        'email': 'test@example.com',
        'phone': '123456789',
        'phone_prefix': 'custom',  # Custom selected but no custom_phone_prefix
        'contact_person': 'John Doe',
        'inquiry_content': 'Test',
        'cargo_type': 'container',
        'referral_source': 'google',
        'privacy_consent': True,
        'terms_consent': True,
        'cross_border_consent': True
    }
    is_valid, error_msg, field_errors = validate_form_data(form_data)
    assert not is_valid, "Missing custom phone prefix should be rejected"
    assert 'custom_phone_prefix' in field_errors, "Should have custom_phone_prefix error"
    print(f"   ✅ Correctly rejected missing custom prefix")

    # Test valid custom prefix
    form_data['custom_phone_prefix'] = '+33'
    is_valid, error_msg, field_errors = validate_form_data(form_data)
    assert is_valid, f"Valid custom prefix should be accepted, but got: {error_msg}"
    print(f"   ✅ Correctly accepted valid custom prefix")

if __name__ == '__main__':
    print("=" * 60)
    print("🧪 Running Form Validation Tests")
    print("=" * 60)

    try:
        test_empty_submission()
        test_missing_required_fields()
        test_invalid_email()
        test_missing_consents()
        test_valid_submission()
        test_custom_phone_prefix()

        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        print("\n✨ Validation logic is working correctly")
        print("✨ Ready to deploy!")

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
