# simple command line progres bar with estimated time remaining
#
# Copyright (c) 2013 Olli Erik Keskinen
# All rights reserved.

# This code is released under The BSD 2-Clause License.
# See the file LICENSE.txt for information.

import timeit

class ProgTimer:
    
    def __init__(self):
        self.__start_time = timeit.default_timer()
        self.__percentage = -1
      
    def tick(self, part, total):
        ratio = part/float(total)
        percentage = int(ratio*100)
    
        if percentage != self.__percentage:
    
            delta_time = timeit.default_timer() - self.__start_time
            total_time = delta_time / (ratio + 1e-5)
            remaining_time = total_time - delta_time

            minutes = int(remaining_time/60)
            seconds = int(remaining_time - minutes * 60)
  
            self.__percentage = percentage

            if percentage > 0:
                print percentage, "% - time remaining:",\
                        minutes, "min", seconds, "sec"
            else:
                print percentage, "%"


