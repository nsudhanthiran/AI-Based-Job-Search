from django.db import models

# Create your models here.
class FilesUpload(models.Model):
    file = models.FileField()

class JobApplication(models.Model):
    job_type = models.CharField(max_length=100)
    work_preference = models.CharField(max_length=100)
    resume = models.CharField(max_length=100)  # Assuming resume is a file path/name
    additional_info = models.TextField()
    
    
    def __str__(self):
        data = {'job_name' : 'engineer',
                'job_type' : 'job',
                'work_preference' : 'onsite',
                'company_name' : 'nvdia',
                'comp_desc' : 'best company ever in the world',
                'apply_link' : 'www.google.com'}
        
        
        return data