#ifndef KTH_PY_NATIVE_CHAIN_COMPACT_BLOCK_H_
#define KTH_PY_NATIVE_CHAIN_COMPACT_BLOCK_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <kth/capi.h>
#include <kth/py-native/utils.h>

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_chain_compact_block_header(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_compact_block_is_valid(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_compact_block_serialized_size(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_compact_block_transaction_count(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_compact_block_transaction_nth(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_compact_block_nonce(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_compact_block_destruct(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_compact_block_reset(PyObject* self, PyObject* args);

#ifdef __cplusplus
} //extern "C"
#endif

#endif
