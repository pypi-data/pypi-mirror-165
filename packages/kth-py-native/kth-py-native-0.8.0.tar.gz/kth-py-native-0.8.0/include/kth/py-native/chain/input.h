#ifndef KTH_PY_NATIVE_CHAIN_INPUT_H_
#define KTH_PY_NATIVE_CHAIN_INPUT_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif


PyObject* kth_py_native_chain_input_factory_from_data(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_input_construct(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_input_is_valid(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_input_is_final(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_input_serialized_size(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_input_sequence(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_input_signature_operations(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_input_destruct(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_input_script(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_input_previous_output(PyObject* self, PyObject* args);
//PyObject* kth_py_native_chain_input_hash(PyObject* self, PyObject* args);
//PyObject* kth_py_native_chain_input_index(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_input_to_data(PyObject* self, PyObject* args);


#ifdef __cplusplus
} //extern "C"
#endif


#endif
