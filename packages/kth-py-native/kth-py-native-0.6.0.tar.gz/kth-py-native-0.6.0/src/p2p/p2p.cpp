// Copyright (c) 2016-2022 Knuth Project developers.
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include <kth/py-native/p2p/p2p.h>
#include <kth/capi.h>
#include <kth/py-native/utils.h> //TODO(fernando): poner bien el dir del header


#ifdef __cplusplus
extern "C" {
#endif

// kth_size_t p2p_address_count(kth_p2p_t p2p);
// void p2p_stop(kth_p2p_t p2p);
// void p2p_close(kth_p2p_t p2p);
// kth_bool_t p2p_stopped(kth_p2p_t p2p);


PyObject* kth_py_native_p2p_address_count(PyObject* self, PyObject* args) {
    PyObject* py_p2p;

    if ( ! PyArg_ParseTuple(args, "O", &py_p2p)) {
        return NULL;
    }

    kth_p2p_t p2p = (kth_p2p_t)get_ptr(py_p2p);
    uint64_t res = kth_p2p_address_count(p2p);
    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_p2p_stop(PyObject* self, PyObject* args) {
    PyObject* py_p2p;

    if ( ! PyArg_ParseTuple(args, "O", &py_p2p)) {
        return NULL;
    }

    kth_p2p_t p2p = (kth_p2p_t)get_ptr(py_p2p);
    kth_p2p_stop(p2p);
    Py_RETURN_NONE;
}

PyObject* kth_py_native_p2p_close(PyObject* self, PyObject* args) {
    PyObject* py_p2p;

    if ( ! PyArg_ParseTuple(args, "O", &py_p2p)) {
        return NULL;
    }

    kth_p2p_t p2p = (kth_p2p_t)get_ptr(py_p2p);
    kth_p2p_close(p2p);
    Py_RETURN_NONE;
}

PyObject* kth_py_native_p2p_stopped(PyObject* self, PyObject* args) {
    PyObject* py_p2p;

    if ( ! PyArg_ParseTuple(args, "O", &py_p2p)) {
        return NULL;
    }

    kth_p2p_t p2p = (kth_p2p_t)get_ptr(py_p2p);
    int res = kth_p2p_stopped(p2p);
    return Py_BuildValue("i", res);
}

#ifdef __cplusplus
} //extern "C"
#endif

