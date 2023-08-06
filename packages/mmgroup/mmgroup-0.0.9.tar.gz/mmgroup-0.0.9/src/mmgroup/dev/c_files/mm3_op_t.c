/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm3_op_t.c

 File ``mm3_op_t.c`` implements the operation of the element
 \f$\tau^e\f$ of the monster group on a vector in the
 representation \f$\rho_{3}\f$ of the monster.

 Here the generator \f$\tau\f$, which is the triality element in
 the monster group, is defined as in section **The monster group**
 of the **API reference**.

 The representation \f$\rho_{3}\f$ is equal to the
 196884-dimensional representation  \f$\rho\f$ of the monster,
 with coefficients taken modulo 3, as defined in
 section **The representation of the monster group**
 in the **API reference**.

 An element of \f$\rho_{3}\f$ is implemented as an array of
 integers of type ``uint_mmv_t`` as described in
 section **Description of the mmgroup.mm extension**
 in this document.

 We have \f$\tau^3 = 1\f$, and the opration of \f$\tau^e, e = 1,2\f$
 on \f$\rho\f$ is given in [Seysen19], section 8.1. The
 non-monomial part of the operation of \f$\tau^e\f$ can be decomposed
 into a product of monomial matrices and matrices containing
 blocks of \f$2 \times 2\f$-Hadamard matrices. We use the Python
 functions and classes in files ``hadamard_codegen.py`` and
 ``hadamard_t.py`` in subdirectory ``mmgroup/dev/hadamard`` for
 generating C code that implements the products of Hadamard
 matrices corresponding to the generator \f$\tau^e\f$.
*/


#include <string.h>
#include "mat24_functions.h"
#include "mm_op3.h"   

// %%EXPORT_KWD MM_OP%{P}_API


//  %%GEN h
//  %%GEN c


/// @cond DO_NOT_DOCUMENT 


static void invert3_xyz(uint_mmv_t *v_in, uint_mmv_t *v_out)
{
    uint_fast32_t i;
    const uint16_t *p_theta = MAT24_THETA_TABLE;
    
    for (i = 0; i <2048; ++i) {
        uint_mmv_t mask = 0 - ((uint_mmv_t)(((p_theta[i] >> 12) & 0x1ULL)));
        mask &= 0xffffffffffffULL;
        *v_out++ = *v_in++ ^ mask;
    }
}

/// @endcond  



/// @cond DO_NOT_DOCUMENT 

