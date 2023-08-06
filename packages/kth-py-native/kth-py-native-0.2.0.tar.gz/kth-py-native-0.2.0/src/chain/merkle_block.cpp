// Copyright (c) 2016-2022 Knuth Project developers.
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include <kth/py-native/chain/merkle_block.h>
#include <kth/capi.h>
#include <kth/py-native/utils.h> //TODO(fernando): poner bien el dir del header

#ifdef __cplusplus
extern "C" {
#endif


PyObject* kth_py_native_chain_merkle_block_get_header(PyObject* self, PyObject* args){
    PyObject* py_merkle;

    if ( ! PyArg_ParseTuple(args, "O", &py_merkle)) {
        return NULL;
    }

    kth_merkleblock_t merkle_block = (kth_merkleblock_t)get_ptr(py_merkle);
    kth_header_t header = kth_chain_merkle_block_header(merkle_block);

    return to_py_obj(header);//TODO: Está bien esto? O tiene que ser un BuildValue????

}

PyObject* kth_py_native_chain_merkle_block_is_valid(PyObject* self, PyObject* args){
    PyObject* py_merkle_block;

    if ( ! PyArg_ParseTuple(args, "O", &py_merkle_block)) {
        return NULL;
    }

    kth_merkleblock_t block = (kth_merkleblock_t)get_ptr(py_merkle_block);
    int res = kth_chain_merkle_block_is_valid(block);

    return Py_BuildValue("i", res);
}

PyObject* kth_py_native_chain_merkle_block_hash_count(PyObject* self, PyObject* args){
    PyObject* py_merkle_block;

    if ( ! PyArg_ParseTuple(args, "O", &py_merkle_block)) {
        return NULL;
    }

    kth_merkleblock_t block = (kth_merkleblock_t)get_ptr(py_merkle_block);
    kth_size_t res = kth_chain_merkle_block_hash_count(block);

    return Py_BuildValue("K", res);
}


PyObject* kth_py_native_chain_merkle_block_total_transaction_count(PyObject* self, PyObject* args){
    PyObject* py_merkle_block;

    if ( ! PyArg_ParseTuple(args, "O", &py_merkle_block)) {
        return NULL;
    }

    kth_merkleblock_t block = (kth_merkleblock_t)get_ptr(py_merkle_block);
    kth_size_t res = kth_chain_merkle_block_total_transaction_count(block);

    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_chain_merkle_block_serialized_size(PyObject* self, PyObject* args){
    PyObject* py_merkle_block;
    uint32_t py_version;

    if ( ! PyArg_ParseTuple(args, "OI", &py_merkle_block, &py_version)) {
        return NULL;
    }

    kth_merkleblock_t block = (kth_merkleblock_t)get_ptr(py_merkle_block);
    kth_size_t res = kth_chain_merkle_block_serialized_size(block, py_version);

    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_chain_merkle_block_reset(PyObject* self, PyObject* args){
    PyObject* py_merkle_block;

    if ( ! PyArg_ParseTuple(args, "O", &py_merkle_block)) {
        return NULL;
    }

    kth_merkleblock_t block = (kth_merkleblock_t)get_ptr(py_merkle_block);
    kth_chain_merkle_block_reset(block);

    Py_RETURN_NONE;
}

PyObject* kth_py_native_chain_merkle_block_destruct(PyObject* self, PyObject* args){
    PyObject* py_merkle_block;

    if ( ! PyArg_ParseTuple(args, "O", &py_merkle_block)) {
        return NULL;
    }

    kth_merkleblock_t block = (kth_merkleblock_t)get_ptr(py_merkle_block);
    kth_chain_merkle_block_destruct(block);

    Py_RETURN_NONE;
}


#ifdef __cplusplus
} //extern "C"
#endif
