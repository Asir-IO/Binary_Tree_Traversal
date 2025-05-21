from manim import *
from objects import *
from processing import *

# def animate_L_and_tags(self, L, line, LBTag, BTag, forward=True):
#     if isinstance(L, Line):
#         start = L.get_start()
#         end = L.get_end()
#         mid = (start + end) / 2
#         L1 = Line(start, mid)
#         L2 = Line(mid, end)
#         L = [L1, L2] 
#     if forward:
        
#         BTreeDotAni1 = MoveAlongPath(self.trace_dot_BTree, L[0])
#         BTreeDotAni2 = MoveAlongPath(self.trace_dot_BTree, L[1])
#         LBTreeDotAni = MoveAlongPath(self.trace_dot_LBTree, line)
#     else:
#         BTreeDotAni1 = MoveAlongPath(self.trace_dot_BTree, L[1].put_start_and_end_on(L[1].get_end(), L[1].get_start()))
#         BTreeDotAni2 = MoveAlongPath(self.trace_dot_BTree, L[0].put_start_and_end_on(L[0].get_end(), L[0].get_start()))
#         LBTreeDotAni = MoveAlongPath(self.trace_dot_LBTree, line)
#     self.play(AnimationGroup(Succession(BTreeDotAni1, BTreeDotAni2), LBTreeDotAni), run_time=2)
#     self.play(Indicate(LBTag, color=YELLOW), run_time=2)
#     self.play(Indicate(BTag, color=YELLOW), run_time=2)
#     self.wait(0.2)

def indicate_tags(self, LBTag, BTag):
    self.play(Indicate(LBTag, color=YELLOW), run_time=2)
    self.play(Indicate(BTag, color=YELLOW), run_time=2)
    self.wait(0.2)

# def Trace(self, LBTree, BTree, node, counter, child_side=None):
#     if not node:
#         return
#     if child_side == None:
#         line = LBTree.entry_line
#         L = BTree.entry_line
#         LBTag = LBTree.tags[0]
#         BTag = BTree.tags[0]
#         animate_L_and_tags(self, L, line, LBTag, BTag, forward=True)

#         line = LBTree.lines[1]
#         L = BTree.Ls[0]
#         LBTag = LBTree.tags[1]
#         BTag = BTree.tags[1]
#         animate_L_and_tags(self, L, line, LBTag, BTag, forward=True)
#         counter[0] += 1
#         self.add(Tex(str(counter[0]), color=YELLOW).shift(UP*2))
#         Trace(self, LBTree, BTree, node.left, counter, 'left')
#         if node.left:
#             self.add(Tex(str(counter[0]), color=YELLOW))
#             L = BTree.Ls[counter[0]-2]
#             line = LBTree.lines[counter[0]]
#             LBTag = LBTree.tags[counter[0]]
#             animate_L_and_tags(self, L, line, LBTag, BTag, forward=False)
#         Trace(self, LBTree, BTree, node.right, counter, 'right')
#     else:
#         # Preorder
#         line = LBTree.lines[counter[0]]
#         L = BTree.Ls[counter[0]-1]
#         LBTag = LBTree.tags[counter[0]]
#         BTag = BTree.tags[counter[0]]
#         animate_L_and_tags(self, L, line, LBTag, BTag, forward=True)
#         counter[0] += 1
#         Trace(self, LBTree, BTree, node.left, counter, 'left')
#         Trace(self, LBTree, BTree, node.left, counter, 'right')
#         # Inorder
#         if node.left:
#             line = LBTree.lines[counter[0]]
#             LBTag = LBTree.tags[counter[0]]
#             self.add(Tex(str(counter[0]), color=PINK).shift(DOWN*2))
#             animate_L_and_tags(self, L, line, LBTag, BTag, forward=False)
#         Trace(self, LBTree, BTree, node.right, counter, 'right')
#         # postorder
#         if node.right:
#             line = LBTree.lines[counter[0]]
#             LBTag = LBTree.tags[counter[0]]
#             animate_L_and_tags(self, L, line, LBTag, BTag, forward=False)

def animate_L_and_tags(self, L, BTag, forward=True):
    if isinstance(L, Line):
        start = L.get_start()
        end = L.get_end()
        mid = (start + end) / 2
        L1 = Line(start, mid)
        L2 = Line(mid, end)
        L = [L1, L2] 
    if forward:
        BTreeDotAni1 = MoveAlongPath(self.trace_dot_BTree, L[0])
        BTreeDotAni2 = MoveAlongPath(self.trace_dot_BTree, L[1])
    else:
        BTreeDotAni1 = MoveAlongPath(self.trace_dot_BTree, L[1].put_start_and_end_on(L[1].get_end(), L[1].get_start()))
        BTreeDotAni2 = MoveAlongPath(self.trace_dot_BTree, L[0].put_start_and_end_on(L[0].get_end(), L[0].get_start()))
    self.play(AnimationGroup(Succession(BTreeDotAni1, BTreeDotAni2)), run_time=2)
    self.play(Indicate(BTag, color=YELLOW), run_time=2)
    self.wait(0.2)

def Trace(self, BTree, node, counter):
    if not node:
        return
    if node == BTree.root:
        # Pre traversal 
        L = BTree.entry_line
        BTag = BTree.tags[0]
        animate_L_and_tags(self, L, BTag, forward=True)
    # Preorder
    original_counter = counter[0]
    L = BTree.Ls[counter[0]]
    BTag = BTree.tags[counter[0]+1]
    animate_L_and_tags(self, L, BTag, forward=True)
    counter[0] += 1
    Trace(self, BTree, node.left, counter)
    # Inorder
    # When you're back, you certainly had a left regular or null child
    # Make it connnect to you
    counter[0] = original_counter
    L = BTree.Ls[counter[0]]
    BTag = BTree.tags[counter[0]+1]
    animate_L_and_tags(self, L, BTag, forward=False)
    
    counter[0] += 1
    # check your right children
    Trace(self, BTree, node.right, counter)
    # Postorder

    L = BTree.Ls[counter[0]]
    BTag = BTree.tags[counter[0]+1]
    animate_L_and_tags(self, L, BTag, forward=False)
