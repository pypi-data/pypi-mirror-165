#include <kth/py-native/chain/payment_address.h>

#include <kth/capi.h>
#include <kth/py-native/utils.h>

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_wallet_payment_address_destruct(PyObject* self, PyObject* args){
    PyObject* py_payment_address;
    if ( ! PyArg_ParseTuple(args, "O", &py_payment_address)) {
        return NULL;
    }
    kth_payment_address_t payment_address = (kth_payment_address_t)get_ptr(py_payment_address);
    kth_wallet_payment_address_destruct(payment_address);
    Py_RETURN_NONE;

}

PyObject* kth_py_native_wallet_payment_address_encoded(PyObject* self, PyObject* args){
    PyObject* py_payment_address;

    if ( ! PyArg_ParseTuple(args, "O", &py_payment_address)) {
        return NULL;
    }

    kth_payment_address_t payment_address = (kth_payment_address_t)get_ptr(py_payment_address);
    char const* res = kth_wallet_payment_address_encoded(payment_address);
    return Py_BuildValue("s", res);
}


PyObject* kth_py_native_wallet_payment_address_version(PyObject* self, PyObject* args){
    PyObject* py_payment_address;
    if ( ! PyArg_ParseTuple(args, "O", &py_payment_address)) {
        return NULL;
    }
    kth_payment_address_t payment_address = (kth_payment_address_t)get_ptr(py_payment_address);
    uint8_t res = kth_wallet_payment_address_version(payment_address);

    return Py_BuildValue("i", res);
}

PyObject* kth_py_native_wallet_payment_address_construct_from_string(PyObject* self, PyObject* args){
    char* py_string;
    Py_ssize_t py_size;

    if ( ! PyArg_ParseTuple(args, "s#", &py_string, &py_size)) {
        return NULL;
    }
    kth_payment_address_t res = kth_wallet_payment_address_construct_from_string(py_string);
    return to_py_obj(res);
}

#ifdef __cplusplus
} //extern "C"
#endif