/**
  @brief Auxiliary function for function ``mm_op3_t``

  Parameters ``v_in`` and ``v_out``are as in function ``mm_op3_t``.
  This function performs the action of that function for the 
  tags ``A, B, C``.  Parameter ``exp1`` should be 0 or -1 if the
  actual exponent ``exp`` in function ``mm_op3_t`` is 1 or 2, 
  respectively. This function should not be called in 
  case ``exp = 0``.
*/
static inline void 
op3_t_ABC(uint_mmv_t *v_in,  uint_mmv_t exp1, uint_mmv_t *v_out)
{
    uint_mmv_t i, j;

    for (i = 0; i < 24; ++i) {
        // Compute index of diagonal element
        uint_mmv_t i_diag = i >> 5;
        // Compute mask for diagonal element
        uint_mmv_t m_diag = 0x3ULL << ((i << 1) & 63);
        // Load shifted value of diagonal element of part A to ``v_diag``
        uint_mmv_t v_diag = v_in[i_diag] & m_diag;
 
        // Do off-diagonal part of tags A, B, C
        for (j = 0; j < 1; ++j) {
            // %%MUL_MATRIX_T3 v_in, exp1, v_out

            // This is an automatically generated matrix operation, do not change!
            {
            uint_mmv_t r0, r1, r2, r3, r4;

            // Multiply the vector of integers mod 3 stored in
            // (v_in) by t**e, where t is the 3 times 3 triality
            // matrix [[0, 2,  -2], [1, 1, 1], [1,  -1, -1]] / 2.
            // and e = 1 if exp1 = 0, e = 2 if exp1 = 
            // (uint_mmv_t)(-1). The result is stored in (v_out).
            // 
            // v_in and v_out are pointers of type *uint_mmv_t.
            // Components with tags A, B, C referred by (v_in) 
            // are processed, one integer of type uint_mmv_t
            // for each tag.
            // 
            // 
            // Loading vector from rep 196884x with tags A,B,C
            // to v[0...2]. Here v_in refers to the tag A part. 
            // Negate v[2] if exp1 == -1.
            r0 = (v_in)[0];
            r1 = (v_in)[24];
            r2 = (v_in)[48] ^ ((exp1) & 0xffffffffffffffffULL);
            // Vector is now  r(i) for i = 0,1,2
            exp1 = ~(exp1);
            r4 = (r1 & r2);
            r4 |= ((r4 << 1) & (r1 ^ r2)); // 4 ops
            r4 &= 0xaaaaaaaaaaaaaaaaULL;
            r3 = (((r1 + r2) - r4) - (r4 >> 1)); // 4 ops
            r2 = (r2 ^ 0xffffffffffffffffULL);
            r4 = (r1 & r2);
            r4 |= ((r4 << 1) & (r1 ^ r2)); // 4 ops
            r4 &= 0xaaaaaaaaaaaaaaaaULL;
            r2 = (((r1 + r2) - r4) - (r4 >> 1)); // 4 ops
            r1 = r3;
            r1 = (~r1);
            r2 = (~r2);
            r4 = (r0 & r2);
            r4 |= ((r4 << 1) & (r0 ^ r2)); // 4 ops
            r4 &= 0xaaaaaaaaaaaaaaaaULL;
            r3 = (((r0 + r2) - r4) - (r4 >> 1)); // 4 ops
            r2 = (r2 ^ 0xffffffffffffffffULL);
            r4 = (r0 & r2);
            r4 |= ((r4 << 1) & (r0 ^ r2)); // 4 ops
            r4 &= 0xaaaaaaaaaaaaaaaaULL;
            r2 = (((r0 + r2) - r4) - (r4 >> 1)); // 4 ops
            r0 = r3;
            // Store vector v[0...2] to rep 196884x with 
            // tags A,B,C. Here v_out refers to the tag A part. 
            // Negate v[2] if exp1 == -1.
            (v_out)[0] = r1;
            (v_out)[24] = r0;
            (v_out)[48]  = r2 ^ ((exp1) & 0xffffffffffffffffULL);
            exp1 = ~(exp1);
            // 30 lines of code, 48 operations
            }
            // End of automatically generated matrix operation.
 
            // Advance pointers to input and output
            ++v_in; ++v_out;
        }
        // Zero slack
        v_out[-1] &= 0xffffffffffffULL;
        v_out[23] &= 0xffffffffffffULL;
        v_out[47] &= 0xffffffffffffULL;  
        // Restore diagonal element of part A 
        v_out -= 1; // Same position as at start of loop
        m_diag = ~m_diag;          // Mask for non-diagonal part
        v_out[i_diag] = (v_out[i_diag] & m_diag) | v_diag;
        // Zero diagonal elements of parts B and C 
        v_out[i_diag + 24] &= m_diag;
        v_out[i_diag + 48] &= m_diag;
        // Advance pointer to output
        v_out +=  1;
    }
}

