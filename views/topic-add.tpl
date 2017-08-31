<form class="form" action="/topic/add" method="POST">
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
				<td>
					<b>Subject:</b>
				</td>
				<td>
					<input class="form-control" type="text" name="subject">
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
					% include('summernote',name='topicadd',attr='description')
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
</form>