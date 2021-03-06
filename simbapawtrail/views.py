from django.shortcuts import render, redirect
from django.template import RequestContext
from .forms import FlightForm, PaymentForm, AccomodationForm, PassengerForm, RentalForm, CancellationForm #,PackageForm
from .models import Airport, Flight, Passenger, Group, Location, Accomodation, Payment, CarRental, CarRentalTime, FlightGroup
import datetime

def strtoDate(string):
    string = string.split('-')
    return datetime.date(int(string[0]),int(string[1]),int(string[2]))

# Create your views here.
def index(request):
    return render(request, 'simbapawtrail/index.html')

def accomodations(request):
    header = 'Accomodations'
    if request.method == 'POST':
        form = AccomodationForm(request.POST)
        if form.is_valid():
            num_rooms=form['num_rooms'].data
            num_guests=form['num_guests'].data
            location = Location.objects.filter(pk= form['location'].data)[0]
            checkin = strtoDate(form['check_in_date'].data)
            checkout = strtoDate(form['check_out_date'].data)
            link = '/information/?type=accomodation&rooms='+num_rooms+"&guests="+num_guests+'&location='+str(location.pk)
            link += '&checkin='+str(form['check_in_date'].data)+'&checkout='+str(form['check_out_date'].data)
            return redirect(link)
    else:
        form = AccomodationForm()
    return render(request, 'simbapawtrail/accomodations.html', {'form' : form, 'pageheader' : header})

def flights(request):
    header = 'Flights'
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            dairport = Airport.objects.filter(AirportName = form['source_location'].data)[0]
            aairport = Airport.objects.filter(AirportName = form['dest_location'].data)[0]
            retdate = None
            if (form['flight_type'].data == "Round Trip"):
                retdate = "&retdate=" + str(form['return_date'].data)
            info = "&trip=" + str(form['flight_type'].data)
            info += '&class=' + str(form['flight_class'].data)+ '&tickets='+str(form['num_tickets'].data)
            src = '&src='+str(dairport.pk)+'&srcdate='+str(form['arrive_date'].data)
            dest = "&dest="+str(aairport.pk)
            link = '/information/?type=flight&to=true' + info + src + dest
            if retdate != None:
                link += retdate
            return redirect(link)
    else:
        form = FlightForm()
    return render(request, 'simbapawtrail/flights.html', {'form' : form, 'pageheader' : header})

'''
def cruises(request):
    header = 'Cruises'
    if request.method == 'POST':
        form = CruiseForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = CruiseForm()
    return render(request, 'simbapawtrail/cruises.html', {'form' : form, 'pageheader' : header})
'''

def rentals(request):
    header = 'Car Rentals'
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            pickup_location = Location.objects.filter(pk=form['pickup_location'].data)[0]
            dropoff_location = Location.objects.filter(pk=form['dropoff_location'].data)[0]
            src = '&src=' + str(pickup_location.pk)
            dest = '&dest=' + str(dropoff_location.pk)
            info = '&srcdate=' + str(form['pickup_date'].data)
            info += '&retdate=' + str(form['dropoff_date'].data)
            base = '/information/?type=rental'
            link = base + src + dest + info
            return redirect(link)
    else:
        form = RentalForm()
    return render(request, 'simbapawtrail/rentals.html', {'form' : form, 'pageheader' : header})

def packages(request):
    header = 'Packages'
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = PackageForm()
    return render(request, 'simbapawtrail/packages.html', {'form' : form, 'pageheader' : header})

