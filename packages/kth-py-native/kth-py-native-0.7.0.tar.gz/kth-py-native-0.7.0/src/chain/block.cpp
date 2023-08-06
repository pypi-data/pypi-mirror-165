// Copyright (c) 2016-2022 Knuth Project developers.
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include <kth/py-native/chain/block.h>
#include <kth/capi.h>
#include <kth/py-native/utils.h> //TODO(fernando): poner bien el dir del header

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_chain_block_get_header(PyObject* self, PyObject* args){
    PyObject* py_block;

    if ( ! PyArg_ParseTuple(args, "O", &py_block)) {
        return NULL;
    }

    kth_block_t block = (kth_block_t)get_ptr(py_block);
    kth_header_t header = kth_chain_block_header(block);

    return to_py_obj(header);
}


//TODO(KNUTH-NEW): implement
// PyObject* kth_py_native_chain_block_transaction_count(PyObject* self, PyObject* args){
//     PyObject* py_block;

//     if ( ! PyArg_ParseTuple(args, "O", &py_block)) {
//         return NULL;
//     }

//     kth_block_t block = (kth_block_t)get_ptr(py_block);
//     kth_size_t res = kth_chain_block_transaction_count(block);

//     return Py_BuildValue("K", res);
// }

//TODO(KNUTH-NEW): implement
//kth_transaction_t kth_chain_block_transaction_nth(kth_block_t block, uint64_t n);
// PyObject* kth_py_native_chain_block_transaction_nth(PyObject* self, PyObject* args){
//     PyObject* py_block;
//     uint64_t py_n;

//     if ( ! PyArg_ParseTuple(args, "OK", &py_block, &py_n)) {
//         return NULL;
//     }

//     kth_block_t block = (kth_block_t)get_ptr(py_block);
//     kth_transaction_t res = kth_chain_block_transaction_nth(block, py_n);

//     return to_py_obj(res);
// }

