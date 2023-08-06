from django.utils.translation import gettext_lazy as _

MENUS = {
    "NAV_MENU_CORE": [
        {
            "name": _("Seating plans"),
            "url": "seating_plans",
            "svg_icon": "mdi:view-list-outline",
            "validators": [
                (
                    "aleksis.core.util.predicates.permission_validator",
                    "stoelindeling.view_seatingplans_rule",
                ),
            ],
        },
    ]
}
