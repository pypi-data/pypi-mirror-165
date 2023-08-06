/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm15_op_eval_A.c

 File ``mm15_op_eval_A.c`` implements the evaluation of the ``A``
 part of a vector in the representation \f$\rho_{15}\f$ of the
 monster.

 That ``A`` part corresponds to a symmetric matrix \f$A\f$ acting on
 the Leech lattice. 

 Let \f$v_2\f$ be a short Leech lattice vector, encoded as a vector 
 in the Leech lattice modulo 2. This module contains a 
 function ``mm_op15_eval_A`` for evaluating the symmetric 
 matrix \f$A\f$ at a \f$v_2\f$.

 The functions in this module are implemented for the representation 
 of the monster modulo 15 only.
*/


#include "mm_op15.h"   
#include "clifford12.h"
 
// %%EXPORT_KWD MM_OP%{P}_API
  



//  %%GEN h
//  %%GEN c




/*************************************************************************
***  Auxiliary function for function  mm_op15_eval_A
*************************************************************************/

/** @brief Auxiliary function for ``mm_op15_eval_A``

   Let matrix ``A`` be the part with tag 'A' of a  vector ``v``
   of the representation of the monster modulo 15. 

   Let ``m_and[i]`` and ``m_xor[i]`` be the bit ``i`` of ``m_and`` 
   and ``m_xor``, respectively. Define a vector ``y = (y[0],...,y[23])``
   by: ``y[i] = m_and[i]  * (-1)**m_xor[i]``.

   If ``row >= 24`` the function returns ``res = y * A * transpose(y)``
   (modulo 15). We have ``0 < res < 0x8000``, but ``res`` is not
   reduced modulo 15.

   In case ``row < 24`` define the vector ``z`` by ``z[i] = y[i]``
   if ``i = row`` and ``z[i] = 0`` otherwise. 
   Put ``zz =  z * A * transpose(y)`` (modulo 15).  We 
   have ``0 < res < 0x8000``, but ``res`` is not reduced modulo 15.

   In case ``row < 24`` the function returns ``0x10000 * zz + res``.
*/
// %%EXPORT px
MM_OP15_API
int32_t mm_op15_eval_A_aux(uint_mmv_t *v, uint32_t m_and, uint32_t m_xor, uint32_t row)
{
    uint_mmv_t xor_mask0;  // XOR mask for integer 0 of row of v
    uint_mmv_t and_mask0;  // AND mask for integer 0 of row of v
    uint_mmv_t xor_mask1;  // XOR mask for integer 1 of row of v
    uint_mmv_t and_mask1;  // AND mask for integer 1 of row of v
    uint_fast32_t i;      // counter for rows
    uint_mmv_t total = 0; // sum of all (modified) entries
    uint_mmv_t a_row[2];  // a_row[1] = sum of (modified) entries in selected row

    a_row[1] = 0;
    xor_mask0 = m_xor >> 0;
    // %%MMV_UINT_SPREAD "xor_mask%{j}", "xor_mask%{j}"
    // Spread bits 0,...,15 of xor_mask0 to the (4-bit long) fields
    // of xor_mask0. A field of xor_mask0 is set to 0xf if its 
    // corresponding bit in input xor_mask0 is one and to 0 otherwise.
    xor_mask0 = (xor_mask0 & 0xffULL) + ((xor_mask0 & 0xff00ULL) << 24);
    xor_mask0 = (xor_mask0 & 0xf0000000fULL) 
        +  ((xor_mask0 & 0xf0000000f0ULL) << 12);
    xor_mask0 = (xor_mask0 & 0x3000300030003ULL) 
        +  ((xor_mask0 & 0xc000c000c000cULL) << 6);
    xor_mask0 = (xor_mask0 & 0x101010101010101ULL) 
        +  ((xor_mask0 & 0x202020202020202ULL) << 3);
    xor_mask0 *= 15;
    // Bit spreading done.
    and_mask0 = m_and >> 0;
    // %%MMV_UINT_SPREAD "and_mask%{j}", "and_mask%{j}"
    // Spread bits 0,...,15 of and_mask0 to the (4-bit long) fields
    // of and_mask0. A field of and_mask0 is set to 0xf if its 
    // corresponding bit in input and_mask0 is one and to 0 otherwise.
    and_mask0 = (and_mask0 & 0xffULL) + ((and_mask0 & 0xff00ULL) << 24);
    and_mask0 = (and_mask0 & 0xf0000000fULL) 
        +  ((and_mask0 & 0xf0000000f0ULL) << 12);
    and_mask0 = (and_mask0 & 0x3000300030003ULL) 
        +  ((and_mask0 & 0xc000c000c000cULL) << 6);
    and_mask0 = (and_mask0 & 0x101010101010101ULL) 
        +  ((and_mask0 & 0x202020202020202ULL) << 3);
    and_mask0 *= 15;
    // Bit spreading done.
    xor_mask1 = m_xor >> 16;
    // %%MMV_UINT_SPREAD "xor_mask%{j}", "xor_mask%{j}"
    // Spread bits 0,...,15 of xor_mask1 to the (4-bit long) fields
    // of xor_mask1. A field of xor_mask1 is set to 0xf if its 
    // corresponding bit in input xor_mask1 is one and to 0 otherwise.
    xor_mask1 = (xor_mask1 & 0xffULL) + ((xor_mask1 & 0xff00ULL) << 24);
    xor_mask1 = (xor_mask1 & 0xf0000000fULL) 
        +  ((xor_mask1 & 0xf0000000f0ULL) << 12);
    xor_mask1 = (xor_mask1 & 0x3000300030003ULL) 
        +  ((xor_mask1 & 0xc000c000c000cULL) << 6);
    xor_mask1 = (xor_mask1 & 0x101010101010101ULL) 
        +  ((xor_mask1 & 0x202020202020202ULL) << 3);
    xor_mask1 *= 15;
    // Bit spreading done.
    and_mask1 = m_and >> 16;
    // %%MMV_UINT_SPREAD "and_mask%{j}", "and_mask%{j}"
    // Spread bits 0,...,15 of and_mask1 to the (4-bit long) fields
    // of and_mask1. A field of and_mask1 is set to 0xf if its 
    // corresponding bit in input and_mask1 is one and to 0 otherwise.
    and_mask1 = (and_mask1 & 0xffULL) + ((and_mask1 & 0xff00ULL) << 24);
    and_mask1 = (and_mask1 & 0xf0000000fULL) 
        +  ((and_mask1 & 0xf0000000f0ULL) << 12);
    and_mask1 = (and_mask1 & 0x3000300030003ULL) 
        +  ((and_mask1 & 0xc000c000c000cULL) << 6);
    and_mask1 = (and_mask1 & 0x101010101010101ULL) 
        +  ((and_mask1 & 0x202020202020202ULL) << 3);
    and_mask1 *= 15;
    // Bit spreading done.
   
    for (i = 0; i < 24; ++i) {
        uint_mmv_t xor_mask_row = 0ULL - (1ULL & (m_xor >> i));
        uint_mmv_t and_mask_row = 0ULL - (1ULL & (m_and >> i));
        uint_mmv_t rowsum = 0;  // sum of (modified) entries in row
        uint_mmv_t w;           // current integer from vector v
        w = v[0] ^ xor_mask0 ^ xor_mask_row;
        w &= and_mask0 & and_mask_row;
        w = (w & 0xf0f0f0f0f0f0f0fULL)
            + ((w >> 4) & 0xf0f0f0f0f0f0f0fULL);
        w = w + (w >> 8);
        w = w + (w >> 16);
        w = w + (w >> 32);
        w &= 0xffULL;
        rowsum += w; 
        w = v[1] ^ xor_mask1 ^ xor_mask_row;
        w &= and_mask1 & and_mask_row;
        w = (w & 0xf0f0f0fULL)
            + ((w >> 4) & 0xf0f0f0fULL);
        w = w + (w >> 8);
        w = w + (w >> 16);
        w = w + (w >> 32);
        w &= 0xffULL;
        rowsum += w; 
        total += rowsum;
        a_row[i == row] = rowsum;
        v += 2;
    }
    
    return (uint32_t)((a_row[1] << 16) + total); 
}



     

