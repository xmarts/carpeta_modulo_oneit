# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    monto_deuda = fields.Float(compute="_compute_montos")
    saldo_cobrar = fields.Float(compute="_compute_cotizacion")
    
    #AGREDAMOS LOS CAMPOS NECESARIOS A LAS FACTURAS DE CLIENTE  PARA ṔODER MOSTRARLOS EN LA VISTA TREE 
    id_venta = fields.Integer(compute="_compute_cotizacion")
    total_venta = fields.Float(compute="_compute_cotizacion")

    #AGREGAMOS LOS CAMPOS NECESARIOS A LAS FACTURAS DE PROVEEDOR PARA MOSTRARLOS EN LA VISTA TREE
    id_compra = fields.Integer(compute="_compute_compra")
    total_compra = fields.Float(compute="_compute_compra")
    saldo_pagar = fields.Float(compute="_compute_compra")

    #CREAMOS UN FUNCION PARA QUE TOMEN UN VALOR LOS NUEVOS CAMPOS DE ACUERDO SI EXISTE UN ORIGEN EN LA FACTURA
    @api.one
    def _compute_cotizacion(self):
        if self.type == 'out_invoice':
            if self.origin:
                buscar_cot = self.env['sale.order'].search([('name','=',self.origin)], limit=1)
                if buscar_cot:
                    self.id_venta = buscar_cot.id
                    self.total_venta = buscar_cot.amount_total

                    saldo = buscar_cot.amount_total - self.amount_total
                    self.saldo_cobrar = saldo

    @api.one
    def _compute_montos(self):
        if self.amount_total and self.residual:
            resto = self.amount_total - self.residual
            self.monto_deuda = resto

    #FUNCIOM PARA MANDAR EN AUTOMATICO VALOR A LOS CAMPOS AGREGADOS EN LA VISTA, PARA FACTURAS DE PROVEEDOR
    @api.one
    def _compute_compra(self):
        if self.type == 'in_invoice':
            if self.origin:
                compra = self.env['purchase.order'].search([('name','=',self.origin)], limit=1)
                if compra:
                    self.id_compra = compra.id
                    self.total_compra = compra.amount_total

                    saldo = compra.amount_total - self.amount_total
                    self.saldo_cobrar = saldo

                    self.saldo_pagar = self.total_compra -self.monto_deuda

class StockMove(models.Model):
    _inherit = 'stock.move'

    stock_provider = fields.Char(string="Proveedor", compute="_compute_origin")

    @api.one
    def _compute_origin(self):
        if self.origin:
            obj_compra = self.env['purchase.order'].search([('name','=',self.origin)], limit=1)
            if obj_compra:
                self.stock_provider = obj_compra.partner_id.name


