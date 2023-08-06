#ifndef KTH_PY_NATIVE_BINARY_H_
#define KTH_PY_NATIVE_BINARY_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif


PyObject* kth_py_native_binary_construct(PyObject* self, PyObject* args);
PyObject* kth_py_native_binary_construct_string(PyObject* self, PyObject* args);
PyObject* kth_py_native_binary_construct_blocks(PyObject* self, PyObject* args);
PyObject* kth_py_native_binary_blocks(PyObject* self, PyObject* args);
PyObject* kth_py_native_binary_encoded(PyObject* self, PyObject* args);

#ifdef __cplusplus
} // extern "C"
#endif

#endif
