from .forms import EmailPostForm, CommentForm
from django.shortcuts import get_object_or_404, render
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail



def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

    
    def post_list(request):
    # Create your views here.def post_list(request):
        object_list = Post.published.all()
        paginator = Paginator(object_list, 3) # 3 posts in each page
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            posts = paginator.page(2)
        except EmptyPage:
            # If page is out of range deliver last page of results
            posts = paginator.page(paginator.num_pages)
        return render(request,
                    'blog/post/list.html',
                    {'page': page,
                    'posts': posts})

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title} by {post.author}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'gloti3483@gmail.com', [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                    status = 'published',publish__year= year, publish__month=month, publish__day=day)


    comments =post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        #a COMMENT WAS POSTED
        comment_form = CommentForm(data =request.POST)
        if comment_form.is_valid():
            #Create comment object but dont save it on the database
            new_comment = comment_form.save(commit=False)
            new_comment.post = post

            #save to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post,  'comments': comments, 'new_comment': new_comment, 'comment_form':comment_form})
    