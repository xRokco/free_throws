#!/usr/bin/python
import sys
import glob
import csv
import itertools
from colorama import Fore, Back, Style


if __name__ == "__main__":
    team = sys.argv[1]
    player = sys.argv[2]
    print(
        f"Team:                                           {Fore.CYAN}{team}{Style.RESET_ALL}"
    )
    print(
        f"Player:                                         {Fore.CYAN}{player}{Style.RESET_ALL}"
    )
    team_games = glob.glob(f"*{team}*.csv")
    free_throw_attempts = 0
    trips_to_line = 0
    fouls_on_three = 0
    two_point_and_one = 0
    three_point_and_one = 0
    for game in team_games:
        with open(game) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            data = list(csv_reader)
            for i, row in enumerate(data):
                if i == 0:
                    pass
                else:
                    if row[31] == player and row[37].startswith("Free Throw 1 of"):
                        if row[37] == "Free Throw 1 of 1":
                            free_throw_attempts = free_throw_attempts + 1
                            trips_to_line = trips_to_line + 1
                            found = False
                            for item in reversed(
                                data[i - min(12, i - 1) : i]
                            ):  # Look back up to 12 events before the free throw for the made shot. Order should be shot > foul > violations (goaltending) > any subs > free throw
                                if item[31] == player and item[35] == "made":
                                    found = True
                                    if item[32] == 3:
                                        three_point_and_one = three_point_and_one + 1
                                    else:
                                        two_point_and_one = two_point_and_one + 1
                                    break
                            if not found:
                                print(
                                    f"ERROR: player threw an and-one free throw but I could not find the made bucket which let to it. File {game}, line {i}"
                                )
                                exit(1)
                        elif row[37] == "Free Throw 1 of 2":
                            free_throw_attempts = free_throw_attempts + 2
                            trips_to_line = trips_to_line + 1
                        elif row[37] == "Free Throw 1 of 3":
                            free_throw_attempts = free_throw_attempts + 3
                            trips_to_line = trips_to_line + 1
                            fouls_on_three = fouls_on_three + 1

    print(f"Free throw attempts:                            {free_throw_attempts}"),
    print(f"Trips to line:                                  {trips_to_line}")
    print(f"Fouls on a three point attempts:                {fouls_on_three}")
    print(
        f"Average free throw attempts per trip to line:   {free_throw_attempts/trips_to_line}"
    )
    print(
        f"Number of and-ones on {Fore.GREEN}two{Style.RESET_ALL} point shots:          {two_point_and_one}"
    )
    print(
        f"Number of and-ones on {Fore.RED}three{Style.RESET_ALL} point shots:        {three_point_and_one}"
    )
    print(
        f"Number of {Fore.YELLOW}total {Style.RESET_ALL}and-ones:                       {two_point_and_one + three_point_and_one}"
    )
