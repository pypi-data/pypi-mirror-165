/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm15_op_t.c

 File ``mm15_op_t.c`` implements the operation of the element
 \f$\tau^e\f$ of the monster group on a vector in the
 representation \f$\rho_{15}\f$ of the monster.

 Here the generator \f$\tau\f$, which is the triality element in
 the monster group, is defined as in section **The monster group**
 of the **API reference**.

 The representation \f$\rho_{15}\f$ is equal to the
 196884-dimensional representation  \f$\rho\f$ of the monster,
 with coefficients taken modulo 15, as defined in
 section **The representation of the monster group**
 in the **API reference**.

 An element of \f$\rho_{15}\f$ is implemented as an array of
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
#include "mm_op15.h"   

// %%EXPORT_KWD MM_OP%{P}_API


//  %%GEN h
//  %%GEN c


/// @cond DO_NOT_DOCUMENT 


static void invert15_xyz(uint_mmv_t *v_in, uint_mmv_t *v_out)
{
    uint_fast32_t i;
    const uint16_t *p_theta = MAT24_THETA_TABLE;
    
    for (i = 0; i <2048; ++i) {
        uint_mmv_t mask = 0 - ((uint_mmv_t)(((p_theta[i] >> 12) & 0x1ULL)));
        mask &= 0xffffffffffffffffULL;
        *v_out++ = *v_in++ ^ mask;
        mask &= 0xffffffffULL;
        *v_out++ = *v_in++ ^ mask;
    }
}

/// @endcond  



/// @cond DO_NOT_DOCUMENT 

