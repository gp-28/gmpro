import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class FrentedeTrabajo(Document):
    def validate(self):
        if self.fecha_inicio and self.fecha_termino:
            if getdate(self.fecha_termino) < getdate(self.fecha_inicio):
                frappe.throw("La fecha de término no puede ser anterior a la fecha de inicio.")
