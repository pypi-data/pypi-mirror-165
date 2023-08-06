try:
    from django.core.exceptions import ImproperlyConfigured
except ImportError:

    class ImproperlyConfigured(ValueError):
        """
        Substitution for Django's ImproperlyConfigured error class
        """