/**
  @brief Auxiliary function for function ``mm_op15_t``

  Parameters ``v_in`` and ``v_out``are as in function ``mm_op15_t``.
  This function performs the action of that function for the 
  tags ``A, B, C``.  Parameter ``exp1`` should be 0 or -1 if the
  actual exponent ``exp`` in function ``mm_op15_t`` is 1 or 2, 
  respectively. This function should not be called in 
  case ``exp = 0``.
*/
static inline void 
op15_t_ABC(uint_mmv_t *v_in,  uint_mmv_t exp1, uint_mmv_t *v_out)
{
    uint_mmv_t i, j;

    for (i = 0; i < 24; ++i) {
        // Compute index of diagonal element
        uint_mmv_t i_diag = i >> 4;
        // Compute mask for diagonal element
        uint_mmv_t m_diag = 0xfULL << ((i << 2) & 63);
        // Load shifted value of diagonal element of part A to ``v_diag``
        uint_mmv_t v_diag = v_in[i_diag] & m_diag;
 
        // Do off-diagonal part of tags A, B, C
        for (j = 0; j < 2; ++j) {
            // %%MUL_MATRIX_T3 v_in, exp1, v_out

            // This is an automatically generated matrix operation, do not change!
            {
            uint_mmv_t r0, r1, r2, r3, r4;
            uint_mmv_t r5, r6;

            // Multiply the vector of integers mod 15 stored in
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
            r1 = (v_in)[48];
            r2 = (v_in)[96] ^ ((exp1) & 0xffffffffffffffffULL);
            // Vector is now  r(i) for i = 0,1,2,3,4,5
            exp1 = ~(exp1);
            r3 = ((r0 >> 4) & 0xf0f0f0f0f0f0f0fULL); // 2 ops
            r0 = (r0 & 0xf0f0f0f0f0f0f0fULL);
            r4 = ((r1 >> 4) & 0xf0f0f0f0f0f0f0fULL); // 2 ops
            r1 = (r1 & 0xf0f0f0f0f0f0f0fULL);
            r5 = ((r2 >> 4) & 0xf0f0f0f0f0f0f0fULL); // 2 ops
            r2 = (r2 & 0xf0f0f0f0f0f0f0fULL);
            r6 = (r4 + (r5 ^ 0xf0f0f0f0f0f0f0fULL)); // 2 ops
            r4 = (r4 + r5);
            r5 = (r6 & 0x1010101010101010ULL);
            r5 = ((r6 - r5) + (r5 >> 4)); // 3 ops
            r6 = (r4 & 0x1010101010101010ULL);
            r4 = ((r4 - r6) + (r6 >> 4)); // 3 ops
            r4 = (((r4 & 0x1111111111111111ULL) << 3)
                | ((r4 & 0xeeeeeeeeeeeeeeeeULL) >> 1)); // 5 ops
            r5 = (((r5 & 0x1111111111111111ULL) << 3)
                | ((r5 & 0xeeeeeeeeeeeeeeeeULL) >> 1)); // 5 ops
            r6 = (r3 + (r5 ^ 0xf0f0f0f0f0f0f0fULL)); // 2 ops
            r3 = (r3 + r5);
            r5 = (r6 & 0x1010101010101010ULL);
            r5 = ((r6 - r5) + (r5 >> 4)); // 3 ops
            r6 = (r3 & 0x1010101010101010ULL);
            r3 = ((r3 - r6) + (r6 >> 4)); // 3 ops
            r6 = (r1 + (r2 ^ 0xf0f0f0f0f0f0f0fULL)); // 2 ops
            r1 = (r1 + r2);
            r2 = (r6 & 0x1010101010101010ULL);
            r2 = ((r6 - r2) + (r2 >> 4)); // 3 ops
            r6 = (r1 & 0x1010101010101010ULL);
            r1 = ((r1 - r6) + (r6 >> 4)); // 3 ops
            r1 = (((r1 & 0x1111111111111111ULL) << 3)
                | ((r1 & 0xeeeeeeeeeeeeeeeeULL) >> 1)); // 5 ops
            r2 = (((r2 & 0x1111111111111111ULL) << 3)
                | ((r2 & 0xeeeeeeeeeeeeeeeeULL) >> 1)); // 5 ops
            r6 = (r0 + (r2 ^ 0xf0f0f0f0f0f0f0fULL)); // 2 ops
            r0 = (r0 + r2);
            r2 = (r6 & 0x1010101010101010ULL);
            r2 = ((r6 - r2) + (r2 >> 4)); // 3 ops
            r6 = (r0 & 0x1010101010101010ULL);
            r0 = ((r0 - r6) + (r6 >> 4)); // 3 ops
            r0 ^= (r3 << 4); // 2 ops
            r1 ^= (r4 << 4); // 2 ops
            r2 ^= (r5 << 4); // 2 ops
            // Store vector v[0...2] to rep 196884x with 
            // tags A,B,C. Here v_out refers to the tag A part. 
            // Negate v[2] if exp1 == -1.
            (v_out)[0] = r1;
            (v_out)[48] = r0;
            (v_out)[96]  = r2 ^ ((exp1) & 0xffffffffffffffffULL);
            exp1 = ~(exp1);
            // 45 lines of code, 85 operations
            }
            // End of automatically generated matrix operation.
 
            // Advance pointers to input and output
            ++v_in; ++v_out;
        }
        // Zero slack
        v_out[-1] &= 0xffffffffULL;
        v_out[47] &= 0xffffffffULL;
        v_out[95] &= 0xffffffffULL;  
        // Restore diagonal element of part A 
        v_out -= 2; // Same position as at start of loop
        m_diag = ~m_diag;          // Mask for non-diagonal part
        v_out[i_diag] = (v_out[i_diag] & m_diag) | v_diag;
        // Zero diagonal elements of parts B and C 
        v_out[i_diag + 48] &= m_diag;
        v_out[i_diag + 96] &= m_diag;
        // Advance pointer to output
        v_out +=  2;
    }
}