/**
  @brief Simplified version of function ``op3_t_ABC``

  Same as function ``op3_t_ABC``; but here we only compute
  the ``A`` part of the output vector.
*/
static inline void 
op3_t_A(uint_mmv_t *v_in,  uint_mmv_t exp1, uint_mmv_t *v_out)
{
    uint_mmv_t i, j;

    for (i = 0; i < 24; ++i) {
        // Compute index of diagonal element
        uint_mmv_t i_diag = i >> 5;
        // Compute mask for diagonal element
        uint_mmv_t m_diag = 0x3ULL << ((i << 1) & 63);
        // Load shifted value of diagonal element of part A to ``v_diag``
        uint_mmv_t v_diag = v_in[i_diag] & m_diag;
 
        // Do off-diagonal part of tags A, B, C
        for (j = 0; j < 1; ++j) {
            // %%MUL_MATRIX_T3A v_in, exp1, v_out

            // This is an automatically generated matrix operation, do not change!
            {
            uint_mmv_t r0, r1, r2;

            // Put dest_A =  (src_B + mask * src_C) / 2   (mod 3)
            // 
            // Here src_B and src_C are the part of a vector of integers 
            // mod 3 stored in (v_in) with tag B and C, and dest_A is 
            // the part of a vector of integers mod 3 stored in (v_out),  
            // with tag A. Here exp1 must be 0 or -1.
            // 
            // This means that the function computes the part with tag A of
            // the vector (v_out) = (v_in) * t**e, where e = 1 - mask.
            // 
            // v_in and v_out are pointers of type *uint_mmv_t.
            // Components with tags B, C referred by (v_in) 
            // are processed, one integer of type uint_mmv_t
            // for each tag.
            // 
            // 
            // Loading vector from rep 196884x with tags A,B,C
            // to v[0...2]. Here v_in refers to the tag A part. 
            // Negate v[2] if exp1 == -1.
            r0 = (v_in)[24];
            r1 = (v_in)[48] ^ ((exp1) & 0xffffffffffffffffULL);
            // Vector is now  r(i) for i = 0,1
            r2 = (r0 & r1);
            r2 |= ((r2 << 1) & (r0 ^ r1)); // 4 ops
            r2 &= 0xaaaaaaaaaaaaaaaaULL;
            r0 = (((r0 + r1) - r2) - (r2 >> 1)); // 4 ops
            r0 = (~r0);
            // Store vector v[0] to rep 196884x with 
            // tags A. Here v_out refers to the tag A part. 
            (v_out)[0] = r0;
            // 8 lines of code, 12 operations
            }
            // End of automatically generated matrix operation.
 
            // Advance pointers to input and output
            ++v_in; ++v_out;
        }
        // Zero slack
        v_out[-1] &= 0xffffffffffffULL;
        // Restore diagonal element of part A 
        v_out -= 1; // Same position as at start of loop
        m_diag = ~m_diag;          // Mask for non-diagonal part
        v_out[i_diag] = (v_out[i_diag] & m_diag) | v_diag;
        // Advance pointer to output
        v_out +=  1;
    }
}


/// @endcond 



