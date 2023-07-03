# Cyber Security Base 2023, Course Project I
The code presented here is for a website that I am permitted to used the template based on part 5 question 21 of the Cyber Security Base 2023 course https://cybersecuritybase.mooc.fi/module-2.5/1-framework offered by University of Helsinki. The project website intentionally includes five security flaws from the OWASP 2021 top ten list.

I have explained these flaws, why they are considered security risks, and provided solutions to fix all the issues in the read me file. These fixes are not implemented within the project files themselves, which makes it easier to compare and test the original code against the fixed code.

You can find the repository for this project at https://github.com/phuongnttruong/Cyber-Security-Base-2023-Course-Project-I. To use the project, download and extract the project files and then run the following command in your preferred command prompt from the project's root folder:

To start the server, execute the command 
```python manage.py runserver```. 
If the database is not functioning properly, you may need to run the following commands:

```
python manage.py makemigrations
python manage.py migrate
```
After the server is up and running, you can access the homepage by navigating to http://127.0.0.1:8000/ 

To modify or add any database tables using the Django admin interface, visit http://127.0.0.1:8000/admin/.
Username: admin
Password: admin

## Flaw 1: [A01:2021 – Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
### Flaw's Location: https://github.com/phuongnttruong/Cyber-Security-Base-2023-Course-Project-I/blob/c75cbbb81f330a03c93b5f18f34fd581356ebdde/cyber%20security%20project/src/pages/views.py#L73
Broken access control is a serious vulnerability that is frequently encountered and needs to be addressed, particularly for websites that handle sensitive or personal information. I introduced this flaw in the code by allowing anyone to access the "finish" page regardless of whether they have completed the quiz or not.

In this code, I introduce a query parameter passed in the URL. The 'passed' session variable will always be set to 1, regardless of the actual value of the 'passed' parameter. This could potentially allow unauthorized access to certain resources or functionalities that are intended to be restricted based on the value of 'passed'. This creates a broken access control vulnerability, as an attacker can manipulate the URL to access topics without the necessary privileges. To mitigate this vulnerability, proper access control checks should be implemented within the topicView function or in the surrounding code. This can involve checking the user's authentication status, role-based permissions, or any other authorization mechanism based on the application's requirements.

To fix the broken access control flaw in the code, you should update the logic to properly handle the value of the 'passed' parameter and ensure that the 'passed' session variable is set based on that value. Here's an updated version of the code. the value of the 'passed' parameter is properly checked using an if-else condition. If the value is '1', the 'passed' session variable is set to 1, indicating that the access is allowed. Otherwise, if the value is not '1', the 'passed' session variable is set to 0, indicating that the access is denied.

By including this check, you ensure that the 'passed' session variable is set correctly based on the value of the 'passed' parameter, and the access control mechanism is working as intended. 
### source: https://docs.djangoproject.com/en/4.2/topics/auth/default/
```
def topicView(request, tid):
    passed = request.GET.get('passed')  # Retrieve the 'passed' parameter from the request
    if passed == '1':
        request.session['passed'] = 1
    else:
        request.session['passed'] = 0

    request.session['topic'] = tid
    print("SESSION TOPIC SET TO: ", tid)
    topic = find_topic(tid)
    return render(request, 'pages/topic.html', {'topic': topic})
  ```
  
## Flaw 2: [A03:2021 – Injection](https://owasp.org/Top10/A03_2021-Injection/)
### Flaw's Location: https://github.com/phuongnttruong/Cyber-Security-Base-2023-Course-Project-I/blob/c75cbbb81f330a03c93b5f18f34fd581356ebdde/cyber%20security%20project/src/pages/views.py#L5

Injection vulnerabilities are one of the most prevalent vulnerabilities on the OWASP Top 10 list. Injection occurs when untrusted or attacker-controlled data is passed to an interpreter, leading to unexpected and malicious behavior. Although injection attacks can occur in various programming languages, they are frequently observed in database query languages such as SQL

The find_topic function is using a raw SQL query to retrieve the topic from the database.the value of tid is directly concatenated into the SQL query without any sanitization or parameterization. This can potentially allow an attacker to manipulate the tid parameter and inject malicious SQL code. For example, if the attacker sets tid to "1; DROP TABLE questions;", it would result in the following query:
```
SELECT * FROM questions WHERE id = 1; DROP TABLE questions;
  ```