/*************************************************************************
*** Function mm_op15_eval_A
*************************************************************************/

/// @cond DO_NOT_DOCUMENT 

// Obtain ``v[i, j]`` for a vector ``v`` in the monster rep mod {P} 
static inline uint32_t entry_v(uint_mmv_t *v, uint32_t i, uint32_t j)
{
     uint_mmv_t w;
     i = (i << 5) + j;
     w = v[i >> 4];
     w >>= (i &  0xfULL) << 2;
     return (uint32_t)(w & 15);
}

/// @endcond



/** @brief Evaluate A part in rep of monster at a short Leech vector

   Let ``v`` be a vector in the 196884-dimensional representation
   of the monster group modulo 15, encoded as described in
   section *Description of the mmgroup.mm<p> extensions* in the
   description of the *C interface*. The entries corresponding to
   tag 'A' of ``v`` form a symmetric 24 times 24 matrix \f$A\f$. 

   Let \f$v_2\f$ be a short Leech lattice vector given by parameter
   ``v2``, encoded as a vector in  the Leech lattice modulo 2. 
   Then \f$v_2\f$ is determined up to sign and \f$v_2 A v_2^\top\f$
   is determined uniquely.

   The function returns \f$r = v_2 A v_2^\top\f$ modulo 15,
   with \f$0 \leq r <  15\f$ in case of success. It returns -1
   if  \f$v_2\f$ is not short (i.e. not of type 2).

   The short Leech lattice vector \f$v_2\f$ (of norm 4) is scaled to
   norm 32 as usual, when \f$v_2\f$ is given in integer coordinates.
*/
// %%EXPORT px
MM_OP15_API
int32_t mm_op15_eval_A(uint64_t *v, uint32_t v2)
{
    uint_fast32_t vect, coc, res, theta, lsb, syn, cocodev, res_row, i, j;

    switch(gen_leech2_type2(v2)) {
        case 0x20:
            // Compute cocode entries of v2
            syn = MAT24_SYNDROME_TABLE[(v2 ^ MAT24_RECIP_BASIS[23]) & 0x7ff];
            syn &= 0x3ff;
            // Bits 9..5 and bits 4..0 contain high and low cocode bit index.
            // Change a high cocode bit index 24 to 23.
            syn -= ((syn + 0x100) & 0x400) >> 5;
            i = syn & 0x1f; j = syn >> 5;
            res = entry_v(v, i, j);
            res ^= (((v2 >> 23) & 1UL) - 1UL) & 15;
            res += res;
            res += entry_v(v, i, i) + entry_v(v, j, j);
            res <<= 4;
            break;
        case 0x21:
            v2 &= 0x7fffffUL;
            theta = MAT24_THETA_TABLE[v2 >> 12];
            vect = mat24_def_gcode_to_vect(v2 >> 12); 
            i = MAT24_SYNDROME_TABLE[(v2 ^ theta) & 0x7ff] & 0x1f;
            vect ^= 0UL - ((vect >> i) & 1UL);
            res = mm_op15_eval_A_aux(v, 0xffffff, vect, i);
            res_row = res >> 16; res &= 0xffff;
            res +=  7 * res_row;
            res += 1 * (entry_v(v, i, i));
            break;
        case 0x22:
            v2 &= 0x7fffffUL;
            theta = MAT24_THETA_TABLE[v2 >> 12];
            vect = mat24_def_gcode_to_vect(v2 >> 12); 
            vect ^=  ((theta >> 13) & 1UL) - 1UL;
            coc = (v2 ^ theta) & 0x7ff;
            lsb = mat24_def_lsbit24(vect);
            coc ^= MAT24_RECIP_BASIS[lsb];
            syn = MAT24_SYNDROME_TABLE[coc & 0x7ff];
            cocodev = mat24_def_syndrome_from_table(syn) ^ (1UL << lsb);
            res = 4 * mm_op15_eval_A_aux(v, vect, cocodev, 24);
            break;
        default:
            return -1;

    }
    return res % 15;
}

