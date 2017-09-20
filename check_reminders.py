import discord
import asyncio
from globalvars import *
import time
import csv
import json
from itertools import chain


async def check_reminders():
  await client.wait_until_ready()
  while not client.is_closed:
    for reminder in calendar:
      if int(reminder[0]) <= time.time():
        users = client.get_all_members()
        channels = client.get_all_channels()

        msg_points = chain(users, channels)

        recipient = discord.utils.get(msg_points,id=reminder[1])

        try:
          await client.send_message(recipient,reminder[2])
          print('Administered reminder to ' + recipient.name)
        except:
          print('Couldn\'t find required channel. Skipping a reminder')

        calendar.remove(reminder)

    for inv in intervals:
      if int(inv[0]) <= time.time():
        channels = client.get_all_channels()

        recipient = discord.utils.get(channels,id=inv[2])

        try:
          await client.send_message(recipient,inv[3])
          print('Administered interval to ' + recipient.name)

          print(inv)
          inv[0] = str(int(inv[0]) + int(inv[1])) ## change the time for the next interval
        except:
          print('Couldn\'t find required channel. Skipping an interval')
          intervals.remove(inv)


    with open('calendar.csv','w') as f:
      writer = csv.writer(f,delimiter=',',lineterminator=';')
      writer.writerows(calendar) ## uses a CSV writer to write the data to file.

    with open('intervals.csv','w') as f:
      writer = csv.writer(f,delimiter=',',lineterminator=';')
      writer.writerows(intervals) ## uses a CSV writer to write the data to file.

    with open('blacklist','w') as f:
      bl_s = ''
      for i in channel_blacklist:
        bl_s += i + ','

      f.write(bl_s)

    await asyncio.sleep(1.2)
