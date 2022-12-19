# **Diems - v1/stable**

**CodeShine (a part of Di website)** - is an application for posting, submitting, and evaluating assignments. As a whole, '**Di**' is a shorthand for `Deogiri Institute of Engineering and Management Studies, Aurangabad 431001, Maharashtra, India`.

This is an open-source and free project, you can use the source code at your convenience and contribute to it. **Now, this code belongs to you!**
 
[![Introductory Video From Youtube](https://drive.google.com/uc?export=view&id=1YaZb8HttKiFnru6IR7es4NMHbMFg8WLA)
](https://www.youtube.com/watch?v=3Zsjpzn37T8)

  

This is an introductory video, for version `v1/stable`, hope you find it helpful.

<br/>


# **DOCUMENTATION**

[...Goto Folder](https://drive.google.com/drive/folders/1BkW4UvcxOwCk9jU4R9cznBPWyNya58AU?usp=sharing)

All the files during the creation of the website, for the first time, as a mini-project work, in December 2022, are stored in the drive folder.
  
<br/>

# **Getting Started**

### **:octocat: STEP 01**

## **HOW TO GET IT?**

1. Switch the branch to v1/stable.
2. Download the code directly (or through releases - if available).
3. Unzip the archive file.
4. Now, you need to configure it as instructed below. That's it.

### **:octocat: STEP 02**

## **HOW TO CONFIGURE?**

  
1. Go to the directory, more likely `./diems` where the `manage.py` is stored. This file is the starting point for any Django project.

  
3. Make sure the [Python](https://www.python.org/) and [Django](https://www.djangoproject.com/) is installed and in it's latest version. At the time of the creation of this project we used the following commands:


	```bash
	$ sudo apt install python3 python3-pip
	$ pip3 install Django==4.1.4
	```

	If you are using a Linux distribution other than Debian-based, or Windows or any other operating system, consider referring to the official documentation.

4. If you want to run in production - i.e.

	```py
	# In ./diems/settings.py
	DEBUG = False
	```

	You need to install the `whitenoise` through the python package manager, as:

	```bash
	$ pip3 install whitenoise
	```

	Also, at the time of configuration, you need to collect static files, for `whitenoise` to serve them automatically, as:

	```bash
	$ python3 manage.py collectstatic
	```

	You may need to run it after each change in the code, for the development. Again, If you are using a Linux distribution other than Debian-based, Windows, or any other operating system, consider referring to the official documentation.

5. If you do not want to run in production, go to `./diems/settings.py` and set the `DEBUG` value to `True`.

	```py
	# In ./diems/settings.py
	DEBUG = True
	```

	Now, you don't need to care about `above point 3`.

  

6. It's time to make a database configuration, to do so, run the following commands:

	```bash
	$ python3 manage.py makemigrations home departments accounts codeshine
	```

	and to apply settings,

	```bash
	$ python3 manage.py migrate
	```

7. Before starting the server, we need to create a superuser, an admin for the website, as:

	```bash
	$ python3 manage.py createsuperuser
	```

	Follow the instructions as instructed and you have done configuring it.

  

### **:octocat: STEP 03**

  

## **HOW TO START SERVER?**

  

1. Make sure you have completed `step 02` successfully.

  

2. To run the server, you must be in the directory where the `manage.py` existed. Then run the following command:

	```bash
	$ python3 manage.py runserver
	```

	That's it, the server is now running. If there is a problem while running, double-check the previous steps, you can even try to find the solution online.

3. If you want to terminate the server, press `CTRL` + `C` simultaneously.

<br/>


# Thanks for Visiting this page... 
