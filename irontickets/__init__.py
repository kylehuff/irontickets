from django.db.models.signals import pre_save, post_save
from irontickets.signals import ticket_pre_save, ticket_post_save, comment_post_save
from irontickets.models import Ticket
from django.contrib.comments.models import Comment

pre_save.connect(ticket_pre_save, sender=Ticket)
post_save.connect(ticket_post_save, sender=Ticket)
post_save.connect(comment_post_save, sender=Comment)