def payment(request):
    header = 'Payment Information'
    rtype = request.GET.get('type')
    if (rtype == 'flight'):
        tickets = int(request.GET.get('tickets'))
        toflight = int(request.GET.get('toflight'))
        fromflight = request.GET.get('fromflight')
        flight_class = request.GET.get('class')
        trip = request.GET.get('trip')
        price = 0
        if fromflight != None:
            fromflight = int(fromflight)
            fromflight = Flight.objects.filter(pk=fromflight)[0]
            price += fromflight.FlightPrice
        if flight_class == 'First Class':
            multiplier = 2
        elif flight_class == 'Business Class':
            multipler = 1.5
        else:
            multiplier = 1
        toflight = Flight.objects.filter(pk=toflight)[0]
        price += toflight.FlightPrice
        price *= multiplier
        context = { 'rtype': rtype,
                    'trip': trip,
                    'toflight': toflight,
                    'fromflight': fromflight,
                    'price' : price,
                    'tickets' : tickets,
                    'flight_class' : flight_class,
                    'pageheader' : header,
        }
        linkcont = '&trip='+trip+'&toflight='+request.GET.get('toflight')+'&class='+flight_class+'&tickets='+str(tickets)+'&price='+str(price)
        if fromflight != None:
            linkcont += '&fromflight='+request.GET.get('fromflight')
    elif (rtype == 'accomodation'):
        guests = int(request.GET.get('guests'))
        accom = int(request.GET.get('accom'))
        accom = Accomodation.objects.filter(pk=accom)[0]
        rooms = int(request.GET.get('rooms'))
        price = accom.Rate * rooms
        checkin = request.GET.get('checkin')
        checkout = request.GET.get('checkout')
        context = { 'rtype' : rtype,
                    'rooms' : rooms,
                    'guests' : guests,
                    'accom' : accom,
                    'checkin' : checkin,
                    'checkout' :checkout,
                    'price' : price,
                    'pageheader' : header,
                }
        linkcont = '&guests='+str(guests)+"&accom="+str(request.GET.get('accom'))+'&rooms='+str(rooms)+'&price='+str(price)+"&checkin="+str(checkin)+"&checkout=" +str(checkout)
    elif rtype == 'rental':
        src = request.GET.get('src')
        dest = request.GET.get('dest')
        srcdate = request.GET.get('srcdate')
        retdate = request.GET.get('retdate')
        duration = (strtoDate(retdate)-strtoDate(srcdate)).days
        rental_req = request.GET.get('rental')
        rental = CarRental.objects.filter(pk=rental_req)[0]
        price = duration * rental.Rate
        context = {
            'rtype' : rtype,
            'src' : src,
            'dest' : dest,
            'srcdate' : srcdate,
            'retdate' : retdate,
            'rental' : rental,
            'price' : price,
            'pageheader' : header,
        }
        linkcont = '&src='+src+'&dest='+dest+'&srcdate='+srcdate+'&retdate='+retdate+'&rental='+rental_req+'&price='+str(price)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            groupid = int(request.GET.get('groupid'))
            pay = Payment(GroupId_id =groupid, Email=form['email'].data,CardNumber=form['card_number'].data, PaymentAmount=price,
                CardExpiryDate=form['card_expiry_date'].data, Type=rtype)
            pay.save()
            if rtype == 'flight':
                tickets = context.get('tickets')
                toflightfail = False
                fromflightfail = False
                toflight = Flight.objects.filter(pk=int(request.GET.get('toflight')))[0]
                fromflight = None
                if context.get('fromflight') != None:
                    fromflight = Flight.objects.filter(pk=int(request.GET.get('fromflight')))[0]
                if context.get('flight_class') == 'First Class':
                    if toflight.AvailFirstSeats - tickets < 0:
                        toflightfail = True
                    else:
                        toflight.AvailFirstSeats -= tickets
                        toflight.save()
                    if context.get('fromflight') != None:
                        if fromflight.AvailFirstSeats - tickets < 0:
                            fromflightfail = True
                        else:
                            fromflight.AvailFirstSeats -= tickets
                            fromflight.save()
                elif context.get('flight_class') == 'Business Class':
                    if toflight.AvailBusinessSeats - tickets < 0:
                        toflightfail = True
                    else:
                        toflight.AvailBusinessSeats -= tickets
                        toflight.save()
                    if context.get('fromflight') != None:
                        if fromflight.AvailBusinessSeats - tickets < 0:
                            fromflightfail = True
                        else:
                            fromflight.AvailBusinessSeats -= tickets
                            fromflight.save()
                else:
                    if toflight.AvailEconomySeats - tickets < 0:
                        toflightfail = True
                    else:
                        toflight.AvailEconomySeats -= tickets
                        toflight.save()
                    if context.get('fromflight') != None:
                        if fromflight.AvailEconomySeats - tickets < 0:
                            fromflightfail = True
                        else:
                            fromflight.AvailEconomySeats -= tickets
                            fromflight.save()
                if not(toflightfail and fromflightfail):
                    link = '/confirmation/?type='+rtype + linkcont+'&paymentid='+str(pay.pk)+'&groupid='+str(groupid)
                    if fromflight != None:
                        retflightgroup = FlightGroup(GroupId_id=groupid, FlightId_id=int(request.GET.get('fromflight')), FlightClass=context.get('flight_class'))
                        retflightgroup.save()
                    toflightgroup = FlightGroup(GroupId_id=groupid, FlightId_id=int(request.GET.get('toflight')), FlightClass=context.get('flight_class'))
                    toflightgroup.save()
                else:
                    group = Group.objects.get(pk=groupid)[0]
                    group.delete()
                    link = '/error/&type=flight'
            return redirect(link)
        else:
            form = PaymentForm()
    else:
        form = PaymentForm()
    return render(request, 'simbapawtrail/payment.html', {'form' : form, 'context': context })


