/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm255_op_t.c

 File ``mm255_op_t.c`` implements the operation of the element
 \f$\tau^e\f$ of the monster group on a vector in the
 representation \f$\rho_{255}\f$ of the monster.

 Here the generator \f$\tau\f$, which is the triality element in
 the monster group, is defined as in section **The monster group**
 of the **API reference**.

 The representation \f$\rho_{255}\f$ is equal to the
 196884-dimensional representation  \f$\rho\f$ of the monster,
 with coefficients taken modulo 255, as defined in
 section **The representation of the monster group**
 in the **API reference**.

 An element of \f$\rho_{255}\f$ is implemented as an array of
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
#include "mm_op255.h"   

// %%EXPORT_KWD MM_OP%{P}_API


//  %%GEN h
//  %%GEN c


/// @cond DO_NOT_DOCUMENT 


static void invert255_xyz(uint_mmv_t *v_in, uint_mmv_t *v_out)
{
    uint_fast32_t i;
    const uint16_t *p_theta = MAT24_THETA_TABLE;
    
    for (i = 0; i <2048; ++i) {
        uint_mmv_t mask = 0 - ((uint_mmv_t)(((p_theta[i] >> 12) & 0x1ULL)));
        mask &= 0xffffffffffffffffULL;
        *v_out++ = *v_in++ ^ mask;
        *v_out++ = *v_in++ ^ mask;
        *v_out++ = *v_in++ ^ mask;
        *v_out++ = 0;
        ++v_in;
    }
}

/// @endcond  



/// @cond DO_NOT_DOCUMENT 

/**
  @brief Auxiliary function for function ``mm_op255_t``

  Parameters ``v_in`` and ``v_out``are as in function ``mm_op255_t``.
  This function performs the action of that function for the 
  tags ``A, B, C``.  Parameter ``exp1`` should be 0 or -1 if the
  actual exponent ``exp`` in function ``mm_op255_t`` is 1 or 2, 
  respectively. This function should not be called in 
  case ``exp = 0``.
*/
static inline void 
op255_t_ABC(uint_mmv_t *v_in,  uint_mmv_t exp1, uint_mmv_t *v_out)
{
    uint_mmv_t i, j;

    for (i = 0; i < 24; ++i) {
        // Compute index of diagonal element
        uint_mmv_t i_diag = i >> 3;
        // Compute mask for diagonal element
        uint_mmv_t m_diag = 0xffULL << ((i << 3) & 63);
        // Load shifted value of diagonal element of part A to ``v_diag``
        uint_mmv_t v_diag = v_in[i_diag] & m_diag;
 
        // Do off-diagonal part of tags A, B, C
        for (j = 0; j < 3; ++j) {
            // %%MUL_MATRIX_T3 v_in, exp1, v_out

            // This is an automatically generated matrix operation, do not change!
            {
            uint_mmv_t r0, r1, r2, r3, r4;
            uint_mmv_t r5, r6;

            // Multiply the vector of integers mod 255 stored in
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
            r1 = (v_in)[96];
            r2 = (v_in)[192] ^ ((exp1) & 0xffffffffffffffffULL);
            // Vector is now  r(i) for i = 0,1,2,3,4,5
            exp1 = ~(exp1);
            r3 = ((r0 >> 8) & 0xff00ff00ff00ffULL); // 2 ops
            r0 = (r0 & 0xff00ff00ff00ffULL);
            r4 = ((r1 >> 8) & 0xff00ff00ff00ffULL); // 2 ops
            r1 = (r1 & 0xff00ff00ff00ffULL);
            r5 = ((r2 >> 8) & 0xff00ff00ff00ffULL); // 2 ops
            r2 = (r2 & 0xff00ff00ff00ffULL);
            r6 = (r4 + (r5 ^ 0xff00ff00ff00ffULL)); // 2 ops
            r4 = (r4 + r5);
            r5 = (r6 & 0x100010001000100ULL);
            r5 = ((r6 - r5) + (r5 >> 8)); // 3 ops
            r6 = (r4 & 0x100010001000100ULL);
            r4 = ((r4 - r6) + (r6 >> 8)); // 3 ops
            r4 = (((r4 & 0x101010101010101ULL) << 7)
                | ((r4 & 0xfefefefefefefefeULL) >> 1)); // 5 ops
            r5 = (((r5 & 0x101010101010101ULL) << 7)
                | ((r5 & 0xfefefefefefefefeULL) >> 1)); // 5 ops
            r6 = (r3 + (r5 ^ 0xff00ff00ff00ffULL)); // 2 ops
            r3 = (r3 + r5);
            r5 = (r6 & 0x100010001000100ULL);
            r5 = ((r6 - r5) + (r5 >> 8)); // 3 ops
            r6 = (r3 & 0x100010001000100ULL);
            r3 = ((r3 - r6) + (r6 >> 8)); // 3 ops
            r6 = (r1 + (r2 ^ 0xff00ff00ff00ffULL)); // 2 ops
            r1 = (r1 + r2);
            r2 = (r6 & 0x100010001000100ULL);
            r2 = ((r6 - r2) + (r2 >> 8)); // 3 ops
            r6 = (r1 & 0x100010001000100ULL);
            r1 = ((r1 - r6) + (r6 >> 8)); // 3 ops
            r1 = (((r1 & 0x101010101010101ULL) << 7)
                | ((r1 & 0xfefefefefefefefeULL) >> 1)); // 5 ops
            r2 = (((r2 & 0x101010101010101ULL) << 7)
                | ((r2 & 0xfefefefefefefefeULL) >> 1)); // 5 ops
            r6 = (r0 + (r2 ^ 0xff00ff00ff00ffULL)); // 2 ops
            r0 = (r0 + r2);
            r2 = (r6 & 0x100010001000100ULL);
            r2 = ((r6 - r2) + (r2 >> 8)); // 3 ops
            r6 = (r0 & 0x100010001000100ULL);
            r0 = ((r0 - r6) + (r6 >> 8)); // 3 ops
            r0 ^= (r3 << 8); // 2 ops
            r1 ^= (r4 << 8); // 2 ops
            r2 ^= (r5 << 8); // 2 ops
            // Store vector v[0...2] to rep 196884x with 
            // tags A,B,C. Here v_out refers to the tag A part. 
            // Negate v[2] if exp1 == -1.
            (v_out)[0] = r1;
            (v_out)[96] = r0;
            (v_out)[192]  = r2 ^ ((exp1) & 0xffffffffffffffffULL);
            exp1 = ~(exp1);
            // 45 lines of code, 85 operations
            }
            // End of automatically generated matrix operation.
 
            // Advance pointers to input and output
            ++v_in; ++v_out;
        }
        // Zero slack
        v_out[0] = 0;
        v_out[96] = 0;
        v_out[192] = 0;
        // Advance pointer to input
        v_in += 1;
        // Restore diagonal element of part A 
        v_out -= 3; // Same position as at start of loop
        m_diag = ~m_diag;          // Mask for non-diagonal part
        v_out[i_diag] = (v_out[i_diag] & m_diag) | v_diag;
        // Zero diagonal elements of parts B and C 
        v_out[i_diag + 96] &= m_diag;
        v_out[i_diag + 192] &= m_diag;
        // Advance pointer to output
        v_out +=  4;
    }
}