To fix this flaw, the tid parameter should be validated and sanitized before being used in the SQL query. This can be done using parameterized queries, which allow the tid parameter to be passed separately from the SQL query string. 
```
def find_topic(tid):
    query = "SELECT * FROM topics WHERE id = %s"
    with topicView.cursor() as cursor:
        cursor.execute(query, (tid,))
        topic = cursor.fetchone()
    if topic:
        return topic
    return None
```
The tid parameter is passed to the execute method as a separate parameter, rather than being concatenated into the SQL query string. This makes it impossible for an attacker to inject malicious SQL code into the query.

## Flaw 3: [A04:2021 – Insecure Design](https://owasp.org/Top10/A04_2021-Insecure_Design/)
### Flaw's Location: https://github.com/phuongnttruong/Cyber-Security-Base-2023-Course-Project-I/blob/509611cedbbeffa71a6f5510cf18666b8f922a7c/cyber%20security%20project/src/pages/test.py#L1
Insecure design refers to a variety of software vulnerabilities that arise from inadequate software architecture and design decisions. These vulnerabilities can manifest in different ways, such as systems being susceptible to automated bots, business logic flaws that may result in financial or privacy breaches, or authentication systems that prioritize convenience over security, allowing users to select weak passwords. 

The quizView() function retrieves user input from the request's GET parameters (level) and directly uses it to set the level session variable without proper validation or sanitization. This design flaw can potentially lead to security vulnerabilities or unexpected behavior if the user input is manipulated by an attacker.

To fix the insecure design flaw in the quizView() function and address the potential security vulnerability, I validated and sanitize the user input before using it. 
```
def quizView(request, tid):
    print("CURRENTLY ON TOPIC: ", request.session['topic'])
    topic = find_topic(tid)

    user_input = request.GET.get('level')
    if user_input is not None and user_input.isdigit():
        level = int(user_input)
        if level >= 0 and level < len(topic['questions']):
            request.session['level'] = level
        else:
            request.session['level'] = 0
    else:
        request.session['level'] = 0

    request.session['passed'] = 0
    return render(request, 'pages/question.html', {'topic': topic, 'question': topic['questions'][request.session['level']]})

```
### Source: https://docs.djangoproject.com/en/4.2/intro/tutorial05/



## Flaw 4: [A06:2021 – Vulnerable and Outdated Components](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/)
### Flaw's Location: There is no specific flaw, this django version is not the latest version: There may be security patches or updates that are not included in this version

Security logging and monitoring moved up in the OWASP Top 10 rankings based on the community survey, rising from the tenth position in the OWASP Top 10 2017. Evaluating the effectiveness of logging and monitoring measures can be complex, often requiring interviews or inquiries about the detection of attacks during penetration testing.

Based on the code from setting.py provided by template, the debug mode is enabled in the settings, which is inappropriate for production environments as it can expose sensitive information.

To address these issues, the debug flag in settings.py should be modified to ```DEBUG = False```. This ensures that debug mode is disabled in production. Furthermore, it is necessary to implement proper logging for all transactions and appropriately catch and handle any potential errors. Since this task requires a comprehensive approach, specific fixes are not provided in the given code.

## Flaw 5: [Cross-site Request Forgery (CSRF)]((https://cybersecuritybase.mooc.fi/module-2.3/1-security)
### Flaw's Location: https://github.com/phuongnttruong/Cyber-Security-Base-2023-Course-Project-I/blob/119f1cd2bce5d332b7d47800bb0265d0d67fea81/cyber%20security%20project/src/pages/templates/pages/finish.html#L15
Cross-site request forgery is an attack in which an attacker can use an authenticated user's existing privileges (such as cookies or tokens) to make malicious requests and access private user data. Essentially, if a user is logged into a website, a malicious actor can use a variety of tactics, such as sending unsolicited emails or exploiting vulnerabilities on sites the user is likely to visit, to implant a malicious URL in an HTML image or link. Once executed, it can appear as though the user has voluntarily transferred funds to the attacker with no means of rectifying the situation other than contacting the bank directly and seeking assistance.

To address these vulnerabilities, it is necessary to include ```{% csrf_token %}```in each form within our application. Django automatically handles the rest, ensuring that the CSRF flaw is resolved and that the demo application is functional.
to fix the flaw, we import csrf_protect to protect against cross-site request forgery
```
from django.views.decorators.csrf import csrf_protect
@csrf_protect
```
and in finish.html page
```
{% extends 'base/main.html' %}
{% block content %}

<div class="header-bar">
    <a href="{% url 'tasks' %}">&#8592; Back</a>
</div>


<div class="card-body">
    <form method="POST" action="">
        <!--Flaw 5, Cross-site Request Forgery (CSRF), we need to put {% csrf_token %} to prevent it -->
        {% csrf_token %}
        {{form.as_p}}
        <input class="button" type="submit" value="Submit">
    </form>
</div>


{% endblock content %}
```
