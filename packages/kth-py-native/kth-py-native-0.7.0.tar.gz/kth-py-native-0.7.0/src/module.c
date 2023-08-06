// Copyright (c) 2016-2022 Knuth Project developers.
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

//TODO: migrate to the new API for Extension Modules
//          https://docs.python.org/3/howto/cporting.html

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"


#include <kth/py-native/node.h>
// #include <kth/py-native/binary.h>
#include <kth/py-native/utils.h>
#include <kth/py-native/chain/point.h>
#include <kth/py-native/chain/history.h>
#include <kth/py-native/chain/chain.h>
#include <kth/py-native/chain/block.h>
#include <kth/py-native/chain/header.h>
#include <kth/py-native/chain/merkle_block.h>
#include <kth/py-native/chain/word_list.h>
#include <kth/py-native/chain/transaction.h>
#include <kth/py-native/chain/output.h>
#include <kth/py-native/chain/output_list.h>
#include <kth/py-native/chain/input.h>
#include <kth/py-native/chain/input_list.h>
#include <kth/py-native/chain/script.h>
#include <kth/py-native/chain/output_point.h>
#include <kth/py-native/chain/compact_block.h>
#include <kth/py-native/chain/payment_address.h>
#include <kth/py-native/chain/block_list.h>
#include <kth/py-native/chain/transaction_list.h>
#include <kth/py-native/chain/stealth_compact.h>
#include <kth/py-native/chain/stealth_compact_list.h>

#include <kth/py-native/p2p/p2p.h>

#include <kth/py-native/config/authority.h>
#include <kth/py-native/config/blockchain_settings.h>
#include <kth/py-native/config/checkpoint.h>
// #include <kth/py-native/config/convertions.h>
#include <kth/py-native/config/database_settings.h>
#include <kth/py-native/config/endpoint.h>
#include <kth/py-native/config/network_settings.h>
#include <kth/py-native/config/node_settings.h>
#include <kth/py-native/config/settings.h>


#include <kth/capi.h>

// #include <iostream>

// #define KTH_PY_SETATTR(to, from, var, fmt) PyObject_SetAttrString(to, #var, Py_BuildValue(fmt, from.var))
#define KTH_PY_SETATTR(to, from, var, fmt) PyObject_SetAttrString(to, #var, Py_BuildValue(fmt, from->var))

