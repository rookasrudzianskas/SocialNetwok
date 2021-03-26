from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import BlogPost
from .forms import BlogPostModelFrom
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.http import Http404


#
#
# def blog_post_detail_page(request, slug):
#     print(request.method, request.path, request.user)
#     # queryset = BlogPost.objects.filter(slug=slug)
#     # if queryset.count() == 0:
#     #     raise Http404
#     #
#     # obj = queryset.first()
#
#     obj = get_object_or_404(BlogPost, slug=slug)
#     template_name = 'blog_post_detail.html'
#     context = {"object": obj}
#     return render(request, template_name, context)


# CRUD create, retrieve, update, delete,

def blog_post_list_view(request):


    qs = BlogPost.objects.all().published()
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        qs = (qs | my_qs).distinct()
    template_name = "blog/list.html"
    context = {'object_list': qs}
    return render(request, template_name, context)


@staff_member_required
@login_required
def blog_post_create_view(request):

    if not request.user.is_authenticated:
        return render(request, "not-a-user.html", {})
    form = BlogPostModelFrom(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.title = form.cleaned_data.get("title")
        obj.save()
        form = BlogPostModelFrom()
    template_name = "form.html"
    context = {'form': form}
    return render(request, template_name, context)


def blog_post_detail_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = "blog/detail.html"
    context = {'object': obj}
    return render(request, template_name, context)

@staff_member_required
def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelFrom(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    template_name = "form.html"
    context = {'form': form, "title": f"Update {obj.title}"}
    return render(request, template_name, context)


@staff_member_required
def blog_post_delete_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = "blog/delete.html"
    if request.method == "POST":
        obj.delete()
        return redirect("/blog")
    context = {'object': obj}
    return render(request, template_name, context)
