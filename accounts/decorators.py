
from functools import partial
from django.contrib.admin.views.decorators import staff_member_required
staff_member_required = partial(staff_member_required, login_url='accounts.login')