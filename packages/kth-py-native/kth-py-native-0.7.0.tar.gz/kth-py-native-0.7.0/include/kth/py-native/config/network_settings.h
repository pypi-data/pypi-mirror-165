#ifndef KTH_PY_NATIVE_CONFIG_NETWORK_SETTINGS_H_
#define KTH_PY_NATIVE_CONFIG_NETWORK_SETTINGS_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

#include <kth/py-native/config/authority.h>
#include <kth/py-native/config/common.h>
#include <kth/py-native/config/endpoint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    PyObject_HEAD

    uint32_t threads;
    uint32_t protocol_maximum;
    uint32_t protocol_minimum;
    uint64_t services;
    uint64_t invalid_services;
    kth_bool_t relay_transactions;
    kth_bool_t validate_checksum;
    uint32_t identifier;
    uint16_t inbound_port;
    uint32_t inbound_connections;
    uint32_t outbound_connections;
    uint32_t manual_attempt_limit;
    uint32_t connect_batch_size;
    uint32_t connect_timeout_seconds;
    uint32_t channel_handshake_seconds;
    uint32_t channel_heartbeat_minutes;
    uint32_t channel_inactivity_minutes;
    uint32_t channel_expiration_minutes;
    uint32_t channel_germination_seconds;
    uint32_t host_pool_capacity;
    PyObject* hosts_file;               // kth_char_t*
    PyObject* self;                     // kth_authority

    // size_t blacklist_count;
    PyObject* blacklist;                // kth_authority*
    // size_t peer_count;
    PyObject* peers;                    // kth_endpoint*
    // size_t seed_count;
    PyObject* seeds;                    // kth_endpoint*

    PyObject* debug_file;               // kth_char_t*
    PyObject* error_file;               // kth_char_t*
    PyObject* archive_directory;        // kth_char_t*
    size_t rotation_size;
    size_t minimum_free_space;
    size_t maximum_archive_size;
    size_t maximum_archive_files;
    PyObject* statistics_server;        // kth_authority

    kth_bool_t verbose;
    kth_bool_t use_ipv6;

    // size_t user_agent_blacklist_count;
    PyObject* user_agent_blacklist;     // char**
} NetworkSettings;

