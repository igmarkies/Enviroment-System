import time

counter = 30
start = time.time()
while True:
    ### Do other stuff, it won't be blocked
    time.sleep(0.1)
    #print ("looping...")

    ### When 1 sec or more has elapsed...
    if time.time() - start > 1:
        start = time.time()
        counter -= 1

        ### This will be updated once per second
        print ("%s seconds remaining" % counter)

        ### Countdown finished, ending loop
        if counter <= 0:
            break