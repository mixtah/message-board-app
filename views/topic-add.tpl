<form class="form" action="/topic/add" method="POST">
	<table class="table" style="width:100%;">
		<thead><th colspan="2"><h4>Add Your own Topic</h4></th></thead>
		<tbody>
			<tr>
				<td>
					<b>Username:</b>
				</td>
				<td>
					<input class="form-control" type="text" name="username" required>
				</td>
			</tr>
			<tr>
				<td>
					<b>Subject:</b>
				</td>
				<td>
					<input class="form-control" type="text" name="subject" required>
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
					<button type="submit" style="float:right;"class="btn btn-default">Add Topic</button>
				</td>
			</tr>
		</tbody>
	</table>
</form>