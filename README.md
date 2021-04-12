## Introduction:
Expectations
- Docker for local development and deployment 
- PostgreSQL
- Use of Custom user model
- Robust user authentication flow with email
- comprehensive testing
- environment variables 
- security and performance improvements, etc

*Reference:*
*[Django for professionals](https://djangoforprofessionals.com/)*

## Docker 
Most interesting thing about Docker:
    - With Docker, you can possibly reproduce a production environment locally  everything from the proper Python version to installing Django and running additional services like a production-level database. This means it no longer matter if you are on a Mac, Windows, or Linux computer. Everything is running within Docker itself.
- Docker is a way to isolate an entire operating system via Linux containers which are a type of virtualization. 

*"C:\Program Files\Docker\Docker\DockerCli.exe" -SwitchDaemon*


#### Virtual environments vs Docker
- The important distinction between virtual environments and Docker is that `virtual environments` can only isolate Python packages. They cannot isolate non-Python software like a `PostgreSQL` or `MySQL` database. And they still rely on a global, system-level installation of Python (in other words, on your computer). The virtual environment points to an existing Python installation; it does not contain Python itself.
- Linux containers go a step further and isolate the entire operating system, not just the Python parts. In other words, we will install Python itself within Docker as well as install and run a production-level database.

### Some basic Docker commands
- docker --version
- docker run hello-world //To inspect successful installation
- docker info //inspect docker 

## Chapter 1: Simple Hello

### Images, Containers and the Docker Host

1. A `Docker image` is a snapshot in time of what a project contains. It is represented by a `Dockerfile` and is literally a list of instructions that must be built. 

2. A `Docker container` is a running instance of an image
- To make this clearer with an apartment anology: The image is the blueprint or set of plans for the apartment (electricity, plumbing, walls, etc); the container is the actual, fully-built building

3. A `Docker Host` which is the underlying `OS`. It's possible to have multiple containers running within a single Docker Host. 
    - When we refer to code or processes running within Docker, that means they are running in the Docker host

### Creating a Dockerfile
- Dockerfiles are read from top-to-bottom when an image is created. 
- The first instruction must be the `FROM` command which lets us import a base image to us for our image, in this case `Python:3.9`
- Then we use the `ENV` command to set two environment variables
    1. PYTHONDONTWRITEBYTECODE: means Python will not write .pyc files which we also do not desire
    *NB: .pyc files are created when .py file is imported. They contain the "compiled bytecode" of the imported module/program*
    2. PYTHONUNBUFFERED: ensures our console output looks familiar and is not buffered by Docker, which we don't want 
- Next we user WORKDIR to set default work directory path within our image called `code` which is where we will store our code. Docker will assume we want to execute all commands from this directory
- For our dependencies we are using Pipenv so we copy over both the    `Pipfile` and `Pipfile.lock` files into a `/code/` directory in Docker

*NB: The benefit of a `lock file` is that this leads to a deterministic build: `no matter how many times you install the software packages, you’ll have the same result.` Without a lock file that “locks down” the dependencies and their order, this is not necessarily the case. Which means that two team members who install the same list of software packages might have slightly different build installations.*

- Moving along we use the `RUN` command to first install Pipenv and then `pipenv install` to install the software packages listed in our `Pipfile.lock`, currently just Django. It’s important to add the `--system` flag as well since by default Pipenv will look for a virtual environment in which to install any package, but since we’re within Docker now, technically there isn’t any virtual environment. In a way, the Docker container is our virtual environment and more. So we must use the --system flag to ensure our packages are available throughout all of Docker for us.

- As the final step we copy over the rest of our local code into the /code/ directory within Docker.

- Our image instructions are now done, so let's build the image using the command `docker build .`

- Moving on we now need to create a `docker-compose.yml` file to control how to run the container that will be built based upon our `Dockerfile` image

## Chapter 2: PostgreSQL

- Repeat the process in the `Dockerfile` and `docker-compose.yml`
- Running `docker-compose.yml` in **Detached Mode**. This requires either `-d` or `-detach` flag
    - `docker-compose up -d`
    - Detached mode runs cotainers in the background, meaning we can use a single command line tab without needing to open another cli
    - `docker-compose logs`: to see error logs

- Since we're working within a traditional docker as opposed to local, things need to change a bit to have the `docker feel` commands in the form: `docker-compose exec [service]` where we specify the name of the service
    Eg: `docker-compose exec web python manage.py createsuperuser` to create superuser

### Switching to PostgreSQL
- Install a database adapter, `psycopg2`, so Python can talk to PostgreSQL
- Update DATABASE config in `settings.py` python file
- Install and run PostgreSQL locally

We will then have two services (in order words containers) running within our Docker host:
1. `web` for the Django local server
2. `db` for our PostgreSQL database

We move to `settings.py` file to update our PostgreSQL settings to connect our web to the db. PostgreSQL requires four things:
    1. Name
    2. USER
    3. PASSWORD
    4. HOST
    5. PORT

- Download the database adapter `psycopg2-binary` for python
- After downloadin, stop the docker: `docker-compose down`
- force build again: `docker-compose up -d --build`

## Chapter 3: Bookstore app
- Before switchig to Docker
    1. create books folder
    2. pipenv intall django and psycopg2-binary
    3. pipenv shell
    4. create django project //boostore_project
    5. exit
- Move to docker:
    1. created `Dockerfile` and `docker-compose.yml`
    2. `Dockerfile` contents will be same as in **chapter 2**
    3. `docker-compose.yml` will change a bit
        - A dedicated volume for the Database so that it can persists even when the `services` containers are stopped.
        - In the web container, add: 
            - `postgres_data:/var/lib/postgresql/data/`
        - In the same `services` directory, add:
            - volumes: `postgres_data:`
        - Run: `docker-compose up -d --build`

### Custom User Model

Custom User Model is recommended by Django because you will need to make some changes to the `User` model in your project one time

Implementation of Custom User Model can be done by either extending `AbstractUser` which keeps the default `User` fields and permissions or extend to `AbstractBaseUser` which gives more granular components to make changes.

The 4 steps to add a customer use model in a project are:
    1. Create a `CustomUser` model 
    2. Update `settings.py` file
    3. Customize `UserCreationForm` and `UserChangeForm`
    4. Add the customer user model to `admin.py` file

Next we move to update the built-in forms to point to out `CustomUser` instead `User`. We do this by creating `users/forms.py` file
- the `get_user_model()` methods imports the `CustomUser` created in the `models.py` file which looks to the `AUTH_USE_MODEL` in the settings.py file. 

- According to William "This might feel a bit more circular than directly importing `CustomUser` here, but it enforces the idea of making one single reference to the custom user model rather than directly referring to it all over our project."

### Tests
Test are very important for the development lifecycle of a project. There two main types of tests:
    1. Unit tests: Are small, fast and isolated tests for specific functionality of the application
    2. Integration tests are large and slow used for testing the entire application or large chunk of it

We will be using Python's built-in `TestCase` module

Process
- First of all we test how to create a `normal user` and a `superuser`. 
- A variable `User`, is assigned to the method `get_user_model()` and we use the manager method `create_user` to create a normal user the manager method `create_superuser` to create a superuser
- We use `assertFalse` to both the attributes `is_staff` and `is_superuser` to make sure that newly created users are not staff and not supersuers
- On the other hand `assertTrue` is used for the same attribues to make sure that the superuser is a staff and the superuser

### Running the tests
1. To run all tests: `docker-compose exec web python manage.py test`
2. To run a specific tests from an app, say pages: `docker-compose exec web python manage.py test pages`


## Chapter 4: Pages App
As usual in our project-level directory, execute the command below
- `docker-compose exec web python manage.py startapp pages`
- Then add it to the installed apps in `settings.py`

### Templates
We need to add `templates` to our `DIRS` so that Django can add it to the root path and search items within it. This can be done in either two ways in the settings.py file

    1. `DIRS = [BASE_DIR / 'templates']` for **Django 3.1**
    2. `DIRS = [os.path.join(BASE_DIR, 'templates')]` for **Lower Django versions**

Create the following two files in the `templates` folder in the root directory

    1. `_base.html`
    2. `home.html`

*NB: Developers prefer to add the underscore _ to any file that intends to be inherited by other files, hence _base.html*

After setting the homepage and necessary views, the server will throw an error. Just like on your local computer where you'll need to stop and run the server again, you'll also stop the docker and run it again.
    - `docker-compose down`
    - `docker-compose up -d`

### More Tests
The `setUp` Method is an initialization to get things DRY (Don't Repeat Yourself)
This method is used in `pages/tests.py` file to eliminate a lot of repetitions in writing the tests

**Resolve**: According to William, "Django uses `resolve` to make sure that a page resolves to its indented view. We import both the view we want to test for and the resolve method.


## Chapter 5: User Registration
The key functionalites for registration are:

    - login (django shipped)
    - logout (django shipped)
    - signup (custom created)

### Auth App:
We implement both login and logout using Django's own `auth` app. With this, Django provides the necessary views and urls which means we only need to update our templates

### Auth URLs and Views
It turns out Django's built-in auth app has a prefix for its urls path which is `accounts/`. 
Below is a list of associated urls with `auth` app

    `
    1. accounts/login/ [name='login']
    2. accounts/logout/ [name='logout']
    3. accounts/password_change/ [name='password_change']
    4. accounts/password_change/done/ [name='password_change_done]
    5. accounts/password_reset/ [name='password_reset']
    6. accounts/password_reset/done/ [name='password_reset_done']
    7. accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    8. accounts/reset/done/ [name='password_reset_complete']
    `

Unlike `login` and `logout`, `signup` is a custom created process that follows the usual `urls>view>template` methodology

### More Tests for User Registration
For the login and logout, we do not need to create tests for them since they are shipped in by Django and already have tests.
We'd rather create tests for the `signup` and populated the `signup_template` to test the following 

    - status code
    - template used (both included and excluded text)
    - signup form is being used
    - signup view actually resolves to the right signup view

Another method for testing your model is the built-in `setUpTestData()` method: This makes it possible to run tests both within a whole class and for each individual test. 


## Chapter 6: Static Assets
According to Williams:

    Django relies on the `staticfiles app` to manage static files from across our entire
    project, make them accessible for rapid local development on the file system, and also
    combine them into a single location that can be served in a better performing manner
    in production. 

This is started with updating the `staticfiles app` configuration in the `settings.py` file

`STATIC_URL = /static/`: defines the path for the static files

`STATICFILES_DIRS`: defines the location of our static files in *local development*. They all live within the top-level directory

`STATIC_ROOT`: Is the location of static files for *production*

`STATICFILES_FINDERS`: This tells Django how to look for static files directories. 

For production, we'd run this to collect all our staticfiles:

    `docker-compose exec web python manage.py collectstatic`

### Django Crispy Forms
This is a third party form that provides an additional aesthetic view to forms in Django
Process to install it is as follows

    - docker-compose exec web pipenv install django-crispy-forms
    - docker-compose down
    - docker-compose up -d --build


## Chapter 7: Advanced User Registration

`DJANGO-ALLAUTH`: This is an integrated set of Django applications addressing authentication, registration, account management as well as 3rd party(social) account authentication

Follow same installation procedure like the Django crispy forms

    - docker-compose exec web pipenv install django-allauth==0.44.0
    - docker-compose down
    - docker-compose up -d --build

`sites framework`: This is a powerful way of adding/editing/publishing etc from the admin dashboard, two or more sites all at ones. Each site is given an ID with `SITE_ID`. All articles posted on say `www.example1.com` and `www.example2.com` accesses one databases and could be assessed with their IDs
In order for `django-allauth` to work, put the followoing in the installed apps section of your settings.py file

    'django.contrib.sites',
    'allauth',
    'allauth.account'

Django's `auth` app looks for templates within a `templates/registration` directory, However, `django-allauth` looks for its templates in the directory `templates/account`. There you need to create a new directory `templates/account` and put your new `login.html` and `signup.html` in it

### django-allauth with Social authentication 

    ....
    chapter 7: page 165
    ....


## Chapter 8: Environment Variables
According to Vincent:

    These are variables that can be loaded into the operating environment of the project at run time as opposed to hard coded into the codebase

## Chapter 9: Email
### Navigating around django-allauth documentation

## Chapter 10: Books App

`__str__` method helps to control how the object is outputted in the Admin and Django shell

`get_absolute_url` method: According to Williams, there’s no need to use the url template tag either, just one canonical reference that can be changed, if needed, in the `books/models.py` file and will propagate throughout the project from there. This is a cleaner approach and should be used whenever you need individual pages for an object.

### Difference between Primary Key and IDs

Django's `DetailView` treats Primary Key and IDs interchangeably, however, there is differerece.

    - pk is the attribute that contains the values of the primary key for the model
    - id is the name of the field created as a primary key by default if none is explicitly specified

### Slugs vs. UUIDs

`Slugs`: A short labele for something. This where titles can be coverted into space-separated sentences. Eg; a new article could be converted to `a-new-article`. The downside of this approach is how to handle duplicates. Though random strings or numbers can be added, it still remains a challenge when it comes to sychronization

`UUIDs` (Universally Unique IDentifier): Helps in generating random objects of 128 bits as IDs. 
    - For encryption purpose, `uuid4` is used

### Fix issue for: django.db.utils.OperationalError: FATAL:  password authentication failed for user "postgres"

Go the `cli` of the postgres db on docker and type:

    docker exec -it Your_Container_Name rengine_db_1 /bin/bash
    su - postgres
    psql
    ALTER USER postgres WITH PASSWORD 'postgres';


### Tests for books
We import `TestCase` and `Client()`
    - Client is imported as a dummy web browser for simulating `GET` and `POST` requests
    - When testing  `views` always use `Client` module/library


## Chapter 11: Reviews App and Foreign keys


## Chapter 12: File/Image Uploads

    1. static: Django refers to this name for any static file that is prepopulated in css, js, or images
    2. media: Django refers to anything that is being uploaded by the user as `media`
NB: Fundamentally, we can always trust `static` files and not `media` files because the former is provided by us and the later is provided by an outsider

`pillow`: This is an image processing library that supports uplaod of images and other features such as basic validation.

Process of installation
1. docker-compose exec web pipenv install pillow==8.2.0
2. docker-compose down
3. docker-compose up -d --build

Move to `settings.py` for the configuration

    MEDIA_ROOT: is the absolute file system path to the directory for user uploaded files.
    Configuration: 
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    MEDIA_URL: is the URL we can use in our templates for the files
    configuration: 
    MEDIA_URL = '/media/'

NB: Since user-uploaded content is assumed to exist in a production context, to see media items locally we to update out `bookstore_project/urls.py` to show the files locally. This means we will import both `settings` and `static` at the top and then adding an additional at the bottom

To update the template to display the book cover, you need a url route. The route will be:
    - `book.cover.url`  //object name, field name, url

If you added a cover photo for one booka and didn't do that for the other books, they'll throw an error when you try to open them because they do not have cover photos. The way out is to put a simple `if statement` before the image tag in the `book_detail.html` which is 
    - {% if book.cover%}...{% endif %}


## Chapter 13: Permissions

Django comes with `built-in authorization options` for locking down pages to either logged in users, specific groups, or users with the proper individual permissions

### Logged-In Users Only
Two ways of restricing permissions to logged-in users are:
    1. `login_required()`: decorator
    2. `LoginRequired mixin`: for class-based views

Practice: Let's try to add restriction to the books page for only those logged in
- First import `LoginRequiredMix` at the top and then add it before `ListView` since mixins are loaded from left-to-right
- Set a `login_url` for the user to be redirected to
- Since we're using `django-allauth` app, the URL will be `account_login`. For raw django authentication system, we'll just use `login`

### Custom Permissions
Custom permissions can be set via the `Meta` class on our database models. 

*PermissionRequiredMixin*: To limit some permissions that the user can do, like ability to view certain books or all books. page: **256**
In other words they have access to the `DetailView`. We will add this `custom permission` to new user we will create called `specialuser`
- Addition of Meta to book model in `book/models.py`
    class Meta:
        permissions = [
            ('special_status', 'can read all books')
        ]
- make new migrations for `book`
- go to the admin site and add `book | book| can read all books` permission to out `specialuser`

- Next is to use `PermissionRequiredMixin`. Import it and add it to the `DetailView` after `LoginRequiredMixin` but before `DetailView`. This order logically makes sense

- Finally add a `permission_required` field which specifies the desired perimission. In our case its name is `special_status` and it exists on the `books` model 


## Chapter 14: Orders with Stripe 

Two main offerings from `Stripe` are:
    1. `Checkout`: which allows for the use of pre-built forms from Stripe
    2. `Connect`: which is used for a marketplace with multiple buyers and sellers.

For example if we added book
authors as users and wanted to process payments on their behalf, taking a commission for ourselves on the Bookstore website, then we would use `Connect`. However, in this project, since we are just processing payments we will use `Checkout`

There are now two `Checkout options` available to developers
    1. `Client Integration`: where the payment form is hosted on Stripe itself
    2. `Server Integration`: where we host the form ourselves. For the purpose of this project using Django, we will opt for option 2, *Server Integration* approach. 

According to Vincent, the second major change is a new API that relies on `Sessions`. It is currently not fully implemented and poorly documented. I have personally not explored it yet. 

### Payments Flow
- There is book page(book_list) for all books
- There is book detail page(book_detail) for each book
NB: We added a permission for a user to have access to all books. Ultimately when an order is successfully completed, that user needs to have this permission flag flipped in the database. That's the main goal 

### Installing Stripe
    - docker-compose exec web pipenv install stripe==2.56.0
    - docker-compose down
    - docker-compose up -d --build

Go to the Stripe website and register an account in order to generate the API keys.

Each Stripe account has 4 API keys
    - 2 for testing
    - 2 for Live use in production

There are two types of keys:
    1. `publishable key`: which will be embedded in the Javascript on your website
    2. `secret key`: which is stored on the server and for private use only

After this settings configuration, move to add the stripe checkout form to the `orders/purchase.html` template

We can test payments with several `test card numbers` provided by stripe. You can find them here:
    [Stripe Test Card Numbers](https://stripe.com/docs/testing#cards)

NB: Don't forget to overide/edit `get_context_data()` in `orders/views.py` to add the stripe publishable key from `settings.py`

On Stripe dashboard, if you then click on “Payments” in the same lefthand menu, there are no charges.
So what’s happening?
*Think back to the Stripe flow. We have used the publishable key to send the credit card information to Stripe, and Stripe has sent us back a `unique token` for the order.*
*But we haven’t used that token yet to make a charge! Recall that we send an order form to Stripe with the Publishable Key, Stripe validates it and sends back a token, and then we process the charge using both the `token` and our own `Secret Key`*

### Stripe + Permissions and 
This step involves that, when we implement the full payment by using stripe token and our secret key, we change the permission of the user by giving them access to the `DetailView`.
This is done in the `orders/views.py`
    1. We create the permission: `permission = Permission.objects.get(codename='special_status')`
    2. Get the user: `user = request.user`
    2. Add the permission to the user:
        `user.user_permission.add(permission)`
    3. Perform POST request/response with function view and render `orders/charge.html` template


### Tests
*NB: Cypress for testing payments*




### Issues identified
1. Sign up form with only one password field instead of two
2. Chapter 13 Permissions(page 255): After creating the custom permission, he added it to the user from the admin dashboard. This doesn't work properly. It only works if you don't add from the admin but rather leave it and after the payment authentication with stripe token and your secret key, the permission is added automatically when you have access to the detail_list. If you check back in the admin dashboard, the permission will be automatically adde. 