#ifdef __cplusplus
extern "C" {
#endif


static
PyMethodDef KnuthNativeMethods[] = {

    {"node_construct",  kth_py_native_node_construct, METH_VARARGS, "Construct the executor object."},
    {"node_destruct",  kth_py_native_node_destruct, METH_VARARGS, "Destruct the executor object."},
    // {"node_stopped",  kth_py_native_node_stopped, METH_VARARGS, "Check if Node is stopped."},
    // {"node_init_run_sync",  kth_py_native_node_init_run_sync, METH_VARARGS, "..."},
    {"node_init_run_and_wait_for_signal",  kth_py_native_node_init_run_and_wait_for_signal, METH_VARARGS, "..."},
    {"node_signal_stop",  kth_py_native_node_signal_stop, METH_VARARGS, "..."},
    {"node_get_chain",  kth_py_native_node_get_chain, METH_VARARGS, "Get Blockchain API."},
    {"node_get_p2p",  kth_py_native_node_get_p2p, METH_VARARGS, "Get P2P Networking API."},

    {"node_print_thread_id",  kth_py_native_node_print_thread_id, METH_VARARGS, "..."},

    {"p2p_address_count",  kth_py_native_p2p_address_count, METH_VARARGS, "..."},
    {"p2p_stop",  kth_py_native_p2p_stop, METH_VARARGS, "..."},
    {"p2p_close",  kth_py_native_p2p_close, METH_VARARGS, "..."},
    {"p2p_stopped",  kth_py_native_p2p_stopped, METH_VARARGS, "..."},

    {"chain_fetch_last_height",  kth_py_native_chain_fetch_last_height, METH_VARARGS, "..."},
    {"chain_fetch_history",  kth_py_native_chain_fetch_history, METH_VARARGS, "..."},
    // {"chain_fetch_stealth",  kth_py_native_chain_fetch_stealth, METH_VARARGS, "..."},
    {"chain_fetch_block_height",  kth_py_native_chain_fetch_block_height, METH_VARARGS, "..."},
    {"chain_fetch_block_header_by_height",  kth_py_native_chain_fetch_block_header_by_height, METH_VARARGS, "..."},
    {"chain_fetch_block_header_by_hash",  kth_py_native_chain_fetch_block_header_by_hash, METH_VARARGS, "..."},
    {"chain_fetch_block_by_height",  kth_py_native_chain_fetch_block_by_height, METH_VARARGS, "..."},
    {"chain_fetch_block_by_hash",  kth_py_native_chain_fetch_block_by_hash, METH_VARARGS, "..."},
    {"chain_fetch_merkle_block_by_height",  kth_py_native_chain_fetch_merkle_block_by_height, METH_VARARGS, "..."},
    {"chain_fetch_merkle_block_by_hash",  kth_py_native_chain_fetch_merkle_block_by_hash, METH_VARARGS, "..."},
    {"chain_fetch_transaction",  kth_py_native_chain_fetch_transaction, METH_VARARGS, "..."},

    {"chain_fetch_transaction_position",  kth_py_native_chain_fetch_transaction_position, METH_VARARGS, "..."},
    {"chain_organize_block",  kth_py_native_chain_organize_block, METH_VARARGS, "..."},
    {"chain_organize_transaction",  kth_py_native_chain_organize_transaction, METH_VARARGS, "..."},
    {"chain_validate_tx",  kth_py_native_chain_validate_tx, METH_VARARGS, "..."},
    {"chain_fetch_compact_block_by_height",  kth_py_native_chain_fetch_compact_block_by_height, METH_VARARGS, "..."},
    {"chain_fetch_compact_block_by_hash",  kth_py_native_chain_fetch_compact_block_by_hash, METH_VARARGS, "..."},
    {"chain_fetch_spend",  kth_py_native_chain_fetch_spend, METH_VARARGS, "..."},
    {"chain_subscribe_blockchain",  kth_py_native_chain_subscribe_blockchain, METH_VARARGS, "..."},
    {"chain_subscribe_transaction",  kth_py_native_chain_subscribe_transaction, METH_VARARGS, "..."},
    {"chain_unsubscribe",  kth_py_native_chain_unsubscribe, METH_VARARGS, "..."},

    {"chain_transaction_destruct",  kth_py_native_chain_transaction_destruct, METH_VARARGS, "..."},
    {"chain_transaction_factory_from_data",  kth_py_native_chain_transaction_factory_from_data, METH_VARARGS, "..."},
    {"chain_transaction_version",  kth_py_native_chain_transaction_version, METH_VARARGS, "..."},
    {"chain_transaction_set_version",  kth_py_native_chain_transaction_set_version, METH_VARARGS, "..."},
    {"chain_transaction_hash",  kth_py_native_chain_transaction_hash, METH_VARARGS, "..."},
    {"chain_transaction_hash_sighash_type",  kth_py_native_chain_transaction_hash_sighash_type, METH_VARARGS, "..."},
    {"chain_transaction_locktime",  kth_py_native_chain_transaction_locktime, METH_VARARGS, "..."},
    {"chain_transaction_serialized_size",  kth_py_native_chain_transaction_serialized_size, METH_VARARGS, "..."},
    {"chain_transaction_fees",  kth_py_native_chain_transaction_fees, METH_VARARGS, "..."},
    {"chain_transaction_signature_operations",  kth_py_native_chain_transaction_signature_operations, METH_VARARGS, "..."},
    {"chain_transaction_signature_operations_bip16_active",  kth_py_native_chain_transaction_signature_operations_bip16_active, METH_VARARGS, "..."},
    {"chain_transaction_total_input_value",  kth_py_native_chain_transaction_total_input_value, METH_VARARGS, "..."},
    {"chain_transaction_total_output_value",  kth_py_native_chain_transaction_total_output_value, METH_VARARGS, "..."},
    {"chain_transaction_is_coinbase",  kth_py_native_chain_transaction_is_coinbase, METH_VARARGS, "..."},
    {"chain_transaction_is_null_non_coinbase",  kth_py_native_chain_transaction_is_null_non_coinbase, METH_VARARGS, "..."},
    {"chain_transaction_is_oversized_coinbase",  kth_py_native_chain_transaction_is_oversized_coinbase, METH_VARARGS, "..."},
    {"chain_transaction_is_mature",  kth_py_native_chain_transaction_is_mature, METH_VARARGS, "..."},
    {"chain_transaction_is_overspent",  kth_py_native_chain_transaction_is_overspent, METH_VARARGS, "..."},
    {"chain_transaction_is_double_spend",  kth_py_native_chain_transaction_is_double_spend, METH_VARARGS, "..."},
    {"chain_transaction_is_missing_previous_outputs",  kth_py_native_chain_transaction_is_missing_previous_outputs, METH_VARARGS, "..."},
    {"chain_transaction_is_final",  kth_py_native_chain_transaction_is_final, METH_VARARGS, "..."},
    {"chain_transaction_is_locktime_conflict",  kth_py_native_chain_transaction_is_locktime_conflict, METH_VARARGS, "..."},
    {"chain_transaction_outputs",  kth_py_native_chain_transaction_outputs, METH_VARARGS, "..."},
    {"chain_transaction_inputs",  kth_py_native_chain_transaction_inputs, METH_VARARGS, "..."},
    {"chain_transaction_to_data",  kth_py_native_chain_transaction_to_data, METH_VARARGS, "..."},

    {"chain_input_destruct",  kth_py_native_kth_chain_input_destruct, METH_VARARGS, "..."},
    {"chain_input_is_valid",  kth_py_native_kth_chain_input_is_valid, METH_VARARGS, "..."},
    {"chain_input_is_final",  kth_py_native_kth_chain_input_is_final, METH_VARARGS, "..."},
    {"chain_input_serialized_size",  kth_py_native_kth_chain_input_serialized_size, METH_VARARGS, "..."},
    {"chain_input_sequence",  kth_py_native_kth_chain_input_sequence, METH_VARARGS, "..."},
    {"chain_input_signature_operations",  kth_py_native_kth_chain_input_signature_operations, METH_VARARGS, "..."},
    {"chain_input_script",  kth_py_native_kth_chain_input_script, METH_VARARGS, "..."},
    {"chain_input_previous_output",  kth_py_native_kth_chain_input_previous_output, METH_VARARGS, "..."},
    //{"chain_input_get_hash",  kth_py_native_kth_chain_input_get_hash, METH_VARARGS, "..."},
    //{"chain_input_get_index",  kth_py_native_kth_chain_input_get_index, METH_VARARGS, "..."},
    {"chain_input_to_data",  kth_py_native_kth_chain_input_to_data, METH_VARARGS, "..."},

    {"chain_input_list_push_back",  kth_py_native_input_list_push_back, METH_VARARGS, "..."},
    {"chain_input_list_count",  kth_py_native_input_list_count, METH_VARARGS, "..."},
    {"chain_input_list_nth",  kth_py_native_input_list_nth, METH_VARARGS, "..."},

    {"chain_output_destruct",  kth_py_native_chain_output_destruct, METH_VARARGS, "..."},
    {"chain_output_is_valid",  kth_py_native_chain_output_is_valid, METH_VARARGS, "..."},
    {"chain_output_serialized_size",  kth_py_native_chain_output_serialized_size, METH_VARARGS, "..."},
    {"chain_output_value",  kth_py_native_chain_output_value, METH_VARARGS, "..."},
    {"chain_output_signature_operations",  kth_py_native_chain_output_signature_operations, METH_VARARGS, "..."},
    {"chain_output_script",  kth_py_native_chain_output_script, METH_VARARGS, "..."},
    //{"chain_output_get_hash",  kth_py_native_chain_output_get_hash, METH_VARARGS, "..."},
    //{"chain_output_get_index",  kth_py_native_chain_output_get_index, METH_VARARGS, "..."},
    {"chain_output_to_data",  kth_py_native_chain_output_to_data, METH_VARARGS, "..."},


    {"chain_output_list_push_back",  kth_py_native_output_list_push_back, METH_VARARGS, "..."},
    {"chain_output_list_count",  kth_py_native_output_list_count, METH_VARARGS, "..."},
    {"chain_output_list_nth",  kth_py_native_output_list_nth, METH_VARARGS, "..."},

    {"chain_merkle_block_destruct",  kth_py_native_chain_merkle_block_destruct, METH_VARARGS, "..."},
    {"chain_merkle_block_get_header",  kth_py_native_chain_merkle_block_get_header, METH_VARARGS, "..."},
    {"chain_merkle_block_is_valid",  kth_py_native_chain_merkle_block_is_valid, METH_VARARGS, "..."},
    {"chain_merkle_block_hash_count",  kth_py_native_chain_merkle_block_hash_count, METH_VARARGS, "..."},
    {"chain_merkle_block_serialized_size",  kth_py_native_chain_merkle_block_serialized_size, METH_VARARGS, "..."},
    {"chain_merkle_block_total_transaction_count",  kth_py_native_chain_merkle_block_total_transaction_count, METH_VARARGS, "..."},
    {"chain_merkle_block_reset",  kth_py_native_chain_merkle_block_reset, METH_VARARGS, "..."},

    {"chain_block_destruct",  kth_py_native_chain_block_destruct, METH_VARARGS, "..."},
    {"chain_block_transactions",  kth_py_native_chain_block_transactions, METH_VARARGS, "..."},

    {"chain_block_get_header",  kth_py_native_chain_block_get_header, METH_VARARGS, "..."},
    {"chain_block_hash",  kth_py_native_chain_block_hash, METH_VARARGS, "..."},

    //TODO(KNUTH-NEW): implement
    // {"block_transaction_count",  kth_py_native_chain_block_transaction_count, METH_VARARGS, "..."},
    // {"block_transaction_nth",  kth_py_native_chain_block_transaction_nth, METH_VARARGS, "..."},

    {"chain_block_serialized_size",  kth_py_native_chain_block_serialized_size, METH_VARARGS, "..."},
    {"chain_block_fees",  kth_py_native_chain_block_fees, METH_VARARGS, "..."},
    {"chain_block_claim",  kth_py_native_chain_block_claim, METH_VARARGS, "..."},
    {"chain_block_reward",  kth_py_native_chain_block_reward, METH_VARARGS, "..."},
    {"chain_block_generate_merkle_root",  kth_py_native_chain_block_generate_merkle_root, METH_VARARGS, "..."},

    {"chain_block_is_valid",  kth_py_native_chain_block_is_valid, METH_VARARGS, "..."},
    {"chain_block_signature_operations",  kth_py_native_chain_block_signature_operations, METH_VARARGS, "..."},
    {"chain_block_signature_operations_bip16_active",  kth_py_native_chain_block_signature_operations_bip16_active, METH_VARARGS, "..."},
    {"chain_block_total_inputs",  kth_py_native_chain_block_total_inputs, METH_VARARGS, "..."},
    {"chain_block_is_extra_coinbases",  kth_py_native_chain_block_is_extra_coinbases, METH_VARARGS, "..."},
    {"chain_block_is_final",  kth_py_native_chain_block_is_final, METH_VARARGS, "..."},
    {"chain_block_is_distinct_transaction_set",  kth_py_native_chain_block_is_distinct_transaction_set, METH_VARARGS, "..."},
    {"chain_block_is_valid_coinbase_claim",  kth_py_native_chain_block_is_valid_coinbase_claim, METH_VARARGS, "..."},
    {"chain_block_is_valid_coinbase_script",  kth_py_native_chain_block_is_valid_coinbase_script, METH_VARARGS, "..."},
    {"chain_block_is_internal_double_spend",  kth_py_native_chain_block_is_internal_double_spend, METH_VARARGS, "..."},
    {"chain_block_is_valid_merkle_root",  kth_py_native_chain_block_is_valid_merkle_root, METH_VARARGS, "..."},

    {"chain_header_destruct",  kth_py_native_chain_header_destruct, METH_VARARGS, "..."},
    {"chain_header_get_version",  kth_py_native_chain_header_get_version, METH_VARARGS, "..."},
    {"chain_header_set_version",  kth_py_native_chain_header_set_version, METH_VARARGS, "..."},
    {"chain_header_get_previous_block_hash",  kth_py_native_chain_header_get_previous_block_hash, METH_VARARGS, "..."},
    //{"chain_header_set_previous_block_hash",  kth_py_native_chain_header_set_previous_block_hash, METH_VARARGS, "..."},
    {"chain_header_get_merkle",  kth_py_native_chain_header_get_merkle, METH_VARARGS, "..."},
    //{"chain_header_set_merkle",  kth_py_native_chain_header_set_merkle, METH_VARARGS, "..."},
    {"chain_header_get_hash",  kth_py_native_chain_header_get_hash, METH_VARARGS, "..."},
    {"chain_header_get_timestamp",  kth_py_native_chain_header_get_timestamp, METH_VARARGS, "..."},
    {"chain_header_set_timestamp",  kth_py_native_chain_header_set_timestamp, METH_VARARGS, "..."},
    {"chain_header_get_bits",  kth_py_native_chain_header_get_bits, METH_VARARGS, "..."},
    {"chain_header_set_bits",  kth_py_native_chain_header_set_bits, METH_VARARGS, "..."},
    {"chain_header_get_nonce",  kth_py_native_chain_header_get_nonce, METH_VARARGS, "..."},
    {"chain_header_set_nonce",  kth_py_native_chain_header_set_nonce, METH_VARARGS, "..."},

    {"chain_history_compact_list_destruct",  kth_py_native_history_compact_list_destruct, METH_VARARGS, "..."},
    {"chain_history_compact_list_count",  kth_py_native_history_compact_list_count, METH_VARARGS, "..."},
    {"chain_history_compact_list_nth",  kth_py_native_history_compact_list_nth, METH_VARARGS, "..."},
    {"chain_history_compact_get_point_kind",  kth_py_native_history_compact_get_point_kind, METH_VARARGS, "..."},
    {"chain_history_compact_get_point",  kth_py_native_history_compact_get_point, METH_VARARGS, "..."},
    {"chain_history_compact_get_height",  kth_py_native_history_compact_get_height, METH_VARARGS, "..."},
    {"chain_history_compact_get_value_or_previous_checksum",  kth_py_native_history_compact_get_value_or_previous_checksum, METH_VARARGS, "..."},

    {"chain_point_get_hash",  kth_py_native_point_get_hash, METH_VARARGS, "..."},
    {"chain_point_is_valid",  kth_py_native_point_is_valid, METH_VARARGS, "..."},
    {"chain_point_get_index",  kth_py_native_point_get_index, METH_VARARGS, "..."},
    {"chain_point_get_checksum",  kth_py_native_point_get_checksum, METH_VARARGS, "..."},

    {"chain_script_destruct",  kth_py_native_chain_script_destruct, METH_VARARGS, "..."},
    {"chain_script_is_valid",  kth_py_native_chain_script_is_valid, METH_VARARGS, "..."},
    {"chain_script_is_valid_operations",  kth_py_native_chain_script_is_valid_operations, METH_VARARGS, "..."},
    {"chain_script_satoshi_content_size",  kth_py_native_chain_script_satoshi_content_size, METH_VARARGS, "..."},
    {"chain_script_serialized_size",  kth_py_native_chain_script_serialized_size, METH_VARARGS, "..."},
    {"chain_script_to_string",  kth_py_native_chain_script_to_string, METH_VARARGS, "..."},
    {"chain_script_sigops",  kth_py_native_chain_script_sigops, METH_VARARGS, "..."},
    // {"chain_script_sigops",  kth_py_native_chain_script_sigops, METH_VARARGS, "..."},

    {"chain_output_point_get_hash",  kth_py_native_chain_output_point_get_hash, METH_VARARGS, "..."},
    //{"chain_point_is_valid",  kth_py_native_point_is_valid, METH_VARARGS, "..."},
    {"chain_output_point_get_index",  kth_py_native_chain_output_point_get_index, METH_VARARGS, "..."},
    {"chain_output_point_construct",  kth_py_native_chain_output_point_construct, METH_VARARGS, "..."},
    {"chain_output_point_construct_from_hash_index",  kth_py_native_chain_output_point_construct_from_hash_index, METH_VARARGS, "..."},
    {"chain_output_point_destruct",  kth_py_native_chain_output_point_destruct, METH_VARARGS, "..."},
    //{"chain_point_get_checksum",  kth_py_native_point_get_checksum, METH_VARARGS, "..."},

    {"chain_compact_block_header",  kth_py_native_chain_compact_block_header, METH_VARARGS, "..."},
    {"chain_compact_block_is_valid",  kth_py_native_chain_compact_block_is_valid, METH_VARARGS, "..."},
    {"chain_compact_block_serialized_size",  kth_py_native_chain_compact_block_serialized_size, METH_VARARGS, "..."},
    {"chain_compact_block_transaction_count",  kth_py_native_chain_compact_block_transaction_count, METH_VARARGS, "..."},
    {"chain_compact_block_transaction_nth",  kth_py_native_chain_compact_block_transaction_nth, METH_VARARGS, "..."},
    {"chain_compact_block_nonce",  kth_py_native_chain_compact_block_nonce, METH_VARARGS, "..."},
    {"chain_compact_block_destruct",  kth_py_native_chain_compact_block_destruct, METH_VARARGS, "..."},
    {"chain_compact_block_reset",  kth_py_native_chain_compact_block_reset, METH_VARARGS, "..."},

    {"chain_block_list_construct_default",  kth_py_native_chain_block_list_construct_default, METH_VARARGS, "..."},
    {"chain_block_list_push_back",  kth_py_native_chain_block_list_push_back, METH_VARARGS, "..."},
    {"chain_block_list_destruct",  kth_py_native_chain_block_list_destruct, METH_VARARGS, "..."},
    {"chain_block_list_count",  kth_py_native_chain_block_list_count, METH_VARARGS, "..."},
    {"chain_block_list_nth",  kth_py_native_chain_block_list_nth, METH_VARARGS, "..."},

    {"chain_transaction_list_construct_default",  kth_py_native_chain_transaction_list_construct_default, METH_VARARGS, "..."},
    {"chain_transaction_list_push_back",  kth_py_native_chain_transaction_list_push_back, METH_VARARGS, "..."},
    {"chain_transaction_list_destruct",  kth_py_native_chain_transaction_list_destruct, METH_VARARGS, "..."},
    {"chain_transaction_list_count",  kth_py_native_chain_transaction_list_count, METH_VARARGS, "..."},
    {"chain_transaction_list_nth",  kth_py_native_chain_transaction_list_nth, METH_VARARGS, "..."},

    {"chain_stealth_compact_ephemeral_public_key_hash",  kth_py_native_stealth_compact_get_ephemeral_public_key_hash, METH_VARARGS, "..."},
    {"chain_stealth_compact_get_transaction_hash",  kth_py_native_stealth_compact_get_transaction_hash, METH_VARARGS, "..."},
    {"chain_stealth_compact_get_public_key_hash",  kth_py_native_stealth_compact_get_public_key_hash, METH_VARARGS, "..."},
    {"chain_stealth_compact_list_destruct",  kth_py_native_chain_stealth_compact_list_destruct, METH_VARARGS, "..."},
    {"chain_stealth_compact_list_count",  kth_py_native_chain_stealth_compact_list_count, METH_VARARGS, "..."},
    {"chain_stealth_compact_list_nth",  kth_py_native_chain_stealth_compact_list_nth, METH_VARARGS, "..."},

    {"wallet_payment_address_destruct",  kth_py_native_wallet_payment_address_destruct, METH_VARARGS, "..."},
    {"wallet_payment_address_encoded",  kth_py_native_wallet_payment_address_encoded, METH_VARARGS, "..."},
    {"wallet_payment_address_version",  kth_py_native_wallet_payment_address_version, METH_VARARGS, "..."},
    {"wallet_payment_address_construct_from_string",  kth_py_native_wallet_payment_address_construct_from_string, METH_VARARGS, "..."},

    {"config_blockchain_settings_default",  kth_py_native_config_blockchain_settings_default, METH_VARARGS, "..."},
    {"config_database_settings_default",  kth_py_native_config_database_settings_default, METH_VARARGS, "..."},
    {"config_network_settings_default",  kth_py_native_config_network_settings_default, METH_VARARGS, "..."},
    {"config_node_settings_default",  kth_py_native_config_node_settings_default, METH_VARARGS, "..."},
    {"config_settings_default",  kth_py_native_config_settings_default, METH_VARARGS, "..."},
    {"config_settings_get_from_file",  kth_py_native_config_settings_get_from_file, METH_VARARGS, "..."},

    // {"word_list_construct",  kth_py_native_word_list_construct, METH_VARARGS, "..."},
    // {"word_list_destruct",  kth_py_native_word_list_destruct, METH_VARARGS, "..."},
    // {"word_list_add_word",  kth_py_native_word_list_add_word, METH_VARARGS, "..."},

    // {"wallet_mnemonics_to_seed",  kth_py_native_wallet_mnemonics_to_seed, METH_VARARGS, "..."},
    // {"wallet_ec_new",  kth_py_native_wallet_ec_new, METH_VARARGS, "..."},
    // {"wallet_ec_to_public",  kth_py_native_wallet_ec_to_public, METH_VARARGS, "..."},
    // {"wallet_ec_to_address",  kth_py_native_wallet_ec_to_address, METH_VARARGS, "..."},
    // {"wallet_hd_new",  kth_py_native_wallet_hd_new, METH_VARARGS, "..."},
    // {"wallet_hd_private_to_ec",  kth_py_native_wallet_hd_private_to_ec, METH_VARARGS, "..."},

    // {"binary_construct",  kth_py_native_binary_construct, METH_VARARGS, "..."},
    // {"binary_construct_string",  kth_py_native_binary_construct_string, METH_VARARGS, "..."},
    // {"binary_construct_blocks",  kth_py_native_binary_construct_blocks, METH_VARARGS, "..."},
    // {"binary_blocks",  kth_py_native_binary_blocks, METH_VARARGS, "..."},
    // {"binary_encoded",  kth_py_native_binary_encoded, METH_VARARGS, "..."},

    //{"long_hash_t_to_str",  kth_py_native_long_hash_t_to_str, METH_VARARGS, "..."},
    //{"long_hash_t_free",  kth_py_native_long_hash_t_free, METH_VARARGS, "..."},

    {NULL, NULL, 0, NULL}        /* Sentinel */
};

struct module_state {
    PyObject* error;
};

#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))

static
int myextension_traverse(PyObject* m, visitproc visit, void *arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}

static
int myextension_clear(PyObject* m) {
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}

// ---------------------------------------------------------------------

static PyTypeObject NodeSettingsType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "kth_native.NodeSettings",
    .tp_basicsize = sizeof(NodeSettings),
    .tp_itemsize = 0,
    // .tp_dealloc = (destructor) NodeSettings_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT, // | Py_TPFLAGS_BASETYPE,
    .tp_doc = "Node Settings",
    // .tp_init = (initproc) NodeSettings_init,
    .tp_members = NodeSettings_members,
    // .tp_methods = NodeSettings_methods,
    .tp_new = PyType_GenericNew,
    // .tp_new = NodeSettings_new,
};

