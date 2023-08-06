/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm3_op_eval_A.c

 File ``mm3_op_eval_A.c`` implements the evaluation of the ``A``
 part of a vector in the representation \f$\rho_{3}\f$ of the
 monster.

 That ``A`` part corresponds to a symmetric matrix \f$A\f$ acting on
 the Leech lattice. 

 Let \f$v_2\f$ be a short Leech lattice vector, encoded as a vector 
 in the Leech lattice modulo 2. This module contains a 
 function ``mm_op3_eval_A`` for evaluating the symmetric 
 matrix \f$A\f$ at a \f$v_2\f$.

 The functions in this module are implemented for the representation 
 of the monster modulo 15 only.
*/


#include "mm_op3.h"   
#include "clifford12.h"
 
// %%EXPORT_KWD MM_OP%{P}_API
  



//  %%GEN h
//  %%GEN c




/*************************************************************************
***  Auxiliary function for function  mm_op3_eval_A
*************************************************************************/

/** @brief Auxiliary function for ``mm_op3_eval_A``

   Let matrix ``A`` be the part with tag 'A' of a  vector ``v``
   of the representation of the monster modulo 3. 

   Let ``m_and[i]`` and ``m_xor[i]`` be the bit ``i`` of ``m_and`` 
   and ``m_xor``, respectively. Define a vector ``y = (y[0],...,y[23])``
   by: ``y[i] = m_and[i]  * (-1)**m_xor[i]``.

   If ``row >= 24`` the function returns ``res = y * A * transpose(y)``
   (modulo 3). We have ``0 < res < 0x8000``, but ``res`` is not
   reduced modulo 3.

   In case ``row < 24`` define the vector ``z`` by ``z[i] = y[i]``
   if ``i = row`` and ``z[i] = 0`` otherwise. 
   Put ``zz =  z * A * transpose(y)`` (modulo 3).  We 
   have ``0 < res < 0x8000``, but ``res`` is not reduced modulo 3.

   In case ``row < 24`` the function returns ``0x10000 * zz + res``.
   
   Caution: This function has not been tested!
*/
// %%EXPORT px
MM_OP3_API
int32_t mm_op3_eval_A_aux(uint_mmv_t *v, uint32_t m_and, uint32_t m_xor, uint32_t row)
{
    uint_mmv_t xor_mask0;  // XOR mask for integer 0 of row of v
    uint_mmv_t and_mask0;  // AND mask for integer 0 of row of v
    uint_fast32_t i;      // counter for rows
    uint_mmv_t total = 0; // sum of all (modified) entries
    uint_mmv_t a_row[2];  // a_row[1] = sum of (modified) entries in selected row

    a_row[1] = 0;
    xor_mask0 = m_xor >> 0;
    // %%MMV_UINT_SPREAD "xor_mask%{j}", "xor_mask%{j}"
    // Spread bits 0,...,31 of xor_mask0 to the (2-bit long) fields
    // of xor_mask0. A field of xor_mask0 is set to 0x3 if its 
    // corresponding bit in input xor_mask0 is one and to 0 otherwise.
    xor_mask0 = (xor_mask0 & 0xffffULL) 
        +  ((xor_mask0 & 0xffff0000ULL) << 16);
    xor_mask0 = (xor_mask0 & 0xff000000ffULL) 
        +  ((xor_mask0 & 0xff000000ff00ULL) << 8);
    xor_mask0 = (xor_mask0 & 0xf000f000f000fULL) 
        +  ((xor_mask0 & 0xf000f000f000f0ULL) << 4);
    xor_mask0 = (xor_mask0 & 0x303030303030303ULL) 
        +  ((xor_mask0 & 0xc0c0c0c0c0c0c0cULL) << 2);
    xor_mask0 = (xor_mask0 & 0x1111111111111111ULL) 
        +  ((xor_mask0 & 0x2222222222222222ULL) << 1);
    xor_mask0 *= 3;
    // Bit spreading done.
    and_mask0 = m_and >> 0;
    // %%MMV_UINT_SPREAD "and_mask%{j}", "and_mask%{j}"
    // Spread bits 0,...,31 of and_mask0 to the (2-bit long) fields
    // of and_mask0. A field of and_mask0 is set to 0x3 if its 
    // corresponding bit in input and_mask0 is one and to 0 otherwise.
    and_mask0 = (and_mask0 & 0xffffULL) 
        +  ((and_mask0 & 0xffff0000ULL) << 16);
    and_mask0 = (and_mask0 & 0xff000000ffULL) 
        +  ((and_mask0 & 0xff000000ff00ULL) << 8);
    and_mask0 = (and_mask0 & 0xf000f000f000fULL) 
        +  ((and_mask0 & 0xf000f000f000f0ULL) << 4);
    and_mask0 = (and_mask0 & 0x303030303030303ULL) 
        +  ((and_mask0 & 0xc0c0c0c0c0c0c0cULL) << 2);
    and_mask0 = (and_mask0 & 0x1111111111111111ULL) 
        +  ((and_mask0 & 0x2222222222222222ULL) << 1);
    and_mask0 *= 3;
    // Bit spreading done.
   
    for (i = 0; i < 24; ++i) {
        uint_mmv_t xor_mask_row = 0ULL - (1ULL & (m_xor >> i));
        uint_mmv_t and_mask_row = 0ULL - (1ULL & (m_and >> i));
        uint_mmv_t rowsum = 0;  // sum of (modified) entries in row
        uint_mmv_t w;           // current integer from vector v
        w = v[0] ^ xor_mask0 ^ xor_mask_row;
        w &= and_mask0 & and_mask_row;
        w = (w & 0x333333333333ULL)
            + ((w >> 2) & 0x333333333333ULL);
        w = w + (w >> 4);
        w &= 0x0f0f0f0f0f0f0f0fULL;
        w = w + (w >> 8);
        w = w + (w >> 16);
        w = w + (w >> 32);
        w &= 0x7fULL;
        rowsum += w; 
        total += rowsum;
        a_row[i == row] = rowsum;
        v += 1;
    }
    
    return (uint32_t)((a_row[1] << 16) + total); 
}



     

