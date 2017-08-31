%import Topics
%setdefault('parent',None)
%if parent:
<form class="form" action="/message/add" method="POST">
	<table class="table table-striped" style="width:100%;">
		<thead><th colspan="2"></th></thead>
		<tbody>
			<tr>
				<td>
					<b>Username:</b>
				</td>
				<td>
					<input class="form-control" type="text" name="username">
				</td>
			</tr>
			<tr>
				<td colspan="2">
					<b>Message:</b>
				</td>
				<td>
				</td>
			</tr>
			<tr>
				<td colspan="2">
					%extra = 'topic'+str(parent.id) if isinstance(parent,Topics.Topic) else 'msg'+str(parent.id)
					% include('summernote',name='commentadd'+extra,attr='message')
				</td>
			</tr>
			<tr>
				<td>
					
				</td>
				<td>
					<button type="submit" style="float:right;"class="btn btn-default">Add Comment</button>
				</td>
			</tr>
		</tbody>
	</table>
	%if isinstance(parent,Topics.Topic):
		<input class="form-control" type="hidden" name="topic" value="{{parent.id}}">
	%else:
		%topic = parent.getTopic()
		%if topic:
			<input class="form-control" type="hidden" name="topic" value="{{topic.id}}">
		%end
		<input class="form-control" type="hidden" name="reply_to" value="{{parent.id}}">
	%end
</form>
%end