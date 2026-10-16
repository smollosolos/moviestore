from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render

from .decorators import staff_member_required


@staff_member_required
def manage(request):
    return engagement(request)


@staff_member_required
def engagement(request):
    users = User.objects.annotate(comment_count=Count('review')).order_by('-comment_count', 'username')
    top_commenter = users.filter(comment_count__gt=0).first()

    return render(request, 'accounts/manage_engagment.html', {
        'template_data': {
            'title': 'User Engagement',
            'users': users,
            'top_commenter': top_commenter,
        },
    })