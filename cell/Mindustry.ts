//#Typescript

declare class Object {
    /**指向当前对象自己 */
    readonly $this: this
    /**获取当前对象自己的X坐标 */
    readonly $thisx: Number
    /**获取当前对象自己的Y坐标 */
    readonly $thisy: Number
    /**获取这个建筑物/单位内的所有物品的总计数量 */
    readonly $totalItems: Number
    /**获取这个建筑物/单位内的所有液体的总计数量 */
    readonly $totalLiquid: Number
    /**获取这个建筑物/单位内总电力 */
    readonly $totalPower: Number
    /**获取这个建筑物/单位内的物品的容量 */
    readonly $itemCapacity: Number
    /**获取这个建筑物/单位内的液体的容量 */
    readonly $liquidCapacity: Number
    /**获取这个建筑物/单位内的电力的容量 */
    readonly powerCapacity: Number
    /**获取这个建筑物/单位内的电力网络的储存量 */
    readonly $powerNetStored: Number
    /**获取这个建筑物/单位内的电力网络的储存量容量 */
    readonly $powerNetCapacity: Number
    /**获取这个建筑物/单位内的电力网络输入量/产生量 */
    readonly $powerNetIn: Number
    /**获取这个建筑物/单位内的电力网络输出量/消耗量 */
    readonly $powerNetOut: Number
    /**获取这个建筑物/单位内的子弹量 */
    readonly $ammo: Number
    /**获取这个建筑物/单位内的子弹量上限 */
    readonly $ammoCapacity: Number
    /**获取这个建筑物/单位的生命值 */
    readonly $health: Number
    /**获取这个建筑物/单位的生命值上限 */
    readonly $maxHealth: Number
    /**获取这个建筑物/单位的发热 */
    readonly $heat: Number
    /**获取这个建筑物/单位的效率 */
    readonly $efficiency: Number
    /**获取这个建筑物/单位的时间流速 */
    readonly $timescale: Number
    /**获取这个炮塔/单位的旋转角度,建筑物则获取朝向(0为沿建筑物x轴方向,逆时针) */
    readonly $rotation: Number
    /**获取这个建筑物/单位的x坐标 */
    readonly $x: Number
    /**获取这个建筑物/单位的y坐标 */
    readonly $y: Number
    /**获取这个建筑物/单位的射击x坐标 */
    readonly $shootX: Number
    /**获取这个建筑物/单位的射击y坐标 */
    readonly $shootY: Number
    /**获取这个建筑物/单位的大小(正方形边长大小) */
    readonly $size: Number
    /**获取这个建筑物/单位是否失效(被摧毁返回1 有效返回0) */
    readonly $dead: boolean
    /**获取这个建筑物/单位的攻击范围 */
    readonly $range: Number
    /**获取这个建筑物/单位的攻击状态(开火返回1 停火返回0) */
    readonly $shooting: boolean
    /**获取这个建筑物/单位的开启状态 */
    readonly $enabled: boolean
    /**获取这个建筑物的配置(常用于分类器) */
    readonly $configure: any
    /**获取这个建筑物/单位的阵营 */
    readonly $team: Number
    /**返回这个建筑物/单位的类型 */
    readonly $type: Number
    /**返回这个建筑物/单位的数字标记 */
    readonly $flag: Number
    /**返回这个建筑物/单位是否被控制(处理器返回1 玩家返回2 编队返回3 如果都不是返回0) */
    readonly $controlled: Number

    constructor(rowId: string)
    /**
     * 
     * @param flag 绑定的方块编号
     * @returns 所绑定的方块
     */
    bind(flag: Number): this
    getRowId(): string
}

declare class Block extends Object { }

// compaign
declare class Accelerator extends Block { }
declare class LaunchPad extends Block { }

