// Copyright (c) 2016-2022 Knuth Project developers.
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef KTH_PY_NATIVE_MODULE_H_
#define KTH_PY_NATIVE_MODULE_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_node_construct(PyObject* self, PyObject* args);
PyObject* kth_py_native_node_destruct(PyObject* self, PyObject* args);
PyObject* kth_py_native_node_init_run_and_wait_for_signal(PyObject* self, PyObject* args);
PyObject* kth_py_native_node_signal_stop(PyObject* self, PyObject* args);
PyObject* kth_py_native_node_get_chain(PyObject* self, PyObject* args);
PyObject* kth_py_native_node_get_p2p(PyObject* self, PyObject* args);

PyObject* kth_py_native_node_print_thread_id(PyObject* self, PyObject* args);

// PyObject* kth_py_native_wallet_mnemonics_to_seed(PyObject* self, PyObject* args);

#ifdef __cplusplus
} // extern "C"
#endif

#endif // KTH_PY_NATIVE_MODULE_H_
