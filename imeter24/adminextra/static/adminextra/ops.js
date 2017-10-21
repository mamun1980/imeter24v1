TRUE_IMG = '<img src="/static/admin/img/icon-yes.svg" alt="True">'
FALSE_IMG = '<img src="/static/admin/img/icon-no.svg" alt="False">'

// Take apply op on each source and apply to input
function update_math_op(input, source, op) {
	return function () {
		total = parseFloat(source[0].value) || 0
		for (i=1; i<source.length; ++i) {
			if (isNaN(source[i]))
				local = parseFloat(source[i].value)
			else
				local = source[i]

			switch (op) {
			case "plus":
				total += local
				break
			case "minus":
				total -= local
				break
			case "multiply":
				total *= local
				break
			case "divide":
				total /= local
				break
			}
		}
		if (isNaN(total)) {
			return
		}
		input.val(total).trigger("update")
	}
}

function math_op(input, source, op) {
	$ = django.jQuery
	var tgt = $('input[name='+input+']')[0]
	if (!tgt)
		return
	src = source.map(function(elmt) {
		input = $('input[name="'+elmt+'"]')[0]
		return input || elmt
	})
	for (i=0; i<src.length; ++i) {
		$(src[i]).on("blur", update_math_op($(tgt), src, op))
	}
}

function sum(input, source) {
	return math_op(input, source, "plus")
}
function sub(input, source) {
	return math_op(input, source, "minus")
}
function mul(input, source) {
	return math_op(input, source, "multiply")
}
function div(input, source) {
	return math_op(input, source, "divide")
}

function update_table(table, hits) {
	" Fill the result table "
	headers = table.headers
	table.find('tr:not(".header")').remove()
	for (i=0; i<hits.length; ++i) {
		var tr = $("<tr>")
		var btn = $("<a class=button>").text("select").data("pk", hits[i].pk)
		tr.append($("<th>").append(btn))
		for (j=0; j<headers.length; ++j) {
			data = hits[i][headers[j]]
			if (typeof(data) == "boolean") {
				tr.append($("<td>").html(data? TRUE_IMG : FALSE_IMG))
			} else if (data === null) {
				tr.append($("<td>").text("-"))
			} else {
				tr.append($("<td>").text(data))
			}
		}
		tr.data("obj", hits[i])
		table.append(tr)
	}
}

function build_search_widget(select, table, headers, search_url) {
	select.hide()

	// create the search input
	var search_input = $("<input type=text>")
	search_input.insertBefore(select)
	search_input.val(select.find('[value="'+select.val()+'"]').text())
	select.on("change", function() {
		search_input.val(select.find('[value="'+select.val()+'"]').text())
		table.hide()
	})

	// create table for search result
	var table_header = $('<thead><tr class="header"><td></td></tr></thead>')
	table.append(table_header)
	table.headers = headers
	table.hide()
	table.on("click", function(evt) {
		if ($(evt.target).data("pk")) {
			select.val($(evt.target).data("pk"))
			obj = $(evt.target).parents("tr").data("obj")
			select.data("obj", obj)
			select.trigger("change")
		}
	})

	// hook the searching to the search input
	var first = true
	var request
	search_input.on("keyup", function(evt) {
		// Cancel previous request
		if (request)
			request.abort()
		// Don't search on empty string
		if (evt.target.value == "") {
			table.hide()
			return
		}
		// Do the search
		request = $.ajax(search_url, {
			data: {"q": evt.target.value},
			timeout: 30000,
		})
		.done(search_success)
		.fail(function() {
			console.warn("fail", arguments)
		})
	})

	function search_success(response) {
		// Hide table on non-result
		if (response.success == false) {
			table.hide()
			console.warn(response.error)
			return
		}
		if (response.hits.length == 0) {
			table.hide()
			console.log("No result")
			return
		}
		// Add header to table
		if (first) {
			first = false
			var verbose_name = response.headers
			for (i=0; i<headers.length; ++i) {
				th = $("<th>").text(verbose_name[headers[i]])
				th.data("name", headers[i])
				table_header.children("tr").append(th)
			}
		}
		// Fill the table and show
		update_table(table, response.hits)
		table.show()
	}
}

function m21(input, headers) {
	$ = django.jQuery
	var tgt = $('select[name='+input+']')
	var table = $('<table>')
	tgt.parents("div.form-row").after(table)
	var search_url = $("#change_id_"+input).data("href-template")
	search_url = search_url.split("__fk__")[0] + "search"

	build_search_widget(tgt, table, headers, search_url)
}

