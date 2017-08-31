%rebase("base-page")
%import Topics
%import random
%setdefault('username','')
%setdefault('topics',Topics.getFiltered({'username':username}))
%lorumCatagory = ['people','animals','cats','nightlife','technics','food','transport']
<div class="row">
	<div class="col-md-3">
		<img class="col-md-3 img-responsive" style="display: block;margin: auto;" src="http://lorempixel.com/400/400/{{random.choice()}}/{{random.randint(0,10)}}">
	</div>
	<div class="col-md-9">
		<h3 style="color:#656565;text-align: center;">{{username}}</h3>
	</div>
</div>
<div class="row">
	<div class="col-md-12">
		%include('topic-list',topics=topics)
	</div>
</div>