# -*- coding: utf-8 -*-
# @Time    : 2018/8/18 16:58
# @Author  : wb
# @File    : tree.py

from treelib import Node,Tree

# 给模板语句创建树

class Templatetree():

    # 构建树的函数
    def create(self,words_list,postags_list,arcs_list):
        # 输入三个list
        # 第一个是words_list 词语序列，词序
        # 第二个词性
        # 第三个是依存关系，这个也是用于构建树的关键

        tree = Tree()

        # 使用一层层的搭建技术
        # 我们设定五个层
        layer1 = []
        layer2 = []
        layer3 = []
        layer4 = []
        # layer5 = []
        # print('words_list' + str(words_list))
        # print('arcs_list'+str(arcs_list))

        # 首节点
        for i in range(len(arcs_list)):
            arc_head = arcs_list[i].split(':')[0]

            # 首节点
            if int(arc_head) == 0:
                HED_id = i

        # layer1层
        for i in range(len(arcs_list)):
            arc_head = arcs_list[i].split(':')[0]

            if int(arc_head) - 1 == int(HED_id):
                node = {'node' + str(i) : 'HED'}
                layer1.append(node)

        # layer2层
        for i in range(len(arcs_list)):
            arc_head = arcs_list[i].split(':')[0]

            # 说明有arc_head在layer1中，那就是这个点在layer2中
            for lay in layer1:
                if int(list(lay.keys())[0].lstrip('node')) == int(arc_head) - 1:
                    node = {'node' + str(i) : list(lay.keys())[0]}
                    layer2.append(node)

        # layer3层
        for i in range(len(arcs_list)):
            arc_head = arcs_list[i].split(':')[0]

            # 说明有arc_head在layer2中，那就是这个点在layer3中
            for lay in layer2:
                if int(list(lay.keys())[0].lstrip('node')) == int(arc_head) - 1:
                    node = {'node' + str(i): list(lay.keys())[0]}
                    layer3.append(node)

        # layer4层
        for i in range(len(arcs_list)):
            arc_head = arcs_list[i].split(':')[0]

            # 说明有arc_head在layer3中，那就是这个点在layer4中
            for lay in layer3:
                if int(list(lay.keys())[0].lstrip('node')) == int(arc_head) - 1:
                    node = {'node' + str(i): list(lay.keys())[0]}
                    layer4.append(node)


        # print(layer1)
        # print(layer2)
        # print(layer3)
        # print(layer4)


        # 四层都构建完毕
        # 下面就根据一层层的搭建树
        # 首先创建根节点
        if not tree.contains('HED'):
            tree.create_node(str(HED_id) + ' ' + words_list[int(HED_id)],
                             'HED',
                             data=postags_list[int(HED_id)] + ' ' + arcs_list[int(HED_id)].split(':')[1])

        # layer1
        for lay in layer1:
            nodename = list(lay.keys())[0]
            parent = list(lay.values())[0]
            tree.create_node(
                nodename.lstrip('node') + ' ' + words_list[int(nodename.lstrip('node'))],
                nodename,
                parent=parent,
                data=postags_list[int(nodename.lstrip('node'))] + ' ' + arcs_list[int(nodename.lstrip('node'))].split(':')[1])

        # layer2
        for lay in layer2:
            nodename = list(lay.keys())[0]
            parent = list(lay.values())[0]
            tree.create_node(
                nodename.lstrip('node') + ' ' + words_list[int(nodename.lstrip('node'))],
                nodename,
                parent=parent,
                data=postags_list[int(nodename.lstrip('node'))] + ' ' + arcs_list[int(nodename.lstrip('node'))].split(':')[1])

        # layer3
        for lay in layer3:
            nodename = list(lay.keys())[0]
            parent = list(lay.values())[0]
            tree.create_node(
                nodename.lstrip('node') + ' ' + words_list[int(nodename.lstrip('node'))],
                nodename,
                parent=parent,
                data=postags_list[int(nodename.lstrip('node'))] + ' ' + arcs_list[int(nodename.lstrip('node'))].split(':')[1])

        # layer4
        for lay in layer4:
            nodename = list(lay.keys())[0]
            parent = list(lay.values())[0]
            tree.create_node(
                nodename.lstrip('node') + ' ' + words_list[int(nodename.lstrip('node'))],
                nodename,
                parent=parent,
                data=postags_list[int(nodename.lstrip('node'))] + ' ' + arcs_list[int(nodename.lstrip('node'))].split(':')[1])

        return tree

    # 树的匹配与生成问句
    def matchandgenerate(self, question_tree, model_tree):
        # 输入由问题生成的tree
        # 输入由模板生成的tree
        # 比较两个tree有没有相同的部分（关系，词性都需要相同）
        # 树的匹配，question的tree是否为modeltree的一部分
        # questiontree的深度优先是否为modeltree子串的一部分

        # 深度遍历序列，节点对应的父节点序列

        # 两棵树的深度优先结果
        question_depeth_list = self.depth_first(question_tree)
        model_depeth_list = self.depth_first(model_tree)

        # print(question_depeth_list)

        # 设置问句与模板匹配标志，也就是能通过模板生成问句
        is_match = None

        for ques_node in question_depeth_list:
            for model_node in model_depeth_list:
                if (question_tree.parent(ques_node.identifier) == None) and (model_tree.parent(model_node.identifier) == None):
                    if ques_node.data == ques_node.data:
                        print(ques_node)
                        is_match = True
                    else:
                        is_match = False

        # 如果可以生成的话
        if is_match:
            print('可以生成')
            for ques_node in question_depeth_list:
                for model_node in model_depeth_list:
                    # 这两个节点的data 也就是 词性与关系相同
                    if ques_node.data == model_node.data:
                        # 并且他们的父节点的词性与关系也相同
                        if (question_tree.parent(ques_node.identifier) != None) and (model_tree.parent(model_node.identifier) != None):
                            if question_tree.parent(ques_node.identifier).data == model_tree.parent(model_node.identifier).data:
                                # 我们认为这样的节点就可以进行替换
                                model_node.tag.split()[1] = ques_node.tag.split()[1]
                        elif (question_tree.parent(ques_node.identifier) == None) and (model_tree.parent(model_node.identifier) == None):
                            # 父节点为None的是根节点，判断根节点的词性就行了
                            model_node.tag.split()[1] = ques_node.tag.split()[1]

            model_depeth_list.sort(key=lambda k: k.tag.split()[0], reverse=False)

            # 生成的新的问句
            new_question = ''
            new_question_list = []

            for i in model_depeth_list:
                new_question += i.tag.split()[1]
                new_question_list.append(i.tag.split()[1])

            print('新的问句：'+new_question)

            return [new_question,new_question_list]

        # 不匹配，无法生成问句
        else:
            return None

    # 树的深度优先遍历
    def depth_first(self,tree):

        # result = []
        # parent = []
        nodes = []
        for i in tree.expand_tree(mode=Tree.DEPTH):
            # print(tree.get_node(i))
            # 以深度优先获取树的节点
            node = tree.get_node(i)
            # nodes为该节点的信息
            nodes.append(node)
            # parent为该节点的父节点信息
            # parent.append(tree.parent(node.identifier))

            # depth_data = depth_data + tree.get_node(i).data + "|||"
        # 合在一起返回
        #　result.append(nodes)
        # result.append(parent)
        return nodes

    # 主运行函数
    # 输入ques_list和model_list 这两个list中包含三个list
    # 输入问句分词words_list
    # 输入词性postags_list
    # 输入关系arcs_list
    def main(self,question_list,model_list):
        print(question_list)
        ques_tree = self.create(words_list=question_list[0], postags_list=question_list[1],
                                        arcs_list=question_list[2])
        print(model_list)
        model_tree = self.create(words_list=model_list[0], postags_list=model_list[1],
                                         arcs_list=model_list[2])

        result = self.matchandgenerate(question_tree=ques_tree, model_tree=model_tree)

        return result

