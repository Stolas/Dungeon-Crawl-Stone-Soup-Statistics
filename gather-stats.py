#!/usr/bit/env python

from sys import argv
from os import environ, path, walk
import logging
import re
import time


class Morgue:
    def __init__(self):
        pass

    def __str__(self):
        return "{}, level {}, points {}, class {}, race {}, death {}, faith {}, turns {}, seconds {}".format(self.name, self.level, self.points, self.klass, self.race, self.death_reason, self.god, self.turns, self.seconds)


def do_corpses(corpses):
    with open("out.csv", "w+") as fd:
        fd.write("Name,Level,Points,Class,Race,Death,Turns,Seconds,Faith\n")
        for c in corpses:
            fd.write("{},{},{},{},{},{},{},{},{}\n".format(c.name, c.level, c.points, c.klass, c.race, c.death_reason, c.turns, c.seconds, c.god))
            # logging.info(str(c))


def parse_file(filename):
    logging.debug("Parsing file: {}".format(filename))
    m = Morgue()
    with open(filename) as fd:
        line = fd.readline() # Dungeon Crawl Stone Soup version
        logging.debug("Readline: {}".format(line))

        line = fd.readline() # Whiteline
        logging.debug("Readline: {}".format(line))

        line = fd.readline() # Basic character info
        logging.debug("Readline: {}".format(line))

        match = re.match(r"(\d*)\s([^\(]*)\s\(level\s(\d*)", line)
        logging.debug("Match Name: {}".format(match.group(2)))
        m.name = match.group(2)

        logging.debug("Match Points: {}".format(match.group(1)))
        m.points = match.group(1)

        logging.debug("Match Level: {}".format(match.group(3)))
        m.level =  match.group(3)


        line = fd.readline() # Class and race
        logging.debug("Readline: {}".format(line))

        match = re.match(r"\s*Began as a (\w*(\sOrc|Stalker|Dwarf|Elf)?)(\s(.*))\son", line)
        logging.debug("Match Class: {}".format(match.group(3)))
        m.klass = match.group(3)

        logging.debug("Match Race: {}".format(match.group(1)))
        m.race = match.group(1)


        line = fd.readline() # Death reason or God...
        logging.debug("Readline: {}".format(line))
        m.god = "Atheist"

        try:
            match = re.match(r"\s*Was a (Believer|Priest|Follower) of ([^\.]*)", line)
            logging.debug("Following the god: {}".format(match.group(2)))
            m.god = match.group(2)

            line = fd.readline() # Death reason for sure now :)
        except AttributeError:
            pass

        m.death_reason = line.strip()

        while True:
            line = fd.readline() # Reading till the game lasted
            logging.debug("Readline: {}".format(line))

            try:
                match = re.match(r"\s*The game lasted (\d\d):(\d\d):(\d\d)\s\((\d*)", line)

                logging.debug("Match Time: {}:{}:{}".format(match.group(1), match.group(2), match.group(3)))
                m.seconds = int(match.group(1)) * 3600
                m.seconds += int(match.group(2)) * 60
                m.seconds += int(match.group(3))

                logging.debug("Turns: {}", match.group(4))
                m.turns = match.group(4)

                break
            except AttributeError:
                pass

    return m


def do_files(morgue_dir):
    logging.debug("Using folder: {}".format(morgue_dir))
    corpses = list()
    for root, dirs, files in walk(morgue_dir):
        for file in files:
            if not file.endswith(".txt"):
                continue

            if not file.startswith("morgue"):
                continue

            m = parse_file(path.join(morgue_dir, file))
            corpses.append(m)

    do_corpses(corpses)


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    try:
        morgue_dir = argv[1]
    except IndexError:
        morgue_dir = path.join(environ['HOME'], ".crawl", "morgue")

    do_files(morgue_dir)