def information(request):
    header = 'Information'
    rtype = request.GET.get('type')
    if (rtype == 'flight'):
        header = 'Flight Information'
        trip = request.GET.get('trip')
        to = request.GET.get('to')
        toflight = request.GET.get('toflight')
        if toflight != None:
            toflight = int(toflight)
        fromflight = request.GET.get('fromflight')
        if fromflight != None:
            fromflight = int(fromflight)
        flight_class = request.GET.get('class')
        tickets = request.GET.get('tickets')
        src = int(request.GET.get('src'))
        srcName = Airport.objects.filter(id=src)[0]
        sdate = request.GET.get('srcdate')
        srcdate = sdate.split('-')
        dest = int(request.GET.get('dest'))
        destName = Airport.objects.filter(id=dest)[0]
        rdate = request.GET.get('retdate')
        retdate = None
        if rdate != None:
            retdate = rdate.split('-')
        dflights = Flight.objects.filter(DepartureAirport_id=src)
        dflights = dflights.filter(DepartureTime__contains=datetime.date(int(srcdate[0]), int(srcdate[1]), int(srcdate[2])))
        if flight_class == ('First Class'):
            dflights = dflights.filter(AvailFirstSeats__gte=int(tickets))
        elif flight_class == ('Business Class'):
            dflights = dflights.filter(AvailBusinessSeats__gte=int(tickets))
        else:
            dflights = dflights.filter(AvailEconomySeats__gte=(tickets))
        rflights = None
        if flight_class == 'First Class':
            classratio = int(tickets)*2
        elif flight_class == 'Business Class':
            classratio = float(tickets) * 1.5
        else:
            classratio = int(tickets)
        if dflights is None or len(dflights) == 0:
            dflights = None
        if retdate != None:
            rflights = Flight.objects.filter(ArrivalAirport_id=src)
            rflights = rflights.filter(ArrivalTime__contains=datetime.date(int(retdate[0]), int(retdate[1]), int(retdate[2])))
            if flight_class == ('First Class'):
                rflights = rflights.filter(AvailFirstSeats__gte=int(tickets))
            elif flight_class == ('Business Class'):
                rflights = rflights.filter(AvailBusinessSeats__gte=int(tickets))
            else:
                rflights = rflights.filter(AvailEconomySeats__gte=int(tickets))
        if rflights is None or len(rflights) == 0:
            rflights = None
        context = { 'rtype' : rtype,
                    'trip' : trip,
                    'to' : to,
                    'toflight' :toflight,
                    'fromflight' : fromflight,
                    'ticket_type' : flight_class,
                    'tickets' : tickets,
                    'classratio' : classratio,
                    'src' : src,
                    'srcName' : srcName,
                    'sdate' : sdate,
                    'dest' : dest,
                    'destName' : destName,
                    'rdate' : rdate,
                    'dflights' : dflights,
                    'rflights' : rflights,
                    'pageheader' : header, }
    elif (rtype == 'accomodation'):
        header = 'Accomodation Information'
        rooms = request.GET.get('rooms')
        num = request.GET.get('num')
        guests = request.GET.get('guests')
        location = int(request.GET.get('location'))
        checkin = request.GET.get('checkin')
        checkout = request.GET.get('checkout')
        duration = (strtoDate(checkout)-strtoDate(checkin)).days
        rate = duration * int(rooms)
        loc = Location.objects.filter(pk=location)[0]
        accomodations = Accomodation.objects.filter(LocationId_id=loc.pk)
        if len(accomodations)==0:
            accomodations = None
        context = { 'rtype' : rtype,
                    'rooms' : rooms,
                    'guests' : guests,
                    'num' : num,
                    'location' : location,
                    'checkin' : checkin,
                    'checkout' : checkout,
                    'duration' : duration,
                    'rate' : rate,
                    'loc' : loc,
                    'accomodations' : accomodations,
                    'pageheader' : header,
        }
    elif rtype == 'rental':
        context = information_rental(request, rtype)
    return render(request, 'simbapawtrail/information.html', context)

