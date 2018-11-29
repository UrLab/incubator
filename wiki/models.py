from django.db import models
import reversion


@reversion.register()
class Article(models.Model):
    creator = models.CharField(max_length=50)
    title = models.CharField(max_length=200, default="Article")
    article = models.TextField()
    nbr_revision = models.IntegerField(default=0)

    def save():
        # Declare a revision block.
        with reversion.create_revision():

            # Save a new model instance.
            obj = Article()
            obj.save()

            # Store some meta-information.
            reversion.set_user(request.user)
            reversion.set_comment("Created revision 1")
