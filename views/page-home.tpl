%rebase("base-page")
%import Topics
%setdefault('topics',None)
<div class="row">
	<div class="col-md-10 col-md-offset-1">
		<div class="panel-group" id="accordion">
			<div class="panel panel-default">
				<div class="panel-heading">
					<h4 class="panel-title" data-toggle="collapse" data-parent="#accordion" href="#collapse1">
						Click to Add a New Topic
					</h4>
				</div>
				<div id="collapse1" class="panel-collapse collapse">
					<div class="panel-body">
						%include('topic-add')
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
%if topics:
<div class="row">
	<div class="col-md-12">
		%include('topic-list',topics=topics)
	</div>
</div>
%end

