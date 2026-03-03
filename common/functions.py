# -*- coding: utf-8 -*-
# VAPT Security Platform

import time


def epoch_to_date(epoch):
    """
    INPUT: Integer epoch
    OUTPUT: Date in %Y-%m-%d %H:%M:%S format
    """

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(epoch))


def current_epoch():
    """
    INPUT: None
    OUTPUT: Current epoch time
    """

    return int(time.time())
