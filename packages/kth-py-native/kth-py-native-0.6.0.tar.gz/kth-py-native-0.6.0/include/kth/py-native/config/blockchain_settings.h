#ifndef KTH_PY_NATIVE_CONFIG_BLOCKCHAIN_SETTINGS_H_
#define KTH_PY_NATIVE_CONFIG_BLOCKCHAIN_SETTINGS_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

#include <kth/py-native/config/common.h>
#include <kth/py-native/config/checkpoint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    PyObject_HEAD

    uint32_t cores;
    kth_bool_t priority;
    float byte_fee_satoshis;
    float sigop_fee_satoshis;
    uint64_t minimum_output_satoshis;
    uint32_t notify_limit_hours;
    uint32_t reorganization_limit;
    // kth_size_t checkpoint_count;
    PyObject* checkpoints;          //kth_checkpoint*
    kth_bool_t fix_checkpoints;
    kth_bool_t allow_collisions;
    kth_bool_t easy_blocks;
    kth_bool_t retarget;
    kth_bool_t bip16;
    kth_bool_t bip30;
    kth_bool_t bip34;
    kth_bool_t bip66;
    kth_bool_t bip65;
    kth_bool_t bip90;
    kth_bool_t bip68;
    kth_bool_t bip112;
    kth_bool_t bip113;
    kth_bool_t bch_uahf;
    kth_bool_t bch_daa_cw144;
    kth_bool_t bch_pythagoras;
    kth_bool_t bch_euclid;
    kth_bool_t bch_pisano;
    kth_bool_t bch_mersenne;
    kth_bool_t bch_fermat;
    kth_bool_t bch_euler;
    uint64_t gauss_activation_time;
    uint64_t descartes_activation_time;
    uint64_t asert_half_life;
} BlockchainSettings;

static PyMemberDef BlockchainSettings_members[] = {
    {"cores", T_INT, offsetof(BlockchainSettings, cores), 0, "cores"},
    {"priority", T_INT, offsetof(BlockchainSettings, priority), 0, "priority"},
    {"byte_fee_satoshis", T_FLOAT, offsetof(BlockchainSettings, byte_fee_satoshis), 0, "byte_fee_satoshis"},
    {"sigop_fee_satoshis", T_FLOAT, offsetof(BlockchainSettings, sigop_fee_satoshis), 0, "sigop_fee_satoshis"},
    {"minimum_output_satoshis", T_ULONGLONG, offsetof(BlockchainSettings, minimum_output_satoshis), 0, "minimum_output_satoshis"},
    {"notify_limit_hours", T_INT, offsetof(BlockchainSettings, notify_limit_hours), 0, "notify_limit_hours"},
    {"reorganization_limit", T_INT, offsetof(BlockchainSettings, reorganization_limit), 0, "reorganization_limit"},
    // {"checkpoint_count", T_ULONGLONG, offsetof(BlockchainSettings, checkpoint_count), 0, "checkpoint_count"},
    {"checkpoints", T_OBJECT_EX, offsetof(BlockchainSettings, checkpoints), 0, "checkpoints"},
    {"fix_checkpoints", T_INT, offsetof(BlockchainSettings, fix_checkpoints), 0, "fix_checkpoints"},
    {"allow_collisions", T_INT, offsetof(BlockchainSettings, allow_collisions), 0, "allow_collisions"},
    {"easy_blocks", T_INT, offsetof(BlockchainSettings, easy_blocks), 0, "easy_blocks"},
    {"retarget", T_INT, offsetof(BlockchainSettings, retarget), 0, "retarget"},
    {"bip16", T_INT, offsetof(BlockchainSettings, bip16), 0, "bip16"},
    {"bip30", T_INT, offsetof(BlockchainSettings, bip30), 0, "bip30"},
    {"bip34", T_INT, offsetof(BlockchainSettings, bip34), 0, "bip34"},
    {"bip66", T_INT, offsetof(BlockchainSettings, bip66), 0, "bip66"},
    {"bip65", T_INT, offsetof(BlockchainSettings, bip65), 0, "bip65"},
    {"bip90", T_INT, offsetof(BlockchainSettings, bip90), 0, "bip90"},
    {"bip68", T_INT, offsetof(BlockchainSettings, bip68), 0, "bip68"},
    {"bip112", T_INT, offsetof(BlockchainSettings, bip112), 0, "bip112"},
    {"bip113", T_INT, offsetof(BlockchainSettings, bip113), 0, "bip113"},
    {"bch_uahf", T_INT, offsetof(BlockchainSettings, bch_uahf), 0, "bch_uahf"},
    {"bch_daa_cw144", T_INT, offsetof(BlockchainSettings, bch_daa_cw144), 0, "bch_daa_cw144"},
    {"bch_pythagoras", T_INT, offsetof(BlockchainSettings, bch_pythagoras), 0, "bch_pythagoras"},
    {"bch_euclid", T_INT, offsetof(BlockchainSettings, bch_euclid), 0, "bch_euclid"},
    {"bch_pisano", T_INT, offsetof(BlockchainSettings, bch_pisano), 0, "bch_pisano"},
    {"bch_mersenne", T_INT, offsetof(BlockchainSettings, bch_mersenne), 0, "bch_mersenne"},
    {"bch_fermat", T_INT, offsetof(BlockchainSettings, bch_fermat), 0, "bch_fermat"},
    {"bch_euler", T_INT, offsetof(BlockchainSettings, bch_euler), 0, "bch_euler"},
    {"gauss_activation_time", T_ULONGLONG, offsetof(BlockchainSettings, gauss_activation_time), 0, "gauss_activation_time"},
    {"descartes_activation_time", T_ULONGLONG, offsetof(BlockchainSettings, descartes_activation_time), 0, "descartes_activation_time"},
    {"asert_half_life", T_ULONGLONG, offsetof(BlockchainSettings, asert_half_life), 0, "asert_half_life"},

    {NULL}  /* Sentinel */
};