PyObject* kth_py_native_config_node_settings_to_py(kth_node_settings const* setts) {
    PyObject* obj = PyObject_CallFunction((PyObject*)&NodeSettingsType, NULL);

    int res2 = KTH_PY_SETATTR(obj, setts, sync_peers, "i");
        res2 = KTH_PY_SETATTR(obj, setts, sync_timeout_seconds, "i");
        res2 = KTH_PY_SETATTR(obj, setts, block_latency_seconds, "i");
        res2 = KTH_PY_SETATTR(obj, setts, refresh_transactions, "i");
        res2 = KTH_PY_SETATTR(obj, setts, compact_blocks_high_bandwidth, "i");
        res2 = KTH_PY_SETATTR(obj, setts, ds_proofs_enabled, "i");

    return obj;
}

PyObject* kth_py_native_config_node_settings_default(PyObject* self, PyObject* args) {
    int py_network;
    if ( ! PyArg_ParseTuple(args, "K", &py_network)) {
        return NULL;
    }
    kth_network_t network = (kth_network_t)py_network;
    kth_node_settings res = kth_config_node_settings_default(network);
    return kth_py_native_config_node_settings_to_py(&res);
}


// ---------------------------------------------------------------------

static
void DatabaseSettings_dealloc(DatabaseSettings* self) {
    Py_XDECREF(self->directory);
    Py_TYPE(self)->tp_free((PyObject* ) self);
}

