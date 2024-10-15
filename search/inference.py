from transformers import AutoModelForCausalLM, AutoTokenizer,pipeline, AutoModelForSeq2SeqLM, TextStreamer
import torch
import ast
from bs4 import BeautifulSoup
import requests
import json
from tqdm import tqdm






# validator_path = "casperhansen/mixtral-instruct-awq"

# # model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype="auto").cuda()

# validator = AutoModelForCausalLM.from_pretrained(
#     validator_path,
#     low_cpu_mem_usage=True,
#     device_map="auto"
# )

# tokenizer = AutoTokenizer.from_pretrained(validator_path)

# val_streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

# generation_params = {
#     "do_sample": True,
#     "temperature": 0.7,
#     "top_p": 0.95,
#     "top_k": 40,
#     "max_new_tokens": 1000,
#     "repetition_penalty": 1.1
# }

# validator_pipe = pipeline(
#     "text-generation",
#     model=validator,
#     tokenizer=tokenizer,
#     streamer=val_streamer,
#     **generation_params
# )



def generate_tag(pipe,resume):

    prompt = f""" <s> [INST]

    You're an LLM who's role is to read the content of the resume, and provide job titles related to their resume that you can generate from that. Eg. [Machine Learning Engineer, Software development Engineer, Backend Engineer] which can be used as filters for job-hunting. Your response should strictly follow the syntax of a python list.


    Resume_content: {resume} [/INST]

    """



    # print("Generating response...")
    output = pipe(prompt)[0]["generated_text"]

    response_index = output.find("/INST]")

    response = output[response_index+6:]

    print(response)
    return response


def validate_jobs(pipe,resume,jobs_json,preferences):


    output_format = {"jobs":[
     
              {
                "title": "Job Title",
                "company": "Company name",
                "location": "Location",
                "application_link": "The link that is parsed."
            },
     
    ]}

#     prompt = f"""<s>[INST]

#     You're an LLM who's role is to recieve a list of available jobs, a list of preferences and a resume as input, and your output will be a JSON RESPONSE of the top 10 most relevant jobs among the given jobs and should contain absolutely no texts other than that, based on the contents of the resume and user's preferences. The output should strictly follow the given output format:

#     Resume_content: {resume}, available jobs: {jobs_json}, preferences: {preferences} 
    
#     Output Format: {output_format}

    
#     [/INST]

# """
    
    prompt = f"""<s>[INST]

    You're an LLM who's role is to recieve a list of available jobs, a list of preferences and a resume as input, and your output will be a JSON RESPONSE of the top 10 most relevant jobs among the given jobs and should contain absolutely no texts other than that, based on the contents of the resume and user's preferences. The output should strictly follow the same format as the input json.

    Resume_content: {resume}, jobs: {jobs_json}, preferences: {preferences} [/INST]

"""


    output = pipe(prompt)[0]["generated_text"]

    return output
    

def get_linkedin(url):

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # with open("parsed_linkedin.txt","w") as file:
    #     file.write(response.text)

    # Find all job cards
    job_cards = soup.find_all("div", class_="base-search-card__info")

    # List to store all job details
    all_job_details = []

    # Iterate over each job card
    for card in job_cards:
        # Find the job details
        job_title = card.find("h3", class_="base-search-card__title").text.strip()
        # print(f"job_title: {job_title}")
        try:
            company_name = card.find("a", class_="hidden-nested-link").text.strip()
        except:
            company_name="Unavailable"
        location = card.find("span", class_="job-search-card__location").text.strip()
        salary_info = card.find("span", class_="job-search-card__salary-info")

        if salary_info:
            salary_info = salary_info.text.strip()
        else:
            salary_info="Salary Info not available"
        try:
            apply_link = card.find("a", class_="hidden-nested-link")["href"]
        except:
            apply_link="unavailable"
        

        # Create a dictionary to store the data for this job
        job_details = {
            "job_title": job_title,
            "company_name": company_name,
            "location": location,
            "salary_info": salary_info,
            "Link":apply_link
        }

        # Append the job details to the list
        all_job_details.append(job_details)

    return all_job_details

