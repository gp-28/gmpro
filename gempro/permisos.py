import frappe
from frappe.permissions import add_permission, update_permission_property

# Permisos que Gempro agrega sobre DocTypes nativos de ERPNext.
# Formato: (DocType, Rol, [permisos que SÍ tiene])
PERMISOS = [
    ("Employee", "Gempro Propietario", ["select", "read", "write", "create"]),
    ("Employee", "Gempro Admin Empresa", ["select", "read", "write", "create"]),
    ("Employee", "Gempro RRHH", ["select", "read", "write", "create"]),
    ("Employee", "Gempro Jefe de Frente", ["select", "read"]),
    ("Company", "Gempro Propietario", ["select", "read"]),
    ("Company", "Gempro Admin Empresa", ["select", "read"]),
    ("Company", "Gempro RRHH", ["select", "read"]),
    ("Company", "Gempro Jefe de Frente", ["select", "read"]),
]

# Todos los tipos de permiso que se controlan. Los que no estén en la lista quedan en 0.
TIPOS = [
    "select", "read", "write", "create", "delete",
    "print", "email", "report", "import", "export", "share",
]


def asegurar_rol(rol):
    if not frappe.db.exists("Role", rol):
        frappe.get_doc({"doctype": "Role", "role_name": rol, "desk_access": 1}).insert(
            ignore_permissions=True
        )


def aplicar_permisos(*args, **kwargs):
    for doctype, rol, permisos in PERMISOS:
        asegurar_rol(rol)
        add_permission(doctype, rol, 0)
        for tipo in TIPOS:
            update_permission_property(doctype, rol, 0, tipo, 1 if tipo in permisos else 0)
    frappe.db.commit()
    frappe.clear_cache()
