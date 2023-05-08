# Cyber-Security-Base-2023-Course-Project-I
The code presented here is for a website, based on part 5 question 21 of the Cyber Security Base 2023 course https://cybersecuritybase.mooc.fi/module-2.5/1-framework offered by the University of Helsinki. The project website intentionally includes five security flaws from the OWASP 2021 top ten list.

I have explained these flaws, why they are considered security risks, and provided solutions to fix all the issues in the read me file. These fixes are not implemented within the project files themselves, which makes it easier to compare and test the original code against the fixed code.

You can find the repository for this project at https://github.com/phuongnttruong/Cyber-Security-Base-2023-Course-Project-I. To use the project, download and extract the project files and then run the following command in your preferred command prompt from the project's root folder:

To start the server, execute the command ```python manage.py runserver```. If the database is not functioning properly, you may need to run the following commands:

```
python manage.py makemigrations
python manage.py migrate
```
After the server is up and running, you can access the homepage by navigating to http://127.0.0.1:8000/ 

To modify or add any database tables using the Django admin interface, visit http://127.0.0.1:8000/admin/.
Username: admin
Password: admin
## Flaw 1: [A03:2021 – Injection](https://owasp.org/Top10/A03_2021-Injection/)
### Flaw's Location:
the find_topic function is using a raw SQL query to retrieve the topic from the database. However, the tid parameter is being inserted directly into the SQL query string without any validation or sanitization. This makes the function vulnerable to SQL injection attacks, where an attacker could craft a malicious tid parameter that would cause the SQL query to execute unintended SQL statements.

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