/**
  @brief Simplified version of function ``op15_t_ABC``

  Same as function ``op15_t_ABC``; but here we only compute
  the ``A`` part of the output vector.
*/
static inline void 
op15_t_A(uint_mmv_t *v_in,  uint_mmv_t exp1, uint_mmv_t *v_out)
{
    uint_mmv_t i, j;

    for (i = 0; i < 24; ++i) {
        // Compute index of diagonal element
        uint_mmv_t i_diag = i >> 4;
        // Compute mask for diagonal element
        uint_mmv_t m_diag = 0xfULL << ((i << 2) & 63);
        // Load shifted value of diagonal element of part A to ``v_diag``
        uint_mmv_t v_diag = v_in[i_diag] & m_diag;
 
        // Do off-diagonal part of tags A, B, C
        for (j = 0; j < 2; ++j) {
            // %%MUL_MATRIX_T3A v_in, exp1, v_out

            // This is an automatically generated matrix operation, do not change!
            {
            uint_mmv_t r0, r1, r2, r3, r4;

            // Put dest_A =  (src_B + mask * src_C) / 2   (mod 15)
            // 
            // Here src_B and src_C are the part of a vector of integers 
            // mod 15 stored in (v_in) with tag B and C, and dest_A is 
            // the part of a vector of integers mod 15 stored in (v_out),  
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
            r0 = (v_in)[48];
            r1 = (v_in)[96] ^ ((exp1) & 0xffffffffffffffffULL);
            // Vector is now  r(i) for i = 0,1,2,3
            r2 = ((r0 >> 4) & 0xf0f0f0f0f0f0f0fULL); // 2 ops
            r0 = (r0 & 0xf0f0f0f0f0f0f0fULL);
            r3 = ((r1 >> 4) & 0xf0f0f0f0f0f0f0fULL); // 2 ops
            r1 = (r1 & 0xf0f0f0f0f0f0f0fULL);
            r2 = (r2 + r3);
            r4 = (r2 & 0x1010101010101010ULL);
            r2 = ((r2 - r4) + (r4 >> 4)); // 3 ops
            r0 = (r0 + r1);
            r4 = (r0 & 0x1010101010101010ULL);
            r0 = ((r0 - r4) + (r4 >> 4)); // 3 ops
            r0 ^= (r2 << 4); // 2 ops
            r0 = (((r0 & 0x1111111111111111ULL) << 3)
                | ((r0 & 0xeeeeeeeeeeeeeeeeULL) >> 1)); // 5 ops
            // Store vector v[0] to rep 196884x with 
            // tags A. Here v_out refers to the tag A part. 
            (v_out)[0] = r0;
            // 15 lines of code, 25 operations
            }
            // End of automatically generated matrix operation.
 
            // Advance pointers to input and output
            ++v_in; ++v_out;
        }
        // Zero slack
        v_out[-1] &= 0xffffffffULL;
        // Restore diagonal element of part A 
        v_out -= 2; // Same position as at start of loop
        m_diag = ~m_diag;          // Mask for non-diagonal part
        v_out[i_diag] = (v_out[i_diag] & m_diag) | v_diag;
        // Advance pointer to output
        v_out +=  2;
    }
}


/// @endcond 



