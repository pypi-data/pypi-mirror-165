The machine operator package runs state machines based on the below meta-model:

```
StateMachine:
    'events'
        events+=Event
    'end'

    'commands'
        commands+=Command
    'end'

    ('commandgroups'
        commandGroupBlocks+=CommandGroupBlock        
    'end')? 

    states+=State
;

Keyword:
    'end' | 'events' | 'state' | 'actions' | 'commandgroups' | 'group' | 'groupend'
;

Event:
    name=SMID code=ID
;

Command:
    name=SMID code=ID
;

CommandGroupBlock:
    'group' name=SMID
        groupCommands+=[Command|SMID]       
    'groupend'
;

GroupOrCommand: Command | CommandGroupBlock;

State:
    'state' name=ID
        ('actions' '{' actions+=[GroupOrCommand | SMID] '}')?
        (transitions+=Transition)?
    'end'
;

Transition:
    event=[Event|SMID] '=>' to_state=[State]
;

SMID:
    !Keyword ID
;

Comment:
    /\/\*(.|\n)*?\*\//
;

```

The package will run a basic microwave oven as the default state machine. The default microwave oven has only 2 functionalities: baking and cleaning. This is a very legacy oven, because of which the cleaning is not timer controlled. You have to manually turn off the cleaning.

To run the oven as a state machine, execute the command `machineop`. If you want to execute a different state machine other than the default one, you can pass the path to the state machine file (with .pymo extension) to the package via the `-m` flag.

`machineop -m <PATH-TO_CUSTOM_STATE_MACHINE>`

To define a custom interpreter to the state machine model, you can pass the python interpreter using the `-i` flag. 

`machineop -i <PATH-TO_CUSTOM_INTERPRETER>`

If you want to get even more creative, you can specify your custom meta-model as well using the `-t` flag.

`machineop -t <PATH-TO_CUSTOM_META_MODEL>`

Connecting all together, you can have your own completely customized textx setup using your own custom meta-model, model and interpreter.

`machineop -m <PATH-TO_CUSTOM_STATE_MACHINE> -i <PATH-TO_CUSTOM_INTERPRETER> -t <PATH-TO_CUSTOM_META_MODEL>`
