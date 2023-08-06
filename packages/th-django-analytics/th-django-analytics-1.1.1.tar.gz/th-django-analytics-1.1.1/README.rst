==================================
Django Analytics App
==================================

Quick start 
============

1. Add "analytics" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'analytics',
    ]

2. Include the polls URLconf in your project urls.py like this:: 
    
    path("analytics/", include("analytics.urls")),

3. Run ``python manage.py migrate`` to create the analytics models. 

4. Run ``python manage.py collectstatics`` to collect the statics files. 


Dashboard Data Processing
==========================

``python manage.py data_processing``