/*************************************************************************
*** Function mm_op15_norm_A
*************************************************************************/


/**
  @brief Compute norm of the 'A' part of a vector in the rep of the monster

  Assume that ``v`` is a vector in the representation of the monster
  modulo 15. Then the part of  ``v`` with tag 'A' is considered as
  a symmetric 24 times 24 matrix. The function returns the norm (i.e.
  the sum of the squares of the entries) of that matrix.
*/
// %%EXPORT px
MM_OP15_API
uint32_t mm_op15_norm_A(uint_mmv_t *v)
{
    uint_mmv_t w;
    uint_fast32_t i, norm = 0;
    static uint8_t SQ[16] = {  // squares mod 15
        0, 1, 4, 9,  1, 10, 6, 4,  4, 6, 10, 1,  9, 4, 1, 0
    };
    for (i = 0; i < 24; ++i) {         // Main loop of rows
        w = v[0];  // Load next integer of v
        norm += SQ[(w >> 0) & 15];
        norm += SQ[(w >> 4) & 15];
        norm += SQ[(w >> 8) & 15];
        norm += SQ[(w >> 12) & 15];
        norm += SQ[(w >> 16) & 15];
        norm += SQ[(w >> 20) & 15];
        norm += SQ[(w >> 24) & 15];
        norm += SQ[(w >> 28) & 15];
        norm += SQ[(w >> 32) & 15];
        norm += SQ[(w >> 36) & 15];
        norm += SQ[(w >> 40) & 15];
        norm += SQ[(w >> 44) & 15];
        norm += SQ[(w >> 48) & 15];
        norm += SQ[(w >> 52) & 15];
        norm += SQ[(w >> 56) & 15];
        norm += SQ[(w >> 60) & 15];
        w = v[1];  // Load next integer of v
        norm += SQ[(w >> 0) & 15];
        norm += SQ[(w >> 4) & 15];
        norm += SQ[(w >> 8) & 15];
        norm += SQ[(w >> 12) & 15];
        norm += SQ[(w >> 16) & 15];
        norm += SQ[(w >> 20) & 15];
        norm += SQ[(w >> 24) & 15];
        norm += SQ[(w >> 28) & 15];

        v += 2;
    }                                  // End main loop of rows
    return norm % 15;
}



