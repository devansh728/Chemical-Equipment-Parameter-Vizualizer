"""
Backend Health Check Script
Tests all backend components and dependencies
"""

import sys
import os
import redis
from django.conf import settings
from urllib.parse import urlparse

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_status(message, status):
    """Print status with color"""
    if status == "OK":
        print(f"{Colors.GREEN}✓{Colors.END} {message}")
        return True
    elif status == "FAIL":
        print(f"{Colors.RED}✗{Colors.END} {message}")
        return False
    elif status == "WARN":
        print(f"{Colors.YELLOW}⚠{Colors.END} {message}")
        return True
    else:
        print(f"{Colors.BLUE}ℹ{Colors.END} {message}")
        return True

def check_imports():
    """Check if all required packages are installed"""
    print(f"\n{Colors.BLUE}=== Checking Python Packages ==={Colors.END}\n")
    
    packages = {
        'django': 'Django',
        'rest_framework': 'Django REST Framework',
        'rest_framework_simplejwt': 'Django REST Framework SimpleJWT',
        'corsheaders': 'Django CORS Headers',
        'celery': 'Celery',
        'redis': 'Redis',
        'channels': 'Django Channels',
        'channels_redis': 'Channels Redis',
        'daphne': 'Daphne',
        'pandas': 'Pandas',
        'reportlab': 'ReportLab',
    }
    
    all_ok = True
    for package, name in packages.items():
        try:
            __import__(package)
            print_status(f"{name}", "OK")
        except ImportError:
            print_status(f"{name} - NOT INSTALLED", "FAIL")
            all_ok = False
    
    return all_ok

def check_django_setup():
    """Check Django configuration"""
    print(f"\n{Colors.BLUE}=== Checking Django Configuration ==={Colors.END}\n")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
        import django
        django.setup()
        print_status("Django settings loaded", "OK")
        
        from django.conf import settings
        
        # Check installed apps
        required_apps = ['api', 'rest_framework', 'channels', 'corsheaders', 'daphne']
        for app in required_apps:
            if app in settings.INSTALLED_APPS:
                print_status(f"App '{app}' installed", "OK")
            else:
                print_status(f"App '{app}' NOT in INSTALLED_APPS", "WARN")
        
        return True
    except Exception as e:
        print_status(f"Django setup failed: {str(e)}", "FAIL")
        return False

def check_database():
    """Check database connection"""
    print(f"\n{Colors.BLUE}=== Checking Database ==={Colors.END}\n")
    
    try:
        from django.db import connection
        cursor = connection.cursor()
        print_status("Database connection", "OK")
        
        # Check if migrations are applied
        from django.contrib.auth.models import User
        user_count = User.objects.count()
        print_status(f"User model accessible ({user_count} users)", "OK")
        
        # Check Dataset model
        from api.models import Dataset
        dataset_count = Dataset.objects.count()
        print_status(f"Dataset model accessible ({dataset_count} datasets)", "OK")
        
        return True
    except Exception as e:
        print_status(f"Database check failed: {str(e)}", "FAIL")
        return False

def check_redis():
    """Check Redis connection"""
    print(f"\n{Colors.BLUE}=== Checking Redis Connection ==={Colors.END}\n")
    
    try:
        
        # Get Redis configuration from Django settings
        redis_url = getattr(settings, 'REDIS_URL', 'redis://localhost:6379/0')
        parsed = urlparse(redis_url)
        
        print_status(f"Redis URL: {redis_url}", "INFO")
        
        # Try to connect
        r = redis.Redis(
            host=parsed.hostname or 'localhost',
            port=parsed.port or 6379,
            password=parsed.password,
            db=0,
            socket_connect_timeout=5
        )
        
        # Test connection
        if r.ping():
            print_status("Redis connection successful", "OK")
            
            # Test read/write
            r.set('test_key', 'test_value')
            if r.get('test_key') == b'test_value':
                print_status("Redis read/write operations", "OK")
                r.delete('test_key')
            
            return True
        else:
            print_status("Redis ping failed", "FAIL")
            return False
            
    except redis.ConnectionError:
        print_status("Redis connection failed - Is Redis running?", "FAIL")
        print(f"{Colors.YELLOW}To start Redis:{Colors.END}")
        print("  Docker: docker run -d --name redis-chemical -p 6379:6379 redis:alpine")
        print("  WSL2:   sudo service redis-server start")
        return False
    except Exception as e:
        print_status(f"Redis check failed: {str(e)}", "FAIL")
        return False

