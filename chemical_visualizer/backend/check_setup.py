"""
Quick diagnostic script to verify AI enhancement setup
Run: python check_setup.py
"""

import sys
import os

print("=" * 60)
print("AI ENHANCEMENT SETUP DIAGNOSTIC")
print("=" * 60)

# Check Python packages
print("\n1. CHECKING PYTHON DEPENDENCIES...")
required_packages = {
    'django': 'Django',
    'rest_framework': 'Django REST Framework',
    'celery': 'Celery',
    'redis': 'Redis',
    'channels': 'Django Channels',
    'pandas': 'Pandas',
    'scipy': 'SciPy',
    'google.generativeai': 'Google Generative AI'
}

missing = []
for package, name in required_packages.items():
    try:
        __import__(package)
        print(f"   ✅ {name}")
    except ImportError:
        print(f"   ❌ {name} - MISSING")
        missing.append(name)

if missing:
    print(f"\n⚠️  Missing packages: {', '.join(missing)}")
    print(f"   Run: pip install {' '.join(missing.lower().replace(' ', '-'))}")
else:
    print("\n✅ All required packages installed!")

# Check Django setup
print("\n2. CHECKING DJANGO SETUP...")
try:
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    django.setup()
    
    from api.models import Dataset
    from django.conf import settings
    
    # Check database fields
    print("   Checking Dataset model fields...")
    model_fields = [f.name for f in Dataset._meta.get_fields()]
    
    required_fields = [
        'enhanced_summary', 'column_profile', 'ai_suggestions',
        'ai_insights', 'correlation_matrix', 'outliers',
        'profiling_complete', 'analysis_complete', 'ai_complete'
    ]
    
    for field in required_fields:
        if field in model_fields:
            print(f"   ✅ {field}")
        else:
            print(f"   ❌ {field} - MISSING (Run migrations!)")
    
    # Check environment variables
    print("\n   Checking environment variables...")
    if hasattr(settings, 'GEMINI_API_KEY') and settings.GEMINI_API_KEY:
        print(f"   ✅ GEMINI_API_KEY configured")
    else:
        print(f"   ⚠️  GEMINI_API_KEY not set (AI features will use fallback)")
    
    # Check database
    print("\n   Checking database...")
    dataset_count = Dataset.objects.count()
    print(f"   📊 Total datasets: {dataset_count}")
    
    if dataset_count > 0:
        latest = Dataset.objects.last()
        print(f"   📁 Latest dataset:")
        print(f"      Status: {latest.status}")
        print(f"      Profiling complete: {latest.profiling_complete}")
        print(f"      Analysis complete: {latest.analysis_complete}")
        print(f"      AI complete: {latest.ai_complete}")
        print(f"      Has AI insights: {bool(latest.ai_insights)}")
        print(f"      Has outliers: {bool(latest.outliers)}")
        print(f"      Has correlations: {bool(latest.correlation_matrix)}")
    
    print("\n✅ Django setup OK!")
    
except Exception as e:
    print(f"\n❌ Django setup error: {str(e)}")
    print("   Make sure you're running from backend/ directory")

# Check Celery tasks
print("\n3. CHECKING CELERY TASKS...")
try:
    from api.tasks import (
        phase1_profile_and_suggest,
        phase2_deep_analysis,
        phase3_ai_insights,
        explain_outlier_task,
        get_recommendations_task
    )
    print("   ✅ phase1_profile_and_suggest")
    print("   ✅ phase2_deep_analysis")
    print("   ✅ phase3_ai_insights")
    print("   ✅ explain_outlier_task")
    print("   ✅ get_recommendations_task")
    print("\n✅ All Celery tasks defined!")
except Exception as e:
    print(f"\n❌ Celery tasks error: {str(e)}")

# Check API endpoints
print("\n4. CHECKING API ENDPOINTS...")
try:
    from api.views import (
        ExplainOutlierView,
        OptimizationView,
        CorrelationHeatmapView
    )
    print("   ✅ ExplainOutlierView")
    print("   ✅ OptimizationView")
    print("   ✅ CorrelationHeatmapView")
    print("\n✅ All API endpoints defined!")
except Exception as e:
    print(f"\n❌ API endpoints error: {str(e)}")

# Check analysis modules
print("\n5. CHECKING ANALYSIS MODULES...")
try:
    from api.advanced_analysis import (
        profile_columns,
        calculate_statistics,
        detect_outliers,
        calculate_correlations,
        analyze_csv_enhanced
    )
    print("   ✅ profile_columns")
    print("   ✅ calculate_statistics")
    print("   ✅ detect_outliers")
    print("   ✅ calculate_correlations")
    print("   ✅ analyze_csv_enhanced")
    print("\n✅ Advanced analysis module OK!")
except Exception as e:
    print(f"\n❌ Advanced analysis error: {str(e)}")

# Check Gemini service
print("\n6. CHECKING GEMINI AI SERVICE...")
try:
    from api.gemini_service import GeminiAnalyzer
    
    gemini = GeminiAnalyzer()
    is_configured = gemini.is_configured()
    
    print(f"   ✅ GeminiAnalyzer class loaded")
    print(f"   {'✅' if is_configured else '⚠️ '} API configured: {is_configured}")
    
    if not is_configured:
        print("   ℹ️  Add GEMINI_API_KEY to .env for full AI features")
    
    print("\n✅ Gemini service OK!")
except Exception as e:
    print(f"\n❌ Gemini service error: {str(e)}")

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

if not missing:
    print("✅ All dependencies installed")
else:
    print(f"❌ {len(missing)} missing dependencies")

print("\nNEXT STEPS:")
print("1. Start Redis: redis-server")
print("2. Start Django: python manage.py runserver")
print("3. Start Celery: celery -A backend worker --loglevel=info --pool=solo")
print("4. Start Frontend: cd ../chemical_visualizer_frontend && npm run dev")
print("5. Upload a NEW CSV file to test AI features")

print("\n" + "=" * 60)