/*************************************************************************
*** Function mm_op3_eval_A
*************************************************************************/

/// @cond DO_NOT_DOCUMENT 

// Obtain ``v[i, j]`` for a vector ``v`` in the monster rep mod {P} 
static inline uint32_t entry_v(uint_mmv_t *v, uint32_t i, uint32_t j)
{
     uint_mmv_t w;
     i = (i << 5) + j;
     w = v[i >> 5];
     w >>= (i &  0x1fULL) << 1;
     return (uint32_t)(w & 3);
}

/// @endcond



/** @brief Evaluate A part in rep of monster at a short Leech vector

   Let ``v`` be a vector in the 196884-dimensional representation
   of the monster group modulo 3, encoded as described in
   section *Description of the mmgroup.mm<p> extensions* in the
   description of the *C interface*. The entries corresponding to
   tag 'A' of ``v`` form a symmetric 24 times 24 matrix \f$A\f$. 

   Let \f$v_2\f$ be a short Leech lattice vector given by parameter
   ``v2``, encoded as a vector in  the Leech lattice modulo 2. 
   Then \f$v_2\f$ is determined up to sign and \f$v_2 A v_2^\top\f$
   is determined uniquely.

   The function returns \f$r = v_2 A v_2^\top\f$ modulo 3,
   with \f$0 \leq r <  3\f$ in case of success. It returns -1
   if  \f$v_2\f$ is not short (i.e. not of type 2).

   The short Leech lattice vector \f$v_2\f$ (of norm 4) is scaled to
   norm 32 as usual, when \f$v_2\f$ is given in integer coordinates.
   
   Caution: This function has not been tested!
*/
// %%EXPORT px
MM_OP3_API
int32_t mm_op3_eval_A(uint64_t *v, uint32_t v2)
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
            res ^= (((v2 >> 23) & 1UL) - 1UL) & 3;
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
            res = mm_op3_eval_A_aux(v, 0xffffff, vect, i);
            res_row = res >> 16; res &= 0xffff;
            res +=  1 * res_row;
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
            res = 4 * mm_op3_eval_A_aux(v, vect, cocodev, 24);
            break;
        default:
            return -1;

    }
    return res % 3;
}

/*************************************************************************
*** Function mm_op3_norm_A
*************************************************************************/


/**
  @brief Compute norm of the 'A' part of a vector in the rep of the monster

  Assume that ``v`` is a vector in the representation of the monster
  modulo 3. Then the part of  ``v`` with tag 'A' is considered as
  a symmetric 24 times 24 matrix. The function returns the norm (i.e.
  the sum of the squares of the entries) of that matrix.
   
  Caution: This function has not been tested!
*/
// %%EXPORT px
MM_OP3_API
uint32_t mm_op3_norm_A(uint_mmv_t *v)
{
    uint_mmv_t w;
    uint_fast32_t i, norm = 0;
    for (i = 0; i < 24; ++i) {         // Main loop of rows
        w = v[0]; // Load next integer of v
        w = (w ^ (w >> 1));     // square is same as parity (mod 3)
        norm += (w >> 0) & 1; 
        norm += (w >> 2) & 1; 
        norm += (w >> 4) & 1; 
        norm += (w >> 6) & 1; 
        norm += (w >> 8) & 1; 
        norm += (w >> 10) & 1; 
        norm += (w >> 12) & 1; 
        norm += (w >> 14) & 1; 
        norm += (w >> 16) & 1; 
        norm += (w >> 18) & 1; 
        norm += (w >> 20) & 1; 
        norm += (w >> 22) & 1; 
        norm += (w >> 24) & 1; 
        norm += (w >> 26) & 1; 
        norm += (w >> 28) & 1; 
        norm += (w >> 30) & 1; 
        norm += (w >> 32) & 1; 
        norm += (w >> 34) & 1; 
        norm += (w >> 36) & 1; 
        norm += (w >> 38) & 1; 
        norm += (w >> 40) & 1; 
        norm += (w >> 42) & 1; 
        norm += (w >> 44) & 1; 
        norm += (w >> 46) & 1; 

        v += 1;
    }                                  // End main loop of rows
    return norm % 3;
}



