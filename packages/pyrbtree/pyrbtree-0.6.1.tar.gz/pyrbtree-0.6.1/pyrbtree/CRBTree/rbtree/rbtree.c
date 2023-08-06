#ifndef EXPORT
#define EXPORT __declspec(dllexport)
#endif

#include <stddef.h>
#include <stdlib.h>
#include <string.h>

#include "rbtree.h"
#include "rbinternal.h"


extern const unsigned char RBVERSION[];

/**
 * @brief Returns the current library version as 4 bytes.
 * 
 * @return a pointer to a 4 bytes array major, minor, patch, level
*/
const unsigned char* RBversion() {
	return RBVERSION;
}

static RBIter* search(RBTree* tree, void* data, int* how) {
	if (0 == tree->black_depth) return NULL;
	int md = 1 + 2 * tree->black_depth;
	RBIter *iter = malloc(sizeof(RBIter) + md * sizeof(struct iter_elt));
	if (NULL == iter) return NULL;
	RBNode* curr = tree->root;
	int_fast8_t side = 0;
	int err = 0;
	for (int i = 0; i < md; i++) {
		iter->elt[i].node = curr;
		iter->elt[i].right = side;
		int next = tree->comperr(data, curr->data, &err, tree->comp);
		if (err != 0) {
			free(iter);
			return NULL;
		}
		if (0 == next) {
			iter->curdepth = i;
			*how = 0;
			break;
		}
		side = (next > 0);
		curr = curr->child[side];
		if (NULL == curr) {
			iter->curdepth = i;
			*how = side ? 1 : -1;
			break;
		}
		// md should be large enough for never falling out of the loop
	}
	return iter;
}

/**
 * @brief Searches a tree from a key and returns an iterator positioned there.
 * 
 * If the key is found in the tree, the next call of `RBnext` on the iterator
 * will return the element for that key. If it is not found, the next call will
 * return the first element with a greater key.
 * 
 * @param tree : the tree where the key is searched
 * @param key : the key to be searched
 * @return : an iterator positioned at that key
*/
RBIter* RBsearch(RBTree* tree, void* key) {
	int how;
	RBIter* iter = search(tree, key, &how);
	if (iter == NULL) {
		return NULL;
	}
	if (how > 0) {
		RBnext(iter);
	}
	return iter;
}


// 

/**
 * @brief Finds an element from a tree and returns it if found or returns NULL.
 * @param tree : the tree where the key is searched
 * @param key : the key to be searched
 * @return : the element for that key
*/
EXPORT void* RBfind(RBTree* tree, void* key) {
	int how;
	RBIter* iter = search(tree, key, &how);
	void* data = ((iter == NULL) || (how != 0)) ? NULL :
		iter->elt[iter->curdepth].node->data;
	RBiter_release(iter);
	return data;
}

static void iter_push(RBIter* iter, RBNode* node, int side) {
	iter->elt[++iter->curdepth].node = node;
	iter->elt[iter->curdepth].right = side;
}

/**
 * @brief Builds an iterator pointing to the first element.
 * 
 * @param tree : the tree which is to be iterated
 * @return : and iterator pointing to the first element of the tree
*/
RBIter* RBfirst(RBTree* tree) {
	int md = 1 + 2 * tree->black_depth;
	RBIter* iter = malloc(sizeof(RBIter) + md * sizeof(struct iter_elt));
	if (NULL == iter) return NULL;
	RBNode* curr = tree->root;
	if (curr == NULL) {
		iter->curdepth = -1;
	}
	else {
		for (int i = 0; i < md; i++) {
			iter->elt[i].node = curr;
			iter->elt[i].right = 0;
			iter->curdepth = i;
			if (curr->child[0]) curr = curr->child[0];
			else break;
		}
	}
	return iter;
}

/**
 * @brief : Returns the currently pointed element and advances the iterator.
 * 
 * @param iter : the iterator
 * @return : the currently pointed element
*/
void* RBnext(RBIter* iter) {
	if (iter->curdepth == -1) return NULL;
	RBNode* node = iter->elt[iter->curdepth].node;
	void* data = node->data;
	if (node->child[1]) {
		node = node->child[1];
		iter_push(iter, node, 1);
		while (node->child[0]) {
			node = node->child[0];
			iter_push(iter, node, 0);
		}
	}
	else {
		while (iter->elt[iter->curdepth--].right);
	}
	return data;
}