def check_celery_config():
    """Check Celery configuration"""
    print(f"\n{Colors.BLUE}=== Checking Celery Configuration ==={Colors.END}\n")
    
    try:
        from backend.celery import app
        print_status("Celery app configured", "OK")
        
        from django.conf import settings
        broker_url = getattr(settings, 'CELERY_BROKER_URL', None)
        if broker_url:
            print_status(f"Celery broker: {broker_url}", "OK")
        else:
            print_status("Celery broker not configured", "WARN")
        
        return True
    except Exception as e:
        print_status(f"Celery check failed: {str(e)}", "FAIL")
        return False

def check_channels_config():
    """Check Django Channels configuration"""
    print(f"\n{Colors.BLUE}=== Checking Django Channels ==={Colors.END}\n")
    
    try:
        from django.conf import settings
        
        # Check ASGI application
        asgi_app = getattr(settings, 'ASGI_APPLICATION', None)
        if asgi_app:
            print_status(f"ASGI application: {asgi_app}", "OK")
        else:
            print_status("ASGI application not configured", "WARN")
        
        # Check channel layers
        channel_layers = getattr(settings, 'CHANNEL_LAYERS', None)
        if channel_layers:
            print_status("Channel layers configured", "OK")
        else:
            print_status("Channel layers not configured", "WARN")
        
        return True
    except Exception as e:
        print_status(f"Channels check failed: {str(e)}", "FAIL")
        return False

def check_jwt_config():
    """Check JWT configuration"""
    print(f"\n{Colors.BLUE}=== Checking JWT Configuration ==={Colors.END}\n")
    
    try:
        from django.conf import settings
        
        jwt_settings = getattr(settings, 'SIMPLE_JWT', None)
        if jwt_settings:
            print_status("JWT settings configured", "OK")
            
            access_lifetime = jwt_settings.get('ACCESS_TOKEN_LIFETIME')
            refresh_lifetime = jwt_settings.get('REFRESH_TOKEN_LIFETIME')
            
            print_status(f"Access token lifetime: {access_lifetime}", "INFO")
            print_status(f"Refresh token lifetime: {refresh_lifetime}", "INFO")
        else:
            print_status("JWT settings not found", "WARN")
        
        return True
    except Exception as e:
        print_status(f"JWT check failed: {str(e)}", "FAIL")
        return False

def print_summary(results):
    """Print summary of all checks"""
    print(f"\n{Colors.BLUE}{'='*50}{Colors.END}")
    print(f"{Colors.BLUE}=== Summary ==={Colors.END}")
    print(f"{Colors.BLUE}{'='*50}{Colors.END}\n")
    
    total = len(results)
    passed = sum(results.values())
    
    if passed == total:
        print(f"{Colors.GREEN}All checks passed! ({passed}/{total}){Colors.END}")
        print(f"\n{Colors.GREEN}✓ Backend is ready to run!{Colors.END}\n")
        print("Start the backend with:")
        print(f"{Colors.BLUE}Terminal 1:{Colors.END} celery -A backend worker --loglevel=info --pool=solo")
        print(f"{Colors.BLUE}Terminal 2:{Colors.END} daphne -b 0.0.0.0 -p 8000 backend.asgi:application")
    else:
        print(f"{Colors.RED}Some checks failed ({passed}/{total} passed){Colors.END}")
        print(f"\n{Colors.YELLOW}Please fix the issues above before running the backend.{Colors.END}\n")
    
    print(f"\n{Colors.BLUE}{'='*50}{Colors.END}\n")

def main():
    """Run all health checks"""
    print(f"\n{Colors.BLUE}{'='*50}{Colors.END}")
    print(f"{Colors.BLUE}Chemical Visualizer - Backend Health Check{Colors.END}")
    print(f"{Colors.BLUE}{'='*50}{Colors.END}")
    
    results = {
        'packages': check_imports(),
        'django': check_django_setup(),
        'database': check_database(),
        'redis': check_redis(),
        'celery': check_celery_config(),
        'channels': check_channels_config(),
        'jwt': check_jwt_config(),
    }
    
    print_summary(results)
    
    return all(results.values())

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Health check interrupted{Colors.END}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {str(e)}{Colors.END}\n")
        sys.exit(1)
