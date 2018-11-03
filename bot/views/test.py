import sandbox

bad = '''
import time

for i in range(4):
    print(i)
    time.sleep(0.5)
'''

eh = '''
import sys
'''

print(sandbox.execute(bad))
