class OutputFormat:
    def __init__(self, i_f, i_t):
        self.i_f = i_f
        self.i_t = i_t

    def display(self):
        print(f"Current needed for target torque: I_x = {self.i_t[0]}, I_y = {self.i_t[1]}, I_z = {self.i_t[2]}")
        print(f"Current needed for target force: I_x = {self.i_f[0]}, I_y = {self.i_f[1]}, I_z = {self.i_f[2]}")