static RBNode* new_node(void* data) {
	RBNode* node = malloc(sizeof(*node));
	if (NULL != node) {
		memset(node->child, 0, sizeof(node->child));
		node->red = 1;
		node->data = data;
	}
	return node;
}

static RBNode* rotate(RBNode* node, int side) {
	RBNode *next = node->child[1 - side];
	node->child[1 - side] = next->child[side];
	next->child[side] = node;
	return next;
}

static RBNode* fix_red_violation(RBIter* iter, int side) {
	for (;;) {
		RBNode* parent = iter->elt[iter->curdepth - 1].node;
		if (parent->child[!iter->elt[iter->curdepth].right] &&
			parent->child[!iter->elt[iter->curdepth].right]->red) {
			// sibling is red: just swap colors
			for (int i = 0; i < 2; i++) parent->child[i]->red = 0;
			parent->red = 1;
		}
		else {
			int curside = iter->elt[iter->curdepth].right;
			// sibling is black: we will have to rotate
			if (side != curside) {
				// we need an additional rotation
				parent->child[1 - side] = rotate(parent->child[1 - side],
					1 - side);
			}
			parent = rotate(parent, 1 - curside);
			parent->child[1-curside]->red = 1;
			parent->red = 0;
			if (iter->curdepth == 1) {
				return parent;
			}
			iter->elt[iter->curdepth - 2].node->child[iter->elt[iter->curdepth - 1].right] = parent;
			break;
		}
		if (iter->curdepth > 2) {
			iter->curdepth -= 2;
			if (!iter->elt[iter->curdepth].node->red) break;
			side = iter->elt[iter->curdepth + 1].right;
		}
		else break;
	}
	return iter->elt[0].node;
}

static int defcomp2(const void* a, const void* b, int* err,
		int (*comp)()) {
	return comp(a, b);
}

static int defcomp3(const void* a, const void* b, int* err, int (*comp)()) {
	return comp(a, b, err);
}
/**
 * @brief Initializes a new tree given a comparison function.
 *
 * Initialization makes a valid empty tree: the root node is set to NULL,
 * the black depth and the count to 0 and the comparison function pointer
 * points to the passed function.
 *
 * @param tree : pointer to the RBTree to initialize
 * @param comp : the comparison function
*/
void RBinit(RBTree* tree, int (*comp)(const void*, const void*)) {
	tree->root = NULL;
	tree->black_depth = 0;
	tree->count = 0;
	tree->comp = comp;
	tree->comperr = defcomp2;
}

/**
 * @brief Initializes a new tree given a comparison function handling errors.
 *
 * Initialization makes a valid empty tree: the root node is set to NULL,
 * the black depth and the count to 0 and the 3 args comparison function pointer
 * points to the passed function.
 *
 * @param tree : pointer to the RBTree to initialize
 * @param comp : the comparison function handling exceptional condition
*/
void RBinit2(RBTree* tree, int (*comp)(const void*, const void*, int*)) {
	tree->root = NULL;
	tree->black_depth = 0;
	tree->count = 0;
	tree->comp = comp;
	tree->comperr = defcomp3;
}

/**
 * @brief Releases all resources associated with an iterator.
 *
 * @param iter : the iterator to release
*/
void RBiter_release(RBIter* iter) {
	free(iter);
}

static void node_destroy(RBNode* node, void (*dele)(const void *)) {
	if (NULL == node) return;
	node_destroy(node->child[0], dele);
	node_destroy(node->child[1], dele);
	if (dele) dele(node->data);
	free(node);
}

/**
 * @brief Completely cleans a tree.
 *
 * RBdestroy removes all nodes from a tree and if dele is not null, applies
 * if to any referenced element (intended to free the elements resources).
 *
 * @param tree : the tree do clean
 * @param dele : an optional function that would be applied on evey element
*/
void RBdestroy(RBTree* tree, void (*dele)(const void*)) {
	node_destroy(tree->root, dele);
	tree->root = NULL;
	tree->black_depth = 0;
}

