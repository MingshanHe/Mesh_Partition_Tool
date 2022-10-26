import Sofa
import Sofa.Core
import Sofa.constants.Key as Key
import os
path = os.path.dirname(os.path.abspath(__file__))+'/mesh/'
filepath = os.path.dirname(os.path.abspath(__file__))

class SMA_wireController(Sofa.Core.Controller):
        def __init__(self, *a, **kw):
                Sofa.Core.Controller.__init__(self, *a, **kw)
                self.node = kw["node"]
                # self.constraints = []
                # self.constraints.append(self.node.getChild('finger').SMA_WireActuator.actuator_wire)
                print("initGraph SMA_wireController") 
        def onKeypressedEvent(self, e):
                if e["key"] == Sofa.constants.Key.plus:
                        print("heating")
                        wire = self.node.getChild('finger').SMA_WireActuator.actuator_wire
                        print(self.node.gravity.value)
                        # ls = Sofa.LinearSpring(0,0,0,0,0)  #(0, 1, 500., 5., 100.)
                        # for i in range (0, len(wire.spring)):
                        #         ls = wire.spring[i]            # insert SMA heating algorithm here
                        #         ls.L *=0.95
                        #         ls.Ks +=100
                        #         wire.spring[i] = ls
                        print(wire.stiffness.value)    

                elif e["key"] == Sofa.constants.Key.minus:
                        print("cooling")
                        wire = self.node.getChild('finger').SMA_WireActuator.actuator_wire
                        # ls = Sofa.LinearSpring(0,0,0,0,0)#(0, 1, 500., 5., 100.)
                        # for i in range (0, len(wire.spring)):
                        #         ls = wire.spring[i]            # insert SMA cooling algorithm here
                        #         ls.L /=0.95
                        #         ls.Ks -=100
                        #         wire.spring[i] = ls
                        print((len(wire.spring.value[0])))
                        print(type(wire.stiffness.value))
                        print(type(wire.spring))
                        print(type(wire.stiffness))


class FEMcontroller(Sofa.Core.Controller):
        def __init__(self, *a, **kw):
                Sofa.Core.Controller.__init__(self, *a, **kw)
                self.node = kw["node"]
                print("initGraph FEMcontroller") 
        def onKeypressedEvent(self, e):     
                if e["key"] == Sofa.constants.Key.uparrow:
                        print("stiffen") #UP key
                        print(self.node.getObject('FEM').findData('youngModulus').value)
                        self.node.getObject('FEM').findData('youngModulus').setValue(0,180000.0)
                        self.node.getObject('FEM').reinit()
                        print(self.node.getObject('FEM').findData('youngModulus'))
                elif e["key"] == Sofa.constants.Key.downarrow:
                        print("soften") #DOWN key
                        print(self.node.getObject('FEM').findData('youngModulus'))
                        self.node.getObject('FEM').findData('youngModulus').setValue(0,18000.0)
                        self.node.getObject('FEM').reinit()
                        print(self.node.getObject('FEM').findData('youngModulus'))
                elif e["key"] == "M":
                        print("localStiffnessFactor=")
                        #self.node.getObject('FEM').findData('localStiffnessFactor').setValue(0,1)
                        #self.node.getObject('FEM').findData('localStiffnessFactor').setValue(1,10)
                        self.node.getObject('FEM').reinit()
                        print(self.node.getObject('FEM').findData('localStiffnessFactor'))

