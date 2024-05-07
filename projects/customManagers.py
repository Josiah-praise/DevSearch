from django.db.models import Manager, Q

class ProjectFilter(Manager):
    def search(self, q_string=''):
        query_set = super().filter(
            Q(title__icontains=q_string) |
            Q(description__icontains=q_string) |
            Q(owner__first_name__icontains=q_string) |
            Q(owner__last_name__icontains=q_string) |
            Q(tags__name__icontains=q_string)
        ).distinct()
        return query_set