static PyMemberDef NetworkSettings_members[] = {

    {"threads", T_INT, offsetof(NetworkSettings, threads), 0, "threads"},
    {"protocol_maximum", T_INT, offsetof(NetworkSettings, protocol_maximum), 0, "protocol_maximum"},
    {"protocol_minimum", T_INT, offsetof(NetworkSettings, protocol_minimum), 0, "protocol_minimum"},
    {"services", T_ULONGLONG, offsetof(NetworkSettings, services), 0, "services"},
    {"invalid_services", T_ULONGLONG, offsetof(NetworkSettings, invalid_services), 0, "invalid_services"},
    {"relay_transactions", T_INT, offsetof(NetworkSettings, relay_transactions), 0, "relay_transactions"},
    {"validate_checksum", T_INT, offsetof(NetworkSettings, validate_checksum), 0, "validate_checksum"},
    {"identifier", T_UINT, offsetof(NetworkSettings, identifier), 0, "identifier"},
    {"inbound_port", T_INT, offsetof(NetworkSettings, inbound_port), 0, "inbound_port"},
    {"inbound_connections", T_INT, offsetof(NetworkSettings, inbound_connections), 0, "inbound_connections"},
    {"outbound_connections", T_INT, offsetof(NetworkSettings, outbound_connections), 0, "outbound_connections"},
    {"manual_attempt_limit", T_INT, offsetof(NetworkSettings, manual_attempt_limit), 0, "manual_attempt_limit"},
    {"connect_batch_size", T_INT, offsetof(NetworkSettings, connect_batch_size), 0, "connect_batch_size"},
    {"connect_timeout_seconds", T_INT, offsetof(NetworkSettings, connect_timeout_seconds), 0, "connect_timeout_seconds"},
    {"channel_handshake_seconds", T_INT, offsetof(NetworkSettings, channel_handshake_seconds), 0, "channel_handshake_seconds"},
    {"channel_heartbeat_minutes", T_INT, offsetof(NetworkSettings, channel_heartbeat_minutes), 0, "channel_heartbeat_minutes"},
    {"channel_inactivity_minutes", T_INT, offsetof(NetworkSettings, channel_inactivity_minutes), 0, "channel_inactivity_minutes"},
    {"channel_expiration_minutes", T_INT, offsetof(NetworkSettings, channel_expiration_minutes), 0, "channel_expiration_minutes"},
    {"channel_germination_seconds", T_INT, offsetof(NetworkSettings, channel_germination_seconds), 0, "channel_germination_seconds"},
    {"host_pool_capacity", T_INT, offsetof(NetworkSettings, host_pool_capacity), 0, "host_pool_capacity"},
    {"hosts_file", T_OBJECT_EX, offsetof(NetworkSettings, hosts_file), 0, "hosts_file"},
    {"self", T_OBJECT_EX, offsetof(NetworkSettings, self), 0, "self"},
    // {"blacklist_count", T_INT, offsetof(NetworkSettings, blacklist_count), 0, "blacklist_count"},
    {"blacklist", T_OBJECT_EX, offsetof(NetworkSettings, blacklist), 0, "blacklist"},
    // {"peer_count", T_INT, offsetof(NetworkSettings, peer_count), 0, "peer_count"},
    {"peers", T_OBJECT_EX, offsetof(NetworkSettings, peers), 0, "peers"},
    // {"seed_count", T_INT, offsetof(NetworkSettings, seed_count), 0, "seed_count"},
    {"seeds", T_OBJECT_EX, offsetof(NetworkSettings, seeds), 0, "seeds"},
    {"debug_file", T_OBJECT_EX, offsetof(NetworkSettings, debug_file), 0, "debug_file"},
    {"error_file", T_OBJECT_EX, offsetof(NetworkSettings, error_file), 0, "error_file"},
    {"archive_directory", T_OBJECT_EX, offsetof(NetworkSettings, archive_directory), 0, "archive_directory"},
    {"rotation_size", T_ULONGLONG, offsetof(NetworkSettings, rotation_size), 0, "rotation_size"},
    {"minimum_free_space", T_ULONGLONG, offsetof(NetworkSettings, minimum_free_space), 0, "minimum_free_space"},
    {"maximum_archive_size", T_ULONGLONG, offsetof(NetworkSettings, maximum_archive_size), 0, "maximum_archive_size"},
    {"maximum_archive_files", T_ULONGLONG, offsetof(NetworkSettings, maximum_archive_files), 0, "maximum_archive_files"},
    {"statistics_server", T_OBJECT_EX, offsetof(NetworkSettings, statistics_server), 0, "statistics_server"},
    {"verbose", T_INT, offsetof(NetworkSettings, verbose), 0, "verbose"},
    {"use_ipv6", T_INT, offsetof(NetworkSettings, use_ipv6), 0, "use_ipv6"},
    // {"user_agent_blacklist_count", T_INT, offsetof(NetworkSettings, user_agent_blacklist_count), 0, "user_agent_blacklist_count"},
    {"user_agent_blacklist", T_OBJECT_EX, offsetof(NetworkSettings, user_agent_blacklist), 0, "user_agent_blacklist"},

    {NULL}  /* Sentinel */
};

PyObject* kth_py_native_config_network_settings_default(PyObject* self, PyObject* args);


