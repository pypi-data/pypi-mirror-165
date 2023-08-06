#ifndef KTH_PY_NATIVE_CHAIN_POINT_H_
#define KTH_PY_NATIVE_CHAIN_POINT_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_point_get_hash(PyObject* self, PyObject* args);
PyObject* kth_py_native_point_is_valid(PyObject* self, PyObject* args);
PyObject* kth_py_native_point_get_index(PyObject* self, PyObject* args);
PyObject* kth_py_native_point_get_checksum(PyObject* self, PyObject* args);

#ifdef __cplusplus
} //extern "C"
#endif

#endif
