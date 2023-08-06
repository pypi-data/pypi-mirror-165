#ifndef KTH_PY_NATIVE_CHAIN_OUTPUT_POINT_H_
#define KTH_PY_NATIVE_CHAIN_OUTPUT_POINT_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif


PyObject* kth_py_native_chain_output_point_hash(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_output_point_construct(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_output_point_construct_from_hash_index(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_output_point_index(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_output_point_destruct(PyObject* self, PyObject* args);

#ifdef __cplusplus
} //extern "C"
#endif

#endif