inline
kth_network_settings kth_py_native_config_network_settings_to_c(PyObject* setts) {
    kth_network_settings res;

    KTH_PY_GETATTR(res, setts, threads, "i");
    KTH_PY_GETATTR(res, setts, protocol_maximum, "i");
    KTH_PY_GETATTR(res, setts, protocol_minimum, "i");
    KTH_PY_GETATTR(res, setts, services, "K");
    KTH_PY_GETATTR(res, setts, invalid_services, "K");
    KTH_PY_GETATTR(res, setts, relay_transactions, "i");
    KTH_PY_GETATTR(res, setts, validate_checksum, "i");
    KTH_PY_GETATTR(res, setts, identifier, "I");
    KTH_PY_GETATTR(res, setts, inbound_port, "i");
    KTH_PY_GETATTR(res, setts, inbound_connections, "i");
    KTH_PY_GETATTR(res, setts, outbound_connections, "i");
    KTH_PY_GETATTR(res, setts, manual_attempt_limit, "i");
    KTH_PY_GETATTR(res, setts, connect_batch_size, "i");
    KTH_PY_GETATTR(res, setts, connect_timeout_seconds, "i");
    KTH_PY_GETATTR(res, setts, channel_handshake_seconds, "i");
    KTH_PY_GETATTR(res, setts, channel_heartbeat_minutes, "i");
    KTH_PY_GETATTR(res, setts, channel_inactivity_minutes, "i");
    KTH_PY_GETATTR(res, setts, channel_expiration_minutes, "i");
    KTH_PY_GETATTR(res, setts, channel_germination_seconds, "i");
    KTH_PY_GETATTR(res, setts, host_pool_capacity, "i");
    KTH_PY_GETATTR(res, setts, hosts_file, "s");

    // res2 = PyObject_SetAttrString(obj, "self", config_authority_to_py(setts.self));
    res.self = config_authority_to_c(PyObject_GetAttrString(setts, "self"));

    // res2 = PyObject_SetAttrString(obj, "blacklist", config_authorities_to_py(setts.blacklist, setts.blacklist_count));
    res.blacklist = config_authorities_to_c(PyObject_GetAttrString(setts, "blacklist"), &res.blacklist_count);

    // res2 = PyObject_SetAttrString(obj, "peers", config_endpoints_to_py(setts.peers, setts.peer_count));
    res.peers = config_endpoints_to_c(PyObject_GetAttrString(setts, "peers"), &res.peer_count);

    // res2 = PyObject_SetAttrString(obj, "seeds", config_endpoints_to_py(setts.seeds, setts.seed_count));
    res.seeds = config_endpoints_to_c(PyObject_GetAttrString(setts, "seeds"), &res.seed_count);

    KTH_PY_GETATTR(res, setts, debug_file, "s");
    KTH_PY_GETATTR(res, setts, error_file, "s");
    KTH_PY_GETATTR(res, setts, archive_directory, "s");
    KTH_PY_GETATTR(res, setts, rotation_size, "K");
    KTH_PY_GETATTR(res, setts, minimum_free_space, "K");
    KTH_PY_GETATTR(res, setts, maximum_archive_size, "K");
    KTH_PY_GETATTR(res, setts, maximum_archive_files, "K");

    // res2 = PyObject_SetAttrString(obj, "statistics_server", config_authority_to_py(setts.statistics_server));
    res.statistics_server = config_authority_to_c(PyObject_GetAttrString(setts, "statistics_server"));

    KTH_PY_GETATTR(res, setts, verbose, "i");
    KTH_PY_GETATTR(res, setts, use_ipv6, "i");

    // res2 = PyObject_SetAttrString(obj, "user_agent_blacklist", config_strings_to_py(setts.user_agent_blacklist, setts.user_agent_blacklist_count));
    res.user_agent_blacklist = config_strings_to_c(PyObject_GetAttrString(setts, "user_agent_blacklist"), &res.user_agent_blacklist_count);

    return res;
}

#ifdef __cplusplus
} //extern "C"
#endif

#endif // KTH_PY_NATIVE_CONFIG_NETWORK_SETTINGS_H_
