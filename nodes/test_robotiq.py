#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import signal
from argonne_final_project.RobotiqHand import RobotiqHand

#------------------------------------------------------------------------------
# test_robotiq.py
#------------------------------------------------------------------------------
HOST = "192.168.12.248"
PORT = 54321

cont = True

def handler(signal, frame):
    global cont
    cont = False

def test_robotiq():
    print 'test_robotiq start'
    hand = RobotiqHand()
    hand.connect(HOST, PORT)

    try:
        print 'activate: start'
        # hand.reset()
        hand.activate()
        result = hand.wait_activate_complete()
        print 'activate: result = 0x{:02x}'.format(result)
        if result != 0x31:
            hand.disconnect()
            return
        # print 'adjust: start'
        # hand.adjust()
        # print 'adjust: finish'

        # while cont:
        print 'close slow'
        hand.move(255, 100, 10)
        (status, position, force) = hand.wait_move_complete()
        position_mm = hand.get_position_mm(position)
        force_mA = hand.get_force_mA(force)

        if status == 0:
            print 'no object detected: position = {:.1f}mm, force = {:.1f}mA '.format(position_mm, force_mA)
        elif status == 1:
            print 'object detected closing: position = {:.1f}mm, force = {:.1f}mA '.format(position_mm, force_mA)
            print 'keeping'
            time.sleep(5)
        elif status == 2:
            print 'object detected opening: position = {:.1f}mm, force = {:.1f}mA '.format(position_mm, force_mA)
        else:
            print 'failed'

        print 'open fast'
        hand.move(0, 0, 0)
        (status, position, force) = hand.wait_move_complete()
        position_mm = hand.get_position_mm(position)
        force_mA = hand.get_force_mA(force)
        print 'position = {:.1f}mm, force = {:.1f}mA '.format(position_mm, force_mA)
    except:
        print 'Ctrl-c pressed'

    hand.disconnect()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    test_robotiq()
