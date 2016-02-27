from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import Context, loader, RequestContext
from django.http import HttpResponse

from blog.models import Post
from blog.forms import PostForm

def index(request):
  latest_posts = Post.objects.all().order_by('-created_at')
  t = loader.get_template('blog/index.html')
  context_dict = {'latest_posts': latest_posts, }
  for post in latest_posts:
    post.url = post.title.replace(' ', '_')
  c = Context(context_dict)
  return HttpResponse(t.render(c))

def post(request, post_url):
  single_post = get_object_or_404(Post, title=post_url.replace('_', ' '))
  single_post.views += 1
  single_post.save()
  t = loader.get_template('blog/post.html')
  c = Context({'single_post': single_post, })
  return HttpResponse(t.render(c))

def add_post(request):
  context = RequestContext(request)
  if request.method == 'POST':
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
      form.save(commit=True)
      return redirect(index)
    else:
      print form.errors
  else:
    form = PostForm()
    return render_to_response('blog/add_post.html', {'form': form}, context)