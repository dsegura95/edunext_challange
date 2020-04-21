Challenge stack
===============

This application is a sample REST API provided for the eduNEXT developer challenge.

The application you develop should interact with this app as it would do with other applications on our production environment. There is no need to modify the code running here.


Rationale
=========

This part of the challenge tests your ability to initialize a similar stack to the ones we use during everyday development. Also in the real world you are not always in control of the complete infrastructure and stack. You need to make your own solutions work as pieces of the puzzle.


Getting started
===============

To get you started on the challenge quickly, we have created some bootstrapping scripts to make things easier.

In plain language all you need to do is create a virtualenv[^1] and run the bootstrap target with make.

A detailed step by step description is:

```
cd 001_challenge_stack
virtualenv venv
source venv/bin/activate
make bootstrap
make run
```

The development server should have started now. You can visit the API by navigating in a browser to : `http://localhost:8010/api/v1/customerdata/`.

Imagine that what you just launched is the service where we keep information of all our customers. Each customer gets an unique ID. For example `1b2f7b83-7b4d-441d-a210-afaa970e5b76`, then you can interact with the data for any specific customer using the URL `http://localhost:8010/api/v1/customerdata/1b2f7b83-7b4d-441d-a210-afaa970e5b76`. You can find the IDs for all the customers and the object for each customer by looking at the development server in a browser.

Now leave this running and move to the step 002 of the challenge. If you mess up your work later, you can come back and use `make erase` to clear everything again. Then start over at the step 2 of the list.


Solution
===============

It was decided to create another new application for a modularization of functionalities with the future in mind.

The new application is called *payments*. A model was created to store (own decision) the IPN messages because I consider efficient the backup of the information for the system.

An API service was created with Django Rest Framework, where these stored IPN messages could be obtained and in turn also be received.

When receiving an IPN message through a POST request, in addition to being stored, the necessary information is extracted and sent to the customer API through a PUT request that was implemented in the app that contains it. Then when received by the customer API, the information to be updated is obtained and changed in the database.

The payment API was tested, 5 cases were generated and approved. In general, the cases tested were:

+ Test 1: Verify if the payment_status is not Completed, the account is changed to 'free'
+ Test 2: Verify a customer's account change to 'premium'
+ Test 3: Verify only the change of the last payment day on a 'premium' to 'premium payment'
+ Test 4: Verify a bad request when sending the IPN message without one of the required fields
+ Test 5: Verify a customer's account change to 'basic'

---

[^1]:
Virtualenv is a python utility to make development simple.

A guide on how to install virtualenv for Linux, Mac and Windows is available here (no need to do the django part):
http://pythoncentral.io/how-to-install-python-django-windows-mac-linux/

Disclaimer: this instructions were tested using a linux OS, if you have problems running this in a different OS, please let us know.