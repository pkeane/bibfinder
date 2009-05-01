BF = {};


$(document).ready(function() {
	BF.initDelete();
	BF.initHello();
});

BF.initHello = function() {
	alert('hello');
};

BF.initDelete = function() {
	$('#todos').find("a[class='delete']").click(function() {
		if (confirm('are you sure?')) {
			var del_o = {
				'url': $(this).attr('href'),
				'type':'DELETE',
			'complete': function() { location.reload(); },
			};
			$.ajax(del_o);
		}
		return false;
	});
};
