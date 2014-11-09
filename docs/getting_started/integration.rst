############
Integration
############

******************
Deactivate Celery
******************

It is recommended to run django-bmf with celery. Nethertheless it's also possible to deactivate
celery. If celery is installed, you can set ``CELERY_ALWAYS_EAGER`` to ``True``.

http://celery.readthedocs.org/en/latest/configuration.html#celery-always-eager

With this setting celery is loaded, but the tasks are excecuted locally.

There is also an the 
BMF_USE_CELERY setting. Set this to ``False`` and django-bmf won't load celery at all. Use this only
in testing or small installations.
