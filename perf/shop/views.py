from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate
from django.contrib.auth import authenticate
from Cibil.models import Credit_Card
from .forms import pay_form
from math import ceil
import json
import datetime
from dateutil.relativedelta import relativedelta
from Cibil.models import *
from django.core.mail import send_mail


# payment
import razorpay
razorpay_client = razorpay.Client(auth=("rzp_test_HjTkiDCGJADmpE", "FFuLbceQq7d3bxsL2rawq6oR"))


# Create your views here.
def perf(request):
    if request.method == 'POST':
        form = pay_form(request.POST)
        if form.is_valid():
            number = form.cleaned_data['Credit_card_no']
            h = Credit_Card.objects.get(Credit_Card_No=number)
            passw = form.cleaned_data['password']
            username = form.cleaned_data['username']
            print(username)
            print(h.Username)
            user = authenticate(username=username, password=passw)
            print(user)
            if user is not None:
                amount = Orders.objects.order_by('order_id').last()
                print(amount.amount)
                s = amount.amount
                n = h.Current_Balance
                if s < n :
                    print("hii")
                    h.Current_Balance = h.Current_Balance - s
                    h.save()
                    order_db = Orders.objects.order_by('order_id').last()
                    update = OrderUpdate(order_id=order_db.order_id, update_desc="The order has been placed, Payment done by PERF CARD")
                    update.save()
                    p = OrderUpdate.objects.order_by('order_id').last()
                    id = p.order_id
                    thank = True
                    params = {'thank': thank, 'id': id}
                    return render(request, 'shop/checkout.html', params)
                
                else:
                    loan = Loan_Details()
                    no = form.cleaned_data['Credit_card_no']
                    loan.Credit_Card_No = Credit_Card.objects.get(Credit_Card_No=no)
                    credit = Credit_Card.objects.get(Credit_Card_No=no)
                    print(credit.Username)
                    usern = credit.Username
                    h = Personal_Information.objects.get(Username=usern)
                    print(h)
                    mail = h.Email
                    loan.Loan_Type = 'Personal'
                    loan.Loan_Amount = amount.amount
                    loan.Loan_Start_Date = datetime.datetime.now()
                    loan.Loan_Duration = 1
                    payment_date = loan.Loan_Start_Date + relativedelta(months=loan.Loan_Duration+1)
                    payment_date = payment_date.replace(day=1) - relativedelta(days=1)
                    loan.Loan_End_Date = payment_date
                    if loan.Loan_Amount < (credit.Credit_Limit - credit.Current_Balance):
                        print("yes")
                        loan.Loan_Status = 'ongoing'
                        print(credit.Current_Balance)
                        print(credit.Credit_Limit - credit.Current_Balance)
                        credit.Current_Balance = credit.Current_Balance + loan.Loan_Amount
                        # option = form.cleaned_data['option']
                        # print(option)
                        mail_subject = 'Loan PERF'
                        message = 'Loan has been created for shopping at our merchandise page'
                        send_mail(mail_subject, message, 'perf.mail.mail@gmail.com', [mail])
                        loan.save()
                        credit.save()
                        
                            
                    else:
                        loan.Loan_Status = 'cancelled'
                        loan.save()
                        mail_subject = 'Loan PERF'
                        message = 'Loan has been canclled'
                        send_mail(mail_subject, message, 'perf.mail.mail@gmail.com', [mail])
                        print("cancelled")
                        return render(request,'shop/failure.html' )
                    thank = False
                    params = {'thank': thank}
                    return render(request, 'shop/perf.html', params)

        




    else:
        form = pay_form()
    return render(request, 'shop/perf.html', {'form': form})



def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))    # formula designed to get no. of slides according to no. of products in database
    allProds=[]
    catprods = Product.objects.values('category','id')
    print(catprods)
    cats = {item['category'] for item in catprods}    # filters unique category out of query set as unique keys 
    print(cats)
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n=len(prod)
        # print(type(prod))
        # print(prod[0].category)   # category is attribute of prod[0] like <Product: watch>.category
        #print(<Product: watch>.category)
        nSlides = nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod, range(1,nSlides),nSlides])
    #params = {'no_of_slides':nSlides,'range':range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #              [products, range(1, nSlides), nSlides]]
    params = {'allProds': allProds}
    return render(request,'shop/index.html',params)
def about(request):
    return render(request,'shop/about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)   # saving in dataset just like by using python as in shell
        contact.save()
    return render(request, 'shop/contact.html')
def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    # print(order[0].items_json)
                    response = json.dumps([updates,order[0].items_json], default=str)
                return HttpResponse(response)      #here sending the json to ajax
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')
def search(request):
    return render(request, 'shop/search.html')
def productView(request,myid):
    # Fetch the product using id
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html',{'product':product[0]})     # product ek list hai jisme kewal ek hi item hai koi id sabki unique hai
def checkout(request):
    return render(request, 'shop/checkout.html')

# Payment Method through Razorpay
def app_create(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson','')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '') + " " + request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order_amount = int(request.POST.get('formprice', ''))
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        notes = {'Shipping address': address}
        razorpay_order = razorpay_client.order.create(dict(amount=order_amount*100, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
        print(razorpay_order['id'])
        order = Orders(items_json=items_json, name=name, email=email,address=address,city=city,state=state,zip_code=zip_code, phone=phone, amount=order_amount, razorpayid=razorpay_order['id'])   # saving in dataset just like by using python as in shell
        order.save()
        return render(request, 'shop/payment.html', {'order_id': razorpay_order['id'], 'cname': name, 'cemail': email,'cphone':phone})
        # ,{'order_id': order.order_id, 'amt': order_amount}

def app_charge(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id','')
            signature = request.POST.get('razorpay_signature','')
            params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
            order_db = Orders.objects.get(razorpayid=order_id)
            order_db.razorpaypaymentid = payment_id
            order_db.razorpaysignature = signature
            order_db.save()
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            print(result)
            if result==None:
                amount = order_db.amount*100
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    update = OrderUpdate(order_id=order_db.order_id, update_desc="The order has been placed")
                    update.save()
                    thank = True
                    # id = request.POST.get('shopping_order_id','')
                    p = OrderUpdate.objects.order_by('order_id').last()
                    id = p.order_id
                    params = {'thank': thank, 'id': id}
                    # response = json.dumps(razorpay_client.payment.fetch(payment_id))
                    return render(request, 'shop/checkout.html', params)
                except:
                    update = OrderUpdate(order_id=order_db.order_id, update_desc="Payment is unsuccessful")
                    update.save()
                    thank =  False
                    return render(request, 'shop/checkout.html', {'thank': thank})
            else:
                update = OrderUpdate(order_id=order_db.order_id, update_desc="Payment is unsuccessful")
                update.save()
                thank =  False
                return render(request, 'shop/checkout.html', {'thank': thank})
        except:
            update = OrderUpdate(order_id=order_db.order_id, update_desc="Payment is unsuccessful")
            update.save()
            thank =  False
            return render(request, 'shop/checkout.html', {'thank': thank})



