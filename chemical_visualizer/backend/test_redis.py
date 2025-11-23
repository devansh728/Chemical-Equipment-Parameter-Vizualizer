"""
Test Redis connectivity for Django Channels
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def test_redis_connection():
    """Test if Redis connection works for Channels"""
    try:
        channel_layer = get_channel_layer()
        
        if channel_layer is None:
            print("❌ ERROR: Channel layer is None!")
            print("Check CHANNEL_LAYERS in settings.py")
            return False
        
        print(f"✅ Channel layer initialized: {type(channel_layer).__name__}")
        print(f"   Config: {channel_layer}")
        
        # Try to send a test message
        test_group = "test_group"
        test_message = {"type": "test.message", "content": "Hello Redis!"}
        
        print("\n🔄 Testing group_send...")
        async_to_sync(channel_layer.group_send)(test_group, test_message)
        print("✅ group_send successful!")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Testing Redis Connection for Django Channels")
    print("=" * 60)
    
    success = test_redis_connection()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Redis connection test PASSED")
        print("WebSocket should work now!")
    else:
        print("❌ Redis connection test FAILED")
        print("\nPossible solutions:")
        print("1. Check if Redis Cloud credentials are correct in .env")
        print("2. Try using local Redis: redis://localhost:6379/0")
        print("3. Check if Redis Cloud allows connections from your IP")
        print("4. Verify CHANNEL_LAYERS configuration in settings.py")
    print("=" * 60)
