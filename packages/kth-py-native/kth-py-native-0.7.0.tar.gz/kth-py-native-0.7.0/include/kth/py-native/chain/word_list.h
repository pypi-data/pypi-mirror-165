#ifndef KTH_PY_NATIVE_CHAIN_WORD_LIST_H_
#define KTH_PY_NATIVE_CHAIN_WORD_LIST_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_word_list_construct(PyObject* self, PyObject* args);
PyObject* kth_py_native_word_list_destruct(PyObject* self, PyObject* args);
PyObject* kth_py_native_word_list_add_word(PyObject* self, PyObject* args);

#ifdef __cplusplus
} //extern "C"
#endif

#endif
