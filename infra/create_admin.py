#!/usr/bin/env python3
"""
Script to create the first admin user for kapitanat dashboard
Run this after deploying the CDK stack
"""

import boto3
import os
import getpass
import sys

def create_admin_user():
    """Create the first admin user"""
    
    # Get user pool ID from environment or ask user
    user_pool_id = os.environ.get('USER_POOL_ID')
    if not user_pool_id:
        user_pool_id = input("Enter Cognito User Pool ID: ").strip()
    
    if not user_pool_id:
        print("❌ User Pool ID is required")
        return False
    
    # Get admin email
    admin_email = input("Enter admin email address: ").strip()
    if not admin_email:
        print("❌ Admin email is required")
        return False
    
    # Get temporary password
    print("Enter temporary password (will be required to change on first login):")
    temp_password = getpass.getpass()
    if not temp_password:
        print("❌ Temporary password is required")
        return False
    
    # Initialize Cognito client
    try:
        cognito = boto3.client('cognito-idp')
        
        print(f"🔧 Creating admin user: {admin_email}")
        
        # Create user
        response = cognito.admin_create_user(
            UserPoolId=user_pool_id,
            Username=admin_email,
            UserAttributes=[
                {'Name': 'email', 'Value': admin_email},
                {'Name': 'email_verified', 'Value': 'true'}
            ],
            TemporaryPassword=temp_password,
            MessageAction='SUPPRESS'  # Don't send email automatically
        )
        
        print(f"✅ User created successfully")
        print(f"   - Username: {admin_email}")
        print(f"   - Status: {response['User']['UserStatus']}")
        
        # Add to admin group
        print(f"🔧 Adding user to admin group...")
        cognito.admin_add_user_to_group(
            UserPoolId=user_pool_id,
            Username=admin_email,
            GroupName='admin'
        )
        
        print(f"✅ User added to admin group successfully")
        
        # Set permanent password if requested
        set_permanent = input("\nDo you want to set a permanent password now? (y/N): ").strip().lower()
        if set_permanent == 'y':
            print("Enter permanent password:")
            permanent_password = getpass.getpass()
            if permanent_password:
                cognito.admin_set_user_password(
                    UserPoolId=user_pool_id,
                    Username=admin_email,
                    Password=permanent_password,
                    Permanent=True
                )
                print("✅ Permanent password set successfully")
        
        print("\n📚 Next steps:")
        print(f"1. The admin user can now log in with:")
        print(f"   - Email: {admin_email}")
        print(f"   - Password: {'permanent password' if set_permanent == 'y' else 'temporary password (must change on first login)'}")
        print(f"2. Access the admin dashboard at: /kapitanat")
        print(f"3. The user will have full admin privileges")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")
        return False

def list_existing_users():
    """List existing users in the user pool"""
    
    user_pool_id = os.environ.get('USER_POOL_ID')
    if not user_pool_id:
        user_pool_id = input("Enter Cognito User Pool ID: ").strip()
    
    if not user_pool_id:
        print("❌ User Pool ID is required")
        return
    
    try:
        cognito = boto3.client('cognito-idp')
        
        print("📋 Existing users:")
        print("-" * 50)
        
        response = cognito.list_users(UserPoolId=user_pool_id)
        
        if not response['Users']:
            print("No users found in the user pool")
            return
        
        for user in response['Users']:
            user_attributes = {attr['Name']: attr['Value'] for attr in user['Attributes']}
            
            # Get user groups
            try:
                groups_response = cognito.admin_list_groups_for_user(
                    UserPoolId=user_pool_id,
                    Username=user['Username']
                )
                groups = [group['GroupName'] for group in groups_response['Groups']]
            except:
                groups = []
            
            print(f"👤 {user['Username']}")
            print(f"   Email: {user_attributes.get('email', 'N/A')}")
            print(f"   Status: {user['UserStatus']}")
            print(f"   Enabled: {user['Enabled']}")
            print(f"   Groups: {', '.join(groups) if groups else 'None'}")
            print(f"   Created: {user['UserCreateDate']}")
            print()
        
    except Exception as e:
        print(f"❌ Error listing users: {str(e)}")

if __name__ == "__main__":
    print("🚀 Dock2Gdansk Admin User Management")
    print("=" * 40)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'list':
        list_existing_users()
    else:
        print("This script will create the first admin user for the kapitanat dashboard.")
        print("The user will have full administrative privileges.\n")
        
        confirm = input("Do you want to continue? (y/N): ").strip().lower()
        if confirm == 'y':
            success = create_admin_user()
            if success:
                print("\n✅ Admin user creation completed successfully!")
            else:
                print("\n❌ Failed to create admin user")
                sys.exit(1)
        else:
            print("❌ Operation cancelled")
            sys.exit(1)