/*************************************************************************
*** Watermark a 24 times 24 times matrix mod 15
*************************************************************************/


/// @cond DO_NOT_DOCUMENT 

static inline void insertsort(uint32_t *a, int32_t n)
// Sort the array ``a`` of length ``n``.
{
    int_fast32_t i, j;
    for (i = 1; i < n; i += 1) {
        uint32_t temp = a[i];
        for (j = i; j >= 1 && a[j - 1] > temp; --j) a[j] = a[j - 1];
        a[j] = temp;
    }
}


/// @endcond


/** @brief Watermark 'A' part of a vector of the representation of the monster

   Let matrix ``A`` be the part with tag 'A' of a  vector ``v`` of
   the representation of the monster modulo ``p``.

   Then we watermark 24 the rows of matrix ``A``. For each of the
   rows ``A[i], 0 <= i < 24`` we compute a watermark ``w(i)`` in
   the array ``w``. Note that the watermark ``w(i)`` contains an
   information about the marked row ``i`` in its lower bits. We store
   the sorted array of these watermarks in the array ``w`` of length
   24. If all these watermarks (ignoring the information about the
   row) are different, we can easily recognize a permutation of the
   rows of matrix ``A`` by comparing the watermark of matrix ``A``
   with the watermark of the permuted matrix ``A``.

   The watermark ``w[i] `` depends on the distribution of the
   absolute values of the entries ``w[i, j] `` (modulo ``p``) of
   row ``i``. Thus permutations of the columns and sign changes in
   the matrix do not affect these watermarks.

   The function returns 0 in case of success and a negative value 
   in case of error.

   The watermark of row \f$i\f$  is equal to \f$i + 32\cdot S(A,i)\f$. 
   Here \f$S(A,i)\f$ depends on the entries of matrix ``A``.
   The value \f$S(A,i)\f$   it is invariant under sign changes of 
   any off-diagonal elements of ``A``. It is also invariant under 
   any permutation of the symmetric matrix ``A`` fixing row and 
   column \f$i\f$. 
*/
// %%EXPORT px
MM_OP15_API
int32_t  mm_op15_watermark_A(uint_mmv_t *v, uint32_t *w)
{
    uint_fast32_t i, j, k, m, d[8];
    uint64_t x, y;

    d[0] = 0; d[1] = 0x20;
    for (i = 2; i < 8; ++i) d[i] = 13 * d[i-1];
    for (i = 0; i < 24; ++i) {
        m = 0;
        for (j = 0; j < 2; ++j) {
            x = v[2*i + j];
            y = x & 0x8888888888888888ULL;
            y = (y << 1) - (y >> 3);
            x ^= y;
            for (k = 0; k < 64 - (j << 5); k += 4) {
                m += d[(x >> k) & 7];
            }                
        }
        w[i] = (m & 0xffffffe0ULL) + i;
    }
    insertsort(w, 24);
    for (i = 0; i < 23; ++i) {
        if (((w[i] ^ w[i+1]) & 0xffffffe0) == 0) return -1L;
    }
    return 0;
}