// defense
declare class BaseTurret extends Block { }
declare class Turret extends BaseTurret { }
declare class ReloadTurret extends BaseTurret { }
declare class TractorBeamTurret extends BaseTurret { }
declare class PowerTurret extends Turret { }
declare class ItemTurret extends Turret { }
declare class LaserTurret extends PowerTurret { }
declare class LiquidTurret extends Turret { }
/*declare class PayloadAmmoTurret extends Turret { }*/
declare class PointDefenseTurret extends ReloadTurret { }
declare class ContinuousTurret extends Turret { }
declare class ContinuousLiquidTurret extends ContinuousTurret { }
declare class Wall extends Block { }
declare class Door extends Wall { }
declare class AutoDoor extends Wall { }
declare class BaseShield extends Block { }
declare class BuildTurret extends BaseTurret { }
declare class DirectionalForceProjector extends Block { }
declare class ForceProjector extends Block { }
declare class MendProjector extends Block { }
declare class OverdriveProjector extends Block { }
declare class Radar extends Block { }
declare class RegenProjector extends Block { }
declare class ShieldWall extends Wall { }
declare class ShockMine extends Block { }
declare class ShockwaveTower extends Block { }
declare class Thruster extends Wall { }

// distribution
declare class Conveyor extends Block { }
declare class ArmoredConveyor extends Conveyor { }
declare class DirectionalUnloader extends Block { }
declare class DirectionBridge extends Block { }
declare class DirectionLiquidBridge extends DirectionBridge { }
declare class Duct extends Block { }
declare class DuctBridge extends DirectionBridge { }
declare class DuctRouter extends Block { }
declare class StackRouter extends DuctRouter { }
declare class ItemBridge extends Block { }
declare class BufferedItemBridge extends ItemBridge { }
declare class Junction extends Block { }
declare class MassDriver extends Block { }
declare class OverflowDuct extends Block { }
declare class OverflowGate extends Block { }
declare class Router extends Block { }
declare class Sorter extends Block { }
declare class StackConveyor extends Block { }
/*declare class StackRouterBuild extends DuctRouterBuild { }*/

// heat
declare class HeatConductor extends Block { }
declare class HeatProducer extends GenericCrafter { }

// liquid
declare class LiquidBlock extends Block { }
declare class Conduit extends LiquidBlock { }
declare class ArmoredConduit extends Conduit { }
declare class LiquidBridge extends ItemBridge { }
declare class LiquidJunction extends LiquidBlock { }
declare class LiquidRouter extends LiquidBlock { }

// logic
declare class CanvasBlock extends Block { }
declare class LogicBlock extends Block {
    /**自游戏启动起所经过的时间 */
    readonly $time: Number
    /**绑定方块数 */
    readonly $links: Number
    /**逻辑执行行数 */
    $counter: Number
    /**当前绑定单位 */
    readonly $unit: Unit
    /**每tick执行行数 */
    readonly $ipt: Number
    /**返回被标记单位控制者名字 */
    readonly $name: string
}
declare class LogicDisplay extends Block { }
declare class MemoryBlock extends Block { }
declare class MessageBlock extends Block {
    /**
     * 打印缓存
     */
    readonly flush: string
    /**
     * 
     * @param msg 需要打印的对象
     * 
     * 把msg存于缓存
     */
    print(msg: any): void
    /**
     * 打印缓存
     */
    printflush(): void
}
declare class SwitchBlock extends Block { }

// payloads
declare class PayloadBlock extends Block { }
declare abstract class BlockProducer extends PayloadBlock { }
declare class Constructor extends BlockProducer { }
declare class PayloadConveyor extends Block { }
declare class PayloadDeconstructor extends PayloadBlock { }
declare class PayloadLoader extends PayloadBlock { }
declare class PayloadMassDriver extends PayloadBlock { }
/*declare class PayloadRouter extends PayloadConveyor { }*/
declare class PayloadSource extends PayloadBlock { }
declare class PayloadUnloader extends PayloadLoader { }
declare class PayloadVoid extends PayloadBlock { }
/*declare class UnitPayload implements Payload { }*/

