from django.db import models


class Text(models.Model):
    original_text = models.TextField()
    corrected_text = models.TextField()
    labeled_text = models.TextField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class GeneralFeedback(models.Model):
    website_feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
