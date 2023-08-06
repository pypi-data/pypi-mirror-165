'''
 #####
#     #  ####   ####  #   ##   #      #      #   #
#       #    # #    # #  #  #  #      #       # #
 #####  #    # #      # #    # #      #        #
      # #    # #      # ###### #      #        #
#     # #    # #    # # #    # #      #        #
 #####   ####   ####  # #    # ###### ######   #

######
#     # ###### ##### ###### #####  #    # # #    # ###### #####
#     # #        #   #      #    # ##  ## # ##   # #      #    #
#     # #####    #   #####  #    # # ## # # # #  # #####  #    #
#     # #        #   #      #####  #    # # #  # # #      #    #
#     # #        #   #      #   #  #    # # #   ## #      #    #
######  ######   #   ###### #    # #    # # #    # ###### #####
'''

"""
This module contains simple, general functions for a variety of uses.
"""

import matplotlib.pyplot as plt
import datetime
import math
import numpy as np
import pandas as pd

def set_sd_plots():
  """
  Set matplotlib parameters for standardized plots.

  Sets the size of the fonts for the legend, axes, and ticks.
  """
  params = {'legend.fontsize': 'xx-large',
          'legend.title_fontsize': 'xx-large',
          'figure.figsize': (27, 18),
          'axes.labelsize': 'xx-large',
          'axes.titlesize':'xx-large',
          'xtick.labelsize':'xx-large',
          'ytick.labelsize':'xx-large'}
          
  plt.rcParams.update(params)


def time_since_date(start_date, end_date = None, unit = None, round_option = None, str_format = None):
  """
  Calculate the time since a given date.

  Given a date or list of dates, we can calculate the time since that date in years, months, days,
  hours or seconds.  This function offers the option to round up, down, or to an exact decimal value.
  The format in which the dates are provided is optional.

  The principle use case for this function is calculating an Age based on a given Date of Birth
  and the current date, so the default parameters are set according to this use.

  Args:
      start_date: (String or List of Strings) The start date or a list of start dates to be computed.
      end_date: (String, optional) The end date by which to calculate a time difference.
      unit: (String, optional) One of ['YEARS', ‘MONTHS’, ‘DAYS’, ‘HOURS’, ‘SECONDS’].
      round_option: (String, optional) One of ['UP', ‘DOWN’, ‘EXACT’]
      str_format: (String, optional) The format string that specifies the input date format.

  Returns:
      Int, Float, List of Ints, or List of Floats
        Computed time between the start date and end date.
  """
  unit_vals = {'YEARS': 'Y', 'MONTHS': 'M', 'DAYS': 'D',
                  'HOURS': 'h', 'SECONDS': 's'}
  unit = 'Y' if unit is None else unit_vals[unit.upper()]
  round_option = 'DOWN' if round_option is None else round_option.upper()
  str_format = '%Y-%m-%d' if str_format is None else str_format
  end_date = datetime.date.today().strftime('%Y-%m-%d') if end_date is None \
              else datetime.datetime.strptime(end_date, str_format)
  end_date = pd.Timestamp(end_date)
      
  if type(start_date) == str:
      start_date = datetime.datetime.strptime(start_date, str_format)
      start_date = pd.Timestamp(start_date)
          
      diff = (end_date - start_date)/np.timedelta64(1, unit)
          
      diff = {
          'DOWN': math.floor(round(diff,1)),
          'UP': math.ceil(round(diff,1)),
          'EXACT': round(diff, 2)
      }[round_option]
          
  else:
      start_date = map(lambda x: datetime.datetime.strptime(x, str_format), start_date)
      start_date = map(lambda x: pd.Timestamp(x), start_date)
      
      diff = map(lambda x: (end_date - x)/np.timedelta64(1, unit), start_date)
          
      diff = {
          'DOWN': map(lambda x: math.floor(round(x,1)), diff),
          'UP': map(lambda x: math.ceil(round(x,1)), diff),
          'EXACT': map(lambda x: round(x, 2), diff)
      }[round_option]
          
      diff = list(diff)
      
  return diff