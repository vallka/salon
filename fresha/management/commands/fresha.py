import requests
from django.core.management.base import BaseCommand, CommandError

from fresha.models import Category,Group,Item

class Command(BaseCommand):
    help = 'update fresha'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print (self.help)
        r=requests.get('https://api.fresha.com/locations/805208/marketplace-offer?context=booking-flow')

        data=r.json()['data']
        included=r.json()['included']

        #"""
        for i in included:
            if i['type']=='offer-item-categories':
                print(i['type'], i['id'], i['attributes']['name'],i['attributes']['position'])
                try:
                    category = Category.objects.get(id=i['id'])
                    category.name=i['attributes']['name']
                    category.description=i['attributes']['description']
                    category.position=i['attributes']['position']
                except Category.DoesNotExist:
                    category = Category(id=i['id'],name=i['attributes']['name'],description=i['attributes']['description'],position=i['attributes']['position'])

                category.save()    

            elif i['type']=='offer-item-groups':
                print(i['type'], i['id'], i['attributes']['name'],i['attributes']['position'],i['relationships']['category']['data']['id'])
                id = i['id'][2:]
                try:
                    group = Group.objects.get(id=id)
                    group.name=i['attributes']['name']
                    group.description=i['attributes']['description']
                    group.position=i['attributes']['position']
                    group.category_id=i['relationships']['category']['data']['id']
                except Group.DoesNotExist:
                    group = Group(
                        id=id,
                        name=i['attributes']['name'],
                        description=i['attributes']['description'],
                        position=i['attributes']['position'],
                        category_id=i['relationships']['category']['data']['id']
                    )

                group.save()
        #"""

        for d in data:
            print(d['id'],d['attributes']['name'],d['attributes']['position'],d['relationships']['item-group']['data']['id'],d['attributes']['retail-price'],d['attributes']['duration-for-customer-in-seconds'])
            try:
                item = Item.objects.get(str_id=d['id'])
                item.caption=d['attributes']['caption']
                item.name=d['attributes']['name']
                item.description=d['attributes']['description']
                item.position=d['attributes']['position']
                item.group_id=d['relationships']['item-group']['data']['id'][2:]
                item.price = d['attributes']['retail-price']
                item.duration = d['attributes']['duration-for-customer-in-seconds']
            except Item.DoesNotExist:
                item = Item(
                    str_id=d['id'],
                    caption=d['attributes']['caption'],
                    name=d['attributes']['name'],
                    description=d['attributes']['description'],
                    position=d['attributes']['position'],
                    group_id=d['relationships']['item-group']['data']['id'][2:],
                    price = d['attributes']['retail-price'],
                    duration = d['attributes']['duration-for-customer-in-seconds']
                )
            item.save()
