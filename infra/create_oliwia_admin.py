#!/usr/bin/env python3
"""
Script to create admin user for oliwia.walter@portgdansk.pl
Run this after deploying the CDK stack
"""

import boto3
import os
import sys

def create_oliwia_admin():
    """Create admin user for oliwia.walter@portgdansk.pl"""
    
    # Configuration
    email = "oliwia.walter@portgdansk.pl"
    password = "Dock2Gdansk!"
    user_pool_id = os.environ.get('USER_POOL_ID')
    region = os.environ.get('AWS_DEFAULT_REGION', 'ap-east-1')
    
    if not user_pool_id:
        print("❌ USER_POOL_ID environment variable not set")
        print("💡 You can get it by running: aws cloudformation describe-stacks --stack-name D2GStack --query 'Stacks[0].Outputs[?OutputKey==`UserPoolId`].OutputValue' --output text")
        return False
    
    print(f"🚀 Creating admin user: {email}")
    print(f"🌍 Region: {region}")
    print(f"👥 User Pool: {user_pool_id}")
    
    try:
        # Initialize Cognito client
        cognito = boto3.client('cognito-idp', region_name=region)
        
        # Create user
        response = cognito.admin_create_user(
            UserPoolId=user_pool_id,
            Username=email,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
                {
                    'Name': 'email_verified',
                    'Value': 'true'
                }
            ],
            TemporaryPassword=password,
            MessageAction='SUPPRESS'  # Don't send welcome email
        )
        
        print(f"✅ User created successfully: {email}")
        
        # Add user to admin group
        try:
            cognito.admin_add_user_to_group(
                UserPoolId=user_pool_id,
                Username=email,
                GroupName='admin'
            )
            print(f"✅ User added to admin group")
        except Exception as e:
            print(f"⚠️  Warning: Could not add to admin group: {str(e)}")
        
        # Set permanent password
        try:
            cognito.admin_set_user_password(
                UserPoolId=user_pool_id,
                Username=email,
                Password=password,
                Permanent=True
            )
            print(f"✅ Password set as permanent")
        except Exception as e:
            print(f"⚠️  Warning: Could not set permanent password: {str(e)}")
            print(f"📝 User will need to change password on first login")
        
        print(f"\n🎉 Admin user created successfully!")
        print(f"📧 Email: {email}")
        print(f"🔑 Password: {password}")
        print(f"🌐 Login at: /kapitanat")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Dock2Gdansk Admin User Creation")
    print("=" * 40)
    print("Creating admin user: oliwia.walter@portgdansk.pl")
    print()
    
    success = create_oliwia_admin()
    
    if success:
        print("\n✅ Admin user creation completed successfully!")
        print("\n📚 Next steps:")
        print("1. The admin user can now log in at /kapitanat")
        print("2. Email: oliwia.walter@portgdansk.pl")
        print("3. Password: Dock2Gdansk")
        print("4. User has full admin privileges")
    else:
        print("\n❌ Failed to create admin user")
        sys.exit(1)