function fkd(target, sources) {
	var info = $('div[class~=field-'+target+'] div p')
	var tpl = info.html()
	info.html("")
	var tokens = []
	var data = {}
	var re = /{{(.*?)}}/mg
	while (match = re.exec(tpl)) {
		var tok = match[1].trim().split(".")
		if (sources.indexOf(tok[0]) == -1) {
			console.warn(tok[0], "is missing from sources")
			continue
		}
		tokens.push(tok)
	}
	for (var i=0; i<sources.length; ++i) {
		// closure, so i is pinned
		(function(i) {
			var select = $('select[name='+sources[i]+']')
			var get_url = $("#change_id_"+sources[i]).data("href-template")
			get_url = get_url.split("__fk__")[0] + "get"
			select.on("change", function() {
				data[sources[i]] = select.data("obj")
				info.trigger("update")
			})
			pk = select.val()
			if (!pk)
				return
			request = $.ajax(get_url, {data: {"pk": pk} })
			.done(function(response) {
				data[sources[i]] = response
				info.trigger("update")
			})
		})(i)
	}
	info.on("update", function() {
		info.html(tpl.replace(re, function(_, match) {
			var token = match.trim().split(".")
			if (data[token[0]])
				return data[token[0]][token[1]]
			return ""
		}))
	})
}

function inline_handler(table, opts, fn) {
/*
	table is the number of the inline table to work on,
	opts is the options for the function. Both come from admin.py
	fn is the function doing the actual work. Takes a row from the inline and
	a copy of opts
*/
	$ = django.jQuery
	var table = $($(".inline-group").get(parseInt(table, 10)))
	var id = table.find("tbody tr").first().attr("id")
	id = id.substring(0, id.length-2)
	if (table.data("inline-type") != "tabular") { console.log("#TODO") }

	rows = table.find("fieldset table tr.form-row:not(.empty-form)")
	rows.map(function(idx, row) { fn(row, opts.slice()) })
	$(document).on('formset:added', function(evt, row, prefix) {
		if (prefix != id)
			return
		fn(row, opts.slice(), "add")
	})
}

function inline_math_op(table, opts, op) {
	function do_math(item, opts) {
		target = opts.shift()
		src = opts.map(function(elmt) {
			input = $(item).children('.field-'+elmt).find('input').get(0)
			if (!input) return parseFloat(elmt)
			else return input
		})
		tgt = $(item).children('.field-'+target).children('input')
		for (i=0; i<src.length; ++i) {
			$(src[i]).blur(update_math_op(tgt, src, op))
		}
	}
	return inline_handler(table, opts, do_math)
}

function ilnsum(input, source) {
	return inline_math_op(input, source, "plus")
}
function ilnsub(input, source) {
	return inline_math_op(input, source, "minus")
}
function ilnmul(input, source) {
	return inline_math_op(input, source, "multiply")
}
function ilndiv(input, source) {
	return inline_math_op(input, source, "divide")
}

function ilnpif(table, opts) {
	function pull_info(item, opts) {
		function update(tgt, val) {
			/* Fetch the data */
			var get_url = $("#change_"+tgt[0].id).data("href-template")
			get_url = get_url.split("__fk__")[0] + "get"
			request = $.ajax(get_url, {data: {"pk": val} })
			.done(function(obj) {
				/* Gather key and destination */
				keys = opts
				if (opts.length == 0) {
					obj_k = Object.keys(obj)
					for (i in obj_k)
						keys.push(obj_k[i], '%')
				}
				/* Update the inputs */
				for (i=0; i<keys.length; i+=2) {
					src = keys[i]
					dst = (keys[i+1] == '%') ? keys[i] : keys[i+1]
					input = $(item).children('.field-'+dst)
					if (input.length == 0)
						continue
					input = input.children('input')
					input.val(obj[src].substr(0, input.attr('maxlength')||99))
				}
			})
		}
		/* Setup event listener */
		source = opts.shift()
		tgt = $(item).children('.field-'+source).find('select, input').first()
		tgt.change(function(evt) { update(tgt, evt.target.value) })
	}
	return inline_handler(table, opts, pull_info)
}

function ilnm21(table, opts) {
	function upgrade_select(item, opts) {
		var select = $(item).find('select[name$="'+opts.shift()+'"]')
		var table = $("<table>")
		$(item).after($("<tr>").append($("<td colspan=99>").append(table)))
		var search_url = $("#change_"+tgt[0].id).data("href-template")
		search_url = search_url.split("__fk__")[0] + "search"

		build_search_widget(select, table, opts, search_url)
	}
	return inline_handler(table, opts, upgrade_select)
}

function ilnext(table, opts) {
	var src = $('input[name="'+opts.shift()+'"]')
	function pull_external(item, opts, add) {
		if (add != "add")
			return
		var tgt = $(item).find('.field-'+opts.shift()+" input").first()
		tgt.val(src.val())
	}
	return inline_handler(table, opts, pull_external)
}