def information_rental(request, rtype):
    header = 'Car Rental Information'
    req_pickup_location = int(request.GET.get('src'))
    req_dropoff_location = int(request.GET.get('dest'))
    req_pickup_date = request.GET.get('srcdate')
    req_dropoff_date = request.GET.get('retdate')

    pickup_location = Location.objects.filter(pk=req_pickup_location)[0]
    dropoff_location = Location.objects.filter(pk=req_dropoff_location)[0]

    duration = (strtoDate(req_dropoff_date)-strtoDate(req_pickup_date)).days

    rentals = CarRental.objects.filter(Location_id=pickup_location.pk)
    nonavaila = CarRentalTime.objects.filter(StartRentalTime__lte=strtoDate(req_dropoff_date))
    nonavaila = nonavaila.filter(StartRentalTime__gte=strtoDate(req_pickup_date))
    nonavailb = CarRentalTime.objects.filter(EndRentalTime__lte=strtoDate(req_dropoff_date))
    nonavailb = nonavailb.filter(StartRentalTime__gte=strtoDate(req_pickup_date))
    nonavailc = CarRentalTime.objects.filter(StartRentalTime__lte=strtoDate(req_pickup_date))
    nonavailc = nonavailc.filter(EndRentalTime__gte=strtoDate(req_dropoff_date))
    nonavail = nonavaila | nonavailb | nonavailc
    for nona in nonavail:
        rentals=rentals.exclude(pk=nona.Car_id)
    if len(rentals) == 0:
        rentals = None

    context = {
        'rtype' : rtype,
        'src' : req_pickup_location,
        'srcdate' : req_pickup_date,
        'dest' : req_dropoff_location,
        'retdate' : req_dropoff_date,
        'pickup' : pickup_location,
        'dropoff' : dropoff_location,
        'pageheader' : header,
        'rentals' : rentals,
        'duration' : duration
    }
    return context

def passenger(request):
    header = 'Passenger Information'
    if request.method == 'POST':
        rtype = request.GET.get('type')
        if rtype == 'flight':
            trip = request.GET.get('trip')
            tickets = request.GET.get('tickets')
            flight_class = request.GET.get('class')
            toflight = request.GET.get('toflight')
            fromflight = request.GET.get('fromflight')
            num = int(request.GET.get('num'))
            form = PassengerForm(request.POST)
            if form.is_valid():
                if num == 1:
                    group = Group(size=int(tickets))
                    group.save()
                    group = group.pk
                else:
                    group = int(request.GET.get('groupid'))
                passenger = Passenger(FirstName=form['first_name'].data, LastName=form['last_name'].data, Email=form['email'].data, Gender=form['gender'].data, GroupId_id=group)
                passenger.save()
                if num == int(tickets):
                    link = '/payment/?type='+rtype+'&tickets='+tickets+'&trip='+trip+'&class='+flight_class+'&toflight='+toflight+'&groupid='+str(group)
                    if fromflight != None:
                        link += '&fromflight=' + fromflight
                    return redirect(link)
                else:
                    num+=1
                    link = '/passenger/?type'+rtype+'&trip='+trip+'&class='+flight_class+'&toflight='+toflight+'&num='+str(num)+'&groupid='+str(group)
                    if fromflight != None:
                        link += '&fromflight=' + fromflight
                    return redirect(link)
        elif rtype == 'accomodation':
            form = PassengerForm(request.POST)
            accom = request.GET.get('accom')
            rooms = request.GET.get('rooms')
            guests = request.GET.get('guests')
            checkin = request.GET.get('checkin')
            checkout = request.GET.get('checkout')
            num = int(request.GET.get('num'))
            if form.is_valid():
                if num == 1:
                    group = Group(size=int(guests))
                    group.save()
                    group = group.pk
                else:
                    group = int(request.GET.get('groupid'))

                passenger = Passenger(FirstName=form['first_name'].data, LastName=form['last_name'].data, Email=form['email'].data, Gender=form['gender'].data, GroupId_id=group)
                passenger.save()
                if num == int(guests):
                    link = '/payment/?type='+rtype+'&accom='+accom+'&guests='+guests+'&rooms='+rooms+'&checkin='+checkin+'&checkout='+checkout+'&groupid='+str(group)
                    return redirect(link)
                else:
                    num+=1
                    link='/passenger/?type='+rtype+'&rooms='+rooms+"&guests"+guests+'&checkin='+checkin+'&checkout='+checkout+'&accom='+accom+'&num='+str(num)+'&groupid='+str(group)
                    return redirect(link)
        elif rtype == 'rental':
            form = PassengerForm(request.POST)
            src = request.GET.get('src')
            dest = request.GET.get('dest')
            srcdate = request.GET.get('srcdate')
            retdate = request.GET.get('retdate')
            rental = request.GET.get('rental')
            if form.is_valid():
                group = Group(size=1)
                group.save()
                passenger = Passenger(FirstName=form['first_name'].data, LastName=form['last_name'].data, Email=form['email'].data, Gender=form['gender'].data, GroupId_id=group.pk)
                passenger.save()
                link = '/payment/?type='+rtype+'&src='+src+'&dest='+dest+'&srcdate='+srcdate+'&retdate='+retdate+'&rental='+rental+'&groupid='+str(group.pk)
                return redirect(link)
    else:
        form = PassengerForm()
    return render(request, 'simbapawtrail/passenger.html', {'form' : form, 'pageheader' : header,})