/**
  @brief Compute an operation of the monster group on a vector

  Let ``v_in`` be a vector of the representation \f$\rho_{15}\f$
  of the monster group.

  The function implements the operation of the element \f$\tau^e\f$
  of the monster group  on a vector ``v_in`` in the
  representation \f$\rho_{15}\f$ of the monster.

  Parameter ``exp`` is the exponent \f$e\f$ of the generator
  \f$\tau^e\f$. The function computes the operation of \f$\tau^e\f$
  on the input  vector ``v_in`` and  stores the result in the output
  vector ``v_out``.

  Input vector ``v_in`` is not changed.
*/
// %%EXPORT px
MM_OP15_API
void mm_op15_t(uint_mmv_t *v_in,  uint32_t exp, uint_mmv_t *v_out)
{
    uint_mmv_t i, exp1;
 
    exp %= 3;
    if (exp == 0) {
        for (i = 0; i < 15468; ++i) v_out[i] = v_in[i];
        return;
    }
    exp1 = 0x1ULL - (uint_mmv_t)exp;

    // Do tags A, B, C
    op15_t_ABC(v_in, exp1, v_out);

    // Do tag T
    v_in += MM_OP15_OFS_T;
    v_out +=  MM_OP15_OFS_T;
    for (i = 0; i < 759; ++i) {
        // %%MUL_MATRIX_T64 v_in, exp1, v_out

        // This is an automatically generated matrix operation, do not change!
        {
        uint_mmv_t r0, r1, r2, r3, r4;
        uint_mmv_t r5, r6, r7, r8;

        // Multiply the vector of integers mod 15 stored
        // in (v_in) by t**e, where t is the 64 times 64 
        // triality matrix and e = 1 if exp1 = 0, e = 2 if
        // exp1 = (uint_mmv_t)(-1). The result is stored
        // in (v_out).
        // 
        // Loading vector v from array v_in; multiply v
        // with diagonal matrix if exp1 == -1.
        r0 = v_in[0] ^ ((exp1) & 0xf0fff0ffffff0ULL);
        r1 = v_in[1] ^ ((exp1) & 0xf000000f000f0fffULL);
        r2 = v_in[2] ^ ((exp1) & 0xf000000f000f0fffULL);
        r3 = v_in[3] ^ ((exp1) & 0xfff0f000f000000fULL);
        // Vector is now  r(i) for i = 0,1,2,3
        exp1 = ~(exp1);
        // Exchange component i with component 63-i if i 
        // has odd parity; fix it if i has even parity.
        r4 = ((r0 & 0xff0f00ff00f0ff0ULL)
            | (r1 & 0xf00f0ff00ff0f00fULL)); // 3 ops
        r4 = ((r4 << 32) | (r4 >> 32)); // 3 ops
        r4 = (((r4 & 0xffff0000ffffULL) << 16)
            | ((r4 >> 16) & 0xffff0000ffffULL)); // 5 ops
        r4 = (((r4 & 0xff00ff00ff00ffULL) << 8)
            | ((r4 >> 8) & 0xff00ff00ff00ffULL)); // 5 ops
        r4 = (((r4 & 0xf0f0f0f0f0f0f0fULL) << 4)
            | ((r4 >> 4) & 0xf0f0f0f0f0f0f0fULL)); // 5 ops
        r5 = ((r2 & 0xf00f0ff00ff0f00fULL)
            | (r3 & 0xff0f00ff00f0ff0ULL)); // 3 ops
        r5 = ((r5 << 32) | (r5 >> 32)); // 3 ops
        r5 = (((r5 & 0xffff0000ffffULL) << 16)
            | ((r5 >> 16) & 0xffff0000ffffULL)); // 5 ops
        r5 = (((r5 & 0xff00ff00ff00ffULL) << 8)
            | ((r5 >> 8) & 0xff00ff00ff00ffULL)); // 5 ops
        r5 = (((r5 & 0xf0f0f0f0f0f0f0fULL) << 4)
            | ((r5 >> 4) & 0xf0f0f0f0f0f0f0fULL)); // 5 ops
        r0 = ((r0 & 0xf00f0ff00ff0f00fULL)
            | (r5 & 0xff0f00ff00f0ff0ULL)); // 3 ops
        r1 = ((r1 & 0xff0f00ff00f0ff0ULL)
            | (r5 & 0xf00f0ff00ff0f00fULL)); // 3 ops
        r2 = ((r2 & 0xff0f00ff00f0ff0ULL)
            | (r4 & 0xf00f0ff00ff0f00fULL)); // 3 ops
        r3 = ((r3 & 0xf00f0ff00ff0f00fULL)
            | (r4 & 0xff0f00ff00f0ff0ULL)); // 3 ops
        // Expansion for Hadamard operation:
        // There is no space for a carry bit between bit fields. So 
        // we move bit field 2*i + 1  to bit field 2*i + 64.
        r4 = ((r0 >> 4) & 0xf0f0f0f0f0f0f0fULL); // 2 ops
        r0 = (r0 & 0xf0f0f0f0f0f0f0fULL);
        r5 = ((r1 >> 4) & 0xf0f0f0f0f0f0f0fULL); // 2 ops
        r1 = (r1 & 0xf0f0f0f0f0f0f0fULL);
        r6 = ((r2 >> 4) & 0xf0f0f0f0f0f0f0fULL); // 2 ops
        r2 = (r2 & 0xf0f0f0f0f0f0f0fULL);
        r7 = ((r3 >> 4) & 0xf0f0f0f0f0f0f0fULL); // 2 ops
        r3 = (r3 & 0xf0f0f0f0f0f0f0fULL);
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        // Butterfly: v[i], v[i+2] = v[i]+v[i+2], v[i]-v[i+2]
        r8 = (((r0 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r0 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r0 = ((r0 ^ 0xf000f000f000f00ULL) + r8); // 2 ops
        r8 = (((r1 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r1 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r1 = ((r1 ^ 0xf000f000f000f00ULL) + r8); // 2 ops
        r8 = (((r2 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r2 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r2 = ((r2 ^ 0xf000f000f000f00ULL) + r8); // 2 ops
        r8 = (((r3 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r3 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r3 = ((r3 ^ 0xf000f000f000f00ULL) + r8); // 2 ops
        r8 = (((r4 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r4 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r4 = ((r4 ^ 0xf000f000f000f00ULL) + r8); // 2 ops
        r8 = (((r5 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r5 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r5 = ((r5 ^ 0xf000f000f000f00ULL) + r8); // 2 ops
        r8 = (((r6 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r6 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r6 = ((r6 ^ 0xf000f000f000f00ULL) + r8); // 2 ops
        r8 = (((r7 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r7 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r7 = ((r7 ^ 0xf000f000f000f00ULL) + r8); // 2 ops
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        // Butterfly: v[i], v[i+4] = v[i]+v[i+4], v[i]-v[i+4]
        r8 = (((r0 << 16) & 0xffff0000ffff0000ULL)
            | ((r0 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r0 = ((r0 ^ 0x1f1f00001f1f0000ULL) + r8); // 2 ops
        r8 = (((r1 << 16) & 0xffff0000ffff0000ULL)
            | ((r1 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r1 = ((r1 ^ 0x1f1f00001f1f0000ULL) + r8); // 2 ops
        r8 = (((r2 << 16) & 0xffff0000ffff0000ULL)
            | ((r2 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r2 = ((r2 ^ 0x1f1f00001f1f0000ULL) + r8); // 2 ops
        r8 = (((r3 << 16) & 0xffff0000ffff0000ULL)
            | ((r3 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r3 = ((r3 ^ 0x1f1f00001f1f0000ULL) + r8); // 2 ops
        r8 = (((r4 << 16) & 0xffff0000ffff0000ULL)
            | ((r4 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r4 = ((r4 ^ 0x1f1f00001f1f0000ULL) + r8); // 2 ops
        r8 = (((r5 << 16) & 0xffff0000ffff0000ULL)
            | ((r5 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r5 = ((r5 ^ 0x1f1f00001f1f0000ULL) + r8); // 2 ops
        r8 = (((r6 << 16) & 0xffff0000ffff0000ULL)
            | ((r6 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r6 = ((r6 ^ 0x1f1f00001f1f0000ULL) + r8); // 2 ops
        r8 = (((r7 << 16) & 0xffff0000ffff0000ULL)
            | ((r7 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r7 = ((r7 ^ 0x1f1f00001f1f0000ULL) + r8); // 2 ops
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        // Butterfly: v[i], v[i+8] = v[i]+v[i+8], v[i]-v[i+8]
        r8 = ((r0 << 32) | (r0 >> 32)); // 3 ops
        r0 = ((r0 ^ 0x3f3f3f3f00000000ULL) + r8); // 2 ops
        r8 = ((r1 << 32) | (r1 >> 32)); // 3 ops
        r1 = ((r1 ^ 0x3f3f3f3f00000000ULL) + r8); // 2 ops
        r8 = ((r2 << 32) | (r2 >> 32)); // 3 ops
        r2 = ((r2 ^ 0x3f3f3f3f00000000ULL) + r8); // 2 ops
        r8 = ((r3 << 32) | (r3 >> 32)); // 3 ops
        r3 = ((r3 ^ 0x3f3f3f3f00000000ULL) + r8); // 2 ops
        r8 = ((r4 << 32) | (r4 >> 32)); // 3 ops
        r4 = ((r4 ^ 0x3f3f3f3f00000000ULL) + r8); // 2 ops
        r8 = ((r5 << 32) | (r5 >> 32)); // 3 ops
        r5 = ((r5 ^ 0x3f3f3f3f00000000ULL) + r8); // 2 ops
        r8 = ((r6 << 32) | (r6 >> 32)); // 3 ops
        r6 = ((r6 ^ 0x3f3f3f3f00000000ULL) + r8); // 2 ops
        r8 = ((r7 << 32) | (r7 >> 32)); // 3 ops
        r7 = ((r7 ^ 0x3f3f3f3f00000000ULL) + r8); // 2 ops
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        // Butterfly: v[i], v[i+16] = v[i]+v[i+16], v[i]-v[i+16]
        r8 = (r0 + (r1 ^ 0x7f7f7f7f7f7f7f7fULL)); // 2 ops
        r0 = (r0 + r1);
        r8 = (r8 - 0x707070707070707ULL);
        r1 = ((r8 & 0xf0f0f0f0f0f0f0fULL)
            + ((r8 >> 4) & 0xf0f0f0f0f0f0f0fULL)); // 4 ops
        r0 = (r0 - 0x606060604040000ULL);
        r0 = ((r0 & 0xf0f0f0f0f0f0f0fULL)
            + ((r0 >> 4) & 0xf0f0f0f0f0f0f0fULL)); // 4 ops
        r8 = (r2 + (r3 ^ 0x7f7f7f7f7f7f7f7fULL)); // 2 ops
        r2 = (r2 + r3);
        r8 = (r8 - 0x707070707070707ULL);
        r3 = ((r8 & 0xf0f0f0f0f0f0f0fULL)
            + ((r8 >> 4) & 0xf0f0f0f0f0f0f0fULL)); // 4 ops
        r2 = (r2 - 0x606060604040000ULL);
        r2 = ((r2 & 0xf0f0f0f0f0f0f0fULL)
            + ((r2 >> 4) & 0xf0f0f0f0f0f0f0fULL)); // 4 ops
        r8 = (r4 + (r5 ^ 0x7f7f7f7f7f7f7f7fULL)); // 2 ops
        r4 = (r4 + r5);
        r8 = (r8 - 0x707070707070707ULL);
        r5 = ((r8 & 0xf0f0f0f0f0f0f0fULL)
            + ((r8 >> 4) & 0xf0f0f0f0f0f0f0fULL)); // 4 ops
        r4 = (r4 - 0x606060604040000ULL);
        r4 = ((r4 & 0xf0f0f0f0f0f0f0fULL)
            + ((r4 >> 4) & 0xf0f0f0f0f0f0f0fULL)); // 4 ops
        r8 = (r6 + (r7 ^ 0x7f7f7f7f7f7f7f7fULL)); // 2 ops
        r6 = (r6 + r7);
        r8 = (r8 - 0x707070707070707ULL);
        r7 = ((r8 & 0xf0f0f0f0f0f0f0fULL)
            + ((r8 >> 4) & 0xf0f0f0f0f0f0f0fULL)); // 4 ops
        r6 = (r6 - 0x606060604040000ULL);
        r6 = ((r6 & 0xf0f0f0f0f0f0f0fULL)
            + ((r6 >> 4) & 0xf0f0f0f0f0f0f0fULL)); // 4 ops
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        // Butterfly: v[i], v[i+32] = v[i]+v[i+32], v[i]-v[i+32]
        r8 = (r0 + (r2 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r0 = (r0 + r2);
        r2 = r8;
        r8 = (r1 + (r3 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r1 = (r1 + r3);
        r3 = r8;
        r8 = (r4 + (r6 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r4 = (r4 + r6);
        r6 = r8;
        r8 = (r5 + (r7 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r5 = (r5 + r7);
        r7 = r8;
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        // Butterfly: v[i], v[i+64] = v[i]+v[i+64], v[i]-v[i+64]
        r8 = (r0 + (r4 ^ 0x3f3f3f3f3f3f3f3fULL)); // 2 ops
        r0 = (r0 + r4);
        r4 = r8;
        r8 = (r1 + (r5 ^ 0x3f3f3f3f3f3f3f3fULL)); // 2 ops
        r1 = (r1 + r5);
        r5 = r8;
        r8 = (r2 + (r6 ^ 0x3f3f3f3f3f3f3f3fULL)); // 2 ops
        r2 = (r2 + r6);
        r6 = r8;
        r8 = (r3 + (r7 ^ 0x3f3f3f3f3f3f3f3fULL)); // 2 ops
        r3 = (r3 + r7);
        r7 = r8;
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        // Multiply vector by scalar 2**-3 mod 15
        r0 = (r0 << 1);
        r1 = (r1 << 1);
        r2 = (r2 << 1);
        r3 = (r3 << 1);
        r4 = (r4 << 1);
        r5 = (r5 << 1);
        r6 = (r6 << 1);
        r7 = (r7 << 1);
        // Final reduction
        r0 = ((r0 & 0xf0f0f0f0f0f0f0fULL)
            + ((r0 >> 4) & 0xf0f0f0f0f0f0f0fULL)); // 4 ops
        r8 = (r0 & 0x1010101010101010ULL);
        r0 = ((r0 - r8) + (r8 >> 4)); // 3 ops
        r1 = ((r1 & 0xf0f0f0f0f0f0f0fULL)
            + ((r1 >> 4) & 0xf0f0f0f0f0f0f0fULL)); // 4 ops
        r8 = (r1 & 0x1010101010101010ULL);
        r1 = ((r1 - r8) + (r8 >> 4)); // 3 ops
        r2 = (r2 - 0x404040404040404ULL);
        r2 = ((r2 & 0xf0f0f0f0f0f0f0fULL)
            + ((r2 >> 4) & 0xf0f0f0f0f0f0f0fULL)); // 4 ops
        r8 = (r2 & 0x1010101010101010ULL);
        r2 = ((r2 - r8) + (r8 >> 4)); // 3 ops
        r3 = (r3 - 0x404040404040404ULL);
        r3 = ((r3 & 0xf0f0f0f0f0f0f0fULL)
            + ((r3 >> 4) & 0xf0f0f0f0f0f0f0fULL)); // 4 ops
        r8 = (r3 & 0x1010101010101010ULL);
        r3 = ((r3 - r8) + (r8 >> 4)); // 3 ops
        r4 = (r4 - 0x606060606060606ULL);
        r4 = ((r4 & 0xf0f0f0f0f0f0f0fULL)
            + ((r4 >> 4) & 0xf0f0f0f0f0f0f0fULL)); // 4 ops
        r8 = (r4 & 0x1010101010101010ULL);
        r4 = ((r4 - r8) + (r8 >> 4)); // 3 ops
        r5 = (r5 - 0x606060606060606ULL);
        r5 = ((r5 & 0xf0f0f0f0f0f0f0fULL)
            + ((r5 >> 4) & 0xf0f0f0f0f0f0f0fULL)); // 4 ops
        r8 = (r5 & 0x1010101010101010ULL);
        r5 = ((r5 - r8) + (r8 >> 4)); // 3 ops
        r6 = (r6 - 0x606060606060606ULL);
        r6 = ((r6 & 0xf0f0f0f0f0f0f0fULL)
            + ((r6 >> 4) & 0xf0f0f0f0f0f0f0fULL)); // 4 ops
        r8 = (r6 & 0x1010101010101010ULL);
        r6 = ((r6 - r8) + (r8 >> 4)); // 3 ops
        r7 = (r7 - 0x606060606060606ULL);
        r7 = ((r7 & 0xf0f0f0f0f0f0f0fULL)
            + ((r7 >> 4) & 0xf0f0f0f0f0f0f0fULL)); // 4 ops
        r8 = (r7 & 0x1010101010101010ULL);
        r7 = ((r7 - r8) + (r8 >> 4)); // 3 ops
        // Reverse expansion for Hadamard operation
        r0 ^= (r4 << 4); // 2 ops
        r1 ^= (r5 << 4); // 2 ops
        r2 ^= (r6 << 4); // 2 ops
        r3 ^= (r7 << 4); // 2 ops
        // Vector is now  r(i) for i = 0,1,2,3
        // Storing vector v to array v_out; multiply v
        // with diagonal matrix if exp1 == -1.
        v_out[0] = r0 ^ ((exp1) & 0xf0fff0ffffff0ULL);
        v_out[1] = r1 ^ ((exp1) & 0xf000000f000f0fffULL);
        v_out[2] = r2 ^ ((exp1) & 0xf000000f000f0fffULL);
        v_out[3] = r3 ^ ((exp1) & 0xfff0f000f000000fULL);
        exp1 = ~(exp1);
        // 170 lines of code, 398 operations
        }
        // End of automatically generated matrix operation.
 
        v_in += 4;
        v_out += 4;
    }

    // Do tags X, Y, and Z
    {
         uint_mmv_t *pXYin, *pYZin, *pZXin;
         uint_mmv_t *pXYout, *pYZout, *pZXout;
         if (exp1 == 0) {
             pXYin = v_in; 
             pXYout = v_out + 8192;  
             pYZin = v_in + 8192; 
             pYZout = v_out + 4096;  
             pZXin = v_in + 4096; 
             pZXout = v_out; 
         } else {
             pXYout = v_out; 
             pXYin = v_in + 8192;  
             pYZout = v_out + 8192; 
             pYZin = v_in + 4096;  
             pZXout = v_out + 4096; 
             pZXin = v_in; 
         }

         // Map X to Y for t and Y to X for t**2
         for (i = 0; i < 4096; ++i) pXYout[i] = pXYin[i];
         mm_op15_neg_scalprod_d_i(pXYout);
         
         // Map Y to Z for t and Z to Y for t**2
         invert15_xyz(pYZin, pYZout);
         mm_op15_neg_scalprod_d_i(pYZout);

         // Map Z to X for t and X to Z for t**2
         invert15_xyz(pZXin, pZXout);
    }
}



/**
  @brief A restricted version of function ``mm_op15_t``

  Function ``mm_op15_t`` computes a certain operation of the
  monster group on a vector ``v_in`` and stores the result in a
  vector ``v_out``. That operation depends on a parameter ``exp``.
  
  Function ``mm_op15_t_A`` performs the same operation, but it
  computes the part of the vector  ``v_out``  that consists of
  the entries of vector ``v_out``  with tag ``A`` only; the
  other entries of vector ``v_out`` are not changed.
  See section **The representation of the monster group**
  in the **API reference** for tags of entries of a vector in
  the representation of the monster. Note that the entries
  of vector ``v_out`` with tag ``A`` also depend on entries
  of vector ``v_in`` with tags different from ``A``.

  Parameters of this function are the same as in the case of
  function ``mm_op15_t``. This function is much faster than
  function ``mm_op15_t``.
*/
// %%EXPORT px
MM_OP15_API
void mm_op15_t_A(uint_mmv_t *v_in,  uint32_t exp, uint_mmv_t *v_out)
{
    uint_mmv_t i, exp1;
 
    exp %= 3;
    if (exp == 0) {
        for (i = 0; i < 48; ++i) v_out[i] = v_in[i];
        return;
    }
    exp1 = 0x1ULL - (uint_mmv_t)exp;
    op15_t_A(v_in, exp1, v_out);
}



/**
  @brief Another restricted version of function ``mm_op15_t``

  Function ``mm_op15_t`` computes a certain operation of the
  monster group on a vector ``v_in`` and stores the result in a
  vector ``v_out``. That operation depends on a parameter ``exp``.
  
  Function ``mm_op15_t_ABC`` computes the same
  operation on the entries of the vector ``v = v_in`` with
  tag ``A, B, C`` only, and ignores the other entries of ``v``.
  See section **The representation of the monster group**
  in the **API reference** for tags of entries of a vector in
  the representation of the monster.

  The function overwrites the vector ``v`` with the result.
  Here only entries of ``v`` with tag ``A, B, C`` are changed. 
  This function is much faster than  function ``mm_op15_t``.
*/
// %%EXPORT px
MM_OP15_API
void mm_op15_t_ABC(uint_mmv_t *v,  uint32_t exp)
{
    uint_mmv_t  exp1;
 
    exp %= 3;
    if (exp == 0) return;
    exp1 = 0x1ULL - (uint_mmv_t)exp;
    op15_t_ABC(v, exp1, v);
}





//  %%GEN h
//  %%GEN c


