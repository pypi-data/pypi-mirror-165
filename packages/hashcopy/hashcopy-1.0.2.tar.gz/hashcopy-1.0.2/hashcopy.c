/*

Copyright (C) 2022 Katie Rust (katie@ktpanda.org)

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

*/

#define PY_SSIZE_T_CLEAN
#define Py_LIMITED_API 0x03040000

#include <Python.h>

#include <stdio.h>
#include <sys/mman.h>
#include "openssl/sha.h"
#include <sys/types.h>
#include <unistd.h>

#define MAX_COPY_LENGTH (1024 * 1024 * 128)
#define DEFAULT_COPY_LENGTH (1024 * 1024 * 4)

const char* module_doc =
    "";

typedef struct HashCopier {
    PyObject_HEAD

    /* Without overriding tp_new, we can't gurantee that __init__ is called, only that the
     * object is zeroed. This prevents using an uninitialized object, and also prevents
     * double initialization */

    int initialized;

    /* OpenSSL SHA256 context. Deprecated, but still supported, */
    SHA256_CTX hash;

    /* Base mmapped address, current position, and pointer to the end of the buffer. */
    unsigned char* baseaddr;
    unsigned char* curpos;
    unsigned char* endpos;

    /* Size of the input file. */
    off_t input_size;

    /* Input and output file descriptors. */
    int inputfd, outputfd;

    /* Number of bytes to copy each time update() is called. */
    Py_ssize_t blocksize;
} HashCopier;

static struct PyModuleDef hashcopy_module;
static PyObject* HashCopierType;
static PyType_Spec HashCopier_Type_spec;

PyMODINIT_FUNC
PyInit_hashcopy(void)
{
    PyObject *m;

    m = PyModule_Create(&hashcopy_module);
    if (m == NULL)
        return NULL;

    HashCopierType = PyType_FromSpec(&HashCopier_Type_spec);
    if (HashCopierType == NULL) {
        Py_DecRef(m);
        return NULL;
    }

    if (PyModule_AddObject(m, "HashCopier", HashCopierType) < 0) {
        Py_DecRef(HashCopierType);
        Py_DecRef(m);
        return NULL;
    }

    return m;
}

int hashcopy_init(HashCopier *self, PyObject *args, PyObject *kwds) {
    static char* keywords[] = {
        "inputfd",
        "outputfd",
        "blocksize"
    };

    unsigned char* mapaddr = MAP_FAILED;
    off_t size;
    if (self->initialized)
        return 0;

    self->initialized = 0;
    self->baseaddr = NULL;
    self->curpos = NULL;
    self->endpos = NULL;
    self->inputfd = -1;
    self->outputfd = -1;
    self->blocksize = DEFAULT_COPY_LENGTH;
    SHA256_Init(&self->hash);

    if (!PyArg_ParseTupleAndKeywords(
            args, kwds, "i|in:hashcopy.HashCopier.__init__", keywords,
            &self->inputfd,
            &self->outputfd,
            &self->blocksize)) {
        return -1;
    }

    if (self->blocksize < 0 || self->blocksize > MAX_COPY_LENGTH) {
        PyErr_SetString(PyExc_ValueError, "Invalid value for `blocksize`");
        return -1;
    }

    size = lseek(self->inputfd, 0, SEEK_END);
    if (size == (off_t)-1) {
        PyErr_SetFromErrno(PyExc_OSError);
        return -1;
    }
    self->input_size = size;

    if (size == 0) {
        self->initialized = 1;
        return 0;
    }
    mapaddr = mmap(NULL, self->input_size, PROT_READ, MAP_SHARED, self->inputfd, 0);
    if (mapaddr == MAP_FAILED) {
        PyErr_SetFromErrno(PyExc_OSError);
        return -1;
    }

    self->baseaddr = mapaddr;
    self->curpos = mapaddr;
    self->endpos = mapaddr + size;

    madvise(mapaddr, size, MADV_SEQUENTIAL);

    self->initialized = 1;
    return 0;
}

