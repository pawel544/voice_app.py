import time


def record_timer(window,pause_event, stop_event,):

    if stop_event:
        last_update_time = 0
        start = time.time()
        pauza_time= None
        pauza_total=0

        while not stop_event.is_set():

            if pause_event.is_set():
                if pauza_time is None:
                    pauza_time= time.time()

                time.sleep(0.1)
                continue
            elif pauza_time is not None:
                pauza_total += time.time() - pauza_time
                #pause_event.wait()
                #pauza_total += time.time()
                pauza_time = None
            elapse = (time.time() - start)- pauza_total
            if elapse - last_update_time > 0.2:
                window.write_event_value('-TIMER-', f"{elapse:.2f}")
                last_update_time = elapse
                time.sleep(0.05)