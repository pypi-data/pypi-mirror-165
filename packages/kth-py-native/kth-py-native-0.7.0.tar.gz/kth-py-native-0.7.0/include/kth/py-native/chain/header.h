#ifndef KTH_PY_NATIVE_CHAIN_HEADER_H_
#define KTH_PY_NATIVE_CHAIN_HEADER_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_chain_header_get_version(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_set_version(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_get_previous_block_hash(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_get_merkle(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_get_hash(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_get_timestamp(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_set_timestamp(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_get_bits(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_set_bits(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_get_nonce(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_set_nonce(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_destruct(PyObject* self, PyObject* args);

#ifdef __cplusplus
} //extern "C"
#endif

#endif
