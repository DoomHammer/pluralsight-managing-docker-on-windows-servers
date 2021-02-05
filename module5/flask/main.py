import os
import sys
import uuid
import atexit
import requests
import time
import json
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


class WorkoutKind(Enum):
    RUNNING = "running"
    JUMPING = "jumping"
    SWIMMING = "swimming"


RUN_CONTROLLER_URL = "please provide url via env vars"


@dataclass
class Workout:
    kind: WorkoutKind
    begin: int
    end: int
    other: Dict

    @classmethod
    def from_dict(cls, d: Dict) -> "Workout":
        kind = d.pop("kind")
        if kind not in set(map(lambda e: e[1].value, dict(WorkoutKind.__members__).items())):
            raise ValueError("'{}' is not a WorkoutKind".format(kind))

        begin = int(d.pop("begin"))
        if not 0 <= begin < 2459:
            raise ValueError("Wrong value for begin!")

        end = int(d.pop("end"))
        if not 0 <= end < 2459:
            raise ValueError("Wrong value for end!")

        other = d

        return cls(kind=kind, begin=begin, end=end, other=other)

    def as_dict(self) -> Dict:
        d = asdict(self)
        do = d.pop("other")
        d.pop("kind")
        d.update(do)

        return d


def do_some_work(x: int) -> int:
    """Efficiently computes a simple polynomial just for kicks

    5 + 3x + 4x^2
    """
    return 5 + x * (3 + x * (4))

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route("/api/", methods=('POST',))
@cross_origin()
def main(r=request):
    try:
        content = r.json

        try:
            workout = Workout.from_dict(content)
        except KeyError as e:
            e_msg = "Missing required field %s" % e

            return e_msg, 400
        except ValueError as e:
            e_msg = str(e)

            return e_msg, 400

        _workout_id = uuid.uuid4()
        workout_id = str(_workout_id)
        p = do_some_work(int(content["intensity"]))

        payload = {**workout.as_dict(), "workout_id": workout_id}
        score = 73
        payload["score"] = score
        print(payload)

        return jsonify(payload)
    finally:
        pass


@app.route("/health", methods=('GET',))
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = os.environ["PORT"]
    RUN_CONTROLLER_URL = os.environ.get("RUN_CONTROLLER_URL", "/")
    debug = bool(os.environ.get("DEBUG"))

    app.run('0.0.0.0', debug=debug, port=port)
