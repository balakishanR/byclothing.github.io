from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from django.views import View


class Signup(View):

    def get(self, request):
        return render(request, "signup.html")

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        repassword = postData.get('repassword')

        # validation
        value = {'first_name': first_name,
                 'last_name': last_name,
                 'phone': phone,
                 'email': email,
                 }

        error_message = None
        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password,
                            repassword=repassword)

        error_message = self.ValidateCustomer(customer)

        # saving
        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.repassword = make_password(customer.repassword)
            customer.register()
            return redirect('login')

        else:
            data = {

                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def ValidateCustomer(self, customer):
        error_message = None

        if (not customer.first_name):
            error_message = 'first name required!'
        elif len(customer.first_name) < 4:
            error_message = 'first name required 4 char long or more!'
        elif (not customer.last_name):
            error_message = 'last name required!'
        elif (not customer.phone):
            error_message = 'phone number required!'
        elif len(customer.phone) < 10 or len(customer.phone) > 10:
            error_message = 'invalid phone number!'
        elif (not customer.email):
            error_message = 'email required!'
        elif customer.ifExist():
            error_message = 'Email id already registered...'
        elif (not customer.password):
            error_message = 'password required!'
        elif len(customer.password) < 8:
            error_message = 'password should be length of 8!'
        elif not customer.repassword == customer.password:
            error_message = 'confirm password not matched!'

        return error_message
