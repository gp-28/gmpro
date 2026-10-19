import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class Asignacion(Document):
    def validate(self):
        self.validar_fechas()
        self.validar_empresa()
        self.validar_duplicado()

    def validar_fechas(self):
        if self.fecha_inicio and self.fecha_termino:
            if getdate(self.fecha_termino) < getdate(self.fecha_inicio):
                frappe.throw("La fecha de término no puede ser anterior a la fecha de inicio.")

    def validar_empresa(self):
        empresa_periodo = frappe.db.get_value("Periodo Operativo", self.periodo_operativo, "company")
        if empresa_periodo != self.company:
            frappe.throw("El período operativo pertenece a otra empresa distinta a la del frente de trabajo.")

        empresa_trabajador = frappe.db.get_value("Employee", self.employee, "company")
        if empresa_trabajador != self.company:
            frappe.throw("El trabajador pertenece a otra empresa distinta a la del frente de trabajo.")

    def validar_duplicado(self):
        existe = frappe.db.exists(
            "Asignacion",
            {
                "employee": self.employee,
                "frente_de_trabajo": self.frente_de_trabajo,
                "periodo_operativo": self.periodo_operativo,
                "estado": ["!=", "Cancelada"],
                "name": ["!=", self.name],
            },
        )
        if existe:
            frappe.throw("Este trabajador ya tiene una asignación vigente en este frente y período.")