static
PyObject* DatabaseSettings_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    DatabaseSettings* self;
    self = (DatabaseSettings*) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->directory = PyUnicode_FromString("");
        if (self->directory == NULL) {
            Py_DECREF(self);
            return NULL;
        }
    }
    return (PyObject* ) self;
}

static PyTypeObject DatabaseSettingsType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "kth_native.DatabaseSettings",
    .tp_basicsize = sizeof(DatabaseSettings),
    .tp_itemsize = 0,
    .tp_dealloc = (destructor) DatabaseSettings_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = PyDoc_STR("Database Settings"),

    .tp_new = DatabaseSettings_new,
    // .tp_init = (initproc) DatabaseSettings_init,
    .tp_members = DatabaseSettings_members,
    // .tp_methods = DatabaseSettings_methods,
};

PyObject* kth_py_native_config_database_settings_to_py(kth_database_settings const* setts) {
    PyObject* obj = PyObject_CallFunction((PyObject*)&DatabaseSettingsType, NULL);

    int res2 = KTH_PY_SETATTR(obj, setts, directory, "s");
        res2 = KTH_PY_SETATTR(obj, setts, flush_writes, "i");
        res2 = KTH_PY_SETATTR(obj, setts, file_growth_rate, "I");
        res2 = KTH_PY_SETATTR(obj, setts, index_start_height, "I");
        res2 = KTH_PY_SETATTR(obj, setts, reorg_pool_limit, "I");
        res2 = KTH_PY_SETATTR(obj, setts, db_max_size, "K");
        res2 = KTH_PY_SETATTR(obj, setts, safe_mode, "i");
        res2 = KTH_PY_SETATTR(obj, setts, cache_capacity, "I");

    return obj;
}

