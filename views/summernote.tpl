%setdefault('name','summernote')
%setdefault('text','')
%setdefault('attr','summernote') #eg description
%setdefault('standalone',False)
%if standalone:
%	include('summernote_head.tpl')
%end
<script>
	$(document).ready(function() {
		var text = `{{!text}}`;
		$('#{{name}}').html(text);
		$.ajax({
		  url: 'https://api.github.com/emojis',
		  async: true 
		}).then(function(data) {
		  window.emojis = Object.keys(data);
		  window.emojiUrls = data; 
		});
		$('#{{name}}').summernote({
			placeholder: 'Edit text here...',
			minHeight: 100,
			focus: true,
			hint: {
			  match: /:([\-+\w]+)$/,
			  search: function (keyword, callback) {
			    callback($.grep(emojis, function (item) {
			      return item.indexOf(keyword)  === 0;
			    }));
			  },
			  onKeyup: function(e) {
			        $("#input{{name}}").val($("#summernote").code());
			  },
			  template: function (item) {
			    var content = emojiUrls[item];
			    return '<img src="' + content + '" width="20" /> :' + item + ':';
			  },
			  content: function (item) {
			    var url = emojiUrls[item];
			    if (url) {
			      return $('<img />').attr('src', url).css('width', 20)[0];
			    }
			    return '';
			  }
			}
		});
  	});
</script>
<textarea id="{{name}}" name="{{attr}}"></textarea>