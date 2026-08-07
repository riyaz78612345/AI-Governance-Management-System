ROLE_PERMISSIONS = {
    "Admin": [
        "Dashboard",
        "Model Registry",
        "Risk Assessment",
        "Compliance",
        "Ethics",
        "Policies",
        "Incidents",
        "Audits",
        "Reports"
    ],

    "Compliance Officer": [
        "Dashboard",
        "Risk Assessment",
        "Compliance",
        "Ethics",
        "Policies",
        "Reports"
    ],

    "Auditor": [
        "Dashboard",
        "Risk Assessment",
        "Incidents",
        "Audits",
        "Reports"
    ],

    "Viewer": [
        "Dashboard",
        "Reports"
    ]
}


def has_permission(role, page):
    return page in ROLE_PERMISSIONS.get(role, [])