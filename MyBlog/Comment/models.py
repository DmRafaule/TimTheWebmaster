from django.db import models


class Comment(models.Model):
    type = models.ForeignKey("Post.Post", on_delete=models.CASCADE, blank=False)
    user = models.ForeignKey("User.User", on_delete=models.CASCADE, blank=True, null=True)
    replies = models.ManyToManyField("Comment", blank=True)
    anonymous_user_name = models.CharField(max_length=100, blank=True, null=True)
    anonymous_user_id = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=False)
    timeCreated = models.DateTimeField(auto_now_add=True)
