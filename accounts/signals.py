from django.db.models.signals import post_save
from .models import CustomUser, Profile
from django.dispatch import receiver



@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Application)
def send_application_notification(sender, instance, created, **kwargs):
    if created:
        job = instance.job
        employer_email = job.employer.email  # Adjust this according to your model structure
        subject = f"New Application for {job.title}"
        message = f"A new application has been submitted for the job '{job.title}'."
        from_email = settings.DEFAULT_FROM_EMAIL  # Set your default sending email

        send_mail(subject, message, from_email, [employer_email])