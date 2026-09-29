"""Pruebas públicas de ejemplo. Añade pruebas propias en test_student.py."""
import argparse
from pathlib import Path
from run_cases import load_module

def check(m):
    original=[0,0,0]
    assert m.tick(0,original,0)==(1,[1,0,0])
    assert original==[0,0,0]
    assert m.tick(1,[1,0,0],0,(4,[0,2,0]))==(5,[2,2,0])
    box=m.CausalInbox()
    later={"id":"b","sender":1,"seq":0,"deps":[1,0,0]}
    first={"id":"a","sender":0,"seq":0,"deps":[0,0,0]}
    assert box.receive(later)==[]
    assert box.receive(later)==[] and len(box.buffer)==1
    assert box.receive(first)==["a","b"]
    assert box.buffer==[]
    assert box.receive(first)==[] and box.delivered==[1,1,0]
    assert box.buffer==[]
    assert m.owner(15,{"A":2,"B":7,"C":13},"ring")=="A"
    assert m.owner(7,{"A":2,"B":7,"C":13},"ring")=="B"
    result=m.compare([1,8],{1:2,8:5},{"A":2,"B":10},{"A":2,"B":10,"C":8},"ring")
    assert result["moved"]==[8] and result["load_after"]=={"A":2,"B":0,"C":5}
    assert result["hops"]==3
    direct=m.compare([1,8],{1:2,8:5},{"A":2,"B":10},{"A":2,"B":10,"C":8},"modulo")
    assert direct["hops"]==2

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--module",type=Path,default=Path(__file__).with_name("analysis.py"))
    args=parser.parse_args()
    check(load_module(args.module))
    print("Ejemplos del contrato correctos")