PyObject* kth_py_native_config_blockchain_settings_default(PyObject* self, PyObject* args);

inline
kth_blockchain_settings kth_py_native_config_blockchain_settings_to_c(PyObject* setts) {

    kth_blockchain_settings res;

    KTH_PY_GETATTR(res, setts, cores, "i");
    KTH_PY_GETATTR(res, setts, priority, "i");
    KTH_PY_GETATTR(res, setts, byte_fee_satoshis, "f");
    KTH_PY_GETATTR(res, setts, sigop_fee_satoshis, "f");
    KTH_PY_GETATTR(res, setts, minimum_output_satoshis, "K");
    KTH_PY_GETATTR(res, setts, notify_limit_hours, "i");
    KTH_PY_GETATTR(res, setts, reorganization_limit, "i");

    res.checkpoints = config_checkpoints_to_c(PyObject_GetAttrString(setts, "checkpoints"), &res.checkpoint_count);

    KTH_PY_GETATTR(res, setts, fix_checkpoints, "i");
    KTH_PY_GETATTR(res, setts, allow_collisions, "i");
    KTH_PY_GETATTR(res, setts, easy_blocks, "i");
    KTH_PY_GETATTR(res, setts, retarget, "i");
    KTH_PY_GETATTR(res, setts, bip16, "i");
    KTH_PY_GETATTR(res, setts, bip30, "i");
    KTH_PY_GETATTR(res, setts, bip34, "i");
    KTH_PY_GETATTR(res, setts, bip66, "i");
    KTH_PY_GETATTR(res, setts, bip65, "i");
    KTH_PY_GETATTR(res, setts, bip90, "i");
    KTH_PY_GETATTR(res, setts, bip68, "i");
    KTH_PY_GETATTR(res, setts, bip112, "i");
    KTH_PY_GETATTR(res, setts, bip113, "i");
    KTH_PY_GETATTR(res, setts, bch_uahf, "i");
    KTH_PY_GETATTR(res, setts, bch_daa_cw144, "i");
    KTH_PY_GETATTR(res, setts, bch_pythagoras, "i");
    KTH_PY_GETATTR(res, setts, bch_euclid, "i");
    KTH_PY_GETATTR(res, setts, bch_pisano, "i");
    KTH_PY_GETATTR(res, setts, bch_mersenne, "i");
    KTH_PY_GETATTR(res, setts, bch_fermat, "i");
    KTH_PY_GETATTR(res, setts, bch_euler, "i");
    KTH_PY_GETATTR(res, setts, gauss_activation_time, "K");
    KTH_PY_GETATTR(res, setts, descartes_activation_time, "K");
    KTH_PY_GETATTR(res, setts, asert_half_life, "K");

    return res;
}

#ifdef __cplusplus
} //extern "C"
#endif

#endif // KTH_PY_NATIVE_CONFIG_BLOCKCHAIN_SETTINGS_H_
