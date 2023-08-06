// Copyright (c) 2016-2022 Knuth Project developers.
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include <kth/py-native/chain/chain.h>
#include <kth/capi.h>
#include <kth/py-native/utils.h> //TODO(fernando): poner bien el dir del header

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_chain_header_to_data(PyObject* self, PyObject* args) {
    PyObject* py_header;
    int py_version;

    if ( ! PyArg_ParseTuple(args, "OI", &py_header, &py_version)) {
        return NULL;
    }

    kth_header_t header = (kth_header_t)get_ptr(py_header);
    kth_size_t out_n;
    uint8_t* data = (uint8_t*)kth_chain_header_to_data(header, py_version, &out_n);
    // uint8_t const* kth_chain_header_to_data(kth_header_t header, uint32_t version, kth_size_t* out_size);
    return Py_BuildValue("y#", data, out_n);
}

// kth_header_t kth_chain_header_construct(uint32_t version, uint8_t* previous_block_hash, uint8_t* merkle, uint32_t timestamp, uint32_t bits, uint32_t nonce);
PyObject* kth_py_native_chain_header_construct(PyObject* self, PyObject* args){
    uint32_t py_version;
    char* py_previous_block_hash;
    size_t py_previous_block_hash_size;
    char* py_merkle;
    size_t py_merkle_size;
    uint32_t py_timestamp;
    uint32_t py_bits;
    uint32_t py_nonce;

    if ( ! PyArg_ParseTuple(args, "Iy#y#III", &py_version, &py_previous_block_hash, &py_previous_block_hash_size, &py_merkle, &py_merkle_size, &py_timestamp, &py_bits, &py_nonce)) {
        return NULL;
    }

    // kth_hash_t previous_block_hash;
    // memcpy(previous_block_hash.hash, py_previous_block_hash, 32);

    // kth_hash_t merkle;
    // memcpy(merkle.hash, py_merkle, 32);

    kth_header_t res = kth_chain_header_construct(py_version, (uint8_t*)py_previous_block_hash, (uint8_t*)py_merkle, py_timestamp, py_bits, py_nonce);
    return to_py_obj(res);
}

PyObject* kth_py_native_chain_header_is_valid(PyObject* self, PyObject* args){
    PyObject* py_header;

    if ( ! PyArg_ParseTuple(args, "O", &py_header)) {
        return NULL;
    }

    kth_header_t header = (kth_header_t)get_ptr(py_header);
    int res = kth_chain_header_is_valid(header);

    return Py_BuildValue("i", res);
}

PyObject* kth_py_native_chain_header_factory_from_data(PyObject* self, PyObject* args){
    uint32_t py_version;
    char* py_data;
    int py_n;

    if ( ! PyArg_ParseTuple(args, "Iy#", &py_version, &py_data, &py_n)) {
        return NULL;
    }

    kth_header_t res = kth_chain_header_factory_from_data(py_version, (uint8_t*)py_data, py_n);
    return to_py_obj(res);
}

PyObject* kth_py_native_chain_header_version(PyObject* self, PyObject* args){
    PyObject* py_header;
    kth_header_t header;
    uint32_t res;

    if ( ! PyArg_ParseTuple(args, "O", &py_header)) {
        return NULL;
    }

    header = (kth_header_t)get_ptr(py_header);
    res = kth_chain_header_version(header);

    return Py_BuildValue("I", res);
}

PyObject* kth_py_native_chain_header_set_version(PyObject* self, PyObject* args){
    PyObject* py_header;
    uint32_t py_version;
    kth_header_t header;

    if ( ! PyArg_ParseTuple(args, "OI", &py_header, &py_version)) {
        return NULL;
    }

    header = (kth_header_t)get_ptr(py_header);
    kth_chain_header_set_version(header, py_version);

    Py_RETURN_NONE;
}

PyObject* kth_py_native_chain_header_previous_block_hash(PyObject* self, PyObject* args){
    PyObject* py_header;

    if ( ! PyArg_ParseTuple(args, "O", &py_header)) {
        return NULL;
    }

    kth_header_t header = (kth_header_t)get_ptr(py_header);
    kth_hash_t res = kth_chain_header_previous_block_hash(header);

    return Py_BuildValue("y#", res.hash, 32);    //TODO: warning, hardcoded hash size!
}



