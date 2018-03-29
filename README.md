# SC2Recorder

## Installation

### Starcraft II

#### Windows & Mac

1. Download and install from the [official website](https://starcraft2.com/) (Starcraft II is free to play by now).

2. Download the [mini games](https://github.com/deepmind/pysc2/releases/download/v1.2/mini_games.zip) and extract them to your `StarcraftII/Maps/` directory.

3. Open [DemoReplay_3-16-1.SC2Replay](DemoReplay_3-16-1.SC2Replay) (directly with the Starcraft II client) to ensure that Starcraft II has downloaded the required version.

If you used the default install location PySC2 should find the latest binary. If you changed the install location, you'll need to set the `SC2PATH` environment variable with the correct location.

#### Linux

1. Download Starcraft II Linux package **Version 3.16.1** from the Blizzard sc2client [GitHub repository](https://github.com/Blizzard/s2client-proto#downloads).  
Be sure to copy the files to `~/StarCraftII/`.

2. Download the [mini games](https://github.com/deepmind/pysc2/releases/download/v1.2/mini_games.zip) and extract them to your `StarcraftII/Maps/` directory.

### PySC2

Install Deepminds [PySC2](https://github.com/deepmind/pysc2) package using pip: 

```
pip install pysc2==1.2
```

## Run Recorder

Record replays using the following command:

```
python record.py
```

By default replays will be stored under `./replays/`.
