// *******************Get Technician*********************

// var field_name = cur_frm.doc.doctype == "Purchase Invoice"? "supplier": "technician";

// calculate gross profit on sales order
frappe.ui.form.on("Sales Order", "exp_supplier_payment", function(frm) {
	get_values(frm.doc)
});

frappe.ui.form.on("Sales Order", "exp_technician_payment", function(frm) {
	get_values(frm.doc)
});

frappe.ui.form.on("Sales Order", "exp_additional_services_payment", function(frm) {
	get_values(frm.doc)
});


function get_values (doc) {
	esp = 0.0; etp = 0.0; easp = 0.0;
	if(doc.exp_supplier_payment){
	 	esp = doc.exp_supplier_payment
	 }
	 
	 if(doc.exp_technician_payment){
	 	etp = doc.exp_technician_payment
	 }
	 
	 if(doc.exp_additional_services_payment){
	 	easp= doc.exp_additional_services_payment
	 }

	doc.gross_profit= (parseFloat(esp) + parseFloat(etp) + parseFloat(easp))
	refresh_field("gross_profit")
}

//set current date on submit of delivery note
frappe.ui.form.on("Delivery Note", "before_submit", function(frm) {
	frm.doc.posting_date=frappe.datetime.get_today();
});

//Make PO Button on sales order mapped with PO
// frappe.ui.form.on("Sales Order", "refresh", function(frm) {
// 	cur_frm.dashboard.reset();
// 	if(frm.doc.docstatus==1) {
// 		if(frm.doc.status != 'Stopped') {
// 			cur_frm.add_custom_button(__('Make PO'), cur_frm.cscript['Make PO']);
// 		}
// 	}
// });
//call mapped method from po
// cur_frm.cscript['Make PO'] = function(doc) {
// 	frappe.model.open_mapped_doc({
// 		method: "das.custom_methods.make_PO",
// 		frm: cur_frm
// 	})
// }

//set sales team contribution to 100%
frappe.ui.form.on("Sales Order", "before_save", function(frm) {
	if(frm.doc.sales_team)
	{
		if(frm.doc.sales_team.length>0 && !frm.doc.sales_team[0].allocated_percentage)
		{
			frm.doc.sales_team[0].allocated_percentage=100
		}
	}
});



cur_frm.fields_dict["technician"].get_query = function(doc) {
	return {
		filters: {
			'supplier_type': 'Technician'
		}
	}
}

cur_frm.cscript.make_po = function(doc){
	frappe.model.open_mapped_doc({
		method: "das.custom_methods.make_PO",
		frm: cur_frm
	})
}

cur_frm.cscript.make_purchase_invoice = function(doc){
	return frappe.call({
		method: "das.custom_methods.is_pi_already_exsits",
		args: {
			sales_order:cur_frm.doc.name
		},
		callback: function(r){
			if(r.message == "no invoice")
				frappe.model.open_mapped_doc({
					method: "das.custom_methods.make_purchase_invoice",
					frm: cur_frm
				});
			else
				frappe.msgprint("Purchase Invoice : "+ r.message +" is already created");
		}
	});
}

is_pi_already_exsits = function(so_name){
	return frappe.call({
		method: "das.custom_methods.is_pi_already_exsits",
		args: {
			sales_order:so_name
		},
		callback: function(r){
			if(r.message == "no invoice")
				return true
			else
				return false
		}
	});
}