/*
PyObject* kth_py_native_chain_header_set_previous_block_hash(PyObject* self, PyObject* args){
    PyObject* py_header;
    Py_ssize_t py_hash;

    if ( ! PyArg_ParseTuple(args, "OO", &py_header, &py_hash)) {
        return NULL;
    }

    char* s = PyString_AsString(py_hash);
    uint8_t * hash = (uint8_t*) malloc (sizeof(uint8_t[32]));
    hex2bin(s,&hash[31]);

    kth_header_t header = (kth_header_t)get_ptr(py_header);
    header_set_previous_block_hash(header, hash);

    Py_RETURN_NONE;
}

PyObject* kth_py_native_chain_header_set_merkle(PyObject* self, PyObject* args){
    PyObject* py_header;
    Py_ssize_t py_merkle;

    if ( ! PyArg_ParseTuple(args, "OO", &py_header, &py_merkle)) {
        return NULL;
    }

    char* s = PyString_AsString(py_merkle);
    uint8_t * hash = (uint8_t*) malloc (sizeof(uint8_t[32]));
    hex2bin(s,&hash[31]);

    kth_header_t header = (kth_header_t)get_ptr(py_header);
    header_set_merkle(header, hash);

    Py_RETURN_NONE;
}
*/

PyObject* kth_py_native_chain_header_merkle(PyObject* self, PyObject* args){
    PyObject* py_header;

    if ( ! PyArg_ParseTuple(args, "O", &py_header)) {
        return NULL;
    }

    kth_header_t header = (kth_header_t)get_ptr(py_header);
    kth_hash_t res = kth_chain_header_merkle(header);

    return Py_BuildValue("y#", res.hash, 32);    //TODO: warning, hardcoded hash size!
}

PyObject* kth_py_native_chain_header_hash(PyObject* self, PyObject* args){
    PyObject* py_header;

    if ( ! PyArg_ParseTuple(args, "O", &py_header)) {
        return NULL;
    }

    kth_header_t header = (kth_header_t)get_ptr(py_header);
    kth_hash_t res = kth_chain_header_hash(header);

    return Py_BuildValue("y#", res.hash, 32);    //TODO: warning, hardcoded hash size!
}

PyObject* kth_py_native_chain_header_timestamp(PyObject* self, PyObject* args){
    PyObject* py_header;

    if ( ! PyArg_ParseTuple(args, "O", &py_header)) {
        return NULL;
    }

    kth_header_t header = (kth_header_t)get_ptr(py_header);
    uint32_t res = kth_chain_header_timestamp(header);

    return Py_BuildValue("I", res);
}

PyObject* kth_py_native_chain_header_set_timestamp(PyObject* self, PyObject* args){
    PyObject* py_header;
    uint32_t py_timestamp;

    if ( ! PyArg_ParseTuple(args, "OI", &py_header, &py_timestamp)) {
        return NULL;
    }

    kth_header_t header = (kth_header_t)get_ptr(py_header);
    kth_chain_header_set_timestamp(header, py_timestamp);

    Py_RETURN_NONE;
}


PyObject* kth_py_native_chain_header_bits(PyObject* self, PyObject* args){
    PyObject* py_header;

    if ( ! PyArg_ParseTuple(args, "O", &py_header)) {
        return NULL;
    }

    kth_header_t header = (kth_header_t)get_ptr(py_header);
    uint32_t res = kth_chain_header_bits(header);

    return Py_BuildValue("I", res);
}

PyObject* kth_py_native_chain_header_set_bits(PyObject* self, PyObject* args){
    PyObject* py_header;
    uint32_t py_bits;

    if ( ! PyArg_ParseTuple(args, "OI", &py_header, &py_bits)) {
        return NULL;
    }

    kth_header_t header = (kth_header_t)get_ptr(py_header);
    kth_chain_header_set_bits(header, py_bits);

    Py_RETURN_NONE;
}

PyObject* kth_py_native_chain_header_nonce(PyObject* self, PyObject* args){
    PyObject* py_header;

    if ( ! PyArg_ParseTuple(args, "O", &py_header)) {
        return NULL;
    }

    kth_header_t header = (kth_header_t)get_ptr(py_header);
    uint32_t res = kth_chain_header_nonce(header);

    return Py_BuildValue("I", res);
}

PyObject* kth_py_native_chain_header_set_nonce(PyObject* self, PyObject* args){
    PyObject* py_header;
    uint32_t py_nonce;

    if ( ! PyArg_ParseTuple(args, "OI", &py_header, &py_nonce)) {
        return NULL;
    }

    kth_header_t header = (kth_header_t)get_ptr(py_header);
    kth_chain_header_set_nonce(header, py_nonce);

    Py_RETURN_NONE;
}


PyObject* kth_py_native_chain_header_destruct(PyObject* self, PyObject* args){
    PyObject* py_header;

    if ( ! PyArg_ParseTuple(args, "O", &py_header)) {
        return NULL;
    }

    kth_header_t header = (kth_header_t)get_ptr(py_header);
    kth_chain_header_destruct(header);

    Py_RETURN_NONE;
}



#ifdef __cplusplus
} //extern "C" {
#endif