// power
declare class PowerBlock extends Block { }
declare class PowerDistributor extends PowerBlock { }
declare class PowerNode extends PowerBlock { }
declare class Battery extends PowerDistributor { }
declare class PowerGenerator extends PowerDistributor { }
declare class BeamNode extends PowerBlock { }
declare class ConsumeGenerator extends PowerGenerator { }
declare class HeaterGenerator extends ConsumeGenerator { }
declare class ImpactReactor extends PowerGenerator { }
declare class LightBlock extends Block { }
declare class LongPowerNode extends PowerNode { }
declare class NuclearReactor extends PowerGenerator { }
declare class PowerDiode extends Block { }
declare class SolarGenerator extends PowerGenerator { }
declare class ThermalGenerator extends PowerGenerator { }
declare class VariableReactor extends PowerGenerator { }

// production
declare class Pump extends LiquidBlock { }
declare class SolidPump extends Pump { }
declare class Drill extends Block { }
declare class GenericCrafter extends Block { }
declare class AttributeCrafter extends GenericCrafter { }
declare class BeamDrill extends Block { }
declare class BurstDrill extends Drill { }
declare class Fracker extends SolidPump { }
declare class HeatCrafter extends GenericCrafter { }
/*declare class Incinerator extends Block { }*/
declare class ItemIncinerator extends Block { }
declare class Separator extends Block { }
/*declare class SingleBlockProducer extends BlockProducer { }*/
declare class WallCrafter extends Block { }

// sandbox
declare class ItemSource extends Block { }
declare class ItemVoid extends Block { }
declare class LiquidSource extends Block { }
declare class LiquidVoid extends Block { }
declare class PowerSource extends PowerNode { }
declare class PowerVoid extends PowerBlock { }

// storage
declare class StorageBlock extends Block { }
declare class CoreBlock extends StorageBlock { }
declare class Unloader extends Block { }

// units
declare class UnitBlock extends PayloadBlock { }
/*declare class DroneCenter extends Block { }*/
declare class Reconstructor extends UnitBlock { }
declare class RepairTower extends Block { }
declare class RepairTurret extends Block { }
declare class UnitAssembler extends PayloadBlock { }
declare class UnitAssemblerModule extends PayloadBlock { }
declare class UnitCargoLoader extends Block { }
declare class UnitCargoUnloadPoint extends Block { }
declare class UnitFactory extends UnitBlock { }