PyObject* kth_py_native_config_database_settings_default(PyObject* self, PyObject* args) {
    int py_network;
    if ( ! PyArg_ParseTuple(args, "K", &py_network)) {
        return NULL;
    }

    kth_network_t network = (kth_network_t)py_network;
    kth_database_settings res = kth_config_database_settings_default(network);
    return kth_py_native_config_database_settings_to_py(&res);
}

// ---------------------------------------------------------------------

static
void Checkpoint_dealloc(Checkpoint* self) {
    Py_XDECREF(self->hash);
    Py_TYPE(self)->tp_free((PyObject* ) self);
}

static
PyObject* Checkpoint_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    Checkpoint* self;
    self = (Checkpoint*) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->hash = PyUnicode_FromString("");  //TODO
        if (self->hash == NULL) {
            Py_DECREF(self);
            return NULL;
        }
    }
    return (PyObject* ) self;
}

static PyTypeObject CheckpointType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "kth_native.Checkpoint",
    .tp_basicsize = sizeof(Checkpoint),
    .tp_itemsize = 0,
    .tp_dealloc = (destructor) Checkpoint_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = PyDoc_STR("Checkpoint"),

    .tp_new = Checkpoint_new,
    // .tp_init = (initproc) Checkpoint_init,
    .tp_members = Checkpoint_members,
    // .tp_methods = Checkpoint_methods,
};

// ---------------------------------------------------------------------

static
void Authority_dealloc(Authority* self) {
    Py_XDECREF(self->ip);
    Py_TYPE(self)->tp_free((PyObject* ) self);
}

static
PyObject* Authority_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    Authority* self;
    self = (Authority*) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->ip = PyUnicode_FromString("");  //TODO
        if (self->ip == NULL) {
            Py_DECREF(self);
            return NULL;
        }
    }
    return (PyObject* ) self;
}

static PyTypeObject AuthorityType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "kth_native.Authority",
    .tp_basicsize = sizeof(Authority),
    .tp_itemsize = 0,
    .tp_dealloc = (destructor) Authority_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = PyDoc_STR("Authority"),

    .tp_new = Authority_new,
    // .tp_init = (initproc) Authority_init,
    .tp_members = Authority_members,
    // .tp_methods = Authority_methods,
};

// ---------------------------------------------------------------------

static
void Endpoint_dealloc(Endpoint* self) {
    Py_XDECREF(self->scheme);
    Py_XDECREF(self->host);
    Py_TYPE(self)->tp_free((PyObject* ) self);
}

static
PyObject* Endpoint_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    Endpoint* self = (Endpoint*) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->scheme = PyUnicode_FromString("");  //TODO
        if (self->scheme == NULL) {
            Py_DECREF(self);
            return NULL;
        }

        self->host = PyUnicode_FromString("");  //TODO
        if (self->host == NULL) {
            Py_DECREF(self);
            return NULL;
        }
    }

    return (PyObject* ) self;
}