RBNode* node_clone(RBNode* old, void* (*process)(void* const)) {
	if (NULL == old) return NULL;
	RBNode* node = new_node((NULL == process) ?
		old->data : process(old->data));
	node->red = old->red;
	for (int i = 0; i < 2; i++) {
		node->child[i] = node_clone(old->child[i], process);
	}
	return node;
}

/**
 * @brief Duplicates a tree.
 * 
 * RBclone duplicates a tree by taking a fresh new copy of every node.
 * Optionaly, an operation can be applied on the data field.
 * (new_data = process(old_data))
 * 
 * @param old : the tree to duplicate 
 * @param process : an optional function to compute the new data from
 *                  the old one
 * @return : a copy of the tree
*/
RBTree* RBclone(RBTree* old, void* (*process)(void* const)) {
	RBTree* tree = malloc(sizeof(*tree));
	memcpy(tree, old, sizeof(*tree));
	tree->root = node_clone(old->root, process);
	return tree;
}

/**
 * @brief Inserts a new element into a valid tree.
 *
 * @param tree : the tree where to insert the element
 * @param data : the element to insert
 * @param error : a pointer to an int variable which if not NULL
 *  will be set to 0 if no error and a non zero value if error
 * @return : the previous element with same key if any or NULL
*/
void * RBinsert(RBTree* tree, void* data, int *error) {
	int how;
	RBIter* iter = search(tree, data, &how);
	if (error) *error = 1; // be conservative
	if (NULL == iter) {
		if (tree->black_depth == 0) {
			tree->root = new_node(data);
			tree->black_depth = 1;
			tree->count = 1;
			tree->root->red = 0;
			if (error) *error = 0;
		}
		return NULL;
	}
	void* old = NULL;
	RBNode* node = iter->elt[iter->curdepth].node;
	if (how == 0) {
		old = node->data;
		node->data = data;
	}
	else {
		int side = (how > 0);
		if (NULL == (node->child[side] = new_node(data))) return NULL;
		if (node->red) {
			tree->root = fix_red_violation(iter, side);
		}
	}
	RBiter_release(iter);
	if (error) *error = 0;
	if (tree->root && tree->root->red) {
		tree->root->red = 0;
		tree->black_depth += 1;
	}
	if (!old) tree->count += 1;
	return old;
}

#ifdef _TEST
EXPORT
#else
static
#endif // !_TEST
RBNode* paint_child_red(RBNode* node, int side) {
	RBNode* child = node->child[side];
	child->red = 1;
	if ((! child->child[side] || ! child->child[side]->red)
		&& child->child[1-side] && child->child[1-side]->red) {
		// additional rotation
		child = node->child[side] = rotate(child, side);
	}
	if (child->child[side] && child->child[side]->red) {
		node = rotate(node, 1 - side);
		node->child[side]->red = 0;
	}
	return node;
}

