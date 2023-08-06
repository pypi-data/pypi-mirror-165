#ifndef KTH_PY_NATIVE_CHAIN_H_
#define KTH_PY_NATIVE_CHAIN_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_chain_fetch_block_by_height(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_fetch_block_by_hash(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_fetch_merkle_block_by_height(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_fetch_merkle_block_by_hash(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_fetch_block_header_by_height(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_fetch_block_header_by_hash(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_fetch_last_height(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_fetch_history(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_fetch_block_height(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_fetch_stealth(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_fetch_transaction(PyObject* self, PyObject* args);

// Note: Removed on 3.3.0
// PyObject* kth_py_native_chain_fetch_output(PyObject* self, PyObject* args);

PyObject* kth_py_native_chain_fetch_transaction_position(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_organize_block(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_organize_transaction(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_validate_tx(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_fetch_compact_block_by_hash(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_fetch_compact_block_by_height(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_fetch_spend(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_subscribe_blockchain(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_subscribe_transaction(PyObject* self, PyObject* args);

PyObject* kth_py_native_chain_unsubscribe(PyObject* self, PyObject* args);


#ifdef __cplusplus
} //extern "C"
#endif

#endif
