#ifndef KTH_PY_NATIVE_CHAIN_MERKLE_BLOCK_H_
#define KTH_PY_NATIVE_CHAIN_MERKLE_BLOCK_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_chain_merkle_block_get_header(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_merkle_block_is_valid(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_merkle_block_hash_count(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_merkle_block_total_transaction_count(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_merkle_block_serialized_size(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_merkle_block_reset(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_merkle_block_destruct(PyObject* self, PyObject* args);

#ifdef __cplusplus
} //extern "C"
#endif

#endif
