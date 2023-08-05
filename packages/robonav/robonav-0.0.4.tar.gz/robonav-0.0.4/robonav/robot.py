class Robot(object):

    def __init__(self,model):
        self.model = model
        # Initial position is (0,0)
        self.x = 0
        self.y = 0

    def print_menu(self):
        print(f"Current location: {self.x},{self.y}")
        print("List of available directions:")
        for i,command in enumerate(self.model.commands):
            print(i+1,'-', command.direction)
        print('q - quit')
        print("Input the number correponding to the direction:")

    def get_inputs(self):
        steps=input()
        try:
            if steps == 'q':
                print('No movement')
                return
            else:
                return steps
        except Exception:
            print('Invalid input')
        

    def command(self,comm):
        if comm.direction=='initial':
            print('Give co-ordinates in x,y format')
            received_inputs = self.get_inputs()
            steps=received_inputs if received_inputs is not None else '0,0'
            self.x=int(steps.split(',')[0])
            self.y=int(steps.split(',')[1])
        else:
            print(f"How many steps you want to go {comm.direction}")
            received_inputs = self.get_inputs()
            steps=received_inputs if received_inputs is not None else '0'
            steps=int(steps)
            move = {
                    "up": (0, 1),
                    "down": (0, -1),
                    "left": (-1, 0),
                    "right": (1, 0)
                }[comm.direction]
            # Calculate new robot position
            self.x += steps * move[0]
            self.y += steps * move[1]       

    def __str__(self):
        return f"Robot position is {self.x}, {self.y}."

    def interpret(self):
        self.print_menu()
        while True:
            try:
                command=input()
                if command == 'q':
                    return
                elif int(command)<=len(self.model.commands):                    
                    command = int(command)
                    command = self.model.commands[command - 1] 
                    self.command(command)
                else:
                    print('Invalid input')              
                    
            except Exception:
                print('Something happened!')
            
            self.print_menu()       

            