declare const MindBlocks: {
    //crafting
    siliconSmelter: GenericCrafter, siliconCrucible: AttributeCrafter, kiln: GenericCrafter, graphitePress: GenericCrafter, plastaniumCompressor: GenericCrafter, multiPress: GenericCrafter, phaseWeaver: GenericCrafter, surgeSmelter: GenericCrafter, pyratiteMixer: GenericCrafter, blastMixer: GenericCrafter, cryofluidMixer: GenericCrafter,
    melter: GenericCrafter, separator: Separator, disassembler: Separator, sporePress: GenericCrafter, pulverizer: GenericCrafter, incinerator: GenericCrafter, coalCentrifuge: GenericCrafter,

    //crafting - erekir
    siliconArcFurnace: GenericCrafter, electrolyzer: GenericCrafter, oxidationChamber: HeatProducer, atmosphericConcentrator: HeatCrafter, electricHeater: HeatProducer, slagHeater: HeatProducer, phaseHeater: HeatProducer, heatRedirector: HeatConductor, heatRouter: HeatConductor, slagIncinerator: ItemIncinerator,
    carbideCrucible: HeatCrafter, slagCentrifuge: GenericCrafter, surgeCrucible: HeatCrafter, cyanogenSynthesizer: HeatCrafter, phaseSynthesizer: HeatCrafter, heatReactor: HeatProducer,

    //sandbox
    powerSource: PowerSource, powerVoid: PowerVoid, itemSource: ItemSource, itemVoid: ItemVoid, liquidSource: LiquidSource, liquidVoid: LiquidVoid, payloadSource: PayloadSource, payloadVoid: PayloadVoid, illuminator: LightBlock, heatSource: HeatProducer,

    //defense
    copperWall: Wall, copperWallLarge: Wall, titaniumWall: Wall, titaniumWallLarge: Wall, plastaniumWall: Wall, plastaniumWallLarge: Wall, thoriumWall: Wall, thoriumWallLarge: Wall, door: Door, doorLarge: Door,
    phaseWall: Wall, phaseWallLarge: Wall, surgeWall: Wall, surgeWallLarge: Wall,

    //walls - erekir
    berylliumWall: Wall, berylliumWallLarge: Wall, tungstenWall: Wall, tungstenWallLarge: Wall, blastDoor: AutoDoor, reinforcedSurgeWall: Wall, reinforcedSurgeWallLarge: Wall, carbideWall: Wall, carbideWallLarge: Wall,
    shieldedWall: ShieldWall,

    mender: MendProjector, mendProjector: MendProjector, overdriveProjector: OverdriveProjector, overdriveDome: OverdriveProjector, forceProjector: ForceProjector, shockMine: ShockMine,
    scrapWall: Wall, scrapWallLarge: Wall, scrapWallHuge: Wall, scrapWallGigantic: Wall, thruster: Thruster,

    //defense - erekir
    radar: Radar,
    buildTower: BuildTurret,
    regenProjector: RegenProjector, barrierProjector: DirectionalForceProjector, shockwaveTower: ShockwaveTower,
    //campaign only
    shieldProjector: BaseShield,
    largeShieldProjector: BaseShield,
    shieldBreaker,

    //transport
    conveyor: Conveyor, titaniumConveyor: Conveyor, plastaniumConveyor: StackConveyor, armoredConveyor: ArmoredConveyor, distributor, junction: Junction, itemBridge: BufferedItemBridge, PhaseConveyor: ItemBridge, sorter: Sorter, invertedSorter: Sorter, router: Router,
    overflowGate: OverflowGate, underflowGate: OverflowGate, massDriver: MassDriver,

    //transport - alternate
    duct: Duct, armoredDuct: Duct, ductRouter: DuctRouter, overflowDuct: OverflowDuct, underflowDuct: OverflowDuct, ductBridge: DuctBridge, ductUnloader: DirectionalUnloader,
    surgeConveyor: StackConveyor, surgeRouter: StackRouter,

    unitCargoLoader: UnitCargoLoader, unitCargoUnloadPoint: UnitCargoUnloadPoint,

    //liquid
    mechanicalPump: Pump, rotaryPump: Pump, impulsePump: Pump, conduit: Conduit, pulseConduit: Conduit, platedConduit: ArmoredConduit, liquidRouter: LiquidRouter, liquidContainer: LiquidRouter, liquidTank: LiquidRouter, liquidJunction: LiquidJunction, bridgeConduit: LiquidBridge, phaseConduit: LiquidBridge,

    //liquid - reinforced
    reinforcedPump: Pump, reinforcedConduit: ArmoredConduit, reinforcedLiquidJunction: LiquidJunction, reinforcedBridgeConduit: DirectionLiquidBridge, reinforcedLiquidRouter: LiquidRouter, reinforcedLiquidContainer: LiquidRouter, reinforcedLiquidTank: LiquidRouter,

    //power
    combustionGenerator: ConsumeGenerator, thermalGenerator: ThermalGenerator, steamGenerator: ConsumeGenerator, differentialGenerator: ConsumeGenerator, rtgGenerator: ConsumeGenerator, solarPanel: SolarGenerator, largeSolarPanel: SolarGenerator, thoriumReactor: NuclearReactor,
    impactReactor: ImpactReactor, battery: Battery, batteryLarge: Battery, powerNode: PowerNode, powerNodeLarge: PowerNode, surgeTower: PowerNode, diode: PowerDiode,

    //power - erekir
    turbineCondenser: ThermalGenerator, ventCondenser: AttributeCrafter, chemicalCombustionChamber: ConsumeGenerator, pyrolysisGenerator: ConsumeGenerator, fluxReactor: VariableReactor, neoplasiaReactor: HeaterGenerator,
    beamNode: BeamNode, beamTower: BeamNode, beamLink: LongPowerNode,

    //production
    mechanicalDrill: Drill, pneumaticDrill: Drill, laserDrill: Drill, blastDrill: Drill, waterExtractor: SolidPump, oilExtractor: Fracker, cultivator: AttributeCrafter,
    cliffCrusher: WallCrafter, plasmaBore: BeamDrill, largePlasmaBore: BeamDrill, impactDrill: BurstDrill, eruptionDrill: BurstDrill,

    //storage
    coreShard: CoreBlock, coreFoundation: CoreBlock, coreNucleus: CoreBlock, vault: StorageBlock, container: StorageBlock, unloader: Unloader,
    //storage - erekir
    coreBastion: CoreBlock, coreCitadel: CoreBlock, coreAcropolis: CoreBlock, reinforcedContainer: StorageBlock, reinforcedVault: StorageBlock,

    //turrets
    duo: ItemTurret, scatter: ItemTurret, scorch: ItemTurret, hail: ItemTurret, arc: PowerTurret, wave: LiquidTurret, lancer: PowerTurret, swarmer: ItemTurret, salvo: ItemTurret, fuse: ItemTurret, ripple: ItemTurret, cyclone: ItemTurret, foreshadow: ItemTurret, spectre: ItemTurret, meltdown: LaserTurret, segment: PointDefenseTurret, parallax: TractorBeamTurret, tsunami: LiquidTurret,

    //turrets - erekir
    breach: ItemTurret, diffuse: ItemTurret, sublimate: ContinuousLiquidTurret, titan: ItemTurret, disperse: ItemTurret, afflict: PowerTurret, lustre: ContinuousTurret, scathe: ItemTurret, smite: ItemTurret, malign: PowerTurret,

    //units
    groundFactory: UnitFactory, airFactory: UnitFactory, navalFactory: UnitFactory,
    additiveReconstructor: Reconstructor, multiplicativeReconstructor: Reconstructor, exponentialReconstructor: Reconstructor, tetrativeReconstructor: Reconstructor,
    repairPoint: RepairTurret, repairTurret: RepairTurret,

    //units - erekir
    tankFabricator: UnitFactory, shipFabricator: UnitFactory, mechFabricator: UnitFactory,

    tankRefabricator: RepairTurret, shipRefabricator: RepairTurret, mechRefabricator: RepairTurret,
    primeRefabricator: RepairTurret,

    tankAssembler: UnitAssembler, shipAssembler: UnitAssembler, mechAssembler: UnitAssembler,
    basicAssemblerModule: UnitAssemblerModule,

    unitRepairTower: RepairTower,

    //payloads
    payloadConveyor: PayloadConveyor, payloadRouter: PayloadConveyor, reinforcedPayloadConveyor: PayloadConveyor, reinforcedPayloadRouter: PayloadConveyor, payloadMassDriver: PayloadMassDriver, largePayloadMassDriver: PayloadMassDriver, smallDeconstructor: PayloadDeconstructor, deconstructor: PayloadDeconstructor, constructor: Constructor, largeConstructor: Constructor, payloadLoader: PayloadLoader, payloadUnloader: PayloadUnloader,

    //logic
    message: MessageBlock, switchBlock: SwitchBlock, microProcessor: LogicBlock, logicProcessor: LogicBlock, hyperProcessor: LogicBlock, largeLogicDisplay: LogicDisplay, logicDisplay: LogicDisplay, memoryCell: MemoryBlock, memoryBank: MemoryBlock,
    canvas: CanvasBlock, reinforcedMessage: MessageBlock,
    worldProcessor: LogicBlock, worldCell: MemoryBlock, worldMessage: MessageBlock,

    //campaign
    launchPad: LaunchPad, interplanetaryAccelerator: Accelerator
}

