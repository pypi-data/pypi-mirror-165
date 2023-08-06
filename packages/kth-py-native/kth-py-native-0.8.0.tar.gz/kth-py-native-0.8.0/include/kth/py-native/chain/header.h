#ifndef KTH_PY_NATIVE_CHAIN_HEADER_H_
#define KTH_PY_NATIVE_CHAIN_HEADER_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_chain_header_to_data(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_construct(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_is_valid(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_factory_from_data(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_version(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_set_version(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_previous_block_hash(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_merkle(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_hash(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_timestamp(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_set_timestamp(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_bits(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_set_bits(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_nonce(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_set_nonce(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_header_destruct(PyObject* self, PyObject* args);

#ifdef __cplusplus
} //extern "C"
#endif

#endif