PyObject* kth_py_native_chain_block_serialized_size(PyObject* self, PyObject* args){
    PyObject* py_block;
    uint32_t py_version;

    if ( ! PyArg_ParseTuple(args, "OI", &py_block, &py_version)) {
        return NULL;
    }

    kth_block_t block = (kth_block_t)get_ptr(py_block);
    kth_size_t res = kth_chain_block_serialized_size(block, py_version);

    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_chain_block_subsidy(PyObject* self, PyObject* args){
    kth_size_t py_height;

    if ( ! PyArg_ParseTuple(args, "K", &py_height)) {
        return NULL;
    }

    uint64_t res = kth_chain_block_subsidy(py_height);
    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_chain_block_fees(PyObject* self, PyObject* args){
    PyObject* py_block;

    if ( ! PyArg_ParseTuple(args, "O", &py_block)) {
        return NULL;
    }

    kth_block_t block = (kth_block_t)get_ptr(py_block);
    uint64_t res = kth_chain_block_fees(block);

    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_chain_block_claim(PyObject* self, PyObject* args){
    PyObject* py_block;


    if ( ! PyArg_ParseTuple(args, "O", &py_block)) {
        return NULL;
    }

    kth_block_t block = (kth_block_t)get_ptr(py_block);
    uint64_t res = kth_chain_block_claim(block);

    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_chain_block_reward(PyObject* self, PyObject* args){
    PyObject* py_block;
    uint64_t py_height;

    if ( ! PyArg_ParseTuple(args, "OK", &py_block, &py_height)) {
        return NULL;
    }

    kth_block_t block = (kth_block_t)get_ptr(py_block);
    uint64_t res = kth_chain_block_reward(block, py_height);

    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_chain_block_generate_merkle_root(PyObject* self, PyObject* args){
    PyObject* py_block;

    if ( ! PyArg_ParseTuple(args, "O", &py_block)) {
        return NULL;
    }

    kth_block_t block = (kth_block_t)get_ptr(py_block);
     kth_hash_t res = kth_chain_block_generate_merkle_root(block);

    return Py_BuildValue("y#", res.hash, 32);    //TODO: warning, hardcoded hash size!
}

PyObject* kth_py_native_chain_block_hash(PyObject* self, PyObject* args){
    PyObject* py_block;

    if ( ! PyArg_ParseTuple(args, "O", &py_block)) {
        return NULL;
    }

    kth_block_t block = (kth_block_t)get_ptr(py_block);
     kth_hash_t res = kth_chain_block_hash(block);

    return Py_BuildValue("y#", res.hash, 32);    //TODO: warning, hardcoded hash size!
}


PyObject* kth_py_native_chain_block_is_valid(PyObject* self, PyObject* args){
    PyObject* py_block;

    if ( ! PyArg_ParseTuple(args, "O", &py_block)) {
        return NULL;
    }

    kth_block_t block = (kth_block_t)get_ptr(py_block);
    int res = kth_chain_block_is_valid(block);

    return Py_BuildValue("i", res);
}

PyObject* kth_py_native_chain_block_signature_operations(PyObject* self, PyObject* args){
    PyObject* py_block;

    if ( ! PyArg_ParseTuple(args, "O", &py_block)) {
        return NULL;
    }

    kth_block_t block = (kth_block_t)get_ptr(py_block);
    uint64_t res = kth_chain_block_signature_operations(block);

    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_chain_block_signature_operations_bip16_active(PyObject* self, PyObject* args){
    PyObject* py_block;
    int py_bip16_active;

    if ( ! PyArg_ParseTuple(args, "Oi", &py_block, &py_bip16_active)) {
        return NULL;
    }

    kth_block_t block = (kth_block_t)get_ptr(py_block);
    uint64_t res = kth_chain_block_signature_operations_bip16_active(block, py_bip16_active);

    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_chain_block_total_inputs(PyObject* self, PyObject* args){
    PyObject* py_block;
    int py_with_coinbase;

    if ( ! PyArg_ParseTuple(args, "Oi", &py_block, &py_with_coinbase)) {
        return NULL;
    }

    kth_block_t block = (kth_block_t)get_ptr(py_block);
    uint64_t res = kth_chain_block_total_inputs(block, py_with_coinbase);

    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_chain_block_is_extra_coinbases(PyObject* self, PyObject* args){
    PyObject* py_block;

    if ( ! PyArg_ParseTuple(args, "O", &py_block)) {
        return NULL;
    }

    kth_block_t block = (kth_block_t)get_ptr(py_block);
    int res = kth_chain_block_is_extra_coinbases(block);

    return Py_BuildValue("i", res);
}

PyObject* kth_py_native_chain_block_is_final(PyObject* self, PyObject* args){
    PyObject* py_block;
    uint64_t py_height;
    uint32_t py_block_time;

    if ( ! PyArg_ParseTuple(args, "OKI", &py_block, &py_height, &py_block_time)) {
        return NULL;
    }

    kth_block_t block = (kth_block_t)get_ptr(py_block);
    int res = kth_chain_block_is_final(block, py_height, py_block_time);

    return Py_BuildValue("i", res);
}

PyObject* kth_py_native_chain_block_is_distinct_transaction_set(PyObject* self, PyObject* args){
    PyObject* py_block;

    if ( ! PyArg_ParseTuple(args, "O", &py_block)) {
        return NULL;
    }

    kth_block_t block = (kth_block_t)get_ptr(py_block);
    int res = kth_chain_block_is_distinct_transaction_set(block);

    return Py_BuildValue("i", res);
}

PyObject* kth_py_native_chain_block_is_valid_coinbase_claim(PyObject* self, PyObject* args){
    PyObject* py_block;
    uint64_t py_height;

    if ( ! PyArg_ParseTuple(args, "OK", &py_block, &py_height)) {
        return NULL;
    }

    kth_block_t block = (kth_block_t)get_ptr(py_block);
    int res = kth_chain_block_is_valid_coinbase_claim(block, py_height);

    return Py_BuildValue("i", res);
}
PyObject* kth_py_native_chain_block_is_valid_coinbase_script(PyObject* self, PyObject* args){
    PyObject* py_block;
    uint64_t py_height;

    if ( ! PyArg_ParseTuple(args, "OK", &py_block, &py_height)) {
        return NULL;
    }

    kth_block_t block = (kth_block_t)get_ptr(py_block);
    int res = kth_chain_block_is_valid_coinbase_script(block, py_height);

    return Py_BuildValue("i", res);
}

PyObject* kth_py_native_chain_block_is_internal_double_spend(PyObject* self, PyObject* args){
    PyObject* py_block;

    if ( ! PyArg_ParseTuple(args, "O", &py_block)) {
        return NULL;
    }

    kth_block_t block = (kth_block_t)get_ptr(py_block);
    int res = kth_chain_block_is_internal_double_spend(block);

    return Py_BuildValue("i", res);
}

PyObject* kth_py_native_chain_block_is_valid_merkle_root(PyObject* self, PyObject* args){
    PyObject* py_block;

    if ( ! PyArg_ParseTuple(args, "O", &py_block)) {
        return NULL;
    }

    kth_block_t block = (kth_block_t)get_ptr(py_block);
    int res = kth_chain_block_is_valid_merkle_root(block);

    return Py_BuildValue("i", res);
}


PyObject* kth_py_native_chain_block_destruct(PyObject* self, PyObject* args){
    PyObject* py_block;

    if ( ! PyArg_ParseTuple(args, "O", &py_block)) {
        return NULL;
    }

    kth_block_t block = (kth_block_t)get_ptr(py_block);
    kth_chain_block_destruct(block);

    Py_RETURN_NONE;
}

PyObject* kth_py_native_chain_block_transactions(PyObject* self, PyObject* args){
    PyObject* py_block;
    // printf("kth_py_native_chain_block_transactions - 1\n");

    if ( ! PyArg_ParseTuple(args, "O", &py_block)) {
        // printf("kth_py_native_chain_block_transactions - 2\n");
        return NULL;
    }

    // printf("kth_py_native_chain_block_transactions - 3\n");

    kth_block_t block = (kth_block_t)get_ptr(py_block);

    // printf("kth_py_native_chain_block_transactions - 4\n");

    kth_transaction_list_t list = kth_chain_block_transactions(block);

    // printf("kth_py_native_chain_block_transactions - 5\n");

    PyObject* py_list = to_py_obj(list);
    return Py_BuildValue("O", py_list);

    // printf("kth_py_native_chain_block_transactions - 6\n");

    // return ret;
}

#ifdef __cplusplus
} //extern "C"
#endif
