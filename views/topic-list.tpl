%setdefault('topics',None)
%if topics:
%import random
%import datetime
%import Messages
<div class="list-group">
%for topic in topics:
<a class="list-group-item" href="/topic/{{topic.id}}">
	<div class="row">
		%random.seed(topic.username+'topic'+str(topic.id))
		%lorumCatagory = ['people','animals','cats','nightlife','technics','food','transport']
		<img class="col-md-3 img-responsive" style="display: block;margin: auto;max-width:400px;" src="http://lorempixel.com/400/200/{{random.choice(lorumCatagory)}}/{{random.randint(0,10)}}">
		<div class="col-md-9">
			<table style="width:100%;">
				<tr>
					<td colspan="3">
						<h2 style="text-align: center;">{{topic.subject}}</h2>
					</td>
				</tr>	
				<tr>
					<td>
						<a href="/user/{{topic.username}}"><h3 style="color:#656565;text-align: center;"><i class="fa fa-user"></i> {{topic.username}}</h3></a>
					</td>
					<td>
						<h4 style="color:#656565;text-align: center;"><i class="fa fa-clock-o"></i> {{datetime.datetime.strptime(topic.timestamp, '%Y-%m-%d %H:%M:%S').strftime('%A, %d %B %Y')}}</h4>
					</td>
					<td>
						<h4 style="color:#656565;text-align: center;">
							<span class="label label-default"> {{Messages.getCount({'topic':topic.id})}} Replies</span>
							<span class="label label-success"> {{topic.likes}} Likes</span>
							<span class="label label-danger"> {{topic.dislikes}} Dislikes</span>
						</h4>
					</td>
				</tr>
			</table>
		</div>
	</div>
</a>
%end
%end
</div>
%end