#ifndef KTH_PY_NATIVE_CHAIN_OUTPUT_H_
#define KTH_PY_NATIVE_CHAIN_OUTPUT_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif


PyObject* kth_py_native_chain_output_is_valid(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_output_serialized_size(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_output_value(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_output_signature_operations(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_output_destruct(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_output_script(PyObject* self, PyObject* args);

//PyObject* kth_py_native_chain_output_get_hash(PyObject* self, PyObject* args);
//PyObject* kth_py_native_chain_output_get_index(PyObject* self, PyObject* args);

PyObject* kth_py_native_chain_output_to_data(PyObject* self, PyObject* args);

#ifdef __cplusplus
} //extern "C"
#endif


#endif
