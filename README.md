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
### Flaw's Location: https://github.com/phuongnttruong/Cyber-Security-Base-2023-Course-Project-I/blob/916f19b782f525c2451c42f39d699bffa09c3a3d/cyber%20security%20project/src/pages/views.py#L52
Broken access control is a serious vulnerability that is frequently encountered and needs to be addressed, particularly for websites that handle sensitive or personal information. I introduced this flaw in the code by allowing anyone to access the "finish" page regardless of whether they have completed the quiz or not.

To fix this flaw, we need to ensure that the user has completed the quiz before rendering the "finish" page. One way to accomplish this is to add a check for ```request.session['level'] == -1``` before rendering the "finish" page. This will ensure that only users who have completed the quiz will be able to access the "finish" page. Following is the fixed code.
```
def finishView(request):
	try:
		if request.session['level'] == -1 and request.session['passed'] == 1:
			request.session['passed'] = 0
			return render(request, 'pages/finish.html')
		else:
			return redirect('/cheater/')
	except:
		return redirect('/cheater/')
  ```
  
## Flaw 2: [A03:2021 – Injection](https://owasp.org/Top10/A03_2021-Injection/)
### Flaw's Location: https://github.com/phuongnttruong/Cyber-Security-Base-2023-Course-Project-I/blob/1b17f8e2bd2f18515834bd878dbb2918ff3df2b7/cyber%20security%20project/src/pages/views.py#L5

Injection vulnerabilities are one of the most prevalent vulnerabilities on the OWASP Top 10 list. Injection occurs when untrusted or attacker-controlled data is passed to an interpreter, leading to unexpected and malicious behavior. Although injection attacks can occur in various programming languages, they are frequently observed in database query languages such as SQL

The find_topic function is using a raw SQL query to retrieve the topic from the database. However, the tid parameter is being inserted directly into the SQL query string without any validation or sanitization. This makes the function vulnerable to SQL injection attacks, where an attacker could craft a malicious tid parameter that would cause the SQL query to execute unintended SQL statements.

To fix this flaw, the tid parameter should be validated and sanitized before being used in the SQL query. This can be done using parameterized queries, which allow the tid parameter to be passed separately from the SQL query string. 
```
def find_topic(tid):
	query = "SELECT * FROM topics WHERE id = %s"
	with connection.cursor() as cursor:
		cursor.execute(query, [tid])
		topic = cursor.fetchone()
	if topic:
		return topic
	return None
  ```
The tid parameter is passed to the execute method as a separate parameter, rather than being concatenated into the SQL query string. This makes it impossible for an attacker to inject malicious SQL code into the query.

## Flaw 3: [A04:2021 – Insecure Design](https://owasp.org/Top10/A04_2021-Insecure_Design/)
### Flaw's Location: https://github.com/phuongnttruong/Cyber-Security-Base-2023-Course-Project-I/blob/509611cedbbeffa71a6f5510cf18666b8f922a7c/cyber%20security%20project/src/pages/test.py#L1
Insecure design refers to a variety of software vulnerabilities that arise from inadequate software architecture and design decisions. These vulnerabilities can manifest in different ways, such as systems being susceptible to automated bots, business logic flaws that may result in financial or privacy breaches, or authentication systems that prioritize convenience over security, allowing users to select weak passwords. In essence, insecure design encompasses inherent logical or systematic flaws within the design itself, rather than being a consequence of poor implementation. To mitigate insecure design, it is crucial to employ robust testing and adhere to sound design protocols. Django, for example, offers tools for creating automated tests, and developers can follow test-driven development (TDD) principles by crafting tests prior to developing functionality.

There is no test file in this app. To address the lack of tests, it is essential to create a comprehensive suite of tests that encompass various scenarios and edge cases. Additionally, another flaw in the application is the ability for users to pick multiple anwser for a single question, potentially distorting the results. Identifying this issue could have been achieved through rigorous testing. To rectify it, a solution similar to the one create the file ```test.py``` for making sure that our function is working as intended
### Source: https://docs.djangoproject.com/en/4.2/intro/tutorial05/



## Flaw 4: [A06:2021 – Vulnerable and Outdated Components](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/)
### Flaw's Location: There is no specific flaw, this django version is not the latest version: There may be security patches or updates that are not included in this version

Another potential flaw is the use of vulnerable and outdated components in the code. This exposes the application to security risks as new vulnerabilities are discovered. To mitigate this risk, developers should regularly audit the components they use and update them as necessary. Fortunately, frameworks like Django provide automatic security warnings to help with this.

Based on the code from setting.py provided by template, there doesn't seem to be any major flaws or vulnerabilities. However, the version of Django used in this code (3.0.8) is not the latest version, and there may be security patches or updates that are not included in this version. It's always a good practice to keep software components up to date to ensure the latest security patches are applied. Additionally, there is a secret key used in this code, which is good for security purposes. However, this key is hard-coded into the code, which is not a recommended practice. It's better to store sensitive information like this in environment variables or a separate configuration file that is not included in version control.

## Flaw 5: [Cross-site Request Forgery (CSRF)]((https://cybersecuritybase.mooc.fi/module-2.3/1-security)
### Flaw's Location:https://github.com/phuongnttruong/Cyber-Security-Base-2023-Course-Project-I/blob/1b17f8e2bd2f18515834bd878dbb2918ff3df2b7/cyber%20security%20project/src/pages/templates/pages/question.html#L12
Cross-site request forgery is an attack in which an attacker can use an authenticated user's existing privileges (such as cookies or tokens) to make malicious requests and access private user data. Essentially, if a user is logged into a website, a malicious actor can use a variety of tactics, such as sending unsolicited emails or exploiting vulnerabilities on sites the user is likely to visit, to implant a malicious URL in an HTML image or link. Once executed, it can appear as though the user has voluntarily transferred funds to the attacker with no means of rectifying the situation other than contacting the bank directly and seeking assistance.

To address these vulnerabilities, it is necessary to include ```{% csrf_token %}```in each form within our application. Django automatically handles the rest, ensuring that the CSRF flaw is resolved and that the demo application is functional.
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
