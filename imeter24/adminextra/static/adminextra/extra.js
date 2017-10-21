var $ = django.jQuery
$(function() {
	var inputs = $('input[type="number"]')

	inputs.on("update", function() {
		var input = $(this)
		var value = parseFloat(input.val())
		var step = input.attr("step")
		if (!value)
			return
		if (step && step.indexOf(".") != -1) {
			precision = step.split(".")[1].length
			input.val(value.toFixed(precision))
		}
	})

	inputs.blur(function() { $(this).trigger("update") })
	inputs.trigger("update")
})
