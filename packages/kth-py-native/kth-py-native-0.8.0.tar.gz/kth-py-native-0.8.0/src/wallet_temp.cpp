// -------------------------------------------------------------------

// long_hash_t wallet_mnemonics_to_seed(word_list_t mnemonics){
//     auto hash_cpp = libbitcoin::wallet::decode_mnemonic(*static_cast<const std::vector<std::string>*>(mnemonics));
//     return hash_cpp.data();
// }

// PyObject* kth_py_native_wallet_mnemonics_to_seed(PyObject* self, PyObject* args) {
//     PyObject* py_wl;

//     if ( ! PyArg_ParseTuple(args, "O", &py_wl)) {
//         return NULL;
//     }

//     word_list_t wl = (word_list_t)get_ptr(py_wl);

//     long_hash_t res = wallet_mnemonics_to_seed(wl);

// #if PY_MAJOR_VERSION >= 3
//     return Py_BuildValue("y#", res.hash, 64);    //TODO: warning, hardcoded hash size!
// #else
//     return Py_BuildValue("s#", res.hash, 64);    //TODO: warning, hardcoded hash size!
// #endif
// }

// PyObject* kth_py_native_wallet_ec_new(PyObject* self, PyObject* args) {
//     uint8_t* py_seed;
//     int py_n;

// #if PY_MAJOR_VERSION >= 3
//     if ( ! PyArg_ParseTuple(args, "y#", &py_seed, &py_n)) {
// #else
//     if ( ! PyArg_ParseTuple(args, "s#", &py_seed, &py_n)) {
// #endif
//         return NULL;
//     }

//     ec_secret_t res = wallet_ec_new(py_seed, py_n);
//     // return to_py_obj(res);

// #if PY_MAJOR_VERSION >= 3
//     return Py_BuildValue("y#", res.data, 32);    //TODO: warning, hardcoded hash size!
// #else
//     return Py_BuildValue("s#", res.data, 32);    //TODO: warning, hardcoded hash size!
// #endif

// }

// PyObject* kth_py_native_wallet_ec_to_public(PyObject* self, PyObject* args) {
//     PyObject* py_secret;
//     int py_size;
//     int py_uncompressed;

// #if PY_MAJOR_VERSION >= 3
//     if ( ! PyArg_ParseTuple(args, "y#i", &py_secret, &py_size, &py_uncompressed)) {
// #else
//     if ( ! PyArg_ParseTuple(args, "s#i", &py_secret, &py_size, &py_uncompressed)) {
// #endif
//         return NULL;
//     }

//     ec_secret_t secret;
//     memcpy(secret.data, py_secret, 32);

//     ec_public_t res = wallet_ec_to_public(secret, py_uncompressed);
//     return to_py_obj(res);
// }

// PyObject* kth_py_native_wallet_ec_to_address(PyObject* self, PyObject* args) {
//     PyObject* py_point;
//     uint32_t py_version;

//     if ( ! PyArg_ParseTuple(args, "OI", &py_point, &py_version)) {
//         return NULL;
//     }

//     ec_public_t point = (ec_public_t)get_ptr(py_point);
//     kth_payment_address_t res = wallet_ec_to_address(point, py_version);
//     return to_py_obj(res);
// }

// PyObject* kth_py_native_wallet_hd_new(PyObject* self, PyObject* args) {
//     // uint8_t* py_seed;
//     char* py_seed;
//     int py_n;
//     uint32_t py_version;

// #if PY_MAJOR_VERSION >= 3
//     if ( ! PyArg_ParseTuple(args, "y#I", &py_seed, &py_n, &py_version)) {
// #else
//     if ( ! PyArg_ParseTuple(args, "s#I", &py_seed, &py_n, &py_version)) {
// #endif
//         return NULL;
//     }

//     hd_private_t res = wallet_hd_new((uint8_t*)py_seed, py_n, py_version);
//     return to_py_obj(res);
// }

// PyObject* kth_py_native_wallet_hd_private_to_ec(PyObject* self, PyObject* args) {
//     PyObject* py_key;

//     if ( ! PyArg_ParseTuple(args, "O", &py_key)) {
//         return NULL;
//     }

//     hd_private_t key = (hd_private_t)get_ptr(py_key);

//     ec_secret_t res = wallet_hd_private_to_ec(key);

// #if PY_MAJOR_VERSION >= 3
//     return Py_BuildValue("y#", res.data, 32);    //TODO: warning, hardcoded hash size!
// #else
//     return Py_BuildValue("s#", res.data, 32);    //TODO: warning, hardcoded hash size!
// #endif
// }


/*
PyObject* kth_py_native_long_hash_t_to_str(PyObject* self, PyObject* args) {
    PyObject* py_lh;

    if ( ! PyArg_ParseTuple(args, "O", &py_lh)) {
        return NULL;
    }

    // long_hash_t lh = (long_hash_t)PyCObject_AsVoidPtr(py_lh);
    long_hash_t lh = (long_hash_t)PyCapsule_GetPointer(py_lh, NULL);

    return Py_BuildValue("y#", lh, 32 * 2);    //TODO: warning, hardcoded long hash size!
}


PyObject* kth_py_native_long_hash_t_free(PyObject* self, PyObject* args) {
    PyObject* py_lh;

    if ( ! PyArg_ParseTuple(args, "O", &py_lh)) {
        return NULL;
    }

    // long_hash_t lh = (long_hash_t)PyCObject_AsVoidPtr(py_lh);
    long_hash_t lh = (long_hash_t)PyCapsule_GetPointer(py_lh, NULL);

    // free(lh);
    long_hash_destroy(lh);

    Py_RETURN_NONE;
}*/
