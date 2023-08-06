#ifndef RBINTERNAL_H
#define RBINTERNAL_H

#include <stdint.h>
#include "rbtree.h"

struct _RBNode {
	void* data;
	struct _RBNode* child[2];
	int_fast8_t red;
};

struct iter_elt {
	struct _RBNode* node;
	int_fast8_t right;
};

struct _RBIter {
	int curdepth;
	struct iter_elt elt[];
};
#endif // 
