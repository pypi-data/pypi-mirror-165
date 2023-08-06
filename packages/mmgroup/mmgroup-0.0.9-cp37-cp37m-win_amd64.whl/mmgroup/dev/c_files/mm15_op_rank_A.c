/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm15_op_rank_A.c

 Function ``mm_op15_eval_A_rank_mod3`` computes the rank of the ``A``
 part of a vector in the representation \f$\rho_{15}\f$ of the
 monster. That rank is computed modulo 3. 

 That ``A`` part corresponds to a symmetric matrix \f$A\f$ acting on
 the Leech lattice. If matrix \f$A\f$  has corank 1 then we also
 compute a nonzero vector in the kernel of \f$A\f$ as a vector in 
 the Leech lattice modulo 3.

 The functions in this module are implemented for the representation 
 of the monster modulo 3 and 15 only.
*/


#include "mm_op15.h"   
#include "clifford12.h"
 
// %%EXPORT_KWD MM_OP%{P}_API
  



//  %%GEN h
//  %%GEN c





/*************************************************************************
***  Operate with a A part of rep as a 24 times 24 matrix modulo 3 
*************************************************************************/

// %%WITH N_COL = 3




/** @brief Load the 'A' part of a vector of the representation of the monster

   The function loads the part of with tag 'A' of a vector ``v`` of
   the  representation of the monster modulo ``p`` to the matrix ``a``.
   Here matrix ``a`` will be given in **matrix mod 3** encoding as
   documented in the header of file ``leech3matrix.c``.

   The function returns 0.
*/
// %%EXPORT px
MM_OP15_API
int32_t mm_op15_load_leech3matrix(uint_mmv_t *v, uint64_t *a)
{
    uint_fast32_t i;
    uint64_t w0, w1, tmp;
    for (i = 0; i < 24; ++i) {
        w0 = v[0]; 
        w1 = v[1] & 0xffffffffULL;  
        v += 2;
        w0 = (w0 & 0x3333333333333333ULL)
             + ((w0 >> 2) & 0x3333333333333333ULL);
        tmp = w0  & 0x4444444444444444ULL; 
        a[0] =  w0 - tmp + (tmp >> 2);
        w1 = (w1 & 0x3333333333333333ULL)
             + ((w1 >> 2) & 0x3333333333333333ULL);
        tmp = w1  & 0x4444444444444444ULL; 
        a[1] =  w1 - tmp + (tmp >> 2);
        a[2] = 0;
        a +=  3;
    } 
    return 0;
}



/** @brief Rank of 'A' part of a vector of the representation of the monster

   Let ``a`` be the symmetric 24 times matrix corrsponding to the part 
   with  tag 'A' of a input vector ``v`` in the representation of 
   the  monster  modulo `15. Let  ``b = a - d * 1``, for an integer
   input `d`, where ``1`` is the unit matrix. 

   Let ``r`` be the rank of matrix ``b`` with entries taken modulo 3.
   If matrix ``b`` has rank 23 then its kernel is one dimensional. In 
   that case the kernel contains two nonzero vectors ``+-w``, and we
   define ``w`` to be one of these vectors. Otherwise we let ``w`` be 
   the zero vector.

   The function returns the value ``(r << 48) + w``, with ``w`` the
   vector defined above given in *Leech lattice mod 3 encoding* as 
   described in *The C interface of the mmgroup project*. 

**/
// %%EXPORT px
MM_OP15_API
uint64_t  mm_op15_eval_A_rank_mod3(uint_mmv_t *v, uint32_t d)
{
     uint64_t a[24 *  3];
     mm_op15_load_leech3matrix(v, a);
     return leech3matrix_rank(a, d);
}



// %%END WITH


/*************************************************************************
*** Watermark a 24 times 24 times matrices mod 15
*************************************************************************/






//  %%GEN h
//  %%GEN c
