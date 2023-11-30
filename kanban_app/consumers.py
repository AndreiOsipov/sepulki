# chat/consumers.py
import json
import datetime
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer
from .models import Sepulka,Shmurdik, Grymzik
import json

def set_datetime_proccessd(sepulka):
    if sepulka.datetime_proccessd != None:
        return sepulka.datetime_proccessd.isoformat()
    

SEPULKA_FIELD_DICT = {
    "id": lambda sepulka: str(sepulka.id),
    "hot": lambda sepulka: sepulka.hot,
    "soft": lambda sepulka: sepulka.soft,
    "square_or_small": lambda sepulka: sepulka.square_or_small,
    "size": lambda sepulka: sepulka.size,
    "state": lambda sepulka: sepulka.state,
    'grymzik': lambda sepulka: sepulka.get_grymzik_id_or_none(),
    'datetime_created': lambda  sepulka: sepulka.datetime_created.isoformat(),
    'datetime_proccessd': set_datetime_proccessd
}

GRYMZIK_FIELD_DICT = {
    "id": lambda grymzik: str(grymzik.id)
}

def get_items_list(items, field_items_dict:dict, objects_name):
    pre_json_list = []
    for item in items:
        pre_json_list.append({json_field: field_items_dict[json_field](item) for json_field in field_items_dict.keys()})
    return {"data_objects":objects_name,"data":pre_json_list}

class SepulkaCreateConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        self.commands = {
            'create':self.create_sepulkas,
            'update':self.update_sepulkas,
            'show':self.show_sepulkas,
            'rebuild_sepulka_card':self.rebuild_sepulka_card,
            'setup_grymzik':self.setup_grymzik,
            'remove_grymzik':self.remove_grymzik,
            'show_grymziks_sepulka':self.show_grymziks_sepulka,
            'change_sepulka_state':self.change_sepulka_state,
            'show_pre_delivired_sepulkas':self.show_pre_delivired_sepulkas
        }
        super().__init__(*args, **kwargs)
    
    def show_pre_delivired_sepulkas(self, content):
        sepulkas = Sepulka.objects.filter(state="D").order_by("-datetime_proccessd")
        sepulkas_dict = get_items_list(sepulkas, SEPULKA_FIELD_DICT, 'ready_for_deliver')
        self.send(json.dumps(sepulkas_dict))
    
    def show_grymziks_sepulka(self, content):
        grymzik = Grymzik.objects.get(id=content['grymzik_id'])
        # print(grymzik.sepulka)
        if hasattr(grymzik,'sepulka'):
            answer = json.dumps({
                "data_objects":"ONE",
                "sepulka_id": grymzik.sepulka.id,
                'state': grymzik.sepulka.state})
            print(answer)
            self.send(answer)
            

    def change_sepulka_state(self, content):
        sepulka = Sepulka.objects.get(id=content['sepulka_id'])
        # print(f'состояние изменено: {sepulka.state}')
        if not(content['state'] == "D" and sepulka.state == "V"):
            sepulka.state = content["state"]
            if sepulka.state == "D":
                sepulka.datetime_proccessd = datetime.datetime.now()
                sepulka.grymzik = None
            sepulka.save()
        async_to_sync(self.channel_layer.group_send)(
            self.kanban_group_name, {"type": "show.sepulkas"}
        )


    def remove_grymzik(self, content):
        sepulka = Sepulka.objects.get(id=content['sepulka_id'])
        sepulka.grymzik = None
        sepulka.save()
        async_to_sync(self.channel_layer.group_send)(
            self.kanban_group_name, {"type": "show.sepulkas"}
        )
        
    def setup_grymzik(self, content):
        sepulka = Sepulka.objects.get(id=content['sepulka_id'])
        grymzik = Grymzik.objects.get(id=content['grymzik_id'])
        if not(hasattr(grymzik, 'sepulka')):
            sepulka.grymzik = grymzik
            if sepulka.state == "C":
                sepulka.state = "V"
            sepulka.save()
        print('state',sepulka.state)
        async_to_sync(self.channel_layer.group_send)(
            self.kanban_group_name, {"type": "show.sepulkas"}
        )

    def rebuild_sepulka_card(self, content):

        sepulka = Sepulka.objects.get(id=content['sepulka_id'])
        grymziks = [grymzik for grymzik in Grymzik.objects.all() if not(hasattr(grymzik, 'sepulka'))]
        grymziks_on_card = get_items_list(grymziks, GRYMZIK_FIELD_DICT, "grymziks")
        if sepulka.grymzik != None:
            grymziks_on_card["current_grymzik_id"] = sepulka.grymzik.id
        else:
            grymziks_on_card["current_grymzik_id"] = None
        
        print(json.dumps(grymziks_on_card))
        self.send(json.dumps(grymziks_on_card))

    def create_sepulkas(self, content):
        shmurdik = Shmurdik.objects.filter(id=content['shmurdik_id']).first()

        Sepulka.objects.create(
            hot=content['hot'],
            soft=content['soft'],
            square_or_small=content['square_or_small'],
            size=content['size'],
            shmurdik=shmurdik,
            datetime_created=datetime.datetime.now(),
            state='C'
        ).save()
        async_to_sync(self.channel_layer.group_send)(
            self.kanban_group_name, {"type": "show.sepulkas"}
        )
        

    def update_sepulkas(self, content):
        sepulka_id = content.pop('sepulka_id')
        print(f"id: {sepulka_id}")
        try:
            sepulka = Sepulka.objects.get(id=sepulka_id)
            sepulka.hot = content['hot']
            sepulka.soft = content['soft']
            sepulka.square_or_small = content['square_or_small']
            sepulka.size = content['size']
            sepulka.save()
            print('сепулька обновлена')
        except:
            pass
        async_to_sync(self.channel_layer.group_send)(
            self.kanban_group_name, {"type": "show.sepulkas"}
        )

    def show_sepulkas(self, content):
        all_sepulkas = Sepulka.objects.all()
        sepulkas = get_items_list(all_sepulkas, SEPULKA_FIELD_DICT, "sepulkas")
        # print()
        self.send(text_data=json.dumps(sepulkas))
 

    def retrive_command_handler(self, command):
        if command in self.commands:
            return self.commands[command]
        raise Exception()

    def connect(self):
        self.kanban_group_name = 'sepulka_create_canban'
        async_to_sync(self.channel_layer.group_add)(
            self.kanban_group_name, self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        content = json.loads(text_data)
        print('CONTENT TYPE ',type(content))
        print(content.items())
        command_handler = self.retrive_command_handler(content.pop('command'))
        command_handler(content)

    def disconnect(self, close_code):
        pass