import frappe
from frappe.utils import get_site_path
import csv
def make_csv():
	column_header=[['Transaction Date', 'Name', 'Customer', 'Customer Address', 'Company', 'Delivery Date', 'Installation End Date', 'Invoices Submitted', 'Products', 'Installation Status', 'Documents Preparation', 'Customer Payment', 'Technician Payment', 'Customer Signed Order']]
	column_data=get_data()
	
	if(column_data):
		for data in column_data:
			column_header.append(data)
		
	write_csv(column_header)
	print "closed"

def get_data():
	frappe.db.sql("""select transaction_date,name,customer,customer_address,company,delivery_date,installation_end_date,
invoices_submitted,products,installation_status,documents_preparation,_customer_payment,technician_payment,
customer_signed_order from `tabSales Order` where docstatus=1""" ,as_list=1)	

def write_csv(column_header):
	my_csv = open(get_site_path('public/files','so_csv.csv'), 'wb')
	final_csv = csv.writer(my_csv, quoting=csv.QUOTE_ALL)
	
	for row in column_header:
		final_csv.writerow(row)
	my_csv.close()