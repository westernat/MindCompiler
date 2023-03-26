from enum import Enum


class Block:
    def __new__(cls, value: str):
        return f'@{value}'


class Unit:
    def __new__(cls, value: str):
        return f'@{value}'


class Item:
    def __new__(cls, value: str):
        return f'@{value}'


class Liquid:
    def __new__(cls, value: str):
        return f'@{value}'


class DrawMode(Enum):
    Clear = 'clear'
    Color = 'color'
    Col = 'col'
    Stroke = 'stroke'
    Line = 'line'
    Rect = 'rect'
    LineRect = 'lineRect'
    Poly = 'poly'
    LinePoly = 'linePoly'
    Triangle = 'triangle'
    Image = 'image'


class ControlSet(Enum):
    Enabled = 'enabled'
    Shoot = 'shoot'
    Shootp = 'shootp'
    Config = 'config'
    Color = 'color'


class RadarTarget(Enum):
    Any = 'any'
    Enemy = 'enemy'
    Ally = 'ally'
    Player = 'player'
    Attacker = 'attacker'
    Flying = 'flying'
    Boss = 'boss'
    Ground = 'ground'


class RadarOrder(Enum):
    _1 = '1'
    _True = '1'
    _0 = '0'
    _False = '0'


class RadarSort(Enum):
    Distance = 'distance'
    Health = 'health'
    Shield = 'shield'
    Armor = 'armor'
    MaxHealth = 'maxhealth'


class SensorAttr(Enum):
    TotalItems = 'totalItems'
    FirstItem = 'firstItem'
    TotalLiquids = 'totalLiquids'
    TotalPower = 'totalPower'
    ItemCapacity = 'itemCapacity'
    LiquidCapacity = 'liquidCapacity'
    PowerCapacity = 'powerCapacity'
    PowerNetStored = 'powerNetStored'
    PowerNetCapacity = 'powerNetCapacity'
    PowerNetIn = 'powerNetIn'
    PowerNetOut = 'powerNetOut'
    Ammo = 'ammo'
    AmmoCapacity = 'ammocapacity'
    Health = 'health'
    MaxHealth = 'maxHealth'
    Heat = 'heat'
    Efficiency = 'efficiency'
    Progress = 'progress'
    Timescale = 'timescale'
    Rotation = 'rotation'
    X = 'x'
    Y = 'y'
    ShootX = 'shootX'
    ShootY = 'shootY'
    Size = 'size'
    Dead = 'dead'
    Range = 'range'
    Shooting = 'shooting'
    Boosting = 'boosting'
    MineX = 'mineX'
    MineY = 'mineY'
    Mining = 'mining'
    Speed = 'speed'
    Team = 'team'
    Type = 'type'
    Flag = 'flag'
    Controlled = 'controlled'
    Controller = 'controller'
    Name = 'name'
    PayloadCount = 'payloadCount'
    PayloadType = 'payloadType'
    Enabled = 'enabled'
    Config = 'config'
    Color = 'color'


OperationMode = {
    '+': 'add',
    '-': 'sub',
    '*': 'mul',
    '/': 'div',
    '%': 'mod',
    '&': 'and',
    '|': 'or',
    '!': 'not',
    '^': 'xor',
    '&&': 'land',
    '||': 'or'
}


class LookupMode(Enum):
    Block = 'block'
    Unit = 'unit'
    Item = 'item'
    Liquid = 'liquid'


JumpMode = {
    'true': 'allways',
    '>': 'greaterThan',
    '>=': 'greaterThanEq',
    '<': 'lessThan',
    '<=': 'lessThanEq',
    '==': 'equal',
    # '===': 'strictEqual',
    '!=': 'notEqual',
    'f>': 'lessThanEq',
    'f>=': 'lessThan',
    'f<': 'greaterThanEq',
    'f<=': 'greaterThan',
    'f==': 'notEqual',
    'f!=': 'equal'
}


class UnitCtrlMode(Enum):
    Idle = 'idle'
    Stop = 'stop'
    Move = 'move'
    Approach = 'Approach'
    Boost = 'boost'
    RadarTarget = 'target'
    RadarTargetp = 'targetp'
    ItemDrop = 'itemDrop'
    ItemTake = 'itemTake'
    PayDrop = 'payDrop'
    PayTake = 'paytake'
    PayEnter = 'payEnter'
    Mine = 'mine'
    Flag = 'flag'
    Build = 'build'
    GetBlock = 'getBlock'
    Within = 'within'
    Unbind = 'unbind'


