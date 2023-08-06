#ifndef KTH_PY_NATIVE_CHAIN_OUTPUT_LIST_H_
#define KTH_PY_NATIVE_CHAIN_OUTPUT_LIST_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_output_list_push_back(PyObject* self, PyObject* args);
PyObject* kth_py_native_output_list_count(PyObject* self, PyObject* args);
PyObject* kth_py_native_output_list_nth(PyObject* self, PyObject* args);


#ifdef __cplusplus
} //extern "C"
#endif

#endif
