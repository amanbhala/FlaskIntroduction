Jinja is the template engine that flask uses to render html templates.
{{}} -> This will take the code inside it and will give us the result in string.
{{%%}} -> It is the jinja syntax to render the template.
To start the database write database and then inside that:
    - from app import db  -> TO import the database object from our application.
    - db.create_all()  -> To create the database
    -  