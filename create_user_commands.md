# Commands to Create User Account in ArcherySec

## Run these commands in Django shell:

```python
# Step 1: Import required models
from user_management.models import UserProfile, Organization, UserRoles

# Step 2: Create an Organization (if not exists)
org, created = Organization.objects.get_or_create(
    name='Default Organization',
    defaults={
        'description': 'Default organization for ArcherySec',
        'logo': '',
        'contact': 'admin@example.com',
        'address': 'Default Address'
    }
)
print(f"Organization: {org.name} (ID: {org.id})")

# Step 3: Create User Roles (if not exist)
admin_role, created = UserRoles.objects.get_or_create(
    role='Admin',
    defaults={'description': 'Administrator role with full access'}
)
print(f"Role: {admin_role.role} (ID: {admin_role.id})")

# Step 4: Create the user
user = UserProfile.objects.create_user(
    email='admin@example.com',
    name='Admin User',
    role=admin_role.id,
    organization=org.id,
    password='admin@123A'
)
print(f"User created successfully: {user.email}")
print(f"Login with: admin@example.com / admin@123A")
```

## Quick Copy-Paste Version:

```python
from user_management.models import UserProfile, Organization, UserRoles
org, created = Organization.objects.get_or_create(name='Default Organization', defaults={'description': 'Default organization', 'logo': '', 'contact': 'admin@example.com', 'address': 'Default'})
admin_role, created = UserRoles.objects.get_or_create(role='Admin', defaults={'description': 'Administrator'})
user = UserProfile.objects.create_user(email='admin@example.com', name='Admin User', role=admin_role.id, organization=org.id, password='admin@123A')
print(f"User created: {user.email} / admin@123A")
exit()
```

## Login Credentials:
- **Email**: admin@example.com
- **Password**: admin@123A
