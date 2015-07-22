frappe.require('assets/frappe/js/lib/jQuery.Gantt/css/style.css');
frappe.require('assets/frappe/js/lib/jQuery.Gantt/js/jquery.fn.gantt.js');

frappe.pages['dispatching-dashboar'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Dispatching Dashboard',
		single_column: true
	});

	var options = {
		doctype: "Delivery Note",
		parent: page
	};

	page.ganttview = new frappe.views.DispachOrderGantt(options,page,wrapper);
}

frappe.views.DispachOrderGantt = frappe.views.Gantt.extend({
	init: function(opts, page, wrapper) {
		$.extend(this, opts);
		this.make_page(page,wrapper);
		frappe.route_options ?
			this.set_filters_from_route_options() :
			this.refresh();
	},
	make_page: function(page,wrapper) {
		var me = this;

		this.page = page;
		this.page.set_title(__("Dispatching Dashboard") + " - " + __("Gantt Chart"));

		this.page.set_secondary_action(__("Refresh"),
			function() { me.refresh(); }, "icon-refresh")

		this.start = this.page.add_field({fieldtype:"Date", label:"From",
			fieldname:"start", "default": frappe.datetime.get_today(), input_css: {"z-index": 3}});

		this.end = this.page.add_field({fieldtype:"Date", label:"To",
			fieldname:"end", "default": frappe.datetime.add_days(frappe.datetime.get_today(),14), input_css: {"z-index": 3}});

		this.technician = this.page.add_field({fieldtype:"Link", label:"Technician",
			fieldname:"technician", options:"Supplier", get_query:{
				filters:{
					"supplier_type":"Technician"
				}
			}, input_css: {"z-index": 3}});

		this.mode = this.page.add_field({fieldtype:"Select", label:"Mode",
			fieldname:"mode", default_value:"Hours", options:["Hours","Days"], input_css: {"z-index": 3}});

		this.add_filters();
		this.wrapper = $("<div style='position: relative;z-index:1;'></div>").appendTo(this.page.main);

	},
	refresh: function() {
		var me = this;
		return frappe.call({
			method: "das.das.page.dispatching_dashboar.dispatching_dashboar.get_dispach_orders",
			type: "GET",
			args: {
				start: this.page.fields_dict.start.get_parsed_value(),
				end: this.page.fields_dict.end.get_parsed_value(),
				filters: {
					"technician": me.page.fields_dict.technician.get_parsed_value()
				}
			},
			callback: function(r) {
				$(me.wrapper).empty();
				if(!r.message || !r.message.length) {
					$(me.wrapper).html('<p class="text-muted" style="padding: 15px;">' + __('Nothing to show for this selection') + '</p>');
				} else {
					var gantt_area = $('<div class="gantt">').appendTo(me.wrapper);

					var mode = me.page.fields_dict.mode.get_parsed_value();
					var gantt_scale = "hours";
					if(mode)
						// gantt_scale = mode
						gantt_scale = mode == "Hours"?"hours":"days"

					gantt_area.gantt({
						source: get_gantt_source_dataset(r.message),
						navigate: "scroll",
						scale: gantt_scale,
						minScale: "hours",
						maxScale: "weeks",
						itemsPerPage: 20,
						onItemClick: function(data) {
							frappe.set_route('Form', "Delivery Note", data.name);
						},
						onAddClick: function(dt, rowId) {
							newdoc("Delivery Note");
						}
					});
				}
			}
		});
	}
});

get_gantt_source_dataset = function(orders){
	me = this
	var result_set = []
	for (var i = 0; i < orders.length; i++) {
		result_set.push({
			name: orders[i].name,
			// values: orders[i].values
			values: get_values(me, orders[i].values)
		})
	}

	return result_set;
}

get_values = function(me, values){
	var result_set = [];
	for (var i = values.length - 1; i >= 0; i--) {
		if (values[i].status == "Draft")
			values[i].customClass = 'ganttBlue';
		else if (values[i].status == "Submitted")
			values[i].customClass = 'ganttGreen';
		else if (values[i].status == "Cancelled")
			values[i].customClass = 'ganttRed';
		else
			values[i].customClass = 'ganttGrey';

		var start = dateutil.convert_to_user_tz(values[i].from)
		var end = dateutil.convert_to_user_tz(values[i].to)
		
		values[i].desc = "<div class='row'><div class='col-xs-6'>Delivery Note</div><div class='col-xs-6'>"+ values[i].name
		+"</div></div><div class='row'><div class='col-xs-6'>Customer</div><div class='col-xs-6'>"+ values[i].customer
		+"</div></div><div class='row'><div class='col-xs-6'>Technician</div><div class='col-xs-6'>"+ values[i].technician
		+"</div></div><div class='row'><div class='col-xs-6'>Start Date</div><div class='col-xs-6'>"+ start
		+"</div></div><div class='row'><div class='col-xs-6'>End Date</div><div class='col-xs-6'>"+ end +"</div></div>"
		values[i].from = '/Date('+moment(start).format("X")+'000)/',
		values[i].to = '/Date('+moment(end).format("X")+'000)/',
		values[i].dataObj = values[i];

		result_set.push(values[i]);
	};

	return result_set;
}
