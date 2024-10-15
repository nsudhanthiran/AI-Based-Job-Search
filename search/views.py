from django.shortcuts import render
from django.http import HttpResponse

from .models import FilesUpload, JobApplication
# import shutil
from PyPDF2 import PdfReader
from .inference import *
# Create your views here.


def JobApplication(data):
    [job_type, work_preference, resume, additional_info ] = data
    
    job_application_instance = []
    
    instance = {'job_name' : 'engineer',
            'job_type' : 'job',
            'work_preference' : 'onsite',
            'company_name' : 'nvdia',
            'comp_desc' : 'best company ever in the world',
            'apply_link' : 'www.google.com'}
    
    job_application_instance.append(instance)
    
    return job_application_instance


def credentials(request):
    return render(request, 'credentials.html')

def get_pdf_text(pdf):
    text = ""
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def results(request):   

    results_parsed = False

    if results_parsed:

        job_type = request.POST.get('job_type')
        work_preference = request.POST.get('work_preference')
        resume = request.FILES['resume']
        document = FilesUpload.objects.create(file = resume)
        document.save()
        
        
        resume_text = get_pdf_text(f"/home/tejasram/CS_projects0/LlaMaHunt/llamahunt/media/{resume.name}")
        # print(resume_text)
        additional_info = request.POST.get('additional_info')
        data = {'job_type':job_type,
            'work_preference':work_preference,
            'additional_info':additional_info
        }
        print(data)
        # print(**data)
        
        # job_application_instance = JobApplication(**data)
        
        # print(job_application_instance)
        
        job_application_instance = get_results(resume_content=resume_text, preferences=data)

        # print(job_application_instance)
        
        return render(request, 'results.html', {'data' : job_application_instance})
    
    return render(request,"waiting.html")