static PyTypeObject EndpointType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "kth_native.Endpoint",
    .tp_basicsize = sizeof(Endpoint),
    .tp_itemsize = 0,
    .tp_dealloc = (destructor) Endpoint_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = PyDoc_STR("Endpoint"),

    .tp_new = Endpoint_new,
    // .tp_init = (initproc) Endpoint_init,
    .tp_members = Endpoint_members,
    // .tp_methods = Endpoint_methods,
};

// ---------------------------------------------------------------------

static
void BlockchainSettings_dealloc(BlockchainSettings* self) {
    Py_XDECREF(self->checkpoints);
    Py_TYPE(self)->tp_free((PyObject* ) self);
}

static
PyObject* BlockchainSettings_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    BlockchainSettings* self = (BlockchainSettings*) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->checkpoints = PyList_New(0);
        if (self->checkpoints == NULL) {
            Py_DECREF(self);
            return NULL;
        }
    }
    return (PyObject* ) self;
}

static PyTypeObject BlockchainSettingsType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "kth_native.BlockchainSettings",
    .tp_basicsize = sizeof(BlockchainSettings),
    .tp_itemsize = 0,
    .tp_dealloc = (destructor) BlockchainSettings_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = PyDoc_STR("Blockchain Settings"),

    .tp_new = BlockchainSettings_new,
    // .tp_init = (initproc) BlockchainSettings_init,
    .tp_members = BlockchainSettings_members,
    // .tp_methods = BlockchainSettings_methods,
};

PyObject* config_checkpoint_to_py(kth_checkpoint const* checkpoint) {
    PyObject* obj = PyObject_CallFunction((PyObject*)&CheckpointType, NULL);

    int res2 = PyObject_SetAttrString(obj, "hash", Py_BuildValue("y#", checkpoint->hash.hash, 32));
        res2 = KTH_PY_SETATTR(obj, checkpoint, height, "i");
    return obj;
}

PyObject* config_checkpoints_to_py(kth_checkpoint* checkpoint, size_t n) {
    PyObject* pyArr = PyList_New(n);
    for (size_t i = 0; i < n; ++i) {
        PyObject* elem = config_checkpoint_to_py(checkpoint);
        PyList_SetItem(pyArr, i, elem);
        ++checkpoint;
    }
    return pyArr;
}

PyObject* kth_py_native_config_blockchain_settings_to_py(kth_blockchain_settings const* setts) {
    PyObject* obj = PyObject_CallFunction((PyObject*)&BlockchainSettingsType, NULL);

    int res2 = KTH_PY_SETATTR(obj, setts, cores, "i");
        res2 = KTH_PY_SETATTR(obj, setts, priority, "i");
        res2 = KTH_PY_SETATTR(obj, setts, byte_fee_satoshis, "f");
        res2 = KTH_PY_SETATTR(obj, setts, sigop_fee_satoshis, "f");
        res2 = KTH_PY_SETATTR(obj, setts, minimum_output_satoshis, "K");
        res2 = KTH_PY_SETATTR(obj, setts, notify_limit_hours, "i");
        res2 = KTH_PY_SETATTR(obj, setts, reorganization_limit, "i");
        res2 = PyObject_SetAttrString(obj, "checkpoints", config_checkpoints_to_py(setts->checkpoints, setts->checkpoint_count));
        res2 = KTH_PY_SETATTR(obj, setts, fix_checkpoints, "i");
        res2 = KTH_PY_SETATTR(obj, setts, allow_collisions, "i");
        res2 = KTH_PY_SETATTR(obj, setts, easy_blocks, "i");
        res2 = KTH_PY_SETATTR(obj, setts, retarget, "i");
        res2 = KTH_PY_SETATTR(obj, setts, bip16, "i");
        res2 = KTH_PY_SETATTR(obj, setts, bip30, "i");
        res2 = KTH_PY_SETATTR(obj, setts, bip34, "i");
        res2 = KTH_PY_SETATTR(obj, setts, bip66, "i");
        res2 = KTH_PY_SETATTR(obj, setts, bip65, "i");
        res2 = KTH_PY_SETATTR(obj, setts, bip90, "i");
        res2 = KTH_PY_SETATTR(obj, setts, bip68, "i");
        res2 = KTH_PY_SETATTR(obj, setts, bip112, "i");
        res2 = KTH_PY_SETATTR(obj, setts, bip113, "i");
        res2 = KTH_PY_SETATTR(obj, setts, bch_uahf, "i");
        res2 = KTH_PY_SETATTR(obj, setts, bch_daa_cw144, "i");
        res2 = KTH_PY_SETATTR(obj, setts, bch_pythagoras, "i");
        res2 = KTH_PY_SETATTR(obj, setts, bch_euclid, "i");
        res2 = KTH_PY_SETATTR(obj, setts, bch_pisano, "i");
        res2 = KTH_PY_SETATTR(obj, setts, bch_mersenne, "i");
        res2 = KTH_PY_SETATTR(obj, setts, bch_fermat, "i");
        res2 = KTH_PY_SETATTR(obj, setts, bch_euler, "i");
        res2 = KTH_PY_SETATTR(obj, setts, gauss_activation_time, "K");
        res2 = KTH_PY_SETATTR(obj, setts, descartes_activation_time, "K");
        res2 = KTH_PY_SETATTR(obj, setts, asert_half_life, "K");

    return obj;
}

PyObject* kth_py_native_config_blockchain_settings_default(PyObject* self, PyObject* args) {
    int py_network;
    if ( ! PyArg_ParseTuple(args, "K", &py_network)) {
        return NULL;
    }

    kth_network_t network = (kth_network_t)py_network;
    kth_blockchain_settings res = kth_config_blockchain_settings_default(network);
    return kth_py_native_config_blockchain_settings_to_py(&res);
}

// ---------------------------------------------------------------------

static
void NetworkSettings_dealloc(NetworkSettings* self) {
    Py_XDECREF(self->hosts_file);
    Py_XDECREF(self->self);
    Py_XDECREF(self->blacklist);
    Py_XDECREF(self->peers);
    Py_XDECREF(self->seeds);
    Py_XDECREF(self->debug_file);
    Py_XDECREF(self->error_file);
    Py_XDECREF(self->archive_directory);
    Py_XDECREF(self->statistics_server);
    Py_XDECREF(self->user_agent_blacklist);
    Py_TYPE(self)->tp_free((PyObject* ) self);
}