def confirmation(request):
    header = 'Confirmation'
    rtype = request.GET.get('type')
    groupid = int(request.GET.get('groupid'))
    passengers = Passenger.objects.filter(GroupId_id=groupid)
    if (rtype == 'flight'):
        toflight = request.GET.get('toflight')
        fromflight = request.GET.get('fromflight')
        if toflight != None:
            toflight = int(toflight)
            toflight = Flight.objects.filter(pk=toflight)[0]
        if fromflight != None:
            fromflight = int(fromflight)
            fromflight = Flight.objects.filter(pk=fromflight)[0]
        context = {
            'rtype' : rtype,
            'trip' : request.GET.get('trip'),
            'toflight' : toflight,
            'class' : request.GET.get('class'),
            'tickets' :request.GET.get('tickets'),
            'price' : request.GET.get('price'),
            'fromflight' : fromflight,
            'price' : request.GET.get('price'),
            'paymentid' : request.GET.get('paymentid'),
            'passengers' : passengers,
            'pageheader' : header,
        }
    elif (rtype == 'accomodation'):
        accom = int(request.GET.get('accom'))
        accom = Accomodation.objects.filter(pk=accom)[0]
        context = {
            'rtype' : rtype,
            'accom' : accom,
            'guests' : request.GET.get('guests'),
            'rooms' : request.GET.get('rooms'),
            'price' : request.GET.get('price'),
            'checkin' : request.GET.get('checkin'),
            'checkout' : request.GET.get('checkout'),
            'paymentid' : request.GET.get('paymentid'),
            'passengers' : passengers,
            'pageheader' : header,
        }
    elif rtype == 'rental':
        r = int(request.GET.get('rental'))
        rental = CarRental.objects.filter(pk=r)[0]
        groupid = int(request.GET.get('groupid'))
        srcdate = request.GET.get('srcdate')
        retdate = request.GET.get('retdate')
        driver = Passenger.objects.filter(GroupId_id=groupid)[0]
        rentalTime = CarRentalTime(Car_id=r, Driver_id=driver.pk, StartRentalTime=strtoDate(srcdate), EndRentalTime=strtoDate(retdate))
        rentalTime.save()
        context = {
            'rtype' : rtype,
            'src' : request.GET.get('src'),
            'dest' : request.GET.get('dest'),
            'srcdate' : srcdate,
            'retdate' : retdate,
            'rental' : rental,
            'price' : request.GET.get('price'),
            'paymentid' : request.GET.get('paymentid'),
            'passengers' : passengers,
            'pageheader' : header,
            'groupid' : groupid
        }

    return render(request, 'simbapawtrail/confirmation.html', {'context' : context})

def cancellation(request):
    if request.method == 'POST':
        form = CancellationForm(request.POST)
        if form.is_valid():
            paymentid = form['payment_id'].data
            email = form['email'].data
            receipt = Payment.objects.filter(pk=paymentid)[0]
            if (email != receipt.Email):
                linkcont = '?invalid=true'
            else:
                linkcont = '?invalid=false&paymentid='+str(paymentid)
                if (receipt.Type=='flight'):
                    group = receipt.GroupId_id
                    tickets = Group.objects.filter(pk=group)[0]
                    tickets = tickets.size
                    flightgroup = FlightGroup.objects.filter(GroupId_id=group)
                    for fg in flightgroup:
                        flight = Flight.objects.filter(pk=fg.FlightId_id)[0]
                        if (fg.FlightClass == 'First Class'):
                            flight.AvailFirstSeats += tickets
                        elif (fg.FlightClass == 'Business Class'):
                            flight.AvailBusinessSeats += tickets
                        else:
                            flight.AvailEconomySeats += tickets
                        flight.save()
                        fg.delete()
                receipt.delete()
            return redirect('/cancellationconfirmation/'+linkcont)
    else:
        form = CancellationForm()
    return render(request, 'simbapawtrail/cancellation.html', {'form' : form })

def cancellationconfirmation(request):
    paymentid = request.GET.get('paymentid')
    if paymentid != None:
        paymentid = int(paymentid)
    context = { 'invalid' : request.GET.get('invalid'),
                'paymentid' : paymentid,
    }
    return render(request, 'simbapawtrail/cancellationconfirmation.html', {'context' : context})
