// disable dragover (to prevent DL)
$(function () {
	$(document).on('drop dragover', function (e) {
		e.stopPropagation();
		e.preventDefault();
	});
});
