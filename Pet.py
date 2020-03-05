import time
from random import randrange
from collections import defaultdict
from threading import Thread, Event
from random import choices
from pyfiglet import figlet_format as fig
from tqdm import tqdm


class Pet:
    raw_stats = {('energy', 'val'): 0,  # to be worked on
                 ('energy', 'max'): 100,
                 ('happiness', 'val'): 0,
                 ('happiness', 'max'): 100,
                 ('hunger', 'val'): 0,
                 ('hunger', 'max'): 100,
                 ('snack meter', 'val'): 1,
                 ('snack meter', 'min'): 1}

    stop_threads = False
    is_alive = True
    lifetime = 0

    def __init__(self, name, kind, game_manager):
        self.name = name
        self.kind = kind

        # transforms the data in raw_stats into a nested dictionary
        self.stats = defaultdict(dict)
        for (attribute, detail), val in self.raw_stats.items():
            self.stats[attribute][detail] = val

        # assigns initial values for stats into nested dictionary with
        # randomized values
        self.stats["energy"]["val"] = randrange(50, 90)
        self.stats["happiness"]["val"] = randrange(50, 90)
        self.stats["hunger"]["val"] = randrange(50, 90)

        self.thread_event = Event()
        self.thread_event.set()  # activates the while loop in decrease_stats.

        self.thread = Thread(
            target=self.decrease_stats, args=(self.thread_event,)
        )
        self.thread.start()

        self.game_manager = game_manager

    def decrease_stats(self, thread_event):
        """Decreases stat values every 60 seconds.

        Keyword arguments:
        thread_event -- a threading.Event() object

        Whilst the thread_event is set to be true, all of the stats of the pet will decrease, either randomly or with a set value, after every 60 seconds. The lifetime is also recorded in minutes. After each change, all values will be evaluated with the check_status() method to ensure that the pet is indeed still alive. Once the game ends, thread_event is then set to false, which ends the while loop.
        """
        frequency = 60  # how many seconds until stat change is in effect.
        last_change = time.time()
        while thread_event.is_set():
            if (time.time() - last_change) > frequency:
                last_change = time.time()
                self.lifetime += 1  # in minutes
                for attr in self.stats:
                    if attr == 'snack meter':
                        self.add_to_stat(attr, -1, False)
                    else:
                        self.add_to_stat(attr, (-1 * randrange(30)), False)

                self.check_status()

    def display_stats(self):
        for key, val in self.stats.items():
            # val = {'max': ..., 'val': ...}, or without the 'max'
            if 'max' in val:
                print(key + ": " + str(val['val']) + "/" + str(val['max']))
            else:
                print(key + ": " + str(val['val']))

    def sleep(self):
        print(f'<(  u _ u )>\n{self.name} is sleeping...')
        self.sleep_animation()
        print(f'<( o  o )>\n{self.name} is awake!')
        self.add_to_stat("energy", 30)

    def sleep_animation(self):
        time.sleep(randrange(60))

    def fed_bread(self):
        print('    bread\n    ^  ^\n( o  o )')
        time.sleep(0.5)
        print('<( o <ead> o )>\nyummy!')
        self.add_to_stat("hunger", randrange(15))

    def fed_snack(self):
        print('    snack\n    ^  ^\n( o  o )')
        time.sleep(0.5)
        print('<( o <ead> o )>\nyummy!')
        self.add_to_stat("hunger", randrange(15))
        self.add_to_stat("snack meter", 1)
        self.add_to_stat("happiness", randrange(10))

    def pet(self):
        print('^( o  o )>')
        time.sleep(0.5)
        print('<( o  o )^')
        self.add_to_stat("happiness", randrange(10))

    def feelings(self):
        threshold = self.stats['happiness']['max'] / 2
        if self.stats['happiness']['val'] >= threshold:
            print('<( ^ ^ )>\ni am very happy!')
        elif self.stats['happiness']['val'] < threshold:
            print('<( o  o )>\nfeeling okay!')

    def transfer(self):
        transferSure = input(f'\nAre you sure you want to transfer {self.name}?\nThis cannot be undone!\nEnter this to continue:\nI am sure I want to transfer my pet.\n')
        if transferSure == 'I am sure I want to transfer my pet.':
            transferTime = randrange(10)
            print(f'\nTransferring {self.name}...\nThis should take about {transferTime} second(s).')
            for i in tqdm(range(transferTime), desc='Transferring'):
                time.sleep(1)
            print(f'{self.name}, a {self.kind}, has been transferred.\nGoodbye, {self.name} :(')
            time.sleep(2)
            quit()
        else:
            print(f'Transfer of {self.name} has been cancelled.')

    def add_to_stat(self, attr, value=100, display=True):
        attribute = self.stats[attr]
        attribute['val'] += value
        if 'max' in attribute and attribute['val'] >= attribute['max']:
            attribute['val'] = attribute['max']
        if 'min' in attribute and attribute['val'] <= attribute['min']:
            attribute['val'] = attribute['min']
        if display:
            print(attr + " is now at " + str(attribute['val']))

        if attr == 'snack meter' and self.stats['snack meter']['val'] > 5:
            print(f'{self.name} has died from severe sugar intake. :(')
            self.die()

    def check_status(self):
        if self.stats['energy']['val'] < 50:
            print('<(-  -)> i\'m tired')
        if self.stats['hunger']['val'] < 50:
            print('<(o  O  o)> i\'m hungry')
        if self.stats['happiness']['val'] < 50:
            print('<(T  T)> i\'m sad')

        if self.stats['energy']['val'] < 0:
            print(f'{self.name} has died due to being too tired. :(')
            self.die()
        elif self.stats['hunger']['val'] < 0:
            print(f'{self.name} has died due to hunger. :(')
            self.die()
        elif self.stats['happiness']['val'] < 0:
            print(f'{self.name} has died due to sadness. :(')
            self.die()
        elif self.stats['snack meter']['val'] > 5:
            print(f'{self.name} has died from severe overeating. :(')
            self.die()

    def play_game1(self):
        self.game_manager.display_fig("DIRECTION GAME")

        answers = ['L', 'R']
        L_or_R = choices(answers)[0]  # choices() returns an array

        guess = self.game_manager.get_user_input(
            'guess if i will go left or right!(L/R)'
        )

        while guess not in answers:
            print('that\'s not a valid answer!')
            guess = self.game_manager.get_user_input(
                'guess if i will go left or right!(L/R)'
            )

        if guess == L_or_R:
            print('congrats! you were right!<( ^ o ^)>')
            self.add_to_stat("happiness", randrange(30))
        else:
            print('sorry. you were wrong. <( o  o )>')
            self.add_to_stat("happiness", randrange(20))

    def die(self):
        print(f'your pet lived for {self.lifetime} minutes.')
        self.is_alive = False
        self.game_manager.quit()
