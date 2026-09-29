"""Lee CASES.json y muestra los resultados que calcula analysis.py."""
import argparse
import importlib.util
import json
from pathlib import Path

def load_module(path):
    spec=importlib.util.spec_from_file_location("homework_analysis",path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run(module):
    fixture=json.loads(Path(__file__).with_name("CASES.json").read_text())
    current=[(0,[0,0,0]) for _ in range(3)]
    clocks={}
    for event in fixture["events"]:
        incoming=clocks[event["received"]] if event["received"] else None
        index=event["process"]
        current[index]=module.tick(*current[index],index,incoming)
        clocks[event["id"]]=current[index]
    inbox=module.CausalInbox()
    arrivals=[{"arrived":message["id"],"delivered":inbox.receive(message),
               "counter":list(inbox.delivered)}
              for message in fixture["messages"]]
    frequency=dict(zip(fixture["keys"],fixture["frequencies"]))
    comparisons={}
    for mode in ("modulo","ring"):
        comparisons[mode]=module.compare(fixture["keys"],frequency,
                                        fixture["before"],fixture["after"],mode)
        hot=frequency | {fixture["hot_key"]:fixture["hot_frequency"]}
        comparisons[mode+"-hot"]=module.compare(fixture["keys"],hot,
                                                fixture["before"],fixture["after"],mode)
    return {"clocks":clocks,"arrivals":arrivals,"comparisons":comparisons}

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--module",type=Path,default=Path(__file__).with_name("analysis.py"))
    args=parser.parse_args()
    print(json.dumps(run(load_module(args.module)),ensure_ascii=False,indent=2))
