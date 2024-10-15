# Llama Hunt

Llama Hunt is a web application designed to streamline the job search process by utilizing cutting-edge language models (LLMs) to find relevant job openings tailored to the user's resume and preferences.


## Features

- **One-Stop Platform**: Llama Hunt serves as a comprehensive platform where users can access job openings from multiple sources like LinkedIn, Indeed, and Glassdoor etc... all in one place.
- **Time Conservation**: By automating the job search process and consolidating information from various sources, Llama Hunt saves users valuable time that would otherwise be spent searching multiple websites individually.
- **Attractive UI**: The user interface of Llama Hunt is designed to be intuitive and visually appealing, providing a seamless experience for users navigating through job listings and preferences.


## How It Works

   ### Input:
   <img src="https://ik.imagekit.io/tejasram/LlamaHunt/input?updatedAt=1709960291021" style="{justify-content: center; align-items: center;}" width=70%>

   <br>
   <br>


1. **Upload Resume**: Users upload their resumes and provide additional preferences as text.
2. **Keyword Generation**: Mistral 7b Instruct generates keywords for job searches.
3. **Job Fetching**: Open job positions are fetched from various websites using the generated keywords.
4. **Filtering**: Mixtral 8x7b Instruct filters the fetched jobs based on user preferences.
5. **Presentation**: The most suitable jobs are displayed to the user for easy application.

<br>

   ### Output:
   <img src="https://ik.imagekit.io/tejasram/LlamaHunt/output?updatedAt=1709971656071" style="{justify-content: center; align-items: center;}" width=70%>
   
## Usage

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/llama-hunt.git
   ```

2. Creating a virtual environment:

    ```
    python3 -m venv <name_of_your_virtual_environment>
    ```

3. Activating the virtual environment:
<br>

    For macOS/Linux:
   
    ```
    source <path_to_virtual_environment>/bin/activate
    ```

    For Windows:
   
    ```
    <path_to_virtual_environment>\Scripts\activate
    ```

5. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

6. Run the Django server:

   ```
   python manage.py runserver
   ```

7. Access the application via the provided URL.

## Technologies Used

- Backend: Django
- Frontend: HTML, CSS, JavaScript (with Bootstrap)
- Language Models: Hugging Face Transformers Library
- Acceleration Library: Intel Acceleration Library and AutoAWQ
- Deployment: Intel DevCloud

## Advantages of Migrating to OneAPI

-  Availability of High Computing Services
-  Good Developer Support
-  Seamless Interface

## Intel OneAPI vs AWS Inference Speed Comparison

![image](https://github.com/nsudhanthiran/LlamaHunt/assets/118297543/116bb402-e630-4f21-bbcc-9f01f57f363a)



## Utilizing Intel OneAPI pytorch Acceleration

To utilize Intel's acceleration, we're using a library <code>intel_extension_for_pytorch</code> 

```
import intel_extension_for_pytorch as ipex

optimized_tag_generator = ipex.optimize(tag_generator, dtype=torch.bfloat16)
```

![intel_acceleration_comparison](https://github.com/nsudhanthiran/LlamaHunt/assets/118297543/87d62f5a-8945-4782-b2b2-ecdbe752900c)


And as it can be observed, both the models performed observably better with Intel's acceleration library.

## Acknowledgments

- Special thanks to Intel DevCloud for providing resources for efficient scaling and performance.
- Inspired by the need to streamline the job search process for job seekers.

## Future Scopes

- Using LLMs for the application process
- Integrating larger sources for openings
- Implementing Spam Detection


## Contact

For any inquiries or feedback, please contact nsudhanthiran2003@gmail.com
