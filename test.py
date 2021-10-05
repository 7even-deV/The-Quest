def ai(self):
        if not self.idling and random.randint(0, 100) == 0:
            self.idling = True
            self.idling_counter = 100
            print(True)
        else:
            if not self.idling:
                if self.direction_x == 1:
                    self.ai_moving_right = True
                else: self.ai_moving_right = False
                if self.direction_x == -1:
                    self.ai_moving_left = True
                else: self.ai_moving_left = False

                # self.ai_moving_left = not self.ai_moving_right
                # self.move_counter += 1

                # if self.move_counter > self.rect.width:
                #     self.direction_x *= -1
                #     self.move_counter *= -1
            else:
                self.idling_counter -= 1
                if self.idling_counter <= 0:
                    self.idling = False

        # print(self.move_counter)



class Timer():

    def __init__(self):
        self.counter = 0
        self.aux = 1

    def time(self, timer, *events):
        self.counter += 1
        if self.counter > timer * 100:
            self.counter = 0
            return events

    def total_time(self, get_ticks):
        ticks = get_ticks // 1000
        if self.aux == ticks:
            self.aux += 1
            return print(ticks)

self.timer = Timer(pygame.time.get_ticks()) # Create self.timer