class UnitLocFind(Enum):
    Ore = 'ore'
    Building = 'building'
    Spawn = 'spawn'
    Damaged = 'damaged'


class UnitLocGroup(Enum):
    Core = 'core'
    Storage = 'storage'
    Generator = 'generator'
    Turret = 'turret'
    Factory = 'factory'
    Repair = 'repair'
    Battery = 'battery'
    Reactor = 'reactor'


def m_read(result='result', _from: Block = Block('cell1'), at='0'):
    return f'read {result} {_from} {at}'


def m_write(result='result', to: Block = Block('cell1'), at='0'):
    return f'write {result} {to} {at}'


def m_draw(mode=DrawMode.Clear, a='0', b='0', c='0', d='0', e='0', f='0'):
    return f'draw {mode} {a} {b} {c} {d} {e} {f}'


def m_print(msg="frog", to='message1'):
    return f'print {msg}'


def m_drawflush(to='display1'):
    return f'drawflush {to}'


def m_printflush(to='message1'):
    return f'printflush {to}'


def m_getlink(result='result', link='0'):
    return f'getlink {result} {link}'


def m_control(_set: ControlSet = ControlSet.Enabled, of: Block = Block('block1'), a='0', b='0', c='0', d='0'):
    return f'control {_set} {of} {a} {b} {c} {d}'


def m_radar(_from: Block = Block('turret1'), target1: RadarTarget = RadarTarget.Enemy, target2: RadarTarget = RadarTarget.Any, target3: RadarTarget = RadarTarget.Any, order: RadarOrder = RadarOrder._1, sort: RadarSort = RadarSort.Distance, output='output'):
    return f'radar {target1} {target2} {target3} {order} {_from} {sort} {output}'


def m_sensor(result='result', _with: Item | Liquid | SensorAttr = Item('@copper'), _in: Block = Block('block1')):
    return f'sensor {result} {_in} {_with}'


def m_set(result='result', value='0'):
    return f'set {result} {value}'


def m_operation(result='result', mode=OperationMode['+'], a='a', b='b'):
    return f'op {mode} {result} {a} {b}'


def m_lookup(result='result', mode: LookupMode = LookupMode.Item, id='0'):
    return f'lookup {mode} {result} {id}'


def m_packcolor(result='result', r='1', g='0', b='0', a='1'):
    return f'packcolor {result} {r} {g} {b} {a}'


def m_wait(delay='0.5'):
    return f'wait {delay}'


def m_stop():
    return 'stop'


def m_end():
    return 'end'


def m_jump(goto: int | str, mode=JumpMode['true'], left='x', right='0'):
    if mode == 'allways':
        return f'set @counter {goto}'
    return f'jump {goto} {mode} {left} {right}'


def m_ubind(type: Unit = Unit('@poly')):
    return f'ubind {type}'


def m_ucontrol(mode: UnitCtrlMode = UnitCtrlMode.Move, a='0', b='0', c='0', d='0', e='0'):
    return f'ucontrol {mode} {a} {b} {c} {d} {e}'


def m_uradar(target1: RadarTarget = RadarTarget.Enemy, target2: RadarTarget = RadarTarget.Any, target3: RadarTarget = RadarTarget.Any, order: RadarOrder = RadarOrder._1, sort: RadarSort = RadarSort.Distance, result='result'):
    return f'uradar {target1} {target2} {target3} {sort} 0 {order} {result}'


def m_ulocate(find: UnitLocFind = UnitLocFind.Building, *, group: UnitLocGroup = UnitLocGroup.Core, enemy='1', ore: Item = Item('@copper'), outX='outx', outY='outy', found='found', building: Block = Block('building')):
    return f'ulocate {find} {group} {enemy} {ore} {outX} {outY} {found} {building}'


Builtins = {
    'read',
    'write',
    'draw',
    'print',
    'drawflush',
    'printflush',
    'getlink',
    'control',
    'radar',
    'sensor',
    'lookup',
    'packcolor',
    'wait',
    'stop',
    'ubind',
    'ucontrol',
    'uradar',
    'ulocate'
}
