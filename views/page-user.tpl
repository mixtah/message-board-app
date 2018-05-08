%rebase("base-page")
%import Topics,Messages
%import random
%setdefault('username','')
%setdefault('topics',Topics.getFiltered({'username':username}))
%lorumCatagory = ['people','animals','cats','nightlife','technics','food','transport']
<div class="row">
	<img class="col-md-3 col-md-offset-3 img-responsive" style="display: block;margin: auto;" src="https://loremflickr.com/400/400/{{random.choice(lorumCatagory)}}/?lock={{random.randint(0,100)}}">
	<div class="col-md-3">
		<h3 style="color:#656565;text-align: center;">{{username}}</h3>
		<h3 style="color:#656565;text-align: center;">Number of Topics: {{Topics.getCount({'username':username})}}</h3>
		<h3 style="color:#656565;text-align: center;">Number of Messages: {{Messages.getCount({'username':username})}}</h3>
	</div>
</div>
<br>
<div class="row">
	<div class="col-md-12">
		%include('topic-list',topics=topics)
	</div>
</div>