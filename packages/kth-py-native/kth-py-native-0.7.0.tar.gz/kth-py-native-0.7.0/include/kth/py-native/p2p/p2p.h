#ifndef KTH_PY_NATIVE_P2P_H_
#define KTH_PY_NATIVE_P2P_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_p2p_address_count(PyObject* self, PyObject* args);
PyObject* kth_py_native_p2p_stop(PyObject* self, PyObject* args);
PyObject* kth_py_native_p2p_close(PyObject* self, PyObject* args);
PyObject* kth_py_native_p2p_stopped(PyObject* self, PyObject* args);

#ifdef __cplusplus
} //extern "C"
#endif

#endif //KTH_PY_P2P_H_
