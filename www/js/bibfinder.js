BF = {};


$(document).ready(function() {
	BF.initDelete();
	BF.initGetTitles();
});

BF.initGetTitles = function() {
	$('#user_lists').find("a[class='titles_link']").click(function() {
		var target = $(this).parent().find("ul");
		$.getJSON($(this).attr('href'),function(data) {
			target.html();
			$.each(data,function(i){
				target.append('<li>'+data[i].title+' <a href="'+data[i].guid+'">get data</a></li>');
			});
		});
		return false;
	});
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