def createScene(rootNode):
        rootNode.addObject('RequiredPlugin', pluginName='SoftRobots SofaPython3')
        rootNode.addObject('VisualStyle', displayFlags='showForceFields showBehaviorModels')
        # rootNode.addObject('VisualStyle', displayFlags='showVisualModels hideBehaviorModels hideCollisionModels hideBoundingCollisionModels hideForceFields showInteractionForceFields hideWireframe')
        rootNode.addObject('FreeMotionAnimationLoop')
        rootNode.addObject('GenericConstraintSolver', tolerance=1e-5, maxIterations=100)
        # rootNode.createObject('BackgroundSetting', color='0 0.168627 0.211765')
        # rootNode.createObject('OglSceneFrame', style="Arrows", alignment="TopRight")

        ##########################################
        #                FEM Model               #
        ##########################################
        finger = rootNode.addChild('finger')
        finger.addObject('EulerImplicitSolver', name='odesolver', rayleighStiffness=0.5, rayleighMass=0.5)
        finger.addObject('SparseLDLSolver', name='directSolver')

        finger.addObject('MeshVTKLoader', name='loader1', filename=path+'finger.vtk')
        finger.addObject('MeshTopology', src='@loader1', name='container')
        # finger.addObject('TetrahedronSetTopologyModifier')
        # finger.addObject('TetrahedronSetTopologyAlgorithms', template='Vec3d')
        # finger.addObject('TetrahedronSetGeometryAlgorithms', template='Vec3d')
        finger.addObject('MechanicalObject', name='tetras', template='Vec3d', showIndices='false', showIndicesScale='4e-5', rx='0', dz='0')
        # finger.addObject('MechanicalObject', name='tetras', template='Vec3', showObject=True, showObjectScale=1)
        finger.addObject('UniformMass', totalMass=0.500)
        finger.addObject('TetrahedronFEMForceField', template='Vec3', name='FEM', method='large', poissonRatio=0.3, youngModulus=18000)

        finger.addObject('BoxROI', name='boxROISubTopo', box=[-15, 0, 0, 5, 10, 15], drawBoxes=True)
        finger.createObject('RestShapeSpringsForceField', points='@ROI1.indices', stiffness=1e20, angularStiffness=1e20)
        finger.addObject('LinearSolverConstraintCorrection')
        rootNode.addObject(FEMcontroller(node=rootNode))
        ##########################################
        #                  Cable                 #
        ##########################################
        sma = finger.addChild('SMA_WireActuator')
        sma.addObject('MechanicalObject', position=(
                        "-17.5 12.5 2.5 " +
                        "-32.5 12.5 2.5 " +
                        "-47.5 12.5 2.5 " +
                        "-62.5 12.5 2.5 " +
                        "-77.5 12.5 2.5 " +

                        "-83.5 12.5 4.5 " +
                        "-85.5 12.5 6.5 " +
                        "-85.5 12.5 8.5 " +
                        "-83.5 12.5 10.5 " +

                        "-77.5 12.5 12.5 " +
                        "-62.5 12.5 12.5 " +
                        "-47.5 12.5 12.5 " +
                        "-32.5 12.5 12.5 " +
                        "-17.5 12.5 12.5 " ))
        sma.addObject('BarycentricMapping')
        # print("------------------------")
        # print("------------------------")
        # wire = rootNode.getChild('finger').SMA_WireActuator.actuator_wire
        # print(wire.getSprings())
        sma.addObject('StiffSpringForceField', stiffness="15000", template="Vec3d", name="actuator_wire", spring="0 1 5000 5 3.5 "+
                "1 2 5000 5 15 "+ 
                "2 3 5000 5 15 "+
                "3 4 5000 5 15 "+
                "4 5 5000 5 15 "+
                "5 6 5000 5 15 "+
                "6 7 5000 5 15 "+
                "7 8 5000 5 15 "+
                "8 9 5000 5 15 "+
                "9 10 5000 5 15 "+
                "10 11 5000 5 15 "+
                "11 12 5000 5 15 "+
                "12 13 5000 5 15 ")
        rootNode.addObject(SMA_wireController(node=rootNode))
        ######  ####################################
        #              Visualization             #
        ##########################################
        # fingerVisu = finger.addChild('visu')
        # fingerVisu.addObject('MeshOBJLoader', name='loader2', filename=path+"finger.stl")
        # fingerVisu.addObject('OglModel', name='Visual', src='@loader2', color=[0.0, 0.7, 0.7], scale=6.2)
        # fingerVisu.createObject('BarycentricMapping')
        
        return rootNode