declare class Unit extends Object {
    /**获取这个单位的飞行状态 */
    readonly $boosting: any
    /**获取这个单位的挖矿x坐标 */
    readonly $mineX: Number
    /**获取这个单位的挖矿y坐标 */
    readonly $mineY: Number
    /**获取这个单位的挖矿状态 */
    readonly $mining: Number
    /**获取这个单位的配置(如工厂生产的物品) */
    readonly $config: any
    /**获取单位的载荷数量 */
    readonly $payloadCount: Number
    /**获取单位的载荷类型 */
    readonly $payloadType: any
    /**返回一个单位的控制者(如果是处理器返回processor 编队返回 leader 如果都不是返回 itself) */
    readonly $controller: any
}

//#region functions

/**从连接的内存读取数字 */
declare function read(result: string | number, from: MemoryBlock, at: number): void
/**向连接的内存写入数字 */
declare function write(to: MemoryBlock, at: number, _with: string | number): void
/**添加绘图操作到绘图缓存
 * 
 * 使用 Draw Flush 后才会真正显示 */
declare function draw(mode: string, ...kwargs: number[]): void
/**用指定的颜色填充整个显示屏 */
declare function draw(mode: "clear", R: number, G: number, B: number): void
/**设置后续画图操作所使用的颜色 */
declare function draw(mode: "color", R: number, G: number, B: number, A: number): void
/**颜色代码
 * 
 * 为以%开头的十六进制代码形式。
 * 
 * 举例: %FF0000 为红色 */
