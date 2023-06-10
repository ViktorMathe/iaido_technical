# Iaido technical test

## REST API:

### The test was: 
    Generate a Django app for a REST API that describes the following entity:
    Person(first name, last name, email, phone, dateOfBirth, age, username, password).
    It describes a person that is part of the system and has the ability to log in using their username and password credentials.
    The app should support:
    In-memory user-based auth (create 2 test persons / roles “admin” and “guest”).
    Usage of Django ORM with in-memory sqlite
    Standard REST CRUD for the entity (with pagination, only admin can access).
    Extra endpoint that returns a list of persons that can be filtered by first / last name (also partial) and/or age (admin and guest can access). Username and password should not be returned on this endpoint.
    Customised API error response.


### Python-Django
 * I used the **Django Rest Framework** to complete the test

### Person
 * I made the **Person model** in the 'api' app which has all the fields which been mentioned above. I used CharField model for most of the fields except the "email" and the "age" fields where I used the *Email* and *PositiveIntegerField*.

 * I had to makemigrations then migrate in the terminal to get the data in to the database.

### Database
 * **SQLite3** the default database has been used in this project with in-memory function.
 * I had to make sure it is using the in-memory database which I had to implement in the *settings.py* file.
 * That is my **database code** in the settings : 
   *  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'memory': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'file::memory:',}}
 * To make sure the app is using the memory db I had to implement in the *apps.py* file which is using *migration* every time when something is updating in the app. Here is the code what I wrote: 
   * def ready(self):
        call_command('migrate',
                     app_label='api',
                     verbosity=1,
                     interactive=False,
                     database='memory')
   * the *call_command* function makes sure the *db* is using the memory for this site and the *migrations* has been applied.

### Views
 * I made different *views* for each function with different approaches.
 * For the **signup** , **login** and the **person_list** function is using the **@api_view** decorator what is returning the data in **JSON** format and you have to write JSON for signup and login as well.
   * With this decorator I could manage to use the basic filtering method which you can access as you write in the url the following keywords: 
      * 'Filter by First Name': 'person_list/?first_name="value" ',

        'Filter by Last Name': 'person_list/?last_name="value" ',

        'Filter by Age': 'person_list/?age="value" ',

        You have to change the "value" field with the desired data.

   * For the *person_list* and *filtering* functions you has to be authenticated which has been completed with a *permission_class* decorator.
     * *@permission_classes([IsAuthenticated])*


 * I have another two classes which is the **PersonCrudView**.
   * This viewset class was helped me a lot with has already implemented **CRUD** functions all I had to do was set a *queryset* and the *serializer class* and connect my **PersonPagination** class where I could set the amount how many *Person* I would ike to see on a single page and how many pages can be all together. The **CRUD** is very easy to use it is returning as an *HTML* form and all you have to do is fill out the fields then *POST* it, if you would like to update an existing person all the data is already populated in the mentioned form and with the *POST* button is updating.
   With the same method you can just **Delete** the person.
   For this **PersonCrudView** viewset I wrote a function which is checks if the *User* who tries to access this CRUD is a superuser or not.
      * *class IsSuperUser(IsAdminUser):
        
        def has_permission(self, request, view):
        
        return bool(request.user and request.user.is_superuser)*

 * In the REST API framework we have to use so called **Serializers**.
   * In the *serializers.py* file I made a few classes which is the following: 
      * **PersonListSerializer**
          * This serializer is makes sure when a user is accessing the *person_list* view, the *username* and *password* is not returning.

      * **PersonSerializer**
         * This serializer is returning all the fields which can be accessed only by the admin.

      * **UserRegistration**
         * This class makes sure what fields you have to provide as a JSON in the *signup* view. You have to provide the same password twice for security purposes and if you don't write the exactly same password you get a custom api error message.