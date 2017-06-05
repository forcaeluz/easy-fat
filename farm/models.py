from django.core.validators import ValidationError

from flocks.models import Flock, AnimalFarmExit, AnimalFlockExit
from buildings.models import Room, AnimalRoomExit, AnimalRoomEntry


class AnimalExit:
    """
    Class that combines Farm, Flock and Room exit information.
    """
    def __init__(self, animal_farm_exit=None):
        self.animal_farm_exit = animal_farm_exit  # AnimalFarmExit
        self.flock_exits = []
        self.room_exits = []

        if animal_farm_exit is not None:
            self.flock_exits = self.animal_farm_exit.animalflockexit_set.all()
            self.room_exits = self.animal_farm_exit.animalroomexit_set.all()

    def set_animal_farm_exit(self, **kwargs):
        instance = kwargs.get('separation', None)
        data = kwargs.get('cleaned_data', None)
        if instance:
            self.animal_farm_exit = instance
            self.flock_exits = self.animal_farm_exit.animalflockexit_set.all()
            self.room_exits = self.animal_farm_exit.animalroomexit_set.all()
        elif data:
            self.animal_farm_exit = AnimalFarmExit(number_of_animals=data['number_of_animals'],
                                                   date=data['date'],
                                                   weight=data['weight'])
        else:
            raise ValueError('Not possible to assign flock information')
        pass

    def set_room_exit_information(self, room_exits_information):
        assert (self.animal_farm_exit is not None)
        date = self.animal_farm_exit.date

        for room_exit_info in room_exits_information:
            room = room_exit_info['room']  # Room
            if len(room.get_flocks_present_at(date)) == 1:
                flock = next(iter(room.get_flocks_present_at(date)))
                room_exit = AnimalRoomExit(number_of_animals=room_exit_info['number_of_animals'],
                                           flock=flock,
                                           date=self.animal_farm_exit.date,
                                           room=room,
                                           farm_exit=self.animal_farm_exit)
                self.room_exits.append(room_exit)
            else:
                print(room.get_flocks_present_at(date))
                raise ValueError('Unable to handle rooms with more than one flock.')

        self.__generate_flock_exits()

    def __generate_flock_exits(self):
        flock_info = {}
        date = self.animal_farm_exit.date
        for room_exit in self.room_exits:
            if len(room_exit.room.get_flocks_present_at(date)) == 1:
                flock = next(iter(room_exit.room.get_flocks_present_at(date)))
                flock_info.update({flock: flock_info.get(flock, 0) + room_exit.number_of_animals})
            else:
                raise ValueError('Unable to handle rooms with multiple flocks present.')

        for flock, number_of_animals in flock_info.items():
            flock_exit = AnimalFlockExit(flock=flock,
                                         farm_exit=self.animal_farm_exit,
                                         number_of_animals=number_of_animals,
                                         weight=self.animal_farm_exit.average_weight * number_of_animals)

            self.flock_exits.append(flock_exit)

    def clean(self):
        self.animal_farm_exit.clean()

    def save(self):
        self.animal_farm_exit.save()

        for flock_exit in self.flock_exits:
            flock_exit.farm_exit = self.animal_farm_exit
            flock_exit.save()

        for room_exit in self.room_exits:
            room_exit.farm_exit = self.animal_farm_exit
            room_exit.save()


class AnimalEntry:
    """
    Class that combines RoomEntry and Flock Information.
    
    This class is used to create or edit RoomEntry and Flock Information.
    """
    def __init__(self, flock=None):
        self.flock = flock
        if self.flock is not None:
            self.room_entries = flock.animalroomentry_set.all()
        else:
            self.room_entries = []

    def set_flock(self, **kwargs):
        instance = kwargs.get('separation', None)
        data = kwargs.get('cleaned_data', None)
        if instance:
            self.flock = instance
            self.room_entries = self.flock.animalroomentry_set.all()
        elif data:
            self.flock = Flock(number_of_animals=data['number_of_animals'],
                               entry_date=data['date'],
                               entry_weight=data['weight'])
        else:
            raise ValueError('Not possible to assign flock information')

    def update_flock(self, data):
        assert(self.flock is not None)
        self.flock.number_of_animals = data['number_of_animals']
        self.flock.entry_date = data['date']
        self.flock.entry_weight = data['weight']
        for room_entry in self.room_entries:
            room_entry.date = self.flock.entry_date

    def set_room_entries(self, room_entries_info):
        assert(self.flock is not None)
        for room_entry_info in room_entries_info:
            room_entry = AnimalRoomEntry(number_of_animals=room_entry_info['number_of_animals'],
                                         flock=self.flock,
                                         date=self.flock.entry_date,
                                         room=room_entry_info['room'])
            self.room_entries.append(room_entry)

    def update_room_entries(self, room_entries_info):
        assert(self.flock is not None)
        existing_list = [obj.room for obj in self.room_entries]
        # The final list
        final_list = [obj['room'] for obj in room_entries_info]
        # Rooms to be deleted
        delete_list = [obj.room for obj in self.room_entries if obj.room not in final_list]
        # Rooms to be added
        add_list = [obj['room'] for obj in room_entries_info if obj['room'] not in existing_list]
        # Rooms to be updated
        update_list = [obj for obj in final_list if obj not in add_list]

        # Delete entries
        for room_entry in self.room_entries:
            if room_entry.room in delete_list:
                room_entry.delete()

        # Only the update list should be in here now.
        self.room_entries = self.flock.animalroomentry_set.all()
        for room_entry in self.room_entries:
            assert(room_entry.room in update_list)
            for new_room_info in room_entries_info:
                if new_room_info['room'] == room_entry.room:
                    room_entry.number_of_animals = new_room_info['number_of_animals']
                    room_entry.date = self.flock.entry_date

        for room in add_list:
            for new_room_info in room_entries_info:
                if new_room_info['room'] == room:
                    room_entry = AnimalRoomEntry(number_of_animals=new_room_info['number_of_animals'],
                                                 flock=self.flock,
                                                 date=self.flock.entry_date,
                                                 room=new_room_info['room'])
                    self.room_entries.append(room_entry)

    def clean(self):
        count = 0
        self.flock.full_clean()
        for room_entry in self.room_entries:
            count += room_entry.number_of_animals

        if count != self.flock.number_of_animals:
            raise ValidationError('Something went wrong.')

    def save(self):
        self.flock.save()
        for room_entry in self.room_entries:
            room_entry.flock = self.flock
            room_entry.save()

    def delete(self):
        self.flock.delete()