def create_search_querries(tags:str):

    tags = tags.replace('\n','')
    
    tags_list = ast.literal_eval(tags)


    jobs = []

    for tag in tags_list[:5]:

        linkedin_keywords = '%20'+tag.replace(' ','%20')


        linkedin_query = f"https://www.linkedin.com/jobs/search?keywords={linkedin_keywords}&location=US&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum={0}"

        # indeed_keywords = '+'.join(tag.split())

        # indeed_query = f"https://in.indeed.com/jobs?q={keywords}&l=&from=searchOnHP"

        # print(indeed_query)

        jobs.append(get_linkedin(linkedin_query))

    internshala_keywords = ''
    for tag in tags_list:
        internshala_keywords+=tag.replace(' ','-')+','

    internshala_keywords= internshala_keywords[:-1]

    # print(internshala_keywords)

    internshala_search_query = f"https://internshala.com/internships/{internshala_keywords}-internship"


    jobs.append(get_internshala(internshala_search_query))

    # with open("final.txt","w") as file:
    #     file.write(str(jobs))
        

    return jobs


def get_internshala(url):

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all internship containers
    internship_containers = soup.find_all("div", class_="internship_meta")

    # List to store all internship details
    all_internship_details = []

    # Iterate over each internship container
    for container in internship_containers:
        # Find the internship details
        internship_name = container.find("h3", class_="heading_4_5 profile").text.strip()
        company_name = container.find("a", class_="link_display_like_text view_detail_button").text.strip()
        location = container.find("a", class_="location_link view_detail_button").text.strip()
        start_date = container.find("div", class_="item_body").text.strip()
        duration = container.find_all("div", class_="item_body")[1].text.strip()
        stipend = container.find("span", class_="stipend").text.strip()
        applying_link = f"""https://internshala.com{soup.find("a", class_="view_detail_button")['href']}"""

        # Create a dictionary to store the data for this internship
        internship_details = {
            "Internship Name": internship_name,
            "Company Name": company_name,
            "Location": location,
            "Start Date": start_date,
            "Duration": duration,
            "Stipend": stipend,
            "Applying Link": applying_link
        }

        # Append the internship details to the list
        all_internship_details.append(internship_details)

    return all_internship_details


def get_results(resume_content,preferences):


    tag_generator_path = "TheBloke/Mistral-7B-Instruct-v0.2-AWQ"

    # model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype="auto").cuda()

    tag_generator = AutoModelForCausalLM.from_pretrained(
        tag_generator_path,
        low_cpu_mem_usage=True,
        device_map="auto"
    )

    tokenizer = AutoTokenizer.from_pretrained(tag_generator_path)

    tag_streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

    generation_params = {
        "do_sample": True,
        "temperature": 0.1,
        "top_p": 0.95,
        "top_k": 40,
        "max_new_tokens": 2048,
        "repetition_penalty": 1.1
    }

    tag_pipe = pipeline(
        "text-generation",
        model=tag_generator,
        tokenizer=tokenizer,
        # streamer=tag_streamer,
        **generation_params
    )


    jobs = (create_search_querries(generate_tag(tag_pipe,resume_content)))

    # with open('parsed_jobs.txt','w') as file:
    #     file.write(str(jobs))
        

    # print(len(jobs))
    # split_ratio = len(jobs)//6

    # job_splits = []

    # for i in range(0, len(jobs), split_ratio):
    #     job_splits.append(jobs[i:i+split_ratio])

    # print(len(job_splits))

    # validated = ""

    # for split in tqdm(job_splits):

    #     validated += validate_jobs(pipe=tag_pipe,resume=resume_content,jobs_json=split,preferences=preferences)

    # print(validated)

    jobs_list = []

    for i in jobs:
        if len(i)>1:
            for j in i:
                jobs_list.append(j)


    return jobs_list