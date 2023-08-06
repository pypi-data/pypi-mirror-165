#include <kth/py-native/chain/transaction.h>

#include <kth/capi.h>
#include <kth/py-native/utils.h>

#ifdef __cplusplus
extern "C" {
#endif

// kth_transaction_t kth_chain_transaction_factory_from_data(uint32_t version, uint8_t* data, uint64_t n) {
//     libbitcoin::data_chunk data_cpp(data, std::next(data, n));
//     auto tx = libbitcoin::message::transaction::factory_from_data(version, data_cpp);
//     return new libbitcoin::message::transaction(std::move(tx));
// }

PyObject* kth_py_native_chain_transaction_factory_from_data(PyObject* self, PyObject* args){
    uint32_t py_version;
    // uint8_t* py_seed;
    char* py_data;
    int py_n;

    if ( ! PyArg_ParseTuple(args, "Iy#", &py_version, &py_data, &py_n)) {
        return NULL;
    }

    kth_transaction_t res = kth_chain_transaction_factory_from_data(py_version, (uint8_t*)py_data, py_n);
    return to_py_obj(res);
}

PyObject* kth_py_native_chain_transaction_version(PyObject* self, PyObject* args){
    PyObject* py_transaction;
    if ( ! PyArg_ParseTuple(args, "O", &py_transaction)) {
        return NULL;
    }
    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);

    uint32_t res = kth_chain_transaction_version(transaction);
    return Py_BuildValue("I", res);
}

