import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt


@frappe.whitelist()
def make_purchase_invoice(source_name, target_doc=None):
	def postprocess(source, target):
		target.sales_order = source.name
		target.supplier = source.technician
		target.credit_to = frappe.db.get_value("Company", frappe.db.get_default("company"), "default_payable_account")
		target.taxes_and_charges = ''

	def update_item(source, target, source_parent):
		target.amount = flt(source.amount) - flt(source.billed_amt)
		target.base_amount = target.amount * flt(source_parent.conversion_rate)
		target.qty = source.qty

	doclist = get_mapped_doc("Sales Order", source_name, {
		"Sales Order": {
			"doctype": "Purchase Invoice",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Sales Order Item": {
			"doctype": "Purchase Invoice Item",
			"field_map": {
				# "name": "pr_detail",
				"parent": "purchase_invoice"
			},
			"postprocess": update_item,
			"condition": lambda doc: frappe.db.get_value("Item",doc.item_code,"is_service_item") == 1
		},
	}, target_doc, postprocess)

	return doclist

@frappe.whitelist()
def is_pi_already_exsits(sales_order):
	invoice = frappe.db.sql("""select name from `tabPurchase Invoice` where docstatus in (0,1) and sales_order='%s'"""%(sales_order))
	if not invoice:
		return "no invoice"
	else:
		return invoice


@frappe.whitelist()
def make_PO(source_name, target_doc=None):
	def postprocess(source, target):
		target.taxes_and_charges = frappe.db.get_value('Purchase Taxes and Charges Template', {'is_default':1}, 'name') or None

	def update_item(source, target, source_parent):
		target.uom = source.stock_uom
		target.conversion_factor = 1
		target.qty = target.amount / flt(source.rate) if (source.rate and source.billed_amt) else source.qty
		target.price_list_rate=0
		target.rate=0
	target_doc = get_mapped_doc("Sales Order", source_name, {
		"Sales Order": {
			"doctype": "Purchase Order",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Sales Order Item": {
			"doctype": "Purchase Order Item",
			"field_map": {
				"parent": "purchase_order",
			},
			"postprocess": update_item,
			"condition": lambda doc: frappe.db.get_value("Item",doc.item_code,"is_service_item") == 0
		}
	}, target_doc, postprocess)
	return target_doc

@frappe.whitelist()
def is_service_items_only(sales_order):
	import json
	pass_item=''
	sales_order = json.loads(sales_order)
	for item in sales_order.get("items"):
		is_serv=frappe.db.get_value("Item",item.get("item_code"),"is_service_item")
		if not is_serv:
			return "success"
	return "Fail"		

		
	