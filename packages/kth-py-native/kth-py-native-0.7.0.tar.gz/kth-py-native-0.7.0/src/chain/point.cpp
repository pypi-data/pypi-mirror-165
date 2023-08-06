// Copyright (c) 2016-2022 Knuth Project developers.
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include <kth/py-native/chain/point.h>
#include <kth/capi.h>
#include <kth/py-native/utils.h> //TODO(fernando): poner bien el dir del header

#ifdef __cplusplus
extern "C" {
#endif

// -------------------------------------------------------------------
// point
// -------------------------------------------------------------------

//  kth_hash_t point_get_hash(kth_point_t point){
// kth_bool_t point_is_valid(kth_point_t point){
// uint32_t point_get_index(kth_point_t point){
// uint64_t point_get_checksum(kth_point_t point){

PyObject* kth_py_native_point_get_hash(PyObject* self, PyObject* args) {
    PyObject* py_point;

    if ( ! PyArg_ParseTuple(args, "O", &py_point)) {
        return NULL;
    }

    kth_point_t p = (kth_point_t)get_ptr(py_point);
    kth_hash_t res = kth_chain_point_get_hash(p);
    return Py_BuildValue("y#", res.hash, 32);    //TODO: warning, hardcoded hash size!
}

PyObject* kth_py_native_point_is_valid(PyObject* self, PyObject* args) {
    PyObject* py_point;

    if ( ! PyArg_ParseTuple(args, "O", &py_point)) {
        return NULL;
    }

    kth_point_t p = (kth_point_t)get_ptr(py_point);

    int res = kth_chain_point_is_valid(p);

    if (res == 0) {
        Py_RETURN_FALSE;
    }

    Py_RETURN_TRUE;
}

PyObject* kth_py_native_point_get_index(PyObject* self, PyObject* args) {
    PyObject* py_point;

    if ( ! PyArg_ParseTuple(args, "O", &py_point)) {
        return NULL;
    }

    kth_point_t p = (kth_point_t)get_ptr(py_point);

    uint32_t res = kth_chain_point_get_index(p);
    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_point_get_checksum(PyObject* self, PyObject* args) {
    PyObject* py_point;

    if ( ! PyArg_ParseTuple(args, "O", &py_point)) {
        return NULL;
    }

    kth_point_t p = (kth_point_t)get_ptr(py_point);

    uint64_t res = kth_chain_point_get_checksum(p);

    return Py_BuildValue("K", res);
}

#ifdef __cplusplus
} //extern "C"
#endif