PyObject* kth_py_native_chain_transaction_set_version(PyObject* self, PyObject* args){
    PyObject* py_transaction;
    uint32_t py_version;

    if ( ! PyArg_ParseTuple(args, "OI", &py_transaction, &py_version)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    kth_chain_transaction_set_version(transaction, py_version);

    Py_RETURN_NONE;
}

PyObject* kth_py_native_chain_transaction_hash(PyObject* self, PyObject* args){
    PyObject* py_transaction;

    if ( ! PyArg_ParseTuple(args, "O", &py_transaction)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
     kth_hash_t res = kth_chain_transaction_hash(transaction);
    return PyByteArray_FromStringAndSize((char const*)res.hash, 32);
}

PyObject* kth_py_native_chain_transaction_hash_sighash_type(PyObject* self, PyObject* args){
    PyObject* py_transaction;
    uint32_t py_sighash_type;
    if ( ! PyArg_ParseTuple(args, "OI", &py_transaction, &py_sighash_type)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
     kth_hash_t res = kth_chain_transaction_hash_sighash_type(transaction, py_sighash_type);
    return PyByteArray_FromStringAndSize((char const*)res.hash, 32);

}

PyObject* kth_py_native_chain_transaction_locktime(PyObject* self, PyObject* args){
    PyObject* py_transaction;

    if ( ! PyArg_ParseTuple(args, "O", &py_transaction)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    uint32_t res = kth_chain_transaction_locktime(transaction);
    return Py_BuildValue("I", res);
}

PyObject* kth_py_native_chain_transaction_serialized_size(PyObject* self, PyObject* args){
    PyObject* py_transaction;
    int py_wire;
    if ( ! PyArg_ParseTuple(args, "Oi", &py_transaction, &py_wire)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    uint64_t res = kth_chain_transaction_serialized_size(transaction, py_wire);
    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_chain_transaction_fees(PyObject* self, PyObject* args){
    PyObject* py_transaction;

    if ( ! PyArg_ParseTuple(args, "O", &py_transaction)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    uint64_t res = kth_chain_transaction_fees(transaction);
    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_chain_transaction_signature_operations(PyObject* self, PyObject* args){
    PyObject* py_transaction;

    if ( ! PyArg_ParseTuple(args, "O", &py_transaction)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    uint64_t res = kth_chain_transaction_signature_operations(transaction);
    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_chain_transaction_signature_operations_bip16_active(PyObject* self, PyObject* args){
    PyObject* py_transaction;
    int py_bip16_active;

    if ( ! PyArg_ParseTuple(args, "Oi", &py_transaction, &py_bip16_active)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    uint64_t res = kth_chain_transaction_signature_operations_bip16_active(transaction, py_bip16_active);
    return Py_BuildValue("K", res);

}

PyObject* kth_py_native_chain_transaction_total_input_value(PyObject* self, PyObject* args){
    PyObject* py_transaction;

    if ( ! PyArg_ParseTuple(args, "O", &py_transaction)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    uint64_t res = kth_chain_transaction_total_input_value(transaction);
    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_chain_transaction_total_output_value(PyObject* self, PyObject* args){
    PyObject* py_transaction;

    if ( ! PyArg_ParseTuple(args, "O", &py_transaction)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    uint64_t res = kth_chain_transaction_total_output_value(transaction);
    return Py_BuildValue("K", res);

}

PyObject* kth_py_native_chain_transaction_is_coinbase(PyObject* self, PyObject* args){
    PyObject* py_transaction;

    if ( ! PyArg_ParseTuple(args, "O", &py_transaction)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    int res = kth_chain_transaction_is_coinbase(transaction);
    return Py_BuildValue("i", res);
}

PyObject* kth_py_native_chain_transaction_is_null_non_coinbase(PyObject* self, PyObject* args){
    PyObject* py_transaction;

    if ( ! PyArg_ParseTuple(args, "O", &py_transaction)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    int res = kth_chain_transaction_is_null_non_coinbase(transaction);
    return Py_BuildValue("i", res);
}

PyObject* kth_py_native_chain_transaction_is_oversized_coinbase(PyObject* self, PyObject* args){
    PyObject* py_transaction;

    if ( ! PyArg_ParseTuple(args, "O", &py_transaction)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    int res = kth_chain_transaction_is_oversized_coinbase(transaction);
    return Py_BuildValue("i", res);
}

PyObject* kth_py_native_chain_transaction_is_mature(PyObject* self, PyObject* args){
    PyObject* py_transaction;
    uint64_t py_target_height;

    if ( ! PyArg_ParseTuple(args, "OK", &py_transaction, &py_target_height)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    int res = kth_chain_transaction_is_mature(transaction, py_target_height);
    return Py_BuildValue("i", res);
}

PyObject* kth_py_native_chain_transaction_is_overspent(PyObject* self, PyObject* args){
    PyObject* py_transaction;

    if ( ! PyArg_ParseTuple(args, "O", &py_transaction)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    int res = kth_chain_transaction_is_overspent(transaction);
    return Py_BuildValue("i", res);
}

PyObject* kth_py_native_chain_transaction_is_double_spend(PyObject* self, PyObject* args){
    PyObject* py_transaction;
    int py_include_unconfirmed;

    if ( ! PyArg_ParseTuple(args, "Oi", &py_transaction, &py_include_unconfirmed)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    int res = kth_chain_transaction_is_double_spend(transaction, py_include_unconfirmed);
    return Py_BuildValue("i", res);
}


PyObject* kth_py_native_chain_transaction_is_missing_previous_outputs(PyObject* self, PyObject* args){
    PyObject* py_transaction;

    if ( ! PyArg_ParseTuple(args, "O", &py_transaction)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    int res = kth_chain_transaction_is_missing_previous_outputs(transaction);
    return Py_BuildValue("i", res);
}

//int kth_chain_transaction_is_final(kth_transaction_t transaction, uint64_t block_height, uint32_t block_time);
PyObject* kth_py_native_chain_transaction_is_final(PyObject* self, PyObject* args){
    PyObject* py_transaction;
    uint64_t py_block_height;
    uint32_t py_block_time;

    if ( ! PyArg_ParseTuple(args, "OKI", &py_transaction, &py_block_height, &py_block_time)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    int res = kth_chain_transaction_is_final(transaction, py_block_height, py_block_time);
    return Py_BuildValue("i", res);
}

PyObject* kth_py_native_chain_transaction_is_locktime_conflict(PyObject* self, PyObject* args){
    PyObject* py_transaction;

    if ( ! PyArg_ParseTuple(args, "O", &py_transaction)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    int res = kth_chain_transaction_is_locktime_conflict(transaction);
    return Py_BuildValue("i", res);
}

PyObject* kth_py_native_chain_transaction_destruct(PyObject* self, PyObject* args){
    PyObject* py_transaction;

    if ( ! PyArg_ParseTuple(args, "O", &py_transaction)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    kth_chain_transaction_destruct(transaction);
    Py_RETURN_NONE;
}


PyObject* kth_py_native_chain_transaction_outputs(PyObject* self, PyObject* args){
    PyObject* py_transaction;
    if ( ! PyArg_ParseTuple(args, "O", &py_transaction)) {
        return NULL;
    }
    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    kth_output_list_t res = kth_chain_transaction_outputs(transaction);
    return to_py_obj(res);

}

PyObject* kth_py_native_chain_transaction_inputs(PyObject* self, PyObject* args){
    PyObject* py_transaction;

    if ( ! PyArg_ParseTuple(args, "O", &py_transaction)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    kth_input_list_t res = kth_chain_transaction_inputs(transaction);
    return to_py_obj(res);
}

// uint8_t const* kth_chain_transaction_to_data(kth_transaction_t transaction, kth_bool_t wire, kth_size_t* out_size) {
PyObject* kth_py_native_chain_transaction_to_data(PyObject* self, PyObject* args) {
    PyObject* py_transaction;
    int py_wire;

    if ( ! PyArg_ParseTuple(args, "Oi", &py_transaction, &py_wire)) {
        return NULL;
    }

    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    kth_size_t out_n;
    uint8_t* data = (uint8_t*)kth_chain_transaction_to_data(transaction, py_wire, &out_n);

    return Py_BuildValue("y#", data, out_n);
}

#ifdef __cplusplus
} //extern "C"
#endif