declare function draw(mode: "col", RGB: string): void
/**设置线条宽度 */
declare function draw(mode: "stroke", width: number): void
/**绘制线段 */
declare function draw(mode: "line", x: number, y: number, x2: number, y2: number): void
/**绘制实心矩形 */
declare function draw(mode: "rect", x: number, y: number, width: number, height: number): void
/**绘制矩形轮廓 */
declare function draw(mode: "lineRect", x: number, y: number, x2: number, y2: number): void
/**绘制实心多边形 */
declare function draw(mode: "poly", x: number, y: number, sides: number, radius: number, rotation: number): void
/**绘制正多边形轮廓 */
declare function draw(mode: "linePoly", x: number, y: number, sides: number, radius: number, rotation: number): void
/**绘制实心三角形 */
declare function draw(mode: "triangle", x: number, y: number, x2: number, y2: number, x3: number, y3: number): void
/**画出某个游戏内容的图像
 * 
 * 例如 @router 或者 @dagger */
declare function draw(mode: "image", x: number, y: number, image: string, size: number, rotation: number): void
/**添加文字到打印缓存
 * 
 * 使用 Print Flush 后才会真正显示 */
declare function print(msg: string | number | boolean): void
/**将绘图缓存中的 Draw 队列刷新到显示屏 */
declare function drawflush(to: "display1"): void
/**将打印缓存中的 Print 队列刷新到信息板 */
declare function printflush(to: "message1"): void
/**获取与处理器连接的建筑
 * 
 * 建筑编号从0开始 */
declare function getlink(result: string, link: number): void
/**控制建筑 */
declare function control(set: string, of: string, kwargs: number[]): void
/**建筑是否已启用 */
declare function control(set: "enabled", of: string, to: number): void
/**向某个位置瞄准/射击 */
declare function control(set: "shoot", of: string, x: number, y: number): void
/**根据提前量向某个单位或建筑瞄准/射击 */
declare function control(set: "shootp", of: string, unit: number, shoot: number): void
/**建筑设置，例如分类器所设置的筛选物品种类 */
declare function control(set: "config", of: string, to: number): void
/**照明器发光的颜色 */
declare function control(set: "color", of: string, to: number): void
/**让建筑搜寻感知范围内的单位 */
declare function radar(from: string, target1: string, target2: string, target3: string, order: boolean, sort: string, output: string): void
/**从建筑或者单位中获取数据 */
declare function sensor(result: string, _with: string, _in: string): void
/**根据ID查阅一种物品/液体/单位/建筑
 * 
 * 各个分类中的项目总数
 * 
 * 是 @unitCount / @itemCount / @liquidCount / @blockCount */
