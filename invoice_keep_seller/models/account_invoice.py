# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class KeepAccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_invoice_open(self):
        if self.origin and self.type in ['out_refund','out_invoice']:
            origen = self.origin
            if origen.find("SO") > -1:
                # Pedido de Venta
                obj_sale_order = self.env['sale.order'].search([('name', '=', origen)])
                if obj_sale_order:
                    for id in obj_sale_order:
                        self.user_id = id.user_id


            if origen.find("OUT") > -1:
                # Salida de Almacen
                # Primero Buscamos la SO
                obj_stock_picking = self.env['stock.picking'].search([('name', '=', origen)])
                if obj_stock_picking:
                    for id in obj_stock_picking:
                        origen = id.origin

                # Buscamos en la SO
                obj_sale_order = self.env['sale.order'].search([('name', '=', origen)])
                if obj_sale_order:
                    for id in obj_sale_order:
                        self.user_id = id.user_id

        res = super(KeepAccountInvoice, self).action_invoice_open()
        return res
