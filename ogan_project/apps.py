from django.contrib.admin.apps import AdminConfig as BaseAdminConfig

class OganAdminConfig(BaseAdminConfig):
    default_site = 'ogan_project.admin_site.OganAdminSite'
