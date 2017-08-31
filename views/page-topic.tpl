%rebase("base-page")
%setdefault('topic',None)
%if topic:
%import random
%import datetime
%lorumCatagory = ['people','animals','cats','nightlife','technics','food','transport']
<div class="row">
	%random.seed(topic.username+'topic'+str(topic.id))
	<img class="col-md-3 img-responsive" style="display: block;margin: auto;" src="http://lorempixel.com/400/400/{{random.choice(lorumCatagory)}}/{{random.randint(0,10)}}">
	<div class="col-md-9">
		<table style="width:100%;">
			<tr>
				<td colspan="2">
					<h1 style="text-align: center;">{{topic.subject}}</h1>
				</td>
			</tr>	
			<tr>
				<td>
					<a href="/user/{{topic.username}}"><h4 style="color:#656565;text-align: center;"><i class="fa fa-user"></i> {{topic.username}}</h4></a>
				</td>
				<td>
					<h4 style="color:#656565;text-align: center;"><i class="fa fa-clock-o"></i> {{datetime.datetime.strptime(topic.timestamp, '%Y-%m-%d %H:%M:%S').strftime('%A, %d %B %Y')}}</h4>
				</td>
				<td>
					<h4 style="color:#656565;text-align: center;">
						<a href="/topic/{{topic.id}}/like" class="btn btn-success btn-sm"><i class="fa fa-thumbs-o-up"></i> Like <span class="badge">{{topic.likes}}</span></a>
		                <a href="/topic/{{topic.id}}/dislike" class="btn btn-danger btn-sm"><i class="fa fa-thumbs-o-down"></i> Dislike <span class="badge">{{topic.dislikes}}</span></a>
		                <a data-toggle="modal" data-target="#replyTopic" class="btn btn-default btn-sm"><i class="fa fa-reply"></i> Reply</a>
					</h4>
				</td>
			</tr>
		</table>
	</div>
</div>
<div class="row">
	<div class="col-md-12">
		{{!topic.description}}
	</div>
</div>
<div class="row">
	<div class="col-md-12">
		<section class="comment-list">
			%messages = topic.getMessages()
			%if messages:
				%for message in messages:
					<article class="row">
			            <div class="col-md-2 col-sm-2 hidden-xs">
			              <figure class="thumbnail">
			              	%random.seed(message.username)
			                <img class="img-responsive" src="http://lorempixel.com/400/400/{{random.choice(lorumCatagory)}}/{{random.randint(0,10)}}" />
			                <figcaption class="text-center">{{message.username}}</figcaption>
			              </figure>
			            </div>
			            <div class="col-md-10 col-sm-10">
			              <div class="panel panel-default arrow left">
			                <div class="panel-body">
			                  <header class="text-left">
			                    <div class="comment-user"><i class="fa fa-user"></i><a href="/user/{{message.username}}"> {{message.username}}</a></div>
			                    <time class="comment-date" datetime="16-12-2014 01:05"><i class="fa fa-clock-o"></i> {{datetime.datetime.strptime(message.timestamp, '%Y-%m-%d %H:%M:%S').strftime('%A, %d %B %Y')}}</time>
			                  </header>
			                  <div class="comment-post">
			                    <p>
			                    	{{!message.message}}
			                    </p>
			                  </div>
			                  <p class="text-right">
			                  	<a href="/message/{{message.id}}/like" class="btn btn-success btn-sm"><i class="fa fa-thumbs-o-up"></i> Like <span class="badge">{{message.likes}}</span></a>
			                 	<a href="/message/{{message.id}}/dislike" class="btn btn-danger btn-sm"><i class="fa fa-thumbs-o-down"></i> Dislike <span class="badge">{{message.dislikes}}</span></a>
			                 	<a data-toggle="modal" data-target="#replyComment{{message.id}}" class="btn btn-default btn-sm"><i class="fa fa-reply"></i> Reply</a>
			                  </p>
			                </div>
			              </div>
			            </div>
			            <div class="modal fade" id="replyComment{{message.id}}" role="dialog">
							<div class="modal-dialog modal-lg">
								<div class="modal-content">
									<div class="modal-header">
										<button type="button" class="close" data-dismiss="modal">&times;</button>
										<h4 class="modal-title">Add Reply</h4>
									</div>
									<div class="modal-body">
										%include('comment-add',parent=message)
									</div>
									<div class="modal-footer">
									</div>
								</div>
							</div>
						</div>
			        </article>
			        %replies = message.getMessages()
			        %if replies:
			        	<article class="row">
				            <div class="col-md-2 col-sm-2 col-md-offset-1 col-sm-offset-0 hidden-xs">
				              <figure class="thumbnail">
				              	%random.seed(reply.username)
				                <img class="img-responsive" src="http://lorempixel.com/400/400/{{random.choice(lorumCatagory)}}/{{random.randint(0,10)}}" />
				                <figcaption class="text-center">{{reply.username}}</figcaption>
				              </figure>
				            </div>
				            <div class="col-md-9 col-sm-9">
				              <div class="panel panel-default arrow left">
				                <div class="panel-heading right">Reply</div>
				                <div class="panel-body">
				                  <header class="text-left">
				                    <div class="comment-user"><i class="fa fa-user"></i><a href="/user/{{message.username}}"> {{reply.username}}</a></div>
				                    <time class="comment-date" datetime="16-12-2014 01:05"><i class="fa fa-clock-o"></i> {{datetime.datetime.strptime(reply.timestamp, '%Y-%m-%d %H:%M:%S').strftime('%A, %d %B %Y')}}</time>
				                  </header>
				                  <div class="comment-post">
				                    <p>
				                    	{{!reply.message}}
				                    </p>
				                  </div>
				                  <p class="text-right">
				                  	<a href="/message/{{reply.id}}/like" class="btn btn-success btn-sm"><i class="fa fa-thumbs-o-up"></i> Like <span class="badge">{{message.likes}}</span></a>
				                 	<a href="/message/{{reply.id}}/dislike" class="btn btn-danger btn-sm"><i class="fa fa-thumbs-o-down"></i> Dislike <span class="badge">{{message.dislikes}}</span></a>
				                  </p>
				                </div>
				              </div>
				            </div>
				        </article>
			        %end
			    %end
			%end
		</section>
	</div>
</div>
<div class="modal fade" id="replyTopic" role="dialog">
	<div class="modal-dialog modal-lg">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal">&times;</button>
				<h4 class="modal-title">Add Comment</h4>
			</div>
			<div class="modal-body">
				%include('comment-add',parent=topic)
			</div>
			<div class="modal-footer">
			</div>
		</div>
	</div>
</div>
%end