static
PyObject* NetworkSettings_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    NetworkSettings* self;
    self = (NetworkSettings*) type->tp_alloc(type, 0);
    if (self != NULL) {

        self->hosts_file = PyUnicode_FromString("");
        if (self->hosts_file == NULL) {
            Py_DECREF(self);
            return NULL;
        }

        self->self = Py_None;

        self->blacklist = PyList_New(0);
        if (self->blacklist == NULL) {
            Py_DECREF(self);
            return NULL;
        }

        self->peers = PyList_New(0);
        if (self->peers == NULL) {
            Py_DECREF(self);
            return NULL;
        }

        self->seeds = PyList_New(0);
        if (self->seeds == NULL) {
            Py_DECREF(self);
            return NULL;
        }

        self->debug_file = PyUnicode_FromString("");
        if (self->debug_file == NULL) {
            Py_DECREF(self);
            return NULL;
        }

        self->error_file = PyUnicode_FromString("");
        if (self->error_file == NULL) {
            Py_DECREF(self);
            return NULL;
        }

        self->archive_directory = PyUnicode_FromString("");
        if (self->archive_directory == NULL) {
            Py_DECREF(self);
            return NULL;
        }

        self->statistics_server = Py_None;

        self->user_agent_blacklist = PyList_New(0);
        if (self->user_agent_blacklist == NULL) {
            Py_DECREF(self);
            return NULL;
        }
    }
    return (PyObject* ) self;
}

static PyTypeObject NetworkSettingsType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "kth_native.NetworkSettings",
    .tp_basicsize = sizeof(NetworkSettings),
    .tp_itemsize = 0,
    .tp_dealloc = (destructor) NetworkSettings_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = PyDoc_STR("Network Settings"),

    .tp_new = NetworkSettings_new,
    // .tp_init = (initproc) NetworkSettings_init,
    .tp_members = NetworkSettings_members,
    // .tp_methods = NetworkSettings_methods,
};

PyObject* config_authority_to_py(kth_authority const* authority) {
    PyObject* obj = PyObject_CallFunction((PyObject*)&AuthorityType, NULL);

    int res2 = PyObject_SetAttrString(obj, "ip", Py_BuildValue("s", authority->ip));
        res2 = KTH_PY_SETATTR(obj, authority, port, "i");
    return obj;
}

PyObject* config_authorities_to_py(kth_authority* authorities, size_t n) {
    PyObject* pyArr = PyList_New(n);
    for (size_t i = 0; i < n; ++i) {
        PyObject* elem = config_authority_to_py(authorities);
        PyList_SetItem(pyArr, i, elem);
        ++authorities;
    }
    return pyArr;
}

PyObject* config_endpoint_to_py(kth_endpoint const* endpoint) {
    PyObject* obj = PyObject_CallFunction((PyObject*)&EndpointType, NULL);

    int res2 = PyObject_SetAttrString(obj, "scheme", Py_BuildValue("s", endpoint->scheme));
        res2 = PyObject_SetAttrString(obj, "host", Py_BuildValue("s", endpoint->host));
        res2 = KTH_PY_SETATTR(obj, endpoint, port, "i");

    return obj;
}

PyObject* config_endpoints_to_py(kth_endpoint* endpoints, size_t n) {
    PyObject* pyArr = PyList_New(n);
    for (size_t i = 0; i < n; ++i) {
        PyObject* elem = config_endpoint_to_py(endpoints);
        PyList_SetItem(pyArr, i, elem);
        ++endpoints;
    }
    return pyArr;
}

PyObject* config_strings_to_py(char** strs, size_t n) {
    PyObject* pyArr = PyList_New(n);
    for (size_t i = 0; i < n; ++i) {
        PyObject* elem = Py_BuildValue("s", *strs);
        PyList_SetItem(pyArr, i, elem);
        ++strs;
    }
    return pyArr;
}

PyObject* kth_py_native_config_network_settings_to_py(kth_network_settings const* setts) {
    PyObject* obj = PyObject_CallFunction((PyObject*)&NetworkSettingsType, NULL);

    int res2 = KTH_PY_SETATTR(obj, setts, threads, "i");
        res2 = KTH_PY_SETATTR(obj, setts, protocol_maximum, "i");
        res2 = KTH_PY_SETATTR(obj, setts, protocol_minimum, "i");
        res2 = KTH_PY_SETATTR(obj, setts, services, "K");
        res2 = KTH_PY_SETATTR(obj, setts, invalid_services, "K");
        res2 = KTH_PY_SETATTR(obj, setts, relay_transactions, "i");
        res2 = KTH_PY_SETATTR(obj, setts, validate_checksum, "i");
        res2 = KTH_PY_SETATTR(obj, setts, identifier, "I");
        res2 = KTH_PY_SETATTR(obj, setts, inbound_port, "i");
        res2 = KTH_PY_SETATTR(obj, setts, inbound_connections, "i");
        res2 = KTH_PY_SETATTR(obj, setts, outbound_connections, "i");
        res2 = KTH_PY_SETATTR(obj, setts, manual_attempt_limit, "i");
        res2 = KTH_PY_SETATTR(obj, setts, connect_batch_size, "i");
        res2 = KTH_PY_SETATTR(obj, setts, connect_timeout_seconds, "i");
        res2 = KTH_PY_SETATTR(obj, setts, channel_handshake_seconds, "i");
        res2 = KTH_PY_SETATTR(obj, setts, channel_heartbeat_minutes, "i");
        res2 = KTH_PY_SETATTR(obj, setts, channel_inactivity_minutes, "i");
        res2 = KTH_PY_SETATTR(obj, setts, channel_expiration_minutes, "i");
        res2 = KTH_PY_SETATTR(obj, setts, channel_germination_seconds, "i");
        res2 = KTH_PY_SETATTR(obj, setts, host_pool_capacity, "i");
        res2 = KTH_PY_SETATTR(obj, setts, hosts_file, "s");
        res2 = PyObject_SetAttrString(obj, "self", config_authority_to_py(&setts->self));
        res2 = PyObject_SetAttrString(obj, "blacklist", config_authorities_to_py(setts->blacklist, setts->blacklist_count));
        res2 = PyObject_SetAttrString(obj, "peers", config_endpoints_to_py(setts->peers, setts->peer_count));
        res2 = PyObject_SetAttrString(obj, "seeds", config_endpoints_to_py(setts->seeds, setts->seed_count));
        res2 = KTH_PY_SETATTR(obj, setts, debug_file, "s");
        res2 = KTH_PY_SETATTR(obj, setts, error_file, "s");
        res2 = KTH_PY_SETATTR(obj, setts, archive_directory, "s");
        res2 = KTH_PY_SETATTR(obj, setts, rotation_size, "K");
        res2 = KTH_PY_SETATTR(obj, setts, minimum_free_space, "K");
        res2 = KTH_PY_SETATTR(obj, setts, maximum_archive_size, "K");
        res2 = KTH_PY_SETATTR(obj, setts, maximum_archive_files, "K");
        res2 = PyObject_SetAttrString(obj, "statistics_server", config_authority_to_py(&setts->statistics_server));
        res2 = KTH_PY_SETATTR(obj, setts, verbose, "i");
        res2 = KTH_PY_SETATTR(obj, setts, use_ipv6, "i");
        res2 = PyObject_SetAttrString(obj, "user_agent_blacklist", config_strings_to_py(setts->user_agent_blacklist, setts->user_agent_blacklist_count));

    return obj;
}