/*************************************************************************
*** Watermark a 24 times 24 times matrix mod 3
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

   When working in the representation modulo 3 we fail unless at 
   least nine rows of ``A`` have a unique watermark. This is
   sufficient for reconstructing a permutation in the Mathieu group.
   
   We assert that watermarking ``A + k*I`` succeeds if and only if
   watermarking ``A`` succeeds, for any multiple  ``k*I`` of the
   unit matrix.
*/
// %%EXPORT px
MM_OP3_API
int32_t  mm_op3_watermark_A(uint_mmv_t *v, uint32_t *w)
{
    uint_fast32_t i, j, d[8], m;
    uint32_t w0[24];
    uint64_t mask = 3, diag = 0, a;
    for (i = 0; i < 8; ++i) d[i] = 0;  // avoid compiler warnings
    for (i = 0; i < 9; ++i) w[i] = 24; // make output w erroneous
    for (i = 0; i < 24; ++i) {
        diag += v[i] & mask;   // store diagonal of A in ``diag``
        mask <<= 2; 
    }
    // Reduce diagonal entries of ``A`` in ``diag`` mod 3
    a = diag & (diag >> 1) & 0x555555555555ULL;
    diag ^= a ^ (a << 1);
    diag <<= 1;  // diag[i] = A[i,i] is now in bits (2*i+2, 2*i+1)
    // The main loop now computes a watermark value a0[i] for the  
    // rows i (with 0 <= i < 24) of matrix ``A``
    for (i = 0; i < 24; ++i) {
        // Store abs(A[i,j]) in bit 2*j of variable ``a``
        a = v[i] ^ (v[i] >> 1);
        // Count entries j with diag[j] = x and abs(A[i,j]) = y 
        // in d[2*x + j]. We only need the cases y = 1.
        d[5] = d[3] = d[1] = 0; 
        for (j = 0; j < 48; j += 2) {
            ++d[((diag >> j) & 6) + ((a >> j) & 1)];
        }
        // Enter d[j], j = 1,3,5 and diag[i] into bits 21...5 of
        // the watermark; store i in the low bits of the watermark.
        w0[i] = i + (d[1] << 5) + (d[3] << 10) + (d[5] << 15)
                 + (((diag >> (i << 1)) & 6) << 19);
    }
    // Sort the array of watermarks
    insertsort(w0, 24);
    // Duplicate watermarks are likely when computing in the rep mod 3.
    // Set bit m[i] if watermark w0[i] is not duplicated in another row.
    m = 0;
    for (i = 0; i < 23; ++i) {
        if (((w0[i] ^ w0[i+1]) & 0xffffffe0) == 0) m |= 3UL << i;
       
    }
    m ^= 0xffffffUL;
    // Abort if there are less than 9 non-duplicate watermarks.
    if (mat24_bw24(m) < 9) return -1;
    // Store the (sorted) lowest 9 non-duplicate watermarks in array w.
    for (i = j = 0; j < 9; ++i) {
        w[j] = w0[i];
        j += (m >> i) & 1;
    }
    return 0;    // success
}


/** @brief Compute permutation from watermarks of matrices

   Let matrix ``A`` be the part with tag 'A' of a  vector ``v``
   of the representation of the monster modulo ``p``. Let ``w``
   be the watermark of another matrix ``A'`` which is obtained
   from ``A`` by permutations of the rows and columns, and by
   sign changes. Here the watermark ``w`` must have been computed
   by function ``mm_op3_watermark_A``.

   Then the function watermarks matrix ``A`` and computes a
   permutation that maps ``A'`` to ``A``. If that permutation
   is in the Mathieu group \f$M_{24}\f$ then the function
   returns the number of that permutation, as given by
   function ``mat24_perm_to_m24num`` in file ``mat24_functions.c``.

   The function returns a nonegative permutation number in case of 
   success and a negative value in case of error.

   If the first 9 watermarks in the array ``w`` (ignoring the 
   information about the row in the lower 5 bits) are different 
   then there is at most one permutation in \f$M_{24}\f$ that 
   maps ``A'`` to ``A``. If such a permutation exists then the 
   function returns the number of that permutation. In all other 
   cases the function fails.
*/
// %%EXPORT px
MM_OP3_API
int32_t mm_op3_watermark_A_perm_num(uint32_t *w, uint_mmv_t *v)
{
    uint32_t w1[9], err = 0;
    uint8_t perm[32], h[9], h1[9];
    uint_fast32_t i;
    
    if (mm_op3_watermark_A(v, w1) < 0) return -2001L;
    for (i = 0; i < 9; ++i) {
        err |= w[i] ^ w1[i];
        h[i] = w[i] & 0x1f;
        h1[i] = w1[i] & 0x1f;
    }
    if (err & 0xffffffe0) return -2002L;
    err =  mat24_perm_from_map(h, h1, 9, perm);
    if (err != 1) return (err % 1000) - 1000;
    return mat24_perm_to_m24num(perm);
   
}








//  %%GEN h
//  %%GEN c
