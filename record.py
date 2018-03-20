from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import ntpath
import pathlib
import platform
import shutil
import sys
import time
import os

from absl.flags import FLAGS
from pysc2 import maps
from pysc2 import run_configs
from pysc2.env import sc2_env
from s2clientprotocol import sc2api_pb2 as sc_pb


def copy_replay_to_project_path(
        replay_file_path: str,
        score: any,
        project_replay_path: str="./replays"
) -> None:
    pathlib.Path(project_replay_path).mkdir(parents=True, exist_ok=True)
    replay_name = ntpath.basename(replay_file_path)
    project_replay_file_path = os.path.join(project_replay_path, replay_name)
    shutil.copyfile(replay_file_path, project_replay_file_path)
    replay_score_file_path = project_replay_file_path.replace("SC2Replay", "txt")
    with open(replay_score_file_path, "w") as f:
        f.write("{}\n".format(score))
    print("Replay saved to: {}".format(project_replay_file_path))


def record(
        map_name: str= "CollectMineralsAndGas",
        sc2_version: str="3.16.1",
        realtime: bool=True,  # False,
        full_screen: bool=False,
        # fps: float=22.4,
        fps: float=60,
        step_mul: int=1,
        user_race: int="R",
        bot_race: int="R",
        difficulty: int="1",
        disable_fog: bool=False
) -> None:
    if platform.system() == "Linux" and (realtime or full_screen):
        sys.exit("realtime and full_screen only make sense on Windows/MacOS.")

    run_config = run_configs.get()

    map_inst = maps.get(map_name)

    create = sc_pb.RequestCreateGame(
        realtime=realtime,
        disable_fog=disable_fog,
        local_map=sc_pb.LocalMap(
            map_path=map_inst.path,
            map_data=map_inst.data(run_config)
        )
    )
    interface = sc_pb.InterfaceOptions()
    interface.raw = False
    interface.score = True
    create.player_setup.add(
        type=sc_pb.Participant
    )
    create.player_setup.add(
        type=sc_pb.Computer,
        race=sc2_env.races[bot_race],
        difficulty=sc2_env.difficulties[difficulty]
    )
    join = sc_pb.RequestJoinGame(
        race=sc2_env.races[user_race],
        options=interface
    )

    with run_config.start(
            game_version=sc2_version,
            full_screen=full_screen
    ) as controller:
        controller.create_game(create)
        controller.join_game(join)
        obs = controller.observe()
        result = obs.player_result
        try:
            while not result:
                frame_start_time = time.time()
                if not realtime:
                    controller.step(step_mul)
                obs = controller.observe()
                result = obs.player_result
                time.sleep(max(0, frame_start_time + 1 / fps - time.time()))
        except KeyboardInterrupt:
            pass
        print("Score: ", obs.observation.score.score)
        print("Result: ", obs.player_result)
        replay_file_path = run_config.save_replay(
            replay_data=controller.save_replay(),
            replay_dir="local",
            map_name=map_name
        )
        copy_replay_to_project_path(
            replay_file_path=replay_file_path,
            score=obs.observation.score.score
        )


if __name__ == "__main__":
    FLAGS(sys.argv)
    record()
