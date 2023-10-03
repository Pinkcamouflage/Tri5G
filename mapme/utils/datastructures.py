"""
The following file, will be the implementation of necessary data structures such as binary search trees, hashmaps and Dataframes etc.
"""
import pdb
class HexTree:

    class TreeNode:
        def __init__(self, hex_marker):
            self.hex_marker = hex_marker
            self.left = None
            self.right = None
            self.height = 1  # Height of the subtree rooted at this node

    def __init__(self):
        self.root = None

    @staticmethod
    def get_height(node):
        if node is None:
            return 0
        return node.height

    @staticmethod
    def update_height(node):
        node.height = 1 + max(HexTree.get_height(node.left), HexTree.get_height(node.right))

    @staticmethod
    def get_balance_factor(node):
        if node is None:
            return 0
        return HexTree.get_height(node.left) - HexTree.get_height(node.right)

    @staticmethod
    def left_rotate(node):
        new_root = node.right
        node.right = new_root.left
        new_root.left = node

        HexTree.update_height(node)
        HexTree.update_height(new_root)

        return new_root

    @staticmethod
    def right_rotate(node):
        new_root = node.left
        node.left = new_root.right
        new_root.right = node

        HexTree.update_height(node)
        HexTree.update_height(new_root)

        return new_root

    def insert(self, hex_marker):
        self.root = self._insert(self.root, hex_marker)

    def _insert(self, root, hex_marker):
        if root is None:
            return HexTree.TreeNode(hex_marker)

        if hex_marker.hex_info['hex_id'] < root.hex_marker.hex_info['hex_id']:
            root.left = self._insert(root.left, hex_marker)
        else:
            root.right = self._insert(root.right, hex_marker)

        # Update height and balance factor
        HexTree.update_height(root)
        balance_factor = HexTree.get_balance_factor(root)

        # Perform rotations if needed to balance the tree
        if balance_factor > 1:
            if hex_marker.hex_info['hex_id'] < root.left.hex_marker.hex_info['hex_id']:
                return HexTree.right_rotate(root)
            else:
                root.left = HexTree.left_rotate(root.left)
                return HexTree.right_rotate(root)
        if balance_factor < -1:
            if hex_marker.hex_info['hex_id'] > root.right.hex_marker.hex_info['hex_id']:
                return HexTree.left_rotate(root)
            else:
                root.right = HexTree.right_rotate(root.right)
                return HexTree.left_rotate(root)

        return root

    def inorder_traversal(self):
        nodes = []

        def traverse(node):
            if node:
                traverse(node.left)
                nodes.append(node.hex_marker.hex_info)
                traverse(node.right)

        traverse(self.root)
        return nodes

    def balance_tree(self):
        # Create a list to store the nodes in sorted order
        nodes = []

        # Inorder traversal to extract nodes in sorted order
        self._inorder_traversal(self.root, nodes)

        # Rebuild the balanced tree using the sorted nodes
        self.root = self._build_balanced_tree(nodes, 0, len(nodes) - 1)

    def _inorder_traversal(self, node, nodes):
        if node:
            self._inorder_traversal(node.left, nodes)
            nodes.append(node)
            self._inorder_traversal(node.right, nodes)

    def _build_balanced_tree(self, nodes, start, end):
        if start > end:
            return None

        mid = (start + end) // 2
        root = nodes[mid]
        root.left = self._build_balanced_tree(nodes, start, mid - 1)
        root.right = self._build_balanced_tree(nodes, mid + 1, end)
        HexTree.update_height(root)

        return root

    def search(self, target_hex_id):
        return self._search(self.root, target_hex_id)

    def _search(self, root, target_hex_id):
        if root is None:
            return None

        if root.hex_marker.hex_info['hex_id'] == target_hex_id:
            return root.hex_marker
        elif target_hex_id < root.hex_marker.hex_info['hex_id']:
            return self._search(root.left, target_hex_id)
        else:
            return self._search(root.right, target_hex_id)

    def get(self, target_hex_id):
        return self._get(self.root, target_hex_id)

    def _get(self, root, target_hex_id):
        if root is None:
            return None

        if root.hex_marker.hex_info['hex_id'] == target_hex_id:
            return root.hex_marker
        elif target_hex_id < root.hex_marker.hex_info['hex_id']:
            return self._get(root.left, target_hex_id)
        else:
            return self._get(root.right, target_hex_id)
        

    #the following are test functions.

    def get_all_hex_ids(self):
        hex_ids = []
        self._get_all_hex_ids(self.root, hex_ids)
        return hex_ids

    def _get_all_hex_ids(self, root, hex_ids):
        if root:
            self._get_all_hex_ids(root.left, hex_ids)
            hex_ids.append(root.hex_marker.hex_info['hex_id'])
            self._get_all_hex_ids(root.right, hex_ids)















