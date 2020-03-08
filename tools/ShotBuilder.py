import hou
import os
import string


def abc_in(abc, i):
    abc_name = abc.rpartition("/")[2][:-4]
    abc_node = hou.node('/obj').createNode('geo', 'abc_' + abc_name)
    alembic = abc_node.createNode('alembic', 'In_' + abc_name)
    alembic.parm('fileName').set(abc)
    node_pos = [0, i * 1]
    abc_node.setPosition(node_pos)


def cam_in(abc, i):
    camera = hou.node('/obj').createNode('alembicarchive', 'Cam1')
    camera.parm('fileName').set(abc)
    camera.parm('buildHierarchy').pressButton()
    node_pos = [3, i * 1]
    camera.setPosition(node_pos)


def build_shot():
    abc_files = hou.ui.selectFile(multiple_select=True)
    abcs = abc_files.split(' ; ')

    if abc_files is '' or '.abc' not in abc_files:
        pass

    else:
        prevs = hou.node('/obj').children()
        prev_cam = 0
        prev_abc = 0
        prev_null = 0
        for prev in prevs:
            if prev.type().name() == 'alembicarchive' and 'cam' in prev.name().lower():
                prev_cam -= 1
            elif prev.type().name() == 'geo' and prev.name().startswith('abc_'):
                prev_abc -= 1
            elif prev.type().name() == 'null':
                prev_null = 1
            else:
                pass

        if prev_null == 0:
            null_node = hou.node('/obj').createNode('null')
            null_node.parm('scale').set(0.1)
            null_node.setDisplayFlag(0)
            null_node.setPosition([1.5, 2])

        for abc in abcs:
            if '.abc' in abc:
                if 'cam' in abc.lower():
                    cam_in(abc, prev_cam)
                    prev_cam -= 1
                else:
                    abc_in(abc, prev_abc)
                    prev_abc -= 1


build_shot()