PyObject* kth_py_native_config_network_settings_default(PyObject* self, PyObject* args) {
    int py_network;
    if ( ! PyArg_ParseTuple(args, "K", &py_network)) {
        return NULL;
    }

    kth_network_t network = (kth_network_t)py_network;
    kth_network_settings res = kth_config_network_settings_default(network);
    return kth_py_native_config_network_settings_to_py(&res);
}

// ---------------------------------------------------------------------

static
void Settings_dealloc(Settings* self) {
    Py_XDECREF(self->node);
    Py_XDECREF(self->chain);
    Py_XDECREF(self->database);
    Py_XDECREF(self->network);
    Py_TYPE(self)->tp_free((PyObject* ) self);
}

static
PyObject* Settings_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    Settings* self;
    self = (Settings*) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->node = Py_None;
        self->chain = Py_None;
        self->database = Py_None;
        self->network = Py_None;
    }
    return (PyObject* ) self;
}

static PyTypeObject SettingsType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "kth_native.Settings",
    .tp_basicsize = sizeof(Settings),
    .tp_itemsize = 0,
    .tp_dealloc = (destructor) Settings_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = PyDoc_STR("Settings"),

    .tp_new = Settings_new,
    // .tp_init = (initproc) Settings_init,
    .tp_members = Settings_members,
    // .tp_methods = Settings_methods,
};

PyObject* kth_py_native_config_settings_to_py(kth_settings const* setts) {
    PyObject* obj = PyObject_CallFunction((PyObject*)&SettingsType, NULL);
    int res2 = PyObject_SetAttrString(obj, "node", kth_py_native_config_node_settings_to_py(&setts->node));
        res2 = PyObject_SetAttrString(obj, "chain", kth_py_native_config_blockchain_settings_to_py(&setts->chain));
        res2 = PyObject_SetAttrString(obj, "database", kth_py_native_config_database_settings_to_py(&setts->database));
        res2 = PyObject_SetAttrString(obj, "network", kth_py_native_config_network_settings_to_py(&setts->network));
    return obj;
}

PyObject* kth_py_native_config_settings_default(PyObject* self, PyObject* args) {
    int py_network;
    if ( ! PyArg_ParseTuple(args, "K", &py_network)) {
        return NULL;
    }

    kth_network_t network = (kth_network_t)py_network;
    kth_settings res = kth_config_settings_default(network);
    return kth_py_native_config_settings_to_py(&res);
}

PyObject* kth_py_native_config_settings_get_from_file(PyObject* self, PyObject* args) {

    char const* path;
    if ( ! PyArg_ParseTuple(args, "s", &path)) {
        return NULL;
    }

    kth_settings* settings;
    char* error_message;
    kth_bool_t res = kth_config_settings_get_from_file(path, &settings, &error_message);

    if (res == 0) {
        // return PyTuple_Pack(3, false, Py_None, Py_BuildValue("s", error_message));
        return Py_BuildValue("(iOO)", 0, Py_None, Py_BuildValue("s", error_message));
    }

    PyObject* setts = kth_py_native_config_settings_to_py(settings);
    PyObject* tuple = Py_BuildValue("(iOO)", 1, setts, Py_None);
    kth_config_settings_destruct(settings);
    return tuple;
}


// ---------------------------------------------------------------------

static
struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "kth_native",
        NULL,
        sizeof(struct module_state),
        KnuthNativeMethods,
        NULL,
        myextension_traverse,
        myextension_clear,
        NULL
};

#define INITERROR return NULL

PyMODINIT_FUNC
PyInit_kth_native(void) {

    // Make sure the GIL has been created since we need to acquire it in our
    // callback to safely call into the python application.
    // if (! PyEval_ThreadsInitialized()) {
    //     printf("PyEval_InitThreads() ----------------------\n");
    //     PyEval_InitThreads();
    // }
    Py_Initialize();

    if (PyType_Ready(&NodeSettingsType) < 0) {
        return NULL;
    }

    if (PyType_Ready(&DatabaseSettingsType) < 0) {
        return NULL;
    }

    if (PyType_Ready(&BlockchainSettingsType) < 0) {
        return NULL;
    }

    if (PyType_Ready(&NetworkSettingsType) < 0) {
        return NULL;
    }

    if (PyType_Ready(&CheckpointType) < 0) {
        return NULL;
    }

    if (PyType_Ready(&AuthorityType) < 0) {
        return NULL;
    }

    if (PyType_Ready(&EndpointType) < 0) {
        return NULL;
    }

    if (PyType_Ready(&SettingsType) < 0) {
        return NULL;
    }

    PyObject* module = PyModule_Create(&moduledef);
    if (module == NULL) {
        INITERROR;
    }

    Py_INCREF(&NodeSettingsType);
    if (PyModule_AddObject(module, "NodeSettings", (PyObject*) &NodeSettingsType) < 0) {
        Py_DECREF(&NodeSettingsType);
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&DatabaseSettingsType);
    if (PyModule_AddObject(module, "DatabaseSettings", (PyObject*) &DatabaseSettingsType) < 0) {
        Py_DECREF(&DatabaseSettingsType);
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&BlockchainSettingsType);
    if (PyModule_AddObject(module, "BlockchainSettings", (PyObject*) &BlockchainSettingsType) < 0) {
        Py_DECREF(&BlockchainSettingsType);
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&NetworkSettingsType);
    if (PyModule_AddObject(module, "NetworkSetting", (PyObject*) &NetworkSettingsType) < 0) {
        Py_DECREF(&NetworkSettingsType);
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&CheckpointType);
    if (PyModule_AddObject(module, "Checkpoint", (PyObject*) &CheckpointType) < 0) {
        Py_DECREF(&CheckpointType);
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&AuthorityType);
    if (PyModule_AddObject(module, "Authority", (PyObject*) &AuthorityType) < 0) {
        Py_DECREF(&AuthorityType);
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&EndpointType);
    if (PyModule_AddObject(module, "Endpoint", (PyObject*) &EndpointType) < 0) {
        Py_DECREF(&EndpointType);
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&SettingsType);
    if (PyModule_AddObject(module, "Setting", (PyObject*) &SettingsType) < 0) {
        Py_DECREF(&SettingsType);
        Py_DECREF(module);
        return NULL;
    }


    struct module_state *st = GETSTATE(module);
    st->error = PyErr_NewException((char*)"myextension.Error", NULL, NULL);

    if (st->error == NULL) {
        Py_DECREF(module);
        INITERROR;
    }

    return module;
}

#ifdef __cplusplus
} // extern "C"
#endif
