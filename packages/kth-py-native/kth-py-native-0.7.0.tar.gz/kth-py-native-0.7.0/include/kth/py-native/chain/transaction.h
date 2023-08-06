#ifndef KTH_PY_NATIVE_CHAIN_TRANSACTION_H_
#define KTH_PY_NATIVE_CHAIN_TRANSACTION_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_chain_transaction_factory_from_data(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_transaction_version(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_transaction_set_version(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_transaction_hash(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_transaction_hash_sighash_type(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_transaction_locktime(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_transaction_serialized_size(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_transaction_fees(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_transaction_signature_operations(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_transaction_signature_operations_bip16_active(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_transaction_total_input_value(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_transaction_total_output_value(PyObject* self, PyObject* args);

PyObject* kth_py_native_chain_transaction_is_coinbase(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_transaction_is_null_non_coinbase(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_transaction_is_oversized_coinbase(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_transaction_is_mature(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_transaction_is_overspent(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_transaction_is_double_spend(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_transaction_is_missing_previous_outputs(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_transaction_is_final(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_transaction_is_locktime_conflict(PyObject* self, PyObject* args);

PyObject* kth_py_native_chain_transaction_destruct(PyObject* self, PyObject* args);

PyObject* kth_py_native_chain_transaction_outputs(PyObject* self, PyObject* args);
PyObject* kth_py_native_chain_transaction_inputs(PyObject* self, PyObject* args);

PyObject* kth_py_native_chain_transaction_to_data(PyObject* self, PyObject* args);

#ifdef __cplusplus
} //extern "C"
#endif

#endif //KTH_PY_CHAIN_TRANSACTION_H_
