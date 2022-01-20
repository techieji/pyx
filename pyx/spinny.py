# pylint: skip-file
import itertools, time, threading, sys
class Spinner:
    def __init__(self, dt='Loading...', at='Done.'): self.spinner,self.dt,self.at,self.busy = itertools.cycle('⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'),dt,at,True
    def spin(self):
        while self.busy: [print(f'{next(self.spinner)} {self.dt}', end='\r', flush=True), time.sleep(0.1)]
    def __enter__(self): self.busy, _ = True, threading.Thread(target=self.spin).start()
    def __exit__(self, v1, v2, v3):
        self.busy, _, _ = False, time.sleep(0.1), print(' ' * (len(self.dt) + 2), end='\r')
        return [True, print('❌ Failed: ' + repr(v2)), sys.exit(1)][0] if v1 is not None else print('\r\033[0;32m✓\033[0m ' + self.at)