static PyObject* hashcopy_update(HashCopier* self) {
    ptrdiff_t copy_length;
    if (!self->initialized)
        return PyLong_FromSsize_t(0);

    copy_length = self->endpos - self->curpos;
    if (copy_length > self->blocksize) copy_length = self->blocksize;

    /* Reached the end of the file. */
    if (copy_length == 0)
        return PyLong_FromSsize_t(0);

    SHA256_Update(&self->hash, self->curpos, copy_length);
    if (self->outputfd != -1) {
        if (write(self->outputfd, self->curpos, copy_length) == -1) {
            PyErr_SetFromErrno(PyExc_OSError);
            return NULL;
        }
    }
    madvise(self->curpos, copy_length, MADV_DONTNEED);
    self->curpos += copy_length;
    return PyLong_FromSsize_t(copy_length);
}

static PyObject* hashcopy_finalize(HashCopier* self, PyObject* args) {
    unsigned char out[32];
    SHA256_Final(out, &self->hash);
    return PyBytes_FromStringAndSize((char*)out, 32);
}

/* Unmaps the memory. Called by close() and tp_dealloc. */
static void hashcopy_unmap(HashCopier* self) {
    if (self->initialized && self->baseaddr != NULL) {
        munmap(self->baseaddr, self->input_size);
        self->initialized = 0;
        self->baseaddr = NULL;
        self->curpos = NULL;
        self->endpos = NULL;
    }
}

/* Implementation of context manager. */
static PyObject* hashcopy_enter(HashCopier* self, PyObject* args) {
    Py_IncRef((PyObject*)self);
    return (PyObject*)self;
}

static PyObject* hashcopy_close(HashCopier* self, PyObject* args) {
    hashcopy_unmap(self);
    Py_IncRef(Py_None);
    return Py_None;
}

static void hashcopy_dealloc(HashCopier* self, unsigned char* out) {
    PyObject* type;
    freefunc tp_free;

    type = PyObject_Type((PyObject*)self);
    tp_free = (freefunc)PyType_GetSlot((PyTypeObject*)type, Py_tp_free);

    hashcopy_unmap(self);
    tp_free((PyObject*)self);

    /* Decref once for PyObject_Type, then once more for the object's reference to its own type. */
    Py_DecRef(type);
    Py_DecRef(type);
}

static PyMethodDef hashcopy_methods[] = {
    {NULL}
};

static struct PyModuleDef hashcopy_module = {
    PyModuleDef_HEAD_INIT,
    "hashcopy",   /* name of module */
    NULL,         /* module documentation, may be NULL */
    -1,           /* size of per-interpreter state of the module,
                     or -1 if the module keeps state in global variables. */
    hashcopy_methods
};

static PyMethodDef HashCopier_methods[] = {
    {"close", (PyCFunction)hashcopy_close, METH_NOARGS,
     "Frees resources allocated for the copier. NOTE: Does not close the file descriptors."},

    {"update", (PyCFunction)hashcopy_update, METH_NOARGS,
     "Reads and hashes one block from the source file, and writes the result to the output file if given."},

    {"finalize", (PyCFunction)hashcopy_finalize, METH_NOARGS,
     "Finalizes and returns the result of the hash as a `bytes` object."},

    {"__enter__", (PyCFunction)hashcopy_enter, METH_NOARGS,
     "Entry method for use with the `with` statement."},

    {"__exit__", (PyCFunction)hashcopy_close, METH_VARARGS,
     "Exit method for use with the `with` statement."},

    {NULL}
};

static PyType_Slot HashCopier_slots[] = {
    {Py_tp_init, hashcopy_init},
    {Py_tp_dealloc, hashcopy_dealloc},
    {Py_tp_methods, HashCopier_methods},
    {0, 0}
};

static PyType_Spec HashCopier_Type_spec = {
    "hashcopy.HashCopier",
    sizeof(HashCopier),
    0,
    Py_TPFLAGS_DEFAULT,
    HashCopier_slots
};
