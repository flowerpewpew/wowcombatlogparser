# WoW Offline Advanced Combat Log Real-Time Analyzer

[![Build and Release](https://github.com/flowerpewpew/wowcombatlogparser/actions/workflows/build-and-release.yml/badge.svg)](https://github.com/flowerpewpew/wowcombatlogparser/actions/workflows/build-and-release.yml)


The Combat Log Analyzer is a Python script that analyzes World of Warcraft combat log files and provides statistics about player damage and performance. It processes the log files in real-time, continuously updating the statistics as new log entries are added. It has support for Augmentation Evoker's _SUPPORT events and attributes the values to the Evoker.

![Alt Text](docs/example.png)
*Green bar is Augmentation Evoker in real time*

## Features

- **Compatible with Augmentation Evokers** - intelligently parses _SUPPORT flag and updates the values accordingly.
- Real-time analysis: The script constantly monitors the newest combat log file and updates the statistics accordingly.
- Player damage statistics: The script calculates the total damage dealt by each player and displays it along with their DPS (damage per second).
- Spell damage breakdown: For each player, the script also provides a breakdown of damage dealt by individual spells.
- Color-coded output: The script uses color coding to highlight players based on their character specialization.

## FAQ
#### _Is it safe?_

The script reads the WoWCombatLog.log file on your hard drive the same way WarcraftLogs does. It just does it in real time and updates the graphs rather than waiting for the end of the encounter.

#### _How accurate is it?_

It's within 0.5-1% of accuracy of warcraftlogs. There are bugs to be expected and I'm still working on improving the accuracy. Help with this is highly appreciated!

#### Can others see it?

The script runs entirely on your machine.

## Requirements

1. Make sure you have Python 3.x installed on your system.
```
winget install python
```


# Usage:

## By downloading the executable

1. Download the executable from the Releases section and unzip to `WoW/_retail_/Logs`.

This exe file is automatically built by Github Actions and does not pose a risk to your system. Nevertheless you can use manual method if you desire: 

## Manually with python

1. Open a terminal or command prompt and navigate to the project directory.
2. Install the required packages by running the following command:

```
pip install -r requirements.txt
```
3. Copy the python file to `WoW/_retail_/Logs` directory and run it:
```
python wowparser.py
```
4. To stop the script, press `Ctrl+C` in the terminal or command prompt.

## Make terminal stay on top of WoW window

1. In Terminal on the top click on the dropdown window and Settings
2. In appearance tab, find "Always on Top" and enable it

![Alt Text](docs/terminaltop.png)

## Contributing

Contributions to the Combat Log Analyzer are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).