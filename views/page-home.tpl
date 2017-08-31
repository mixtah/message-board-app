%rebase("base-page")
%import Topics
%setdefault('topics',Topics.getAll())
<div class="row">
	<div class="col-md-12">
		%include('topic-list',topics=topics)
	</div>
</div>
<div class="row">
	<div class="col-md-8 col-md-offset-2">
		%include('topic-add')
	</div>
</div>