/**
 * @brief Removes an element from a tree and returns it.
 * 
 * @param tree : the tree to search
 * @param key : the key for which an element is to be retrieved
 * @return : NULL if the key could not be found or the removed element
*/
void* RBremove(RBTree* tree, void* key) {
	int how;
	RBNode* to_del = NULL;

	RBIter* iter = search(tree, key, &how);
	if (iter == NULL) return NULL;
	if (how != 0) {
		RBiter_release(iter);
		return NULL;
	}
	RBNode * node = iter->elt[iter->curdepth].node;
	void *data = node->data;
	void** old = &(node->data);
	RBNode* child;
	if (node->child[1] != NULL) {
		node = node->child[1];
		iter_push(iter, node, 1);
		while (node->child[0] != NULL) {
			node = node->child[0];
			iter_push(iter, node, 0);
		}
		child = node->child[1];
		*old = node->data;
	}
	else {
		child = node->child[0];
	}
	if (0 == iter->curdepth) {
		to_del = node;
		tree->root = child;
		tree->black_depth -= 1;
	}
	else {
		to_del = node;
		iter->elt[iter->curdepth - 1].node->child[iter->elt[
			iter->curdepth].right] = child
		;
		// handle a possible black violation.
		if (node->child[1] && node->child[1]->red) {
			node->child[1]->red = 0;
		}
		else if (0 == node->red) {
			int done = 0;
			while (! done) {
				int side = iter->elt[iter->curdepth].right;
				iter->curdepth -= 1;
				node = iter->elt[iter->curdepth].node;
				if (node->red) {
					// found a red ancestor
					node->red = 0;
					node = paint_child_red(node, 1 - side);
					done = 1;
				}
				else if (node->child[1 - side]->red) {
					// found a red sibling
					RBNode* old = node;
					node = rotate(node, side);
					node->red = 0;
					node->child[side] = paint_child_red(
						old, 1 - side);
					done = 1;
				}
				else {
					node = paint_child_red(node, 1 - side);
					if (node->red) {
						node->red = 0;
						done = 1;
					}
				}
				if (iter->curdepth > 0) {
					iter->elt[iter->curdepth - 1].node->child[
						iter->elt[iter->curdepth].right] = node;
				}
				else {
					tree->root = node;
					if (!done) tree->black_depth -= 1;
					done = 1;
				}
			}
		}
	}
	RBiter_release(iter);
	// handle a possible red root
	if (tree->root && tree->root->red) {
		tree->root->red = 0;
		tree->black_depth += 1;
	}
	tree->count -= 1;
	free(to_del);
	return data;
}

/* *
 * @brief Inserts an array of elements into a valid tree.
 *
 * Inserts a number of elements in one single call. The returned value
 * is the number of elements that did not pre-exist in the tree. If an
 * element is replaced and if dele is not NULL, it is called with that
 * element as parameter.
 *
 * @param tree : the tree where to insert the elements
 * @param data : an array of elements
 * @param n : number of elements in data
 * @param dele : an optional function to release replaced elements or NULL
 * @return : the number of new elements inserted in the tree
*//*
size_t RBbulk_insert(RBTree* tree, void** data, size_t n,
	void (*dele)(const void *)) {
	int inserted = 0, err;
	while (n-- > 0) {
		void* old = RBinsert(tree, *data++, &err);
		if (err) break;
		if (old) dele(old);
		else inserted += 1;
	}
	return inserted;
}
*/

static int node_validate(RBNode *node, int *total, 
		int (*comp)(const void *, const void *),
		int (*comperr)(const void*, const void *, int *,
			int (*c)(const void *, const void*))) {
	int child_level[2];
	int err = 0;
	*total += 1;
	for (int i = 0; i < 2; i++) {
		if (node->child[i] == 0) child_level[i] = 0;
		else {
			if (node->red && node->child[i]->red) return -RED_VIOLATION;
			int delta = comperr(node->child[i]->data, node->data, &err, comp);
			if (err || (delta >= 0 && 0 == i) || (delta <= 0 && 1 == i)) {
				return -ORDER_ERROR;
			}
			int lev = node_validate(node->child[i], total, comp, comperr);
			if (lev < 0) return lev;
			child_level[i] = lev;
		}
	}
	if (child_level[0] != child_level[1]) return -BLACK_VIOLATION;
	return child_level[0] + (!node->red);
}

/**
 * @brief Validates a tree.
 *
 * RBvalidate controls that a tree is correctly ordered, contains neither
 * red nor black violation and that its black_depth and count are correct.
 *
 * @param tree : the tree to validate
 * @return : 0 if the tree is correct or a (non-zero) error code
*/
int RBvalidate(RBTree* tree) {
	if ((0 == tree->black_depth) && (NULL == tree->root)) return 0;
	if ((0 == tree->black_depth) || (NULL == tree->root)) return DEPTH_ERROR;
	if (tree->root->red) return RED_ROOT;
	int total = 0;
	int lev = node_validate(tree->root, &total, tree->comp, tree->comperr);
	if (lev < 0) return -lev;
	if (lev != tree->black_depth) return DEPTH_ERROR;
	if (total != tree->count) return COUNT_ERROR;
	return 0;
}
