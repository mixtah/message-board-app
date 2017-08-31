%rebase("base-page")
%import Topics
%setdefault('topics',None)
%if topics:
<div class="row">
	<div class="col-md-12">
		%include('topic-list',topics=topics)
	</div>
</div>
%end
<div class="row">
	<div class="col-md-8 col-md-offset-2">
		%include('topic-add')
	</div>
</div>
