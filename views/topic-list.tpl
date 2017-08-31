%setdefault('topics',None)
%if topics:
%import random
%import datetime
<div class="list-group">
%for topic in topics:
<a class="list-group-item" href="/topic/{{topic.id}}">
	<div class="row">
		%random.seed(topic.username+'topic'+str(topic.id))
		%lorumCatagory = ['people','animals','cats','nightlife','technics','food','transport']
		<img class="col-md-3 img-responsive" style="display: block;margin: auto;max-width:250px;" src="http://lorempixel.com/400/400/{{random.choice()}}/{{random.randint(0,10)}}">
		<div class="col-md-9">
			<table style="width:100%;">
				<tr>
					<td colspan="3">
						<h3 style="text-align: center;">{{topic.subject}}</h3>
					</td>
				</tr>	
				<tr>
					<td>
						<p style="color:#656565;text-align: center;"><i class="fa fa-user"></i> {{topic.username}}</p>
					</td>
					<td>
						<p style="color:#656565;text-align: center;"><i class="fa fa-clock-o"></i> {{datetime.datetime.strptime(topic.timestamp, '%Y-%m-%d %H:%M:%S').strftime('%A, %d %B %Y')}}</p>
					</td>
					<td>
						<p style="color:#656565;text-align: center;">
							<span class="label label-success"> {{topic.likes}} Likes</span>
							<span class="label label-danger"> {{topic.dislikes}} Dislikes</span>
						</p>
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