declare function lookup(result: string, mode: string, id: number): void
/**将[0, 1]范围内的RGBA分量整合成单个数字
 * 
 * 用于绘图或者规则设置 */
declare function packcolor(result: string, r: number, g: number, b: number, a: number): void
/**指定等待的秒数 */
declare function wait(delay: number): void
/**停止该处理器的运行 */
declare function stop(): void
/**绑定某个类型的下一个单位
 * 
 * 或者直接绑定指定单位
 * 
 * 并保存至 @unit */
declare function ubind(type: string): void
/**控制已绑定的单位 */
declare function ucontrol(mode: string, kwargs: number[]): void
/**原地不动，但继续进行手上的采矿/建造动作
 * 
 * 单位的默认状态 */
declare function ucontrol(mode: "idle"): void
/**停止移动/采矿/建造动作 */
declare function ucontrol(mode: "stop"): void
/**移动到某个位置 */
declare function ucontrol(mode: "move", x: number, y: number): void
/**靠近某个位置一定距离内 */
declare function ucontrol(mode: "approach", x: number, y: number, radius: number): void
/**开始/停止助推 */
declare function ucontrol(mode: "boost", enable: boolean): void
/**向某个位置瞄准/射击 */
declare function ucontrol(mode: "target", x: number, y: number, shoot: boolean): void
/**根据提前量向某个目标瞄准/射击 */
declare function ucontrol(mode: "targetp", unit: string, shoot: boolean): void
/**将携带的物品放入一座建筑 */
declare function ucontrol(mode: "itemDrop", to: number, amount: number): void
/**从建筑中取出某种物品 */
declare function ucontrol(mode: "itemTake", from: number, item: number, amount: number): void
/**卸下当前载荷 */
declare function ucontrol(mode: "payDrop"): void
/**从当前位置拾取载荷 */
declare function ucontrol(mode: "payTake", takeUnits: number): void
/**进入/降落到单位下方的载荷方块中 */
declare function ucontrol(mode: "payEnter"): void
/**从某个位置采集矿物 */
declare function ucontrol(mode: "mine", x: number, y: number): void
/**给单位赋予数字形式的标记 */
declare function ucontrol(mode: "flag", value: number): void
/**建造建筑 */
declare function ucontrol(mode: "build", x: number, y: number, block: number, rotation: number, config: number): void
/**获取某个坐标处的建筑及其类型
 * 
 * 坐标需要在单位的感知范围内
 * 
 * 无建筑的地面返回 @air ， 墙壁返回 @solid */
declare function ucontrol(mode: "getBlock", x: number, y: number, type: number, building: number, floor: number): void
/**检查单位是否接近了某个位置 */
declare function ucontrol(mode: "within", x: number, y: number, radius: number, result: number): void
/**停用单位扽逻辑控制
 * 
 * 恢复常规AI */
declare function ucontrol(mode: "unbind"): void
/**让绑定的单位搜寻感知范围内的其他单位 */
declare function uradar(target1: string, target2: string, target3: string, order: boolean, sort: string, output: string): void
/**让绑定的单位搜寻整个地图中特定的建筑或位置 */
declare function ulocate(find: string, kwargs: any[]): void
/**矿脉 */
declare function ulocate(find: "ore", ore: string, outX: string, outY: string, found: string): void
/**某个分类下的建筑 */
declare function ulocate(find: "building", group: string, enemy: boolean, outX: string, outY: string, found: string, building: string): void
/**敌人出生点
 * 
 * 可以是核心或者某个坐标 */
declare function ulocate(find: "spawn", outX: string, outY: string, found: string, building: string): void
/**受损的己方建筑 */
declare function ulocate(find: "damaged", outX: string, outY: string, found: string, building: string): void

const MindFunc = { read, write, draw, print, drawflush, printflush, getlink, control, radar, sensor, lookup, packcolor, wait, stop, ubind, ucontrol, uradar, ulocate }

//#endregion


export { MindBlocks, MindFunc }