/** @brief Compute permutation from watermarks of matrices

   Let matrix ``A`` be the part with tag 'A' of a  vector ``v``
   of the representation of the monster modulo ``p``. Let ``w``
   be the watermark of another matrix ``A'`` which is obtained
   from ``A`` by permutations of the rows and columns, and by
   sign changes. Here the watermark ``w`` must have been computed
   by function ``mm_op15_watermark_A``.

   Then the function watermarks matrix ``A`` and computes a
   permutation that maps ``A'`` to ``A``. If that permutation
   is in the Mathieu group \f$M_{24}\f$ then the function
   returns the number of that permutation, as given by
   function ``mat24_perm_to_m24num`` in file ``mat24_functions.c``.

   The function returns a nonegative permutation number in case of 
   success and a negative value in case of error.

   If all watermarks in the array ``w`` (ignoring the information
   about the row in the lower 5 bits) are different then there is
   at most one permutation that maps ``A'`` to ``A``. If that
   permutation is in \f$M_{24}\f$ then the function returns the
   number of that permutation. In all other cases the function
   fails.
*/
// %%EXPORT px
MM_OP15_API
int32_t mm_op15_watermark_A_perm_num(uint32_t *w, uint_mmv_t *v)
{
    uint32_t w1[24], err = 0;
    uint8_t perm[32];
    uint_fast32_t i;
    
    if (mm_op15_watermark_A(v, w1) < 0) return -1L;
    for (i = 0; i < 24; ++i) perm[i] = 24;
    for (i = 0; i < 24; ++i) {
        err |= w[i] ^ w1[i];
        perm[w[i] & 0x1f] = w1[i] & 0x1f;
    }
    if ((err & 0xffffffe0) || mat24_perm_check(perm)) return -1L;
    return mat24_perm_to_m24num(perm);
   
}








//  %%GEN h
//  %%GEN c