/**
  @brief Compute an operation of the monster group on a vector

  Let ``v_in`` be a vector of the representation \f$\rho_{3}\f$
  of the monster group.

  The function implements the operation of the element \f$\tau^e\f$
  of the monster group  on a vector ``v_in`` in the
  representation \f$\rho_{3}\f$ of the monster.

  Parameter ``exp`` is the exponent \f$e\f$ of the generator
  \f$\tau^e\f$. The function computes the operation of \f$\tau^e\f$
  on the input  vector ``v_in`` and  stores the result in the output
  vector ``v_out``.

  Input vector ``v_in`` is not changed.
*/
// %%EXPORT px
MM_OP3_API
void mm_op3_t(uint_mmv_t *v_in,  uint32_t exp, uint_mmv_t *v_out)
{
    uint_mmv_t i, exp1;
 
    exp %= 3;
    if (exp == 0) {
        for (i = 0; i < 7734; ++i) v_out[i] = v_in[i];
        return;
    }
    exp1 = 0x1ULL - (uint_mmv_t)exp;

    // Do tags A, B, C
    op3_t_ABC(v_in, exp1, v_out);

    // Do tag T
    v_in += MM_OP3_OFS_T;
    v_out +=  MM_OP3_OFS_T;
    for (i = 0; i < 759; ++i) {
        // %%MUL_MATRIX_T64 v_in, exp1, v_out

        // This is an automatically generated matrix operation, do not change!
        {
        uint_mmv_t r0, r1, r2, r3;

        // Multiply the vector of integers mod 3 stored
        // in (v_in) by t**e, where t is the 64 times 64 
        // triality matrix and e = 1 if exp1 = 0, e = 2 if
        // exp1 = (uint_mmv_t)(-1). The result is stored
        // in (v_out).
        // 
        // Loading vector v from array v_in; multiply v
        // with diagonal matrix if exp1 == -1.
        r0 = v_in[0] ^ ((exp1) & 0xc003033f033f3ffcULL);
        r1 = v_in[1] ^ ((exp1) & 0xfcc0c003c003033fULL);
        // Vector is now  r(i) for i = 0,1
        exp1 = ~(exp1);
        // Exchange component i with component 63-i if i 
        // has odd parity; fix it if i has even parity.
        r2 = ((r0 & 0xc33c3cc33cc3c33cULL)
            | (r1 & 0x3cc3c33cc33c3cc3ULL)); // 3 ops
        r2 = ((r2 << 32) | (r2 >> 32)); // 3 ops
        r2 = (((r2 & 0xffff0000ffffULL) << 16)
            | ((r2 >> 16) & 0xffff0000ffffULL)); // 5 ops
        r2 = (((r2 & 0xff00ff00ff00ffULL) << 8)
            | ((r2 >> 8) & 0xff00ff00ff00ffULL)); // 5 ops
        r2 = (((r2 & 0xf0f0f0f0f0f0f0fULL) << 4)
            | ((r2 >> 4) & 0xf0f0f0f0f0f0f0fULL)); // 5 ops
        r2 = (((r2 & 0x3333333333333333ULL) << 2)
            | ((r2 >> 2) & 0x3333333333333333ULL)); // 5 ops
        r0 = ((r0 & 0x3cc3c33cc33c3cc3ULL)
            | (r2 & 0xc33c3cc33cc3c33cULL)); // 3 ops
        r1 = ((r1 & 0xc33c3cc33cc3c33cULL)
            | (r2 & 0x3cc3c33cc33c3cc3ULL)); // 3 ops
        // Butterfly: v[i], v[i+1] = v[i]+v[i+1], v[i]-v[i+1]
        r2 = (((r0 << 2) & 0xccccccccccccccccULL)
            | ((r0 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r0 = (r0 ^ 0xccccccccccccccccULL);
        r3 = (r0 & r2);
        r3 |= ((r3 << 1) & (r0 ^ r2)); // 4 ops
        r3 &= 0xaaaaaaaaaaaaaaaaULL;
        r0 = (((r0 + r2) - r3) - (r3 >> 1)); // 4 ops
        r2 = (((r1 << 2) & 0xccccccccccccccccULL)
            | ((r1 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r1 = (r1 ^ 0xccccccccccccccccULL);
        r3 = (r1 & r2);
        r3 |= ((r3 << 1) & (r1 ^ r2)); // 4 ops
        r3 &= 0xaaaaaaaaaaaaaaaaULL;
        r1 = (((r1 + r2) - r3) - (r3 >> 1)); // 4 ops
        // Vector is now  r(i) for i = 0,1
        // Butterfly: v[i], v[i+2] = v[i]+v[i+2], v[i]-v[i+2]
        r2 = (((r0 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r0 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r0 = (r0 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r3 = (r0 & r2);
        r3 |= ((r3 << 1) & (r0 ^ r2)); // 4 ops
        r3 &= 0xaaaaaaaaaaaaaaaaULL;
        r0 = (((r0 + r2) - r3) - (r3 >> 1)); // 4 ops
        r2 = (((r1 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r1 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r1 = (r1 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r3 = (r1 & r2);
        r3 |= ((r3 << 1) & (r1 ^ r2)); // 4 ops
        r3 &= 0xaaaaaaaaaaaaaaaaULL;
        r1 = (((r1 + r2) - r3) - (r3 >> 1)); // 4 ops
        // Vector is now  r(i) for i = 0,1
        // Butterfly: v[i], v[i+4] = v[i]+v[i+4], v[i]-v[i+4]
        r2 = (((r0 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r0 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r0 = (r0 ^ 0xff00ff00ff00ff00ULL);
        r3 = (r0 & r2);
        r3 |= ((r3 << 1) & (r0 ^ r2)); // 4 ops
        r3 &= 0xaaaaaaaaaaaaaaaaULL;
        r0 = (((r0 + r2) - r3) - (r3 >> 1)); // 4 ops
        r2 = (((r1 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r1 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r1 = (r1 ^ 0xff00ff00ff00ff00ULL);
        r3 = (r1 & r2);
        r3 |= ((r3 << 1) & (r1 ^ r2)); // 4 ops
        r3 &= 0xaaaaaaaaaaaaaaaaULL;
        r1 = (((r1 + r2) - r3) - (r3 >> 1)); // 4 ops
        // Vector is now  r(i) for i = 0,1
        // Butterfly: v[i], v[i+8] = v[i]+v[i+8], v[i]-v[i+8]
        r2 = (((r0 << 16) & 0xffff0000ffff0000ULL)
            | ((r0 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r0 = (r0 ^ 0xffff0000ffff0000ULL);
        r3 = (r0 & r2);
        r3 |= ((r3 << 1) & (r0 ^ r2)); // 4 ops
        r3 &= 0xaaaaaaaaaaaaaaaaULL;
        r0 = (((r0 + r2) - r3) - (r3 >> 1)); // 4 ops
        r2 = (((r1 << 16) & 0xffff0000ffff0000ULL)
            | ((r1 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r1 = (r1 ^ 0xffff0000ffff0000ULL);
        r3 = (r1 & r2);
        r3 |= ((r3 << 1) & (r1 ^ r2)); // 4 ops
        r3 &= 0xaaaaaaaaaaaaaaaaULL;
        r1 = (((r1 + r2) - r3) - (r3 >> 1)); // 4 ops
        // Vector is now  r(i) for i = 0,1
        // Butterfly: v[i], v[i+16] = v[i]+v[i+16], v[i]-v[i+16]
        r2 = ((r0 << 32) | (r0 >> 32)); // 3 ops
        r0 = (r0 ^ 0xffffffff00000000ULL);
        r3 = (r0 & r2);
        r3 |= ((r3 << 1) & (r0 ^ r2)); // 4 ops
        r3 &= 0xaaaaaaaaaaaaaaaaULL;
        r0 = (((r0 + r2) - r3) - (r3 >> 1)); // 4 ops
        r2 = ((r1 << 32) | (r1 >> 32)); // 3 ops
        r1 = (r1 ^ 0xffffffff00000000ULL);
        r3 = (r1 & r2);
        r3 |= ((r3 << 1) & (r1 ^ r2)); // 4 ops
        r3 &= 0xaaaaaaaaaaaaaaaaULL;
        r1 = (((r1 + r2) - r3) - (r3 >> 1)); // 4 ops
        // Vector is now  r(i) for i = 0,1
        // Butterfly: v[i], v[i+32] = v[i]+v[i+32], v[i]-v[i+32]
        r3 = (r0 & r1);
        r3 |= ((r3 << 1) & (r0 ^ r1)); // 4 ops
        r3 &= 0xaaaaaaaaaaaaaaaaULL;
        r2 = (((r0 + r1) - r3) - (r3 >> 1)); // 4 ops
        r1 = (r1 ^ 0xffffffffffffffffULL);
        r3 = (r0 & r1);
        r3 |= ((r3 << 1) & (r0 ^ r1)); // 4 ops
        r3 &= 0xaaaaaaaaaaaaaaaaULL;
        r1 = (((r0 + r1) - r3) - (r3 >> 1)); // 4 ops
        r0 = r2;
        // Vector is now  r(i) for i = 0,1
        // Multiply vector by scalar 2**-3 mod 3
        r0 = (~r0);
        r1 = (~r1);
        // Storing vector v to array v_out; multiply v
        // with diagonal matrix if exp1 == -1.
        v_out[0] = r0 ^ ((exp1) & 0xc003033f033f3ffcULL);
        v_out[1] = r1 ^ ((exp1) & 0xfcc0c003c003033fULL);
        exp1 = ~(exp1);
        // 86 lines of code, 219 operations
        }
        // End of automatically generated matrix operation.
 
        v_in += 2;
        v_out += 2;
    }

    // Do tags X, Y, and Z
    {
         uint_mmv_t *pXYin, *pYZin, *pZXin;
         uint_mmv_t *pXYout, *pYZout, *pZXout;
         if (exp1 == 0) {
             pXYin = v_in; 
             pXYout = v_out + 4096;  
             pYZin = v_in + 4096; 
             pYZout = v_out + 2048;  
             pZXin = v_in + 2048; 
             pZXout = v_out; 
         } else {
             pXYout = v_out; 
             pXYin = v_in + 4096;  
             pYZout = v_out + 4096; 
             pYZin = v_in + 2048;  
             pZXout = v_out + 2048; 
             pZXin = v_in; 
         }

         // Map X to Y for t and Y to X for t**2
         for (i = 0; i < 2048; ++i) pXYout[i] = pXYin[i];
         mm_op3_neg_scalprod_d_i(pXYout);
         
         // Map Y to Z for t and Z to Y for t**2
         invert3_xyz(pYZin, pYZout);
         mm_op3_neg_scalprod_d_i(pYZout);

         // Map Z to X for t and X to Z for t**2
         invert3_xyz(pZXin, pZXout);
    }
}



/**
  @brief A restricted version of function ``mm_op3_t``

  Function ``mm_op3_t`` computes a certain operation of the
  monster group on a vector ``v_in`` and stores the result in a
  vector ``v_out``. That operation depends on a parameter ``exp``.
  
  Function ``mm_op3_t_A`` performs the same operation, but it
  computes the part of the vector  ``v_out``  that consists of
  the entries of vector ``v_out``  with tag ``A`` only; the
  other entries of vector ``v_out`` are not changed.
  See section **The representation of the monster group**
  in the **API reference** for tags of entries of a vector in
  the representation of the monster. Note that the entries
  of vector ``v_out`` with tag ``A`` also depend on entries
  of vector ``v_in`` with tags different from ``A``.

  Parameters of this function are the same as in the case of
  function ``mm_op3_t``. This function is much faster than
  function ``mm_op3_t``.
*/
// %%EXPORT px
MM_OP3_API
void mm_op3_t_A(uint_mmv_t *v_in,  uint32_t exp, uint_mmv_t *v_out)
{
    uint_mmv_t i, exp1;
 
    exp %= 3;
    if (exp == 0) {
        for (i = 0; i < 24; ++i) v_out[i] = v_in[i];
        return;
    }
    exp1 = 0x1ULL - (uint_mmv_t)exp;
    op3_t_A(v_in, exp1, v_out);
}



/**
  @brief Another restricted version of function ``mm_op3_t``

  Function ``mm_op3_t`` computes a certain operation of the
  monster group on a vector ``v_in`` and stores the result in a
  vector ``v_out``. That operation depends on a parameter ``exp``.
  
  Function ``mm_op3_t_ABC`` computes the same
  operation on the entries of the vector ``v = v_in`` with
  tag ``A, B, C`` only, and ignores the other entries of ``v``.
  See section **The representation of the monster group**
  in the **API reference** for tags of entries of a vector in
  the representation of the monster.

  The function overwrites the vector ``v`` with the result.
  Here only entries of ``v`` with tag ``A, B, C`` are changed. 
  This function is much faster than  function ``mm_op3_t``.
*/
// %%EXPORT px
MM_OP3_API
void mm_op3_t_ABC(uint_mmv_t *v,  uint32_t exp)
{
    uint_mmv_t  exp1;
 
    exp %= 3;
    if (exp == 0) return;
    exp1 = 0x1ULL - (uint_mmv_t)exp;
    op3_t_ABC(v, exp1, v);
}





//  %%GEN h
//  %%GEN c


