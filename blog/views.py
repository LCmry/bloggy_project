from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import Context, loader, RequestContext
from django.http import HttpResponse

from blog.models import Post
from blog.forms import PostForm

def index(request):
  latest_posts = Post.objects.all().order_by('-created_at')
  t = loader.get_template('blog/index.html')
  context_dict = {'latest_posts': latest_posts, }
  c = Context(context_dict)
  return HttpResponse(t.render(c))

def post(request, slug):
  single_post = get_object_or_404(Post, slug=slug)
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
      saved_post = form.save(commit=True)
      return redirect(post, slug=saved_post.slug)
    else:
      print(form.errors)
  else:
    form = PostForm()
    return render_to_response('blog/add_post.html', {'form': form}, context)