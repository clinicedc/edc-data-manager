from edc_navbar.navbar import Navbar
from edc_navbar.site_navbars import site_navbars
from edc_review_dashboard.navbars import navbar as review_navbar

navbar = Navbar(name="data_manager_app")

for item in review_navbar.items:
    navbar.append_item(item)


site_navbars.register(navbar)
