#-*-coding:utf-8-*-
from openerp import models, fields, api
from datetime import datetime

#Minutas
class jmd_minuta(models.Model):
    _inherit = "mail.thread"
    _name = "utils.minuta"
    
    @api.one
    def generar_nueva(self):
        ret = {}
        id_minuta = self.copy({'name': self.nombre})
        print("Id de la minuta " + str(id_minuta))
        for i in self.asuntos_ids:
            if not i.realizado:
                self.env['utils.minuta.asunto'].create({
                'descripcion': i.descripcion,
                'responsable': i.responsable.id,
                'fecha_limite': i.fecha_limite,
                'vuelta': int(i.vuelta + 1),
                'horas_dedicadas': i.horas_dedicadas,
                'comentarios': i.comentarios,
                'minuta_id': id_minuta.id,
                'project_id': i.project_id.id})
        return ret
    
    @api.one
    def planea(self):
        ret = {}
        for i in range(self.veces):
            id_minuta = self.copy({'name': self.name + " - seguimiento"})
            print("Id de la minuta " + str(id_minuta))
            for i in self.asuntos_ids:
                if not i.realizado:
                    self.env['utils.minuta.asunto'].create({
                'descripcion': i.descripcion,
                'responsable': i.responsable.id,
                'fecha_limite': i.fecha_limite,
                'vuelta': int(i.vuelta + 1),
                'horas_dedicadas': i.horas_dedicadas,
                'comentarios': i.comentarios,
                'minuta_id': id_minuta.id,
                'project_id': i.project_id.id})
        return ret
        
    
    name = fields.Char("Consecutivo",  default=lambda self: self.env["ir.sequence"].get("utils.minuta"))
    hora_inicio = fields.Datetime("Hora Inicio")
    hora_fin = fields.Datetime("Hora Fin")
    lugar = fields.Char("Lugar")
    responsable_id = fields.Many2one("hr.employee",  string="Responsable")
    objetivo = fields.Char("Objetivo")
    acuerdos = fields.Text("Acuerdos")
    privada = fields.Boolean("Minuta Privada")
    estado = fields.Selection([("Abierta",  "Abierta"),  ("Cerrada",  "Cerrada")])
    asistentes = fields.Many2many("res.partner",  string="Asistentes")
    proyecto_id = fields.Many2one("project.project", "Proyecto")
    motivo_cambios = fields.Selection([('diseno', 'Problemas de Diseño' ),
                                       ('cliente', 'Problemas de Cliente'),
                                       ('construccion', 'Problemas de Construcción')], 
                                      string="Motivo de los Cambios")
    recurrente = fields.Boolean("Junta Recurrente")
    repetir = fields.Selection([('Semanal', 'Semanal'),
                                ('Mensual', 'Mensual')], string="Repetir")
    veces = fields.Integer("Veces que se repite")
    nombre = fields.Char("Nombre")
    asuntos_ids = fields.One2many("utils.minuta.asunto",  "minuta_id",  string="Asuntos")
    agenda_ids = fields.One2many("utils.minuta.agenda", "minuta_id", string="Agenda")
    asistentes_ids = fields.One2many("utils.minuta.asistente", "minuta_id", string="Asistentes")
    
class jmd_agenda(models.Model):
    _inherit = "mail.thread"
    _name = "utils.minuta.agenda"
    name = fields.Char("Punto")
    tiempo = fields.Float("Tiempo Asignado")
    tratado = fields.Boolean("Tratado")
    minuta_id = fields.Many2one("utils.minuta")
    
class jmd_asistente(models.Model):
    _inherit = "mail.thread"
    _name = "utils.minuta.asistente"
    name = fields.Many2one("res.partner")
    tiempo = fields.Boolean("A tiempo")
    asiste = fields.Boolean("Asistió")
    minuta_id = fields.Many2one("utils.minuta")
    
    
class jmd_asunto(models.Model):
    _inherit = "mail.thread"
    _name = "utils.minuta.asunto"
    
    @api.one
    def task(self):
        ret = {}
        self.project_id.write({'task_ids': [(0,  0,  
                                             {'name': self.descripcion,
                                              'planned_hours': 1,
                                              'user_id': self.responsable.user_id.id,
                                              'date_deadline': self.fecha_limite})]})
        self.write({'tarea': True})
        return ret
    
    @api.one
    def appoint(self):
        ret = {}
        fecha = self.fecha_limite
        print(type(fecha))
        print(fecha)
        fecha_obj = datetime.strptime(self.fecha_limite, "%Y-%m-%d")
        fechastr = datetime.strftime(fecha_obj, "%Y-%m-%d") + " 10:00:00"
        fechastop = datetime.strftime(fecha_obj, "%Y-%m-%d") + " 11:00:00"
        self.env['calendar.event'].create({
            'name': self.descripcion,
            'start_datetime': fechastr,
            'stop_datetime': fechastop,
            })
        self.write({'cita': True})
        return ret
    
    
    name = fields.Char("Consecutivo")
    descripcion = fields.Char("Descripción")
    responsable = fields.Many2one("hr.employee",  string="Responsable")
    fecha_limite = fields.Date("Fecha Límite")
    vuelta = fields.Integer("Vuelta",  default=1)
    horas_dedicadas = fields.Float("Horas Dedicadas")
    realizado = fields.Boolean("Realizado")
    comentarios = fields.Text("Comentarios")
    prioridad = fields.Selection([("Alta",  "Alta"),  ("Media",  "Media"),  ("Baja",  "Baja")], string="Prioridad")
    pasos = fields.Char("Pasos a seguir")
    tarea = fields.Boolean("Tarea")
    cita = fields.Boolean("Cita")
    minuta_id = fields.Many2one("utils.minuta")
    motivo_cambios = fields.Selection([('diseno', 'Problemas de Diseño' ),
                                       ('cliente', 'Problemas de Cliente'),
                                       ('construccion', 'Problemas de Construcción')], 
                                      string="Motivo de los Cambios")
    project_id = fields.Many2one("project.project", string="Proyecto")
    adjunto = fields.Binary("Archivo Adjunto")
    nadjunto = fields.Char("Nombre del Archivo")
    tipo = fields.Selection([('Proveedor', 'Proveedor'), ('Cliente', 'Cliente')], string="Tipo")
    
