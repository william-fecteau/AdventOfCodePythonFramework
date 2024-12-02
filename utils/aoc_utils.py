import os
import sys
import time

import requests


def downloadInput(dayNum, year, sessionToken, inputPath):
    url = "https://adventofcode.com/" + \
        str(year) + "/day/" + str(dayNum) + "/input"
    result = requests.get(url, cookies={'session': sessionToken})
    if result.status_code == 200:
        with open(inputPath, 'w') as f:
            f.write(result.text)
    else:
        raise ConnectionError("Could not connect to AoC website to download input data. "
                              "Error code {}: {}".format(result.status_code, result.text))


class AOCDay:
    year = 2020
    dayNumber = 0
    inputFilename = ""
    outputFilename = ""
    sessionToken = ""
    inputData = None

    def __init__(self, year, dayNumber, sessionToken):
        self.year = int(year)
        self.dayNumber = int(dayNumber)
        self.sessionToken = sessionToken

        fileName = f"day{dayNumber}.txt"

        # Configuring inputs
        os.makedirs(os.path.join(os.getcwd(), year, "inputs"), exist_ok=True)
        self.inputPath = os.path.join(os.getcwd(), year, "inputs", fileName)

        # Configuring outputs
        os.makedirs(os.path.join(os.getcwd(), year, "outputs"), exist_ok=True)
        self.outputPath = os.path.join(os.getcwd(), year, "outputs", fileName)

    def run(self):
        # Getting input
        self.downloadInput()

        # Common thinggy
        startTime = time.time()
        self.common()
        time0 = time.time() - startTime

        # Part 1
        startTime = time.time()
        answer1 = self.part1()
        time1 = time.time() - startTime

        # Part 2
        startTime = time.time()
        answer2 = self.part2()
        time2 = time.time() - startTime

        totalTime = time0 + time1 + time2

        # Writing output
        self.writeOutput(
            f"====================== Day {self.dayNumber} ======================",
            f"Common time (ms) : {time0}",
            f"---------------------------------------------------",
            f"Part 1 : {answer1}",
            f"Time (ms): {time1}",
            f"---------------------------------------------------",
            f"Part 2 : {answer2}",
            f"Time (ms): {time2}",
            f"---------------------------------------------------",
            f"Total time (ms): {totalTime}"
        )

    def downloadInput(self):
        # If file already exists, only read it
        if os.path.exists(self.inputPath):
            self.readInput()
            return

        downloadInput(self.dayNumber, self.year,
                      self.sessionToken, self.inputPath)

    def readInput(self):
        # Opening filestream
        file = open(self.inputPath, "r")

        self.rawData = "".join(file.readlines())
        while self.rawData.endswith("\n"):
            self.rawData = self.rawData[:-1]

        self.inputData = self.rawData.split("\n")

        # Closing filestream
        file.close()

    def writeOutput(self, *args):
        # Concats all the args into one string
        strToWrite = ""
        for arg in args:
            strToWrite += str(arg) + "\n"

        # Writes to console
        sys.stdout.write(strToWrite)

        # Writes to file
        file = open(self.outputPath, "w")
        file.write(strToWrite)
        file.close()

    def common(self):
        pass

    def part1(self):
        pass

    def part2(self):
        pass
