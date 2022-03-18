import random

import faker_commerce
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import address, date_time
from rest_framework.authtoken.models import Token
from weddingapi.helpers import CITIES
# from weddingapi.helpers import STATES
from weddingapi.models import (Host, Rating, Review, Vendor, VendorType,
                               VendorWeddingSize, WeddingSize)
from weddingapi.models.host_vendor import HostVendor
from weddingapi.models.message import Message


class Command(BaseCommand):
    # Faker: Python package for generating random data
    faker = Faker()
    # Each Faker provider has different types of random data available
    faker.add_provider(faker_commerce.Provider)
    faker.add_provider(date_time)
    faker.add_provider(address)

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument(
            '--vendor_count',
            help='Count of vendors to seed',
        )

    def handle(self, *args, **options):
        # if a user count was passed in, use that count as the arg for create_users,
        if options['vendor_count']:
            self.create_users(int(options['vendor_count']))
        # otherwise just call create_users, which uses a default vendor_count of 8
        else:
            self.create_users()

    def create_users(self, vendor_count=100):
        """Create random users"""
        for _ in range(10):
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            username = f'{first_name}_{last_name}'
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                password="password",
                username=username,
                is_staff=False
            )

            Host.objects.create(
                user=user,
                wedding_size=WeddingSize.objects.get(pk=random.randint(1, 3)),
                date=random.choice(
                    ["2022-01-01", "2022-04-25"]),
                time=self.faker.time(),
                street_address=self.faker.street_address(),
                city=random.choice(CITIES),
                state="TN",
                # city=self.faker.city(),
                # state=random.choice(STATES),
                zip_code=self.faker.postcode()[0:5],
                profile_image=random.choice(["hostprofile/image1.jpeg", "hostprofile/image2.jpeg"])
            )

            Token.objects.create(
                user=user
            )

        for _ in range(vendor_count):
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            username = f'{first_name}_{last_name}'
            vendor = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                password="password",
                username=username,
                is_staff=True
            )

            Vendor.objects.create(
                user=vendor,
                vendor_type=VendorType.objects.get(
                    pk=random.randint(1, VendorType.objects.count())),
                business_name=self.faker.ecommerce_name(),
                city=random.choice(CITIES),
                state="TN",
                # city=self.faker.city(),
                # state=random.choice(STATES),
                zip_code=self.faker.postcode()[0:5],
                description=self.faker.paragraph(),
                years_in_business=random.randint(1, 150),
                profile_image=random.choice(["vendorprofile/image1.jpg", "vendorprofile/image2.jpeg"])
            )

            Token.objects.create(
                user=vendor
            )

        hosts = Host.objects.all()
        vendors = Vendor.objects.all()

        for host in hosts:
            self.create_ratings(host, vendors)
            self.create_reviews(host, vendors)
            self.create_contracts(host, vendors)
            self.create_messages_from_host(host, vendors)

        for vendor in vendors:
            self.create_vendor_wedding_sizes(vendor)
            self.create_messages_from_vendor(vendor, hosts)

    def create_ratings(self, host, vendors):
        """_summary_

        """
        if host.id % 2 == 0 or host.id % 3 == 0:
            for vendor in vendors:
                Rating.objects.create(
                    vendor=vendor,
                    host=host,
                    score=random.randint(1, 5)
                )

    def create_reviews(self, host, vendors):
        """_summary_

        """
        if host.id % 2 == 0 or host.id % 3 == 0:
            for vendor in vendors:
                Review.objects.create(
                    vendor=vendor,
                    host=host,
                    body=self.faker.paragraph(),
                    time_sent=self.faker.date_time()
                )

    def create_contracts(self, host, vendors):
        """_summary_

        """
        if host.id % 2 == 0 or host.id % 3 == 0:
            for vendor in vendors:
                random_cost = random.choice(
                    [None, round(random.uniform(33.33, 250.25), 2)])
                if random_cost is None:
                    random_hire = False
                else:
                    random_hire = random.choice([False, True])
                HostVendor.objects.create(
                    vendor=vendor,
                    host=host,
                    cost_per_hour=random_cost,
                    hired=random_hire,
                    fired=False
                )

    def create_vendor_wedding_sizes(self, vendor):
        """_summary_

        """
        num_preferences = random.randint(1, 3)

        if num_preferences > 1:
            for x in range(1, num_preferences):
                VendorWeddingSize.objects.create(
                    vendor=vendor,
                    wedding_size=WeddingSize.objects.get(pk=x)
                )
        elif vendor.id % 2 == 0:
            VendorWeddingSize.objects.create(
                vendor=vendor,
                wedding_size=WeddingSize.objects.get(pk=3)
            )
        else:
            VendorWeddingSize.objects.create(
                vendor=vendor,
                wedding_size=WeddingSize.objects.get(pk=1)
            )

    def create_messages_from_host(self, host, vendors):
        """_summary_

        """
        if host.id % 2 == 0 or host.id % 3 == 0:
            for vendor in vendors:
                if vendor.id % 2 == 0:
                    Message.objects.create(
                        vendor=vendor,
                        host=host,
                        sender=host.user,
                        body=self.faker.paragraph(),
                        time_sent=self.faker.date_time()
                    )

    def create_messages_from_vendor(self, vendor, hosts):
        """_summary_

        """
        if vendor.id % 2 == 0:
            for host in hosts:
                if host.id % 2 == 0 or host.id % 3 == 0:
                    Message.objects.create(
                        host=host,
                        vendor=vendor,
                        sender=vendor.user,
                        body=self.faker.paragraph(),
                        time_sent=self.faker.date_time()
                    )
