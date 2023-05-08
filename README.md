# Cyber-Security-Base-2023-Course-Project-I
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
### Flaw's Location:
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
### Flaw's Location:

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
While Sensitive Data Exposure is not a specific vulnerability, it is ranked number 4 on the OWASP Top 10 list and is an important aspect of website security. This category emphasizes the importance of good design principles and thorough testing of internal logic and user interfaces. Failure to adequately test can result in insecure design and vulnerabilities.

The flaw in this code is that it is potentially exposing sensitive information. The questions variable is being passed directly to the template context, which means that all questions are being sent to the client-side. This could potentially expose sensitive information to an attacker or malicious user, such as question answers or other data that should only be accessible to authorized users.

To fix this flaw, we should only pass the necessary information to the template context. For example, we could create a new list of topics that only includes the necessary information such as topic name and ID. Then we can pass this new list to the template instead of the questions variable. This would reduce the amount of sensitive information being exposed to the client-side.

To add tests to our project, we can simply add the necessary code to the existing tests.py file.
```
def topicsView(request):
    questions = question.objects.all().values('id', 'topic', 'difficulty')
    return render(request, 'pages/topics.html', {'questions': questions})
```

