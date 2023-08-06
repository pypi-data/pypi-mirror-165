#ifndef RBTREE_H
#define RBTREE_H

#ifndef EXPORT
#define EXPORT __declspec(dllimport) 
#endif // EXPORT

#define BLACK_VIOLATION 1
#define RED_VIOLATION 2
#define RED_ROOT 3
#define DEPTH_ERROR 4
#define ORDER_ERROR 5
#define COUNT_ERROR 6

#include <stdlib.h>

#ifdef __cplusplus
extern "C" {
#endif
	// Current version
	EXPORT const unsigned char* RBversion();

	// Some opaque structures
	typedef struct _RBNode RBNode;
	typedef struct _RBIter RBIter;

	// The main structure
	typedef struct _RBTree {
		RBNode* root;
		unsigned black_depth;
		unsigned count;
		int (*comp)();
		int (*comperr)(const void*, const void*, int*, int (*comp)());
	} RBTree;

	// The public interface functions

	// Initializes a new tree given a comparison function.
	EXPORT void RBinit(RBTree* tree, int (*comp)(const void*, const void*));

	// Initializes a new tree given a comparison function handling exceptional conditions.
	EXPORT void RBinit2(RBTree* tree, int (*comperr)(const void*, const void*,
		int*));

	// Inserts a new element into a valid tree and return the previous element with same key if any.
	EXPORT void *RBinsert(RBTree* tree, void* data, int *error);

	// Removes an element from a tree and returns it
	EXPORT void* RBremove(RBTree* tree, void* key);

	// Finds an element from a tree and returns it if found or returns NULL
	EXPORT void* RBfind(RBTree* tree, void* key);

	// Searches a tree from a key and returns an iterator positioned there
	EXPORT RBIter* RBsearch(RBTree* tree, void* key);

	// Gets an iterator positioned at the first element of a tree
	EXPORT RBIter* RBfirst(RBTree* tree);

	// Gets next element from an iterator (returns NULL at the end)
	EXPORT void* RBnext(RBIter* iter);

	// Release all resources associated with an iterator.
	EXPORT void RBiter_release(RBIter* iter);

	// Completely cleans a tree.
	EXPORT void RBdestroy(RBTree* tree, void (*dele)(const void*));

	/*
	// Inserts an array of elements into a valid tree.
	EXPORT size_t RBbulk_insert(RBTree* tree, void** data, size_t n,
		void (*dele)( const void *));
	*/

	// Validates a tree.
	EXPORT int RBvalidate(RBTree* tree);

	// Dump a tree
	EXPORT int RBdump(RBTree* tree, size_t elt_width, void (*dump)(void*, char *));

	// Duplicates a tree
	EXPORT RBTree* RBclone(RBTree* old, void* (*process)(void* const));

#ifdef __cplusplus
}
#endif

#endif // !RBTREE_H

