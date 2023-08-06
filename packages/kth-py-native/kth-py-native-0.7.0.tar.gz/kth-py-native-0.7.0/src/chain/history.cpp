// Copyright (c) 2016-2022 Knuth Project developers.
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include <kth/py-native/chain/history.h>
#include <kth/capi.h>
#include <kth/py-native/utils.h> //TODO(fernando): poner bien el dir del header

#ifdef __cplusplus
extern "C" {
#endif

// -------------------------------------------------------------------
// history_compact_list
// -------------------------------------------------------------------

PyObject* kth_py_native_history_compact_list_destruct(PyObject* self, PyObject* args) {
    PyObject* py_history_compact_list;

    if ( ! PyArg_ParseTuple(args, "O", &py_history_compact_list)) {
        return NULL;
    }

    kth_history_compact_list_t list = (kth_history_compact_list_t)get_ptr(py_history_compact_list);

    kth_chain_history_compact_list_destruct(list);

    Py_RETURN_NONE;
}

PyObject* kth_py_native_history_compact_list_count(PyObject* self, PyObject* args) {
    PyObject* py_history_compact_list;

    if ( ! PyArg_ParseTuple(args, "O", &py_history_compact_list)) {
        return NULL;
    }

    kth_history_compact_list_t list = (kth_history_compact_list_t)get_ptr(py_history_compact_list);

    kth_size_t res = kth_chain_history_compact_list_count(list);

    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_history_compact_list_nth(PyObject* self, PyObject* args) {
    PyObject* py_history_compact_list;
    uint64_t py_n;

    if ( ! PyArg_ParseTuple(args, "OK", &py_history_compact_list, &py_n)) {
        return NULL;
    }

    kth_history_compact_list_t list = (kth_history_compact_list_t)get_ptr(py_history_compact_list);

    kth_history_compact_t hc = kth_chain_history_compact_list_nth(list, py_n);

    PyObject* py_hc = to_py_obj(hc);
    return Py_BuildValue("O", py_hc);
}

// -------------------------------------------------------------------


// -------------------------------------------------------------------
// history_compact
// -------------------------------------------------------------------

PyObject* kth_py_native_history_compact_get_point_kind(PyObject* self, PyObject* args) {
    PyObject* py_history_compact;

    if ( ! PyArg_ParseTuple(args, "O", &py_history_compact)) {
        return NULL;
    }

    kth_history_compact_t hist = (kth_history_compact_t)get_ptr(py_history_compact);

    uint64_t res = kth_chain_history_compact_get_point_kind(hist);

    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_history_compact_get_point(PyObject* self, PyObject* args) {
    PyObject* py_history_compact;

    if ( ! PyArg_ParseTuple(args, "O", &py_history_compact)) {
        return NULL;
    }

    kth_history_compact_t hist = (kth_history_compact_t)get_ptr(py_history_compact);

    kth_point_t p = kth_chain_history_compact_get_point(hist);

    PyObject* py_p = to_py_obj(p);
    return Py_BuildValue("O", py_p);
}

PyObject* kth_py_native_history_compact_get_height(PyObject* self, PyObject* args) {
    PyObject* py_history_compact;

    if ( ! PyArg_ParseTuple(args, "O", &py_history_compact)) {
        return NULL;
    }

    kth_history_compact_t hist = (kth_history_compact_t)get_ptr(py_history_compact);

    uint64_t res = kth_chain_history_compact_get_height(hist);

    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_history_compact_get_value_or_previous_checksum(PyObject* self, PyObject* args) {
    PyObject* py_history_compact;

    if ( ! PyArg_ParseTuple(args, "O", &py_history_compact)) {
        return NULL;
    }

    kth_history_compact_t hist = (kth_history_compact_t)get_ptr(py_history_compact);

    uint64_t res = kth_chain_history_compact_get_value_or_previous_checksum(hist);

    return Py_BuildValue("K", res);
}


#ifdef __cplusplus
} //extern "C"
#endif
