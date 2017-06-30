#include "Python.h"
#include "numpy/arrayobject.h"
#include <stdio.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_linalg.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_blas.h>

/* 
typedef struct {
PyObject_HEAD
double ob_fval;
} PyFloatObject;
*/

/* Inside gsl_cblas.h
enum CBLAS_ORDER {CblasRowMajor=101, CblasColMajor=102};
enum CBLAS_TRANSPOSE {CblasNoTrans=111, CblasTrans=112, CblasConjTrans=113};
enum CBLAS_UPLO {CblasUpper=121, CblasLower=122};
enum CBLAS_DIAG {CblasNonUnit=131, CblasUnit=132};
enum CBLAS_SIDE {CblasLeft=141, CblasRight=142};
*/

static PyObject *update(PyObject *self, PyObject *args)
{

PyArrayObject *_mu, *_cov, *_covInv, *_z, *_obs;
PyFloatObject *_lam, *_adjust;
int dim;


if (!PyArg_ParseTuple(args, "O!O!O!O!O!OOi",
      &PyArray_Type, &_mu,   &PyArray_Type, &_cov,   &PyArray_Type, &_covInv, 
      &PyArray_Type, &_z,    &PyArray_Type, &_obs, 
      &_lam,                 &_adjust,               &dim)
   )
  return NULL;

// _lam is a pointer to PyFloatObject, _lam->ob_fval is its double value
if (_mu->nd != 1 || _cov->nd !=2 || _covInv->nd !=2 || _z->nd !=1 
      || _obs->nd !=1) {
  PyErr_SetString(PyExc_ValueError, 
    "input array dimension error");
}


// convert the inputs into gsl matrix or vector
gsl_vector_view mu_view = gsl_vector_view_array((double*)(_mu->data), dim);
gsl_vector* mu = &(mu_view.vector);

gsl_matrix_view cov_view = gsl_matrix_view_array((double*)(_cov->data), dim, dim);
gsl_matrix* cov = &(cov_view.matrix);

gsl_matrix_view covInv_view = gsl_matrix_view_array((double*)(_covInv->data), dim, dim);
gsl_matrix* covInv = &(covInv_view.matrix);

gsl_vector_view z_view = gsl_vector_view_array((double*)(_z->data), dim);
gsl_vector* z = &(z_view.vector);

gsl_vector_view obs_view = gsl_vector_view_array((double*)(_obs->data), dim);
gsl_vector* obs = &(obs_view.vector);


double *lam = &(_lam->ob_fval);  
double *adjust = &(_adjust->ob_fval);


// cons = lam/(2-lam)
double cons = *lam/(2-*lam);

// z = (1-lam)z + lam(obs-mu), normalization step
gsl_vector_sub(obs,mu);
gsl_vector_scale(obs, *lam);
gsl_vector_scale(z,1-*lam);
gsl_vector_add(z,obs);

//int gsl_blas_dgemv (CBLAS_TRANSPOSE_t TransA, double alpha, 
//        const gsl_matrix * A, const gsl_vector * x, double beta, gsl_vector * y)

// val = z*covInv*z
gsl_vector* temp_z = gsl_vector_calloc(dim);
gsl_blas_dgemv(CblasNoTrans, 1.0, covInv, z, 0, temp_z);
double *val=malloc(sizeof(double)); *val=0.0;
gsl_blas_ddot(z,temp_z,val);

*adjust *= (1-*lam)*(1-*lam);
*val /= (1-*adjust);
*val /= cons;

return PyFloat_FromDouble(*val);  

//return PyFloat_FromDouble(0.01);

/* Irrelevant code,  no use
if (n > array->dimensions[1])
n = array->dimensions[1];
sum = 0.;

for (i = 0; i < n; i++)
//sum += *(double *)(array->data + i*array->strides[0] + i*array->strides[1]);
return PyFloat_FromDouble(sum); */

}


// Module method table 
// This is neccessary to define the methods in your new extension module
static PyMethodDef methods[] = {
  {"update",  update, METH_VARARGS, "Greatest common divisor"},
  //{"in_mandel", py_in_mandel, METH_VARARGS, "Mandelbrot test"},
  //{"divide", py_divide, METH_VARARGS, "Integer division"},
  { NULL, NULL, 0, NULL}
}; 


// Module structure 
static struct PyModuleDef samplemodule = {
  PyModuleDef_HEAD_INIT,

  "sample",           // name of module 
  "A sample module",  // Doc string (may be NULL) 
  -1,                 // Size of per-interpreter state or -1 
  methods       // Method table 
};


// Module initialization function 
// When you "import sample" in your .py file, python interpreter will look for 
// an initialize function which will initialize your module, if your extension modele
// name is "sample", then the initialize function name will be "initsample", 
// its always "init" followed by your module name
PyMODINIT_FUNC
PyInit_sample(void) {
    import_array();
    return PyModule_Create(&samplemodule);
    //(void)Py_InitModule("sample", methods);

    // this is to import the numpy C-API
    
    
    /*
    if(PyArray_API == NULL)
      printf("No API"); 
    else
      printf("API imported");
    */
}