#!/usr/bin/env python3
"""
Standalone test script for form validation logic
Tests the validation function without AWS dependencies
"""

import re
from typing import Dict, Any, Tuple

def validate_form_data(form_data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, str]]:
    """
    Validate form data to prevent empty/invalid submissions.

    Returns:
        Tuple of (is_valid, error_message, field_errors)
    """
    field_errors = {}

    # Define required fields based on your form schema
    required_text_fields = {
        'company': 'Company name',
        'email': 'Email',
        'phone': 'Phone number',
        'contact_person': 'Contact person',
        'inquiry_content': 'Inquiry content'
    }

    required_select_fields = {
        'cargo_type': 'Cargo type',
        'referral_source': 'How did you hear about us'
    }

    required_consent_fields = {
        'privacy_consent': 'Privacy policy consent',
        'terms_consent': 'Terms of service consent',
        'cross_border_consent': 'Cross-border data transfer consent'
    }

    # 1. Check if form_data exists and is not empty
    if not form_data or not isinstance(form_data, dict):
        return False, "Form data is missing or invalid", {}

    # 2. Validate required text fields (must not be empty strings)
    for field, label in required_text_fields.items():
        value = form_data.get(field)
        if not value or not isinstance(value, str) or not value.strip():
            field_errors[field] = f"{label} is required"

    # 3. Validate required select fields (must have a value)
    for field, label in required_select_fields.items():
        value = form_data.get(field)
        if not value or not isinstance(value, str) or not value.strip():
            field_errors[field] = f"{label} is required"

    # 4. Validate required consent checkboxes (must be true)
    for field, label in required_consent_fields.items():
        value = form_data.get(field)
        if value is not True:  # Must be explicitly True, not just truthy
            field_errors[field] = f"{label} must be accepted"

    # 5. Validate email format
    if 'email' in form_data and form_data['email']:
        email = form_data['email'].strip()
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            field_errors['email'] = "Invalid email format"

    # 6. Validate phone number (basic check - not empty and contains digits)
    if 'phone' in form_data and form_data['phone']:
        phone = str(form_data['phone']).strip()
        if not re.search(r'\d', phone):  # Must contain at least one digit
            field_errors['phone'] = "Invalid phone number format"

    # 7. Validate phone prefix exists
    phone_prefix = form_data.get('phone_prefix')
    if not phone_prefix or not isinstance(phone_prefix, str) or not phone_prefix.strip():
        field_errors['phone_prefix'] = "Phone prefix is required"

    # 8. If phone prefix is custom, validate custom_phone_prefix
    if phone_prefix == 'custom':
        custom_prefix = form_data.get('custom_phone_prefix')
        if not custom_prefix or not isinstance(custom_prefix, str) or not custom_prefix.strip():
            field_errors['custom_phone_prefix'] = "Custom phone prefix is required when 'custom' is selected"
        elif not re.match(r'^\+\d{1,4}$', custom_prefix.strip()):
            field_errors['custom_phone_prefix'] = "Custom phone prefix must be in format +XX (e.g., +33)"

    # Return validation result
    if field_errors:
        error_summary = f"Validation failed: {len(field_errors)} field(s) with errors"
        print(f"❌ Form validation failed: {field_errors}")
        return False, error_summary, field_errors

    print("✅ Form validation passed")
    return True, "", {}

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
    print(f"      Missing fields: {', '.join(field_errors.keys())}")

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
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\n✨ Validation logic is working correctly")
        print("✨ Ready to deploy to AWS Lambda!")

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        import sys
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        import sys
        sys.exit(1)
