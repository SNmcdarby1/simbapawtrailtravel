# Generated by Django 4.0.1 on 2022-01-23 13:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('City', models.CharField(max_length=30)),
                ('State', models.CharField(max_length=30)),
                ('Country', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Transportation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Transport_Type', models.CharField(choices=[('Flight', 'Flight'), ('Car', 'Car Rental')], max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarRental',
            fields=[
                ('TransportId', models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='simbapawtrail.transportation')),
                ('Rate', models.IntegerField()),
                ('CarType', models.CharField(max_length=30)),
                ('Location', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='simbapawtrail.location')),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('FlightNumber', models.CharField(max_length=10)),
                ('FlightCarrier', models.CharField(max_length=30)),
                ('FlightPrice', models.IntegerField()),
                ('DepartureTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('ArrivalTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('AvailFirstSeats', models.IntegerField(default=30)),
                ('AvailBusinessSeats', models.IntegerField(default=60)),
                ('AvailEconomySeats', models.IntegerField(default=240)),
                ('TransportId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='simbapawtrail.transportation')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.EmailField(blank=True, max_length=254)),
                ('CardNumber', models.CharField(max_length=16)),
                ('PaymentAmount', models.IntegerField()),
                ('CardExpiryDate', models.CharField(max_length=5)),
                ('Type', models.CharField(blank=True, max_length=15)),
                ('GroupId', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='simbapawtrail.group')),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FirstName', models.CharField(max_length=30)),
                ('LastName', models.CharField(max_length=30)),
                ('Email', models.EmailField(max_length=254)),
                ('Gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male')], default='F', max_length=1)),
                ('GroupId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simbapawtrail.group')),
            ],
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AirportCode', models.CharField(max_length=3)),
                ('AirportName', models.CharField(max_length=100)),
                ('LocationId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simbapawtrail.location')),
            ],
        ),
        migrations.CreateModel(
            name='Accomodation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AccomodationName', models.CharField(default=None, max_length=30)),
                ('AccomodationType', models.CharField(choices=[('Hotel', 'Hotel'), ('Inn', 'Inn'), ('Hostel', 'Hostel'), ('Motel', 'Motel')], default='Hotel', max_length=10)),
                ('Rate', models.DecimalField(decimal_places=2, max_digits=9)),
                ('Discount', models.DecimalField(decimal_places=2, max_digits=2)),
                ('LocationId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simbapawtrail.location')),
            ],
        ),
        migrations.CreateModel(
            name='FlightGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FlightClass', models.CharField(default='Economy', max_length=20)),
                ('GroupId', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='simbapawtrail.group')),
                ('FlightId', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='simbapawtrail.flight')),
            ],
        ),
        migrations.AddField(
            model_name='flight',
            name='ArrivalAirport',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='simbapawtrail.airport'),
        ),
        migrations.AddField(
            model_name='flight',
            name='DepartureAirport',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='Dest_%(class)s', to='simbapawtrail.airport'),
        ),
        migrations.CreateModel(
            name='CarRentalTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StartRentalTime', models.DateField(default=django.utils.timezone.now)),
                ('EndRentalTime', models.DateField(default=django.utils.timezone.now)),
                ('Driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simbapawtrail.passenger')),
                ('Car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simbapawtrail.carrental')),
            ],
        ),
    ]