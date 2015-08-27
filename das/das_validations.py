import frappe
from datetime import datetime as dt
from frappe.utils import cstr, cint

def delivery_note_validations(doc, method):
	# start date end end date
	start = dt.strptime(doc.start_date, "%Y-%m-%d %H:%M:%S")
	end  = dt.strptime(doc.end_date, "%Y-%m-%d %H:%M:%S")

	if start > end:
		frappe.throw("End Date should be greater than Start Date")
	elif start == end:
		frappe.throw("End Date can not be same as Start Date")

	tech_details = is_technician_timeslot_free(doc.name, start, end, doc.technician)
	if tech_details:
		frappe.throw("%s is already assigned for other delivery note between given Start Date & End Date"%(doc.technician))

	# is_valid_delivery_date(doc)

def is_technician_timeslot_free(dn, _from, _to, technician):
	return frappe.db.sql("""SELECT name FROM `tabDelivery Note` WHERE name<>'%s' AND technician='%s' AND docstatus<>2 AND
		(('%s' between start_date AND end_date)
		OR ('%s' between start_date AND end_date)
		OR (start_date between '%s' AND '%s')
		OR (end_date between '%s' AND '%s'))"""%(dn,technician,_from,_to,_from,_to,_from,_to),
		as_dict=True)

def is_valid_delivery_date(doc):
	delivery_date = dt.strptime(doc.posting_date,"%Y-%m-%d")
	start_date = dt.strptime(doc.start_date, "%Y-%m-%d %H:%M:%S")
	if delivery_date.date() != start_date.date():
		frappe.throw("Delivery Date and Start Date should be same")

def validations_against_batch_number(doc, method):
	err_items = []
	for item in doc.items:
		if frappe.db.get_value("Item",item.item_code,"has_batch_no") == 1 and not cint(item.batch_no):
			err_items.append(item.item_code)

	if err_items:
		frappe.throw("Item Batch Number is mandatory for item(s) {err_items}".format(err_items = ",".join(err_items)))

def validations_against_supplier(doc,method):
	if doc.sales_order:
		technician = frappe.db.get_value("Sales Order",doc.sales_order, "technician")
		if technician != doc.supplier:
			frappe.throw("Invalid Supplier !!\nSupplier should be : %s"%(technician))

def sales_order_validations(doc, method):
	doc.gross_profit = doc.base_grand_total - (doc.gross_profit or 0)