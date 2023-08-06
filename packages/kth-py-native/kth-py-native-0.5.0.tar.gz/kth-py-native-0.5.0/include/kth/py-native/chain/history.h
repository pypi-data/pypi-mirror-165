#ifndef KTH_PY_NATIVE_CHAIN_HISTORY_H_
#define KTH_PY_NATIVE_CHAIN_HISTORY_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_history_compact_list_destruct(PyObject* self, PyObject* args);
PyObject* kth_py_native_history_compact_list_count(PyObject* self, PyObject* args);
PyObject* kth_py_native_history_compact_list_nth(PyObject* self, PyObject* args);
PyObject* kth_py_native_history_compact_get_point_kind(PyObject* self, PyObject* args);
PyObject* kth_py_native_history_compact_get_point(PyObject* self, PyObject* args);
PyObject* kth_py_native_history_compact_get_height(PyObject* self, PyObject* args);
PyObject* kth_py_native_history_compact_get_value_or_previous_checksum(PyObject* self, PyObject* args);

#ifdef __cplusplus
} //extern "C" {
#endif

#endif
