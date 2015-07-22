# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "das"
app_title = "das"
app_publisher = "Rohit Waghchaure"
app_description = "das"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "rohit.w@indictranstech.com"
app_version = "0.0.1"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/das/css/das.css"
# app_include_js = "/assets/das/js/das.js"

# include js, css files in header of web template
# web_include_css = "/assets/das/css/das.css"
# web_include_js = "/assets/das/js/das.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "das.install.before_install"
# after_install = "das.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "das.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Delivery Note": {
		"validate": "das.das_validations.delivery_note_validations",
		"on_submit": "das.das_payment_info.on_delivery_note_submit",
		"on_cancel": "das.das_payment_info.on_delivery_note_cancel"
	},
	"Sales Invoice": {
		# "validate": "das.das_validations.validations_against_batch_number",
		"on_submit": "das.das_payment_info.on_sales_invoice_submit",
		"on_cancel": "das.das_payment_info.on_sales_invoice_cancel"
	},
	"Purchase Invoice": {
		"validate": "das.das_validations.validations_against_supplier",
		"on_submit": "das.das_payment_info.on_purchase_invoice_submit",
		"on_cancel": "das.das_payment_info.on_purchase_invoice_cancel"
	},
	"Sales Order": {
		# "validate": "das.das_validations.delivery_note_validations"
		"on_submit": "das.das_payment_info.on_sales_order_submit",
		"on_cancel": "das.das_payment_info.on_sales_order_cancel"
	},
	"Journal Entry": {
		# "validate": "das.das_validations.delivery_note_validations"
		"on_submit": "das.das_payment_info.on_journal_entry_submit",
		"on_cancel": "das.das_payment_info.on_journal_entry_cancel"
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"das.tasks.all"
# 	],
# 	"daily": [
# 		"das.tasks.daily"
# 	],
# 	"hourly": [
# 		"das.tasks.hourly"
# 	],
# 	"weekly": [
# 		"das.tasks.weekly"
# 	]
# 	"monthly": [
# 		"das.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "das.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "das.event.get_events"
# }

fixtures = ["Custom Field","Property Setter"]