/**
  @brief Simplified version of function ``op255_t_ABC``

  Same as function ``op255_t_ABC``; but here we only compute
  the ``A`` part of the output vector.
*/
static inline void 
op255_t_A(uint_mmv_t *v_in,  uint_mmv_t exp1, uint_mmv_t *v_out)
{
    uint_mmv_t i, j;

    for (i = 0; i < 24; ++i) {
        // Compute index of diagonal element
        uint_mmv_t i_diag = i >> 3;
        // Compute mask for diagonal element
        uint_mmv_t m_diag = 0xffULL << ((i << 3) & 63);
        // Load shifted value of diagonal element of part A to ``v_diag``
        uint_mmv_t v_diag = v_in[i_diag] & m_diag;
 
        // Do off-diagonal part of tags A, B, C
        for (j = 0; j < 3; ++j) {
            // %%MUL_MATRIX_T3A v_in, exp1, v_out

            // This is an automatically generated matrix operation, do not change!
            {
            uint_mmv_t r0, r1, r2, r3, r4;

            // Put dest_A =  (src_B + mask * src_C) / 2   (mod 255)
            // 
            // Here src_B and src_C are the part of a vector of integers 
            // mod 255 stored in (v_in) with tag B and C, and dest_A is 
            // the part of a vector of integers mod 255 stored in (v_out),  
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
            r0 = (v_in)[96];
            r1 = (v_in)[192] ^ ((exp1) & 0xffffffffffffffffULL);
            // Vector is now  r(i) for i = 0,1,2,3
            r2 = ((r0 >> 8) & 0xff00ff00ff00ffULL); // 2 ops
            r0 = (r0 & 0xff00ff00ff00ffULL);
            r3 = ((r1 >> 8) & 0xff00ff00ff00ffULL); // 2 ops
            r1 = (r1 & 0xff00ff00ff00ffULL);
            r2 = (r2 + r3);
            r4 = (r2 & 0x100010001000100ULL);
            r2 = ((r2 - r4) + (r4 >> 8)); // 3 ops
            r0 = (r0 + r1);
            r4 = (r0 & 0x100010001000100ULL);
            r0 = ((r0 - r4) + (r4 >> 8)); // 3 ops
            r0 ^= (r2 << 8); // 2 ops
            r0 = (((r0 & 0x101010101010101ULL) << 7)
                | ((r0 & 0xfefefefefefefefeULL) >> 1)); // 5 ops
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
        v_out[0] = 0;
        // Advance pointer to input
        v_in += 1;
        // Restore diagonal element of part A 
        v_out -= 3; // Same position as at start of loop
        m_diag = ~m_diag;          // Mask for non-diagonal part
        v_out[i_diag] = (v_out[i_diag] & m_diag) | v_diag;
        // Advance pointer to output
        v_out +=  4;
    }
}


/// @endcond 



/**
  @brief Compute an operation of the monster group on a vector

  Let ``v_in`` be a vector of the representation \f$\rho_{255}\f$
  of the monster group.

  The function implements the operation of the element \f$\tau^e\f$
  of the monster group  on a vector ``v_in`` in the
  representation \f$\rho_{255}\f$ of the monster.

  Parameter ``exp`` is the exponent \f$e\f$ of the generator
  \f$\tau^e\f$. The function computes the operation of \f$\tau^e\f$
  on the input  vector ``v_in`` and  stores the result in the output
  vector ``v_out``.

  Input vector ``v_in`` is not changed.
*/
// %%EXPORT px
MM_OP255_API
void mm_op255_t(uint_mmv_t *v_in,  uint32_t exp, uint_mmv_t *v_out)
{
    uint_mmv_t i, exp1;
 
    exp %= 3;
    if (exp == 0) {
        for (i = 0; i < 30936; ++i) v_out[i] = v_in[i];
        return;
    }
    exp1 = 0x1ULL - (uint_mmv_t)exp;

    // Do tags A, B, C
    op255_t_ABC(v_in, exp1, v_out);

    // Do tag T
    v_in += MM_OP255_OFS_T;
    v_out +=  MM_OP255_OFS_T;
    for (i = 0; i < 759; ++i) {
        // %%MUL_MATRIX_T64 v_in, exp1, v_out

        // This is an automatically generated matrix operation, do not change!
        {
        uint_mmv_t r0, r1, r2, r3, r4;
        uint_mmv_t r5, r6, r7, r8, r9;
        uint_mmv_t r10, r11, r12, r13, r14;
        uint_mmv_t r15, r16;

        // Multiply the vector of integers mod 255 stored
        // in (v_in) by t**e, where t is the 64 times 64 
        // triality matrix and e = 1 if exp1 = 0, e = 2 if
        // exp1 = (uint_mmv_t)(-1). The result is stored
        // in (v_out).
        // 
        // Loading vector v from array v_in; multiply v
        // with diagonal matrix if exp1 == -1.
        r0 = v_in[0] ^ ((exp1) & 0xffffffffffff00ULL);
        r1 = v_in[1] ^ ((exp1) & 0xff00ffffffULL);
        r2 = v_in[2] ^ ((exp1) & 0xff00ffffffULL);
        r3 = v_in[3] ^ ((exp1) & 0xff000000000000ffULL);
        r4 = v_in[4] ^ ((exp1) & 0xff00ffffffULL);
        r5 = v_in[5] ^ ((exp1) & 0xff000000000000ffULL);
        r6 = v_in[6] ^ ((exp1) & 0xff000000000000ffULL);
        r7 = v_in[7] ^ ((exp1) & 0xffffff00ff000000ULL);
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        exp1 = ~(exp1);
        // Exchange component i with component 63-i if i 
        // has odd parity; fix it if i has even parity.
        r8 = ((r0 & 0xff0000ff00ffff00ULL)
            | (r7 & 0xffff00ff0000ffULL)); // 3 ops
        r8 = ((r8 << 32) | (r8 >> 32)); // 3 ops
        r8 = (((r8 & 0xffff0000ffffULL) << 16)
            | ((r8 >> 16) & 0xffff0000ffffULL)); // 5 ops
        r8 = (((r8 & 0xff00ff00ff00ffULL) << 8)
            | ((r8 >> 8) & 0xff00ff00ff00ffULL)); // 5 ops
        r0 = ((r0 & 0xffff00ff0000ffULL)
            | (r8 & 0xff0000ff00ffff00ULL)); // 3 ops
        r7 = ((r7 & 0xff0000ff00ffff00ULL)
            | (r8 & 0xffff00ff0000ffULL)); // 3 ops
        r8 = ((r1 & 0xffff00ff0000ffULL)
            | (r6 & 0xff0000ff00ffff00ULL)); // 3 ops
        r8 = ((r8 << 32) | (r8 >> 32)); // 3 ops
        r8 = (((r8 & 0xffff0000ffffULL) << 16)
            | ((r8 >> 16) & 0xffff0000ffffULL)); // 5 ops
        r8 = (((r8 & 0xff00ff00ff00ffULL) << 8)
            | ((r8 >> 8) & 0xff00ff00ff00ffULL)); // 5 ops
        r1 = ((r1 & 0xff0000ff00ffff00ULL)
            | (r8 & 0xffff00ff0000ffULL)); // 3 ops
        r6 = ((r6 & 0xffff00ff0000ffULL)
            | (r8 & 0xff0000ff00ffff00ULL)); // 3 ops
        r8 = ((r2 & 0xffff00ff0000ffULL)
            | (r5 & 0xff0000ff00ffff00ULL)); // 3 ops
        r8 = ((r8 << 32) | (r8 >> 32)); // 3 ops
        r8 = (((r8 & 0xffff0000ffffULL) << 16)
            | ((r8 >> 16) & 0xffff0000ffffULL)); // 5 ops
        r8 = (((r8 & 0xff00ff00ff00ffULL) << 8)
            | ((r8 >> 8) & 0xff00ff00ff00ffULL)); // 5 ops
        r2 = ((r2 & 0xff0000ff00ffff00ULL)
            | (r8 & 0xffff00ff0000ffULL)); // 3 ops
        r5 = ((r5 & 0xffff00ff0000ffULL)
            | (r8 & 0xff0000ff00ffff00ULL)); // 3 ops
        r8 = ((r3 & 0xff0000ff00ffff00ULL)
            | (r4 & 0xffff00ff0000ffULL)); // 3 ops
        r8 = ((r8 << 32) | (r8 >> 32)); // 3 ops
        r8 = (((r8 & 0xffff0000ffffULL) << 16)
            | ((r8 >> 16) & 0xffff0000ffffULL)); // 5 ops
        r8 = (((r8 & 0xff00ff00ff00ffULL) << 8)
            | ((r8 >> 8) & 0xff00ff00ff00ffULL)); // 5 ops
        r3 = ((r3 & 0xffff00ff0000ffULL)
            | (r8 & 0xff0000ff00ffff00ULL)); // 3 ops
        r4 = ((r4 & 0xff0000ff00ffff00ULL)
            | (r8 & 0xffff00ff0000ffULL)); // 3 ops
        // Expansion for Hadamard operation:
        // There is no space for a carry bit between bit fields. So 
        // we move bit field 2*i + 1  to bit field 2*i + 64.
        r8 = ((r0 >> 8) & 0xff00ff00ff00ffULL); // 2 ops
        r0 = (r0 & 0xff00ff00ff00ffULL);
        r9 = ((r1 >> 8) & 0xff00ff00ff00ffULL); // 2 ops
        r1 = (r1 & 0xff00ff00ff00ffULL);
        r10 = ((r2 >> 8) & 0xff00ff00ff00ffULL); // 2 ops
        r2 = (r2 & 0xff00ff00ff00ffULL);
        r11 = ((r3 >> 8) & 0xff00ff00ff00ffULL); // 2 ops
        r3 = (r3 & 0xff00ff00ff00ffULL);
        r12 = ((r4 >> 8) & 0xff00ff00ff00ffULL); // 2 ops
        r4 = (r4 & 0xff00ff00ff00ffULL);
        r13 = ((r5 >> 8) & 0xff00ff00ff00ffULL); // 2 ops
        r5 = (r5 & 0xff00ff00ff00ffULL);
        r14 = ((r6 >> 8) & 0xff00ff00ff00ffULL); // 2 ops
        r6 = (r6 & 0xff00ff00ff00ffULL);
        r15 = ((r7 >> 8) & 0xff00ff00ff00ffULL); // 2 ops
        r7 = (r7 & 0xff00ff00ff00ffULL);
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+2] = v[i]+v[i+2], v[i]-v[i+2]
        r16 = (((r0 << 16) & 0xffff0000ffff0000ULL)
            | ((r0 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r0 = ((r0 ^ 0xff000000ff0000ULL) + r16); // 2 ops
        r16 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r16) + (r16 >> 8)); // 3 ops
        r16 = (((r1 << 16) & 0xffff0000ffff0000ULL)
            | ((r1 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r1 = ((r1 ^ 0xff000000ff0000ULL) + r16); // 2 ops
        r16 = (r1 & 0x100010001000100ULL);
        r1 = ((r1 - r16) + (r16 >> 8)); // 3 ops
        r16 = (((r2 << 16) & 0xffff0000ffff0000ULL)
            | ((r2 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r2 = ((r2 ^ 0xff000000ff0000ULL) + r16); // 2 ops
        r16 = (r2 & 0x100010001000100ULL);
        r2 = ((r2 - r16) + (r16 >> 8)); // 3 ops
        r16 = (((r3 << 16) & 0xffff0000ffff0000ULL)
            | ((r3 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r3 = ((r3 ^ 0xff000000ff0000ULL) + r16); // 2 ops
        r16 = (r3 & 0x100010001000100ULL);
        r3 = ((r3 - r16) + (r16 >> 8)); // 3 ops
        r16 = (((r4 << 16) & 0xffff0000ffff0000ULL)
            | ((r4 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r4 = ((r4 ^ 0xff000000ff0000ULL) + r16); // 2 ops
        r16 = (r4 & 0x100010001000100ULL);
        r4 = ((r4 - r16) + (r16 >> 8)); // 3 ops
        r16 = (((r5 << 16) & 0xffff0000ffff0000ULL)
            | ((r5 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r5 = ((r5 ^ 0xff000000ff0000ULL) + r16); // 2 ops
        r16 = (r5 & 0x100010001000100ULL);
        r5 = ((r5 - r16) + (r16 >> 8)); // 3 ops
        r16 = (((r6 << 16) & 0xffff0000ffff0000ULL)
            | ((r6 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r6 = ((r6 ^ 0xff000000ff0000ULL) + r16); // 2 ops
        r16 = (r6 & 0x100010001000100ULL);
        r6 = ((r6 - r16) + (r16 >> 8)); // 3 ops
        r16 = (((r7 << 16) & 0xffff0000ffff0000ULL)
            | ((r7 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r7 = ((r7 ^ 0xff000000ff0000ULL) + r16); // 2 ops
        r16 = (r7 & 0x100010001000100ULL);
        r7 = ((r7 - r16) + (r16 >> 8)); // 3 ops
        r16 = (((r8 << 16) & 0xffff0000ffff0000ULL)
            | ((r8 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r8 = ((r8 ^ 0xff000000ff0000ULL) + r16); // 2 ops
        r16 = (r8 & 0x100010001000100ULL);
        r8 = ((r8 - r16) + (r16 >> 8)); // 3 ops
        r16 = (((r9 << 16) & 0xffff0000ffff0000ULL)
            | ((r9 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r9 = ((r9 ^ 0xff000000ff0000ULL) + r16); // 2 ops
        r16 = (r9 & 0x100010001000100ULL);
        r9 = ((r9 - r16) + (r16 >> 8)); // 3 ops
        r16 = (((r10 << 16) & 0xffff0000ffff0000ULL)
            | ((r10 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r10 = ((r10 ^ 0xff000000ff0000ULL) + r16); // 2 ops
        r16 = (r10 & 0x100010001000100ULL);
        r10 = ((r10 - r16) + (r16 >> 8)); // 3 ops
        r16 = (((r11 << 16) & 0xffff0000ffff0000ULL)
            | ((r11 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r11 = ((r11 ^ 0xff000000ff0000ULL) + r16); // 2 ops
        r16 = (r11 & 0x100010001000100ULL);
        r11 = ((r11 - r16) + (r16 >> 8)); // 3 ops
        r16 = (((r12 << 16) & 0xffff0000ffff0000ULL)
            | ((r12 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r12 = ((r12 ^ 0xff000000ff0000ULL) + r16); // 2 ops
        r16 = (r12 & 0x100010001000100ULL);
        r12 = ((r12 - r16) + (r16 >> 8)); // 3 ops
        r16 = (((r13 << 16) & 0xffff0000ffff0000ULL)
            | ((r13 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r13 = ((r13 ^ 0xff000000ff0000ULL) + r16); // 2 ops
        r16 = (r13 & 0x100010001000100ULL);
        r13 = ((r13 - r16) + (r16 >> 8)); // 3 ops
        r16 = (((r14 << 16) & 0xffff0000ffff0000ULL)
            | ((r14 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r14 = ((r14 ^ 0xff000000ff0000ULL) + r16); // 2 ops
        r16 = (r14 & 0x100010001000100ULL);
        r14 = ((r14 - r16) + (r16 >> 8)); // 3 ops
        r16 = (((r15 << 16) & 0xffff0000ffff0000ULL)
            | ((r15 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r15 = ((r15 ^ 0xff000000ff0000ULL) + r16); // 2 ops
        r16 = (r15 & 0x100010001000100ULL);
        r15 = ((r15 - r16) + (r16 >> 8)); // 3 ops
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+4] = v[i]+v[i+4], v[i]-v[i+4]
        r16 = ((r0 << 32) | (r0 >> 32)); // 3 ops
        r0 = ((r0 ^ 0xff00ff00000000ULL) + r16); // 2 ops
        r16 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r16) + (r16 >> 8)); // 3 ops
        r16 = ((r1 << 32) | (r1 >> 32)); // 3 ops
        r1 = ((r1 ^ 0xff00ff00000000ULL) + r16); // 2 ops
        r16 = (r1 & 0x100010001000100ULL);
        r1 = ((r1 - r16) + (r16 >> 8)); // 3 ops
        r16 = ((r2 << 32) | (r2 >> 32)); // 3 ops
        r2 = ((r2 ^ 0xff00ff00000000ULL) + r16); // 2 ops
        r16 = (r2 & 0x100010001000100ULL);
        r2 = ((r2 - r16) + (r16 >> 8)); // 3 ops
        r16 = ((r3 << 32) | (r3 >> 32)); // 3 ops
        r3 = ((r3 ^ 0xff00ff00000000ULL) + r16); // 2 ops
        r16 = (r3 & 0x100010001000100ULL);
        r3 = ((r3 - r16) + (r16 >> 8)); // 3 ops
        r16 = ((r4 << 32) | (r4 >> 32)); // 3 ops
        r4 = ((r4 ^ 0xff00ff00000000ULL) + r16); // 2 ops
        r16 = (r4 & 0x100010001000100ULL);
        r4 = ((r4 - r16) + (r16 >> 8)); // 3 ops
        r16 = ((r5 << 32) | (r5 >> 32)); // 3 ops
        r5 = ((r5 ^ 0xff00ff00000000ULL) + r16); // 2 ops
        r16 = (r5 & 0x100010001000100ULL);
        r5 = ((r5 - r16) + (r16 >> 8)); // 3 ops
        r16 = ((r6 << 32) | (r6 >> 32)); // 3 ops
        r6 = ((r6 ^ 0xff00ff00000000ULL) + r16); // 2 ops
        r16 = (r6 & 0x100010001000100ULL);
        r6 = ((r6 - r16) + (r16 >> 8)); // 3 ops
        r16 = ((r7 << 32) | (r7 >> 32)); // 3 ops
        r7 = ((r7 ^ 0xff00ff00000000ULL) + r16); // 2 ops
        r16 = (r7 & 0x100010001000100ULL);
        r7 = ((r7 - r16) + (r16 >> 8)); // 3 ops
        r16 = ((r8 << 32) | (r8 >> 32)); // 3 ops
        r8 = ((r8 ^ 0xff00ff00000000ULL) + r16); // 2 ops
        r16 = (r8 & 0x100010001000100ULL);
        r8 = ((r8 - r16) + (r16 >> 8)); // 3 ops
        r16 = ((r9 << 32) | (r9 >> 32)); // 3 ops
        r9 = ((r9 ^ 0xff00ff00000000ULL) + r16); // 2 ops
        r16 = (r9 & 0x100010001000100ULL);
        r9 = ((r9 - r16) + (r16 >> 8)); // 3 ops
        r16 = ((r10 << 32) | (r10 >> 32)); // 3 ops
        r10 = ((r10 ^ 0xff00ff00000000ULL) + r16); // 2 ops
        r16 = (r10 & 0x100010001000100ULL);
        r10 = ((r10 - r16) + (r16 >> 8)); // 3 ops
        r16 = ((r11 << 32) | (r11 >> 32)); // 3 ops
        r11 = ((r11 ^ 0xff00ff00000000ULL) + r16); // 2 ops
        r16 = (r11 & 0x100010001000100ULL);
        r11 = ((r11 - r16) + (r16 >> 8)); // 3 ops
        r16 = ((r12 << 32) | (r12 >> 32)); // 3 ops
        r12 = ((r12 ^ 0xff00ff00000000ULL) + r16); // 2 ops
        r16 = (r12 & 0x100010001000100ULL);
        r12 = ((r12 - r16) + (r16 >> 8)); // 3 ops
        r16 = ((r13 << 32) | (r13 >> 32)); // 3 ops
        r13 = ((r13 ^ 0xff00ff00000000ULL) + r16); // 2 ops
        r16 = (r13 & 0x100010001000100ULL);
        r13 = ((r13 - r16) + (r16 >> 8)); // 3 ops
        r16 = ((r14 << 32) | (r14 >> 32)); // 3 ops
        r14 = ((r14 ^ 0xff00ff00000000ULL) + r16); // 2 ops
        r16 = (r14 & 0x100010001000100ULL);
        r14 = ((r14 - r16) + (r16 >> 8)); // 3 ops
        r16 = ((r15 << 32) | (r15 >> 32)); // 3 ops
        r15 = ((r15 ^ 0xff00ff00000000ULL) + r16); // 2 ops
        r16 = (r15 & 0x100010001000100ULL);
        r15 = ((r15 - r16) + (r16 >> 8)); // 3 ops
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+8] = v[i]+v[i+8], v[i]-v[i+8]
        r16 = (r0 + (r1 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r0 = (r0 + r1);
        r1 = (r16 & 0x100010001000100ULL);
        r1 = ((r16 - r1) + (r1 >> 8)); // 3 ops
        r16 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r2 + (r3 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r2 = (r2 + r3);
        r3 = (r16 & 0x100010001000100ULL);
        r3 = ((r16 - r3) + (r3 >> 8)); // 3 ops
        r16 = (r2 & 0x100010001000100ULL);
        r2 = ((r2 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r4 + (r5 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r4 = (r4 + r5);
        r5 = (r16 & 0x100010001000100ULL);
        r5 = ((r16 - r5) + (r5 >> 8)); // 3 ops
        r16 = (r4 & 0x100010001000100ULL);
        r4 = ((r4 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r6 + (r7 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r6 = (r6 + r7);
        r7 = (r16 & 0x100010001000100ULL);
        r7 = ((r16 - r7) + (r7 >> 8)); // 3 ops
        r16 = (r6 & 0x100010001000100ULL);
        r6 = ((r6 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r8 + (r9 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r8 = (r8 + r9);
        r9 = (r16 & 0x100010001000100ULL);
        r9 = ((r16 - r9) + (r9 >> 8)); // 3 ops
        r16 = (r8 & 0x100010001000100ULL);
        r8 = ((r8 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r10 + (r11 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r10 = (r10 + r11);
        r11 = (r16 & 0x100010001000100ULL);
        r11 = ((r16 - r11) + (r11 >> 8)); // 3 ops
        r16 = (r10 & 0x100010001000100ULL);
        r10 = ((r10 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r12 + (r13 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r12 = (r12 + r13);
        r13 = (r16 & 0x100010001000100ULL);
        r13 = ((r16 - r13) + (r13 >> 8)); // 3 ops
        r16 = (r12 & 0x100010001000100ULL);
        r12 = ((r12 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r14 + (r15 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r14 = (r14 + r15);
        r15 = (r16 & 0x100010001000100ULL);
        r15 = ((r16 - r15) + (r15 >> 8)); // 3 ops
        r16 = (r14 & 0x100010001000100ULL);
        r14 = ((r14 - r16) + (r16 >> 8)); // 3 ops
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+16] = v[i]+v[i+16], v[i]-v[i+16]
        r16 = (r0 + (r2 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r0 = (r0 + r2);
        r2 = (r16 & 0x100010001000100ULL);
        r2 = ((r16 - r2) + (r2 >> 8)); // 3 ops
        r16 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r1 + (r3 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r1 = (r1 + r3);
        r3 = (r16 & 0x100010001000100ULL);
        r3 = ((r16 - r3) + (r3 >> 8)); // 3 ops
        r16 = (r1 & 0x100010001000100ULL);
        r1 = ((r1 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r4 + (r6 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r4 = (r4 + r6);
        r6 = (r16 & 0x100010001000100ULL);
        r6 = ((r16 - r6) + (r6 >> 8)); // 3 ops
        r16 = (r4 & 0x100010001000100ULL);
        r4 = ((r4 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r5 + (r7 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r5 = (r5 + r7);
        r7 = (r16 & 0x100010001000100ULL);
        r7 = ((r16 - r7) + (r7 >> 8)); // 3 ops
        r16 = (r5 & 0x100010001000100ULL);
        r5 = ((r5 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r8 + (r10 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r8 = (r8 + r10);
        r10 = (r16 & 0x100010001000100ULL);
        r10 = ((r16 - r10) + (r10 >> 8)); // 3 ops
        r16 = (r8 & 0x100010001000100ULL);
        r8 = ((r8 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r9 + (r11 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r9 = (r9 + r11);
        r11 = (r16 & 0x100010001000100ULL);
        r11 = ((r16 - r11) + (r11 >> 8)); // 3 ops
        r16 = (r9 & 0x100010001000100ULL);
        r9 = ((r9 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r12 + (r14 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r12 = (r12 + r14);
        r14 = (r16 & 0x100010001000100ULL);
        r14 = ((r16 - r14) + (r14 >> 8)); // 3 ops
        r16 = (r12 & 0x100010001000100ULL);
        r12 = ((r12 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r13 + (r15 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r13 = (r13 + r15);
        r15 = (r16 & 0x100010001000100ULL);
        r15 = ((r16 - r15) + (r15 >> 8)); // 3 ops
        r16 = (r13 & 0x100010001000100ULL);
        r13 = ((r13 - r16) + (r16 >> 8)); // 3 ops
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+32] = v[i]+v[i+32], v[i]-v[i+32]
        r16 = (r0 + (r4 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r0 = (r0 + r4);
        r4 = (r16 & 0x100010001000100ULL);
        r4 = ((r16 - r4) + (r4 >> 8)); // 3 ops
        r16 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r1 + (r5 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r1 = (r1 + r5);
        r5 = (r16 & 0x100010001000100ULL);
        r5 = ((r16 - r5) + (r5 >> 8)); // 3 ops
        r16 = (r1 & 0x100010001000100ULL);
        r1 = ((r1 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r2 + (r6 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r2 = (r2 + r6);
        r6 = (r16 & 0x100010001000100ULL);
        r6 = ((r16 - r6) + (r6 >> 8)); // 3 ops
        r16 = (r2 & 0x100010001000100ULL);
        r2 = ((r2 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r3 + (r7 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r3 = (r3 + r7);
        r7 = (r16 & 0x100010001000100ULL);
        r7 = ((r16 - r7) + (r7 >> 8)); // 3 ops
        r16 = (r3 & 0x100010001000100ULL);
        r3 = ((r3 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r8 + (r12 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r8 = (r8 + r12);
        r12 = (r16 & 0x100010001000100ULL);
        r12 = ((r16 - r12) + (r12 >> 8)); // 3 ops
        r16 = (r8 & 0x100010001000100ULL);
        r8 = ((r8 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r9 + (r13 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r9 = (r9 + r13);
        r13 = (r16 & 0x100010001000100ULL);
        r13 = ((r16 - r13) + (r13 >> 8)); // 3 ops
        r16 = (r9 & 0x100010001000100ULL);
        r9 = ((r9 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r10 + (r14 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r10 = (r10 + r14);
        r14 = (r16 & 0x100010001000100ULL);
        r14 = ((r16 - r14) + (r14 >> 8)); // 3 ops
        r16 = (r10 & 0x100010001000100ULL);
        r10 = ((r10 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r11 + (r15 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r11 = (r11 + r15);
        r15 = (r16 & 0x100010001000100ULL);
        r15 = ((r16 - r15) + (r15 >> 8)); // 3 ops
        r16 = (r11 & 0x100010001000100ULL);
        r11 = ((r11 - r16) + (r16 >> 8)); // 3 ops
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+64] = v[i]+v[i+64], v[i]-v[i+64]
        r16 = (r0 + (r8 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r0 = (r0 + r8);
        r8 = (r16 & 0x100010001000100ULL);
        r8 = ((r16 - r8) + (r8 >> 8)); // 3 ops
        r16 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r1 + (r9 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r1 = (r1 + r9);
        r9 = (r16 & 0x100010001000100ULL);
        r9 = ((r16 - r9) + (r9 >> 8)); // 3 ops
        r16 = (r1 & 0x100010001000100ULL);
        r1 = ((r1 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r2 + (r10 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r2 = (r2 + r10);
        r10 = (r16 & 0x100010001000100ULL);
        r10 = ((r16 - r10) + (r10 >> 8)); // 3 ops
        r16 = (r2 & 0x100010001000100ULL);
        r2 = ((r2 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r3 + (r11 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r3 = (r3 + r11);
        r11 = (r16 & 0x100010001000100ULL);
        r11 = ((r16 - r11) + (r11 >> 8)); // 3 ops
        r16 = (r3 & 0x100010001000100ULL);
        r3 = ((r3 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r4 + (r12 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r4 = (r4 + r12);
        r12 = (r16 & 0x100010001000100ULL);
        r12 = ((r16 - r12) + (r12 >> 8)); // 3 ops
        r16 = (r4 & 0x100010001000100ULL);
        r4 = ((r4 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r5 + (r13 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r5 = (r5 + r13);
        r13 = (r16 & 0x100010001000100ULL);
        r13 = ((r16 - r13) + (r13 >> 8)); // 3 ops
        r16 = (r5 & 0x100010001000100ULL);
        r5 = ((r5 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r6 + (r14 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r6 = (r6 + r14);
        r14 = (r16 & 0x100010001000100ULL);
        r14 = ((r16 - r14) + (r14 >> 8)); // 3 ops
        r16 = (r6 & 0x100010001000100ULL);
        r6 = ((r6 - r16) + (r16 >> 8)); // 3 ops
        r16 = (r7 + (r15 ^ 0xff00ff00ff00ffULL)); // 2 ops
        r7 = (r7 + r15);
        r15 = (r16 & 0x100010001000100ULL);
        r15 = ((r16 - r15) + (r15 >> 8)); // 3 ops
        r16 = (r7 & 0x100010001000100ULL);
        r7 = ((r7 - r16) + (r16 >> 8)); // 3 ops
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Reverse expansion for Hadamard operation
        r0 ^= (r8 << 8); // 2 ops
        r1 ^= (r9 << 8); // 2 ops
        r2 ^= (r10 << 8); // 2 ops
        r3 ^= (r11 << 8); // 2 ops
        r4 ^= (r12 << 8); // 2 ops
        r5 ^= (r13 << 8); // 2 ops
        r6 ^= (r14 << 8); // 2 ops
        r7 ^= (r15 << 8); // 2 ops
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        // Multiply vector by scalar 2**-3 mod 255
        r0 = (((r0 & 0x707070707070707ULL) << 5)
            | ((r0 & 0xf8f8f8f8f8f8f8f8ULL) >> 3)); // 5 ops
        r1 = (((r1 & 0x707070707070707ULL) << 5)
            | ((r1 & 0xf8f8f8f8f8f8f8f8ULL) >> 3)); // 5 ops
        r2 = (((r2 & 0x707070707070707ULL) << 5)
            | ((r2 & 0xf8f8f8f8f8f8f8f8ULL) >> 3)); // 5 ops
        r3 = (((r3 & 0x707070707070707ULL) << 5)
            | ((r3 & 0xf8f8f8f8f8f8f8f8ULL) >> 3)); // 5 ops
        r4 = (((r4 & 0x707070707070707ULL) << 5)
            | ((r4 & 0xf8f8f8f8f8f8f8f8ULL) >> 3)); // 5 ops
        r5 = (((r5 & 0x707070707070707ULL) << 5)
            | ((r5 & 0xf8f8f8f8f8f8f8f8ULL) >> 3)); // 5 ops
        r6 = (((r6 & 0x707070707070707ULL) << 5)
            | ((r6 & 0xf8f8f8f8f8f8f8f8ULL) >> 3)); // 5 ops
        r7 = (((r7 & 0x707070707070707ULL) << 5)
            | ((r7 & 0xf8f8f8f8f8f8f8f8ULL) >> 3)); // 5 ops
        // Storing vector v to array v_out; multiply v
        // with diagonal matrix if exp1 == -1.
        v_out[0] = r0 ^ ((exp1) & 0xffffffffffff00ULL);
        v_out[1] = r1 ^ ((exp1) & 0xff00ffffffULL);
        v_out[2] = r2 ^ ((exp1) & 0xff00ffffffULL);
        v_out[3] = r3 ^ ((exp1) & 0xff000000000000ffULL);
        v_out[4] = r4 ^ ((exp1) & 0xff00ffffffULL);
        v_out[5] = r5 ^ ((exp1) & 0xff000000000000ffULL);
        v_out[6] = r6 ^ ((exp1) & 0xff000000000000ffULL);
        v_out[7] = r7 ^ ((exp1) & 0xffffff00ff000000ULL);
        exp1 = ~(exp1);
        // 394 lines of code, 874 operations
        }
        // End of automatically generated matrix operation.
 
        v_in += 8;
        v_out += 8;
    }

    // Do tags X, Y, and Z
    {
         uint_mmv_t *pXYin, *pYZin, *pZXin;
         uint_mmv_t *pXYout, *pYZout, *pZXout;
         if (exp1 == 0) {
             pXYin = v_in; 
             pXYout = v_out + 16384;  
             pYZin = v_in + 16384; 
             pYZout = v_out + 8192;  
             pZXin = v_in + 8192; 
             pZXout = v_out; 
         } else {
             pXYout = v_out; 
             pXYin = v_in + 16384;  
             pYZout = v_out + 16384; 
             pYZin = v_in + 8192;  
             pZXout = v_out + 8192; 
             pZXin = v_in; 
         }

         // Map X to Y for t and Y to X for t**2
         for (i = 0; i < 8192; ++i) pXYout[i] = pXYin[i];
         mm_op255_neg_scalprod_d_i(pXYout);
         
         // Map Y to Z for t and Z to Y for t**2
         invert255_xyz(pYZin, pYZout);
         mm_op255_neg_scalprod_d_i(pYZout);

         // Map Z to X for t and X to Z for t**2
         invert255_xyz(pZXin, pZXout);
    }
}



/**
  @brief A restricted version of function ``mm_op255_t``

  Function ``mm_op255_t`` computes a certain operation of the
  monster group on a vector ``v_in`` and stores the result in a
  vector ``v_out``. That operation depends on a parameter ``exp``.
  
  Function ``mm_op255_t_A`` performs the same operation, but it
  computes the part of the vector  ``v_out``  that consists of
  the entries of vector ``v_out``  with tag ``A`` only; the
  other entries of vector ``v_out`` are not changed.
  See section **The representation of the monster group**
  in the **API reference** for tags of entries of a vector in
  the representation of the monster. Note that the entries
  of vector ``v_out`` with tag ``A`` also depend on entries
  of vector ``v_in`` with tags different from ``A``.

  Parameters of this function are the same as in the case of
  function ``mm_op255_t``. This function is much faster than
  function ``mm_op255_t``.
*/
// %%EXPORT px
MM_OP255_API
void mm_op255_t_A(uint_mmv_t *v_in,  uint32_t exp, uint_mmv_t *v_out)
{
    uint_mmv_t i, exp1;
 
    exp %= 3;
    if (exp == 0) {
        for (i = 0; i < 96; ++i) v_out[i] = v_in[i];
        return;
    }
    exp1 = 0x1ULL - (uint_mmv_t)exp;
    op255_t_A(v_in, exp1, v_out);
}



/**
  @brief Another restricted version of function ``mm_op255_t``

  Function ``mm_op255_t`` computes a certain operation of the
  monster group on a vector ``v_in`` and stores the result in a
  vector ``v_out``. That operation depends on a parameter ``exp``.
  
  Function ``mm_op255_t_ABC`` computes the same
  operation on the entries of the vector ``v = v_in`` with
  tag ``A, B, C`` only, and ignores the other entries of ``v``.
  See section **The representation of the monster group**
  in the **API reference** for tags of entries of a vector in
  the representation of the monster.

  The function overwrites the vector ``v`` with the result.
  Here only entries of ``v`` with tag ``A, B, C`` are changed. 
  This function is much faster than  function ``mm_op255_t``.
*/
// %%EXPORT px
MM_OP255_API
void mm_op255_t_ABC(uint_mmv_t *v,  uint32_t exp)
{
    uint_mmv_t  exp1;
 
    exp %= 3;
    if (exp == 0) return;
    exp1 = 0x1ULL - (uint_mmv_t)exp;
    op255_t_ABC(v, exp1, v);
}





//  %%GEN h
//  %%GEN c


