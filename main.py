import importlib
import os
import shutil
import sys

from dotenv import load_dotenv

from utils.aoc_utils import downloadInput

if __name__ == "__main__":
    load_dotenv()  # take environment variables from .env.

    year = os.getenv('AOC_YEAR')
    sessionToken = os.getenv('AOC_SESSION_COOKIE')
    if year is None or sessionToken is None or year == "" or sessionToken == "":
        print("Please set the environment variables AOC_YEAR and AOC_SESSION_COOKIE")
        sys.exit(1)

    # Getting parameters
    runAll = False
    dayNumber = 1
    if len(sys.argv) >= 2:
        try:
            if sys.argv[1] == "all":
                runAll = True
            else:
                dayNumber = int(sys.argv[1])
        except Exception:
            print("{} - Run aoc solutions".format(sys.argv[0]))
            print("Usage: {} [day]".format(sys.argv[0]))
            sys.exit(1)
    else:
        print("{} - Run aoc solutions".format(sys.argv[0]))
        print("Usage: {} [day]".format(sys.argv[0]))
        sys.exit(1)

    # Create year dir if not existing
    yearDir = os.path.join(os.getcwd(), year)
    os.makedirs(yearDir, exist_ok=True)

    # Validation
    dayFilePath = os.path.join(yearDir, f"day{dayNumber}.py")
    if dayNumber <= 0 or dayNumber > 25:
        print("Day must be between 0 and 25")
        sys.exit(1)
    # If day file does not exist, create it
    elif not os.path.exists(dayFilePath):
        # Copying template file
        templateFile = os.path.join(os.getcwd(), "template", "_template.py")
        shutil.copy(templateFile, dayFilePath)

        # Replacing template values
        with open(dayFilePath, "rt") as f:
            data = f.read()

        data = data.replace("@day(0)", f"@day({dayNumber})").replace("DayTemplate", f"Day{dayNumber}")

        with open(dayFilePath, "wt") as f:
            f.write(data)

        # Creating output folder
        os.makedirs(os.path.join(yearDir, "inputs"), exist_ok=True)

        # Downloading input
        inputPath = os.path.join(yearDir, "inputs", f"day{dayNumber}.txt")
        downloadInput(dayNumber, year, sessionToken, inputPath)

        print("Day " + str(dayNumber) + " created! glhf")
    else:
        # Running the day
        if runAll:
            daysRun = [x+1 for x in range(25)]
        else:
            daysRun = [dayNumber]

        for dayNum in daysRun:
            # Getting the good days instance
            module = importlib.import_module(f"{year}.day{dayNum}")
            DayClass = getattr(module, f"Day{dayNum}")

            try:
                inst = DayClass(year, dayNum, sessionToken)
                inst.run()
            except Exception as e:
                raise e
