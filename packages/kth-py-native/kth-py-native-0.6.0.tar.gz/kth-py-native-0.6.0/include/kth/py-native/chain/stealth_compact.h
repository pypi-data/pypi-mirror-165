#ifndef KTH_PY_NATIVE_CHAIN_STEALTH_COMPACT_H_
#define KTH_PY_NATIVE_CHAIN_STEALTH_COMPACT_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_stealth_compact_get_ephemeral_public_key_hash(PyObject* self, PyObject* args);
PyObject* kth_py_native_stealth_compact_get_transaction_hash(PyObject* self, PyObject* args);
PyObject* kth_py_native_stealth_compact_get_public_key_hash(PyObject* self, PyObject* args);

#ifdef __cplusplus
} //extern "C"
#endif

#endif
