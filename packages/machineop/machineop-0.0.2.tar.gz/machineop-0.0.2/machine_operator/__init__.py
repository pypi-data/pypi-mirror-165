import sys
from os.path import dirname, join 
from textx import language, metamodel_from_file
from machine_operator.state_machine import StateMachine
import argparse
from importlib.machinery import SourceFileLoader



@language('MachineOp', '*.pymo')
def state_machine_lang():
    """
    State Machine operation language
    """

def interpreter(current_folder,args):
    meta_model = metamodel_from_file(args.metamodel or join(current_folder, 'state_machine.tx'))
    model = meta_model.model_from_file(args.model or join(current_folder,"oven.pymo"))
    if args.interpreter:
        StateMachineImported = SourceFileLoader("StateMachine",args.interpreter).load_module()
        state_machine = StateMachineImported.StateMachine(model)
    else:
        state_machine = StateMachine(model)
    state_machine.interpret()

def operate():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--interpreter", help="Provide user specific python interpreter class") 
    parser.add_argument("-t","--metamodel", help="Provide textx meta model") 	
    parser.add_argument("-m","--model", help="Provide user specific model") 	
    args=parser.parse_args()
    this_folder = dirname(__file__)
    interpreter(this_folder,args)        