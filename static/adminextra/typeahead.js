SEARCH_URL = "search/"
TRUE_IMG = '<img src="/static/admin/img/icon-yes.svg" alt="True">'
FALSE_IMG = '<img src="/static/admin/img/icon-no.svg" alt="False">'

django.jQuery(function($) {
	var initial = $("#result_list tbody")
	var input = $('#changelist-search [name="q"]')

	/* Manage filter widgets */
	filters = $("#changelist-filter form").on("change", function(evt) {
		$('output[for="'+evt.target.id+'"]').val(evt.target.value)
		input.trigger("keyup")
	})

	/* Select the text on focus */
	input.focus(function(evt) {
		$(input).select()
	})

	/* Handle automagic search */
	input[0].autocomplete = "off"
	input.on('keyup', function(evt) {
		/* Don't do multiple search in parrallel */
		if (document.query_in_progress)
			document.query_in_progress.abort()
			document.query_in_progress = null
		/* Restore original results on empty search */
		query = evt.target.value
		// Put back original result if there is no filters widget
		if (query == "" && filters == []) {
			$("#result_list tbody").replaceWith(initial)
			return
		}
		// If there is filters widget, put a neutral query
		if (query == "") {
			query = "*"
		}
		/* Grab filter */
		filters = $("#changelist-filter [data-filter-field]")
		filter = filters.map(function(i, item) {
			item = $(item)
			field = item.data("filter-field")
			switch (item.data("filter-type")) {
			case "numeric":
				min = item.find('input[name="'+field+'__gte"]').val()
				max = item.find('input[name="'+field+'__lte"]').val()
				return [[field, min, max]]
			}
		}).toArray()
		/* Do AJAX */
		document.query_in_progress = $.ajax(SEARCH_URL,
			{data:{"q":query, "f":JSON.stringify(filter)}}
		)
		.done(function(response) {
			document.query_in_progress = null
			if (response["success"]) {
				update_table(response["hits"])
			} else {
				$("#result_list tbody").replaceWith(initial)
			}
		})
	})

	headers = $('#result_list thead tr th:not(.action-checkbox-column)')
		.map(function(i, obj){
			return obj.className.match(/column-([^ ]*)/)[1]
		})

	/* Insert results into the page */
	function update_table(objs) {
		var tbody = $("<tbody>")
		for (var i=0; i<objs.length; ++i) {
			o = objs[i]
			var tr = $("<tr class=row"+(1+i%2)+">")
			tr.attr("score", o["_score"])
			// checkbox for selecting
			var cb = $('<td class=action-checkbox>')
			var input = $('<input type=checkbox class=action-select>')
			input.attr("name", "_selected_action").val(o["pk"])
			cb.append(input)
			tr.append(cb)
			// values
			for (var j=0; j<headers.length; ++j) {
				header = headers[j].toLowerCase()
				tag = (j==0) ? "<th " : "<td "
				td = $(tag+"class=field-"+header+">")
				if (j==0) {
					link = $("<a href="+o["pk"]+">").text(o[header])
					td.append(link)
				} else {
					if (typeof(o[header]) == "boolean") {
						td.html(o[header]? TRUE_IMG : FALSE_IMG)
					} else if (o[header] === null) {
						td.text("-")
					} else {
						td.text(o[header])
					}
				}
				tr.append(td)
			}
			tbody.append(tr)
		}
		$("#result_list tbody").replaceWith(tbody)
	}
})
