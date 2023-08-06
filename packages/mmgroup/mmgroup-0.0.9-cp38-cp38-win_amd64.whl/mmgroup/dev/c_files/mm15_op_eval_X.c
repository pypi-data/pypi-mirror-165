/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm15_op_eval_X.c

 File ``mm15_op_eval_X.c`` implements the evaluation of the
 part of a vector in the representation \f$\rho_{15}\f$ of the
 monster corresponding to part \f$98280_x\f$ of the representation.

 The modules in this function deal with counting and finding entries
 (corresponding to part \f$98280_x\f$) of a 
 vector \f$v \in \rho_{15}\f$ with a certain absolute value.
 This is useful for identifying a 2A axis \f$v\f$.

 These functions in this module are implemented for the
 representation of the  monster modulo 15 only.
*/
#include "mat24_functions.h"
#include "clifford12.h"
#include "mm_basics.h"   
#include "mm_op15.h"   
 
// %%EXPORT_KWD MM_OP%{P}_API
  

// %%IF P != 15
// %%END IF 

// %%IF INT_BITS != 64
// %%END IF 


//  %%GEN h
//  %%GEN c


/*********************************************************************
** Auxiliary functions for function mm_op15_eval_X_find_abs
*********************************************************************/

/// @cond DO_NOT_DOCUMENT 



typedef struct {
    uint64_t mask0;
    uint64_t mask1;
    uint32_t *pstart;
    uint32_t *pend;    
} find_short_type;


static void find_short(
    uint_mmv_t *v, 
    uint32_t n, 
    uint32_t offset, 
    find_short_type *pf
)
{
    uint_fast32_t i, j; 
    uint_mmv_t w, w1;
    
    if (pf->pstart >= pf->pend) return;
    if (pf->mask1) for (i = 0; i < n; ++i) {
        // Compute absolute values of entries of v[i] in w
        w = v[i];
        w1 = w & 0x8888888888888888ULL;
        w ^= w1 - (w1 >> 3);
        w &= 0x7777777777777777ULL;

        // Clear bit 3 of an entry in w if that entry is equal to
        // (the corresponding entry in) pf->mask0
        w1 = w ^ pf->mask0;
        w1 += 0x7777777777777777ULL;
        w1 &= 0x8888888888888888ULL;
        // For all entries in w equal to pf->mask0:
        //   Put pf->pstart[0] = offset + index of that entry;
        //   and then increment the pointer pf->pstart.
        //   No action if not pf->pstart < pf->pend.
        if (w1 != 0x8888888888888888ULL) for (j = 0; j < 64; j += 4) {
            if (pf->pstart >= pf->pend) return;
            if (((w1 >> j) & 8) == 0) 
               *pf->pstart++ = offset + (i << 4) + (j >> 2);
        }

        // Clear bit 3 of an entry in w if that entry is equal to
        // (the corresponding entry in) pf->mask1
        w1 = w ^ pf->mask1;
        w1 += 0x7777777777777777ULL;
        w1 &= 0x8888888888888888ULL;
        // For all entries in w equal to pf->mask1:
        //   Put pf->pend[-1] = 0x1000000 + offset + index of that entry;
        //   and then decrement the pointer pf->pend.
        //   No action if not pf->pstart < pf->pend.
        if (w1 != 0x8888888888888888ULL) for (j = 0; j < 64; j += 4) {
            if (pf->pstart >= pf->pend) return;
            if (((w1 >> j) & 8) == 0) 
               *--pf->pend = 0x1000000UL + offset + (i << 4) + (j >> 2);
        }
    } else for (i = 0; i < n; ++i) {
        // Simplified version of the previous case, ignoring  pf->mask1.
        w = v[i];
        w1 = w & 0x8888888888888888ULL;
        w ^= w1 - (w1 >> 3);
        w &= 0x7777777777777777ULL;

        w1 = w ^ pf->mask0;
        w1 += 0x7777777777777777ULL;
        w1 &= 0x8888888888888888ULL;
        if (w1 != 0x8888888888888888ULL) for (j = 0; j < 64; j += 4) {
            if (pf->pstart >= pf->pend) return;
            if (((w1 >> j) & 8) == 0) 
               *pf->pstart++ = offset + (i << 4) + (j >> 2);
        }
    }
}


static int32_t find_short_all(
    uint_mmv_t *v, 
    uint32_t *p_out,
    uint32_t n, 
    uint32_t value0,
    uint32_t value1
)
{
    uint_fast32_t i, j, tmp; 
    uint_mmv_t *v1, a[30];
    find_short_type f;

    if (value0 > 7) value0 = 0;
    if (value0 == 0) return 0;
    if (value1 > 7 || value1 == value0) value1 = 0;
    f.mask0 = value0 * 0x1111111111111111ULL;
    f.mask1 = value1 * 0x1111111111111111ULL;
    f.pstart = p_out;
    f.pend = p_out + n;   

    for (i = 1; i <= 2; ++i) {
        v1 = v + i * 24 * 2 + 2;
        for (j = 0; j < 30; j += 2) {
            a[j] = v1[j] & ((16ULL << (2*j)) - 1ULL);
            a[j+1] = 0;
        }
        find_short(a, 30, i * 24 * 32 + 32, &f);
        v1 += 30;
        for (j = 0; j < 16; j += 2) {
            a[j] = v1[j];
            a[j+1] = v1[j+1]  & ((1ULL << (2*j)) - 1ULL);
        }
        find_short(a, 16, i * 24 * 32 + 16 * 32, &f);
    }
    v1 =  v + MM_OP15_OFS_T;
    find_short(v1, MM_OP15_OFS_Z - MM_OP15_OFS_T, MM_AUX_OFS_T, &f);

    i = (uint32_t)(p_out + n - f.pend);
    for (j = 0; j < i >> 1; ++j) {
        tmp = f.pend[j]; 
        f.pend[j] = f.pend[i - 1 - j];
        f.pend[i - 1 - j] = tmp;
    }
    for (j = 0; j < i; ++j) f.pstart[j] = f.pend[j];
    i = (uint32_t)(f.pstart - p_out) + i;

    for (j = 0; j < i; ++j) {
        tmp = mm_aux_index_intern_to_sparse(p_out[j] & 0xffffffUL);
        tmp = mm_aux_index_sparse_to_leech2(tmp);
        p_out[j] = (p_out[j] & 0xff000000UL) | (tmp & 0xffffffUL);
    }
    return i;
}

/// @endcond 



/**
  @brief Find certain entries of a vector of the monster rep modulo 15

  Let ``v`` be a vector of the monster group representation modulo 15.
  The function tries to find all entries of the monomial part of ``v``
  with absolute values ``y0`` and ``y1``, ``1 <= y0, y1 <= 7``.
  In case ``y1 = 0`` entries with value ``y1`` are ignored.
   
  Here the monomial part of ``v`` consists of the entries with
  tags 'B', 'C', 'T', 'X'. The coordinates of these entries
  correspond to the short vectors of the Leech lattice.

  Output is written into the array ``p_out`` of length ``n``. If the
  monomial part of ``v`` contains an entry with absolute value ``y0``
  then the coordinate of that entry is written into array ``p_out``
  in **Leech lattice encoding**. If that part of ``v`` contains an
  entry with absolute value ``y1`` then the coordinate of that entry
  is witten into that array in the same encoding.

  In addition, for entries in ``v`` with absolute value  ``y1`` the
  bit 24 of the corresponding entry in ``p_out`` is set. In ``p_out``,
  the entries with absolute value ``y1`` are stored after those with
  absolute value ``y0``. Entries with the same absolute value are
  stored in the same order as in ``v``.

  The function returns the number of valid entries in the
  array ``p_out``. If the length ``n`` of ``p_out`` is too small then
  some entries will be dropped without notice.
*/
// %%EXPORT px
MM_OP15_API
uint32_t mm_op15_eval_X_find_abs(uint_mmv_t *v, uint32_t *p_out, uint32_t n,  uint32_t y0, uint32_t y1)
{
     return find_short_all(v, p_out, n, y0, y1);
}


/*********************************************************************
** Auxiliary functions for function mm_op15_eval_X_count_abs
*********************************************************************/

/// @cond DO_NOT_DOCUMENT 


static inline void count_short24(
    uint_mmv_t *v, 
    uint32_t n, 
    uint_fast32_t *p_out
)
{
   uint32_t i;
   for (i = 0; i < n; ++i) {
       uint_mmv_t w = v[0];
       // %%FOR j in range(0, 64, 4)
       ++p_out[(w >> 0) & 15];
       ++p_out[(w >> 4) & 15];
       ++p_out[(w >> 8) & 15];
       ++p_out[(w >> 12) & 15];
       ++p_out[(w >> 16) & 15];
       ++p_out[(w >> 20) & 15];
       ++p_out[(w >> 24) & 15];
       ++p_out[(w >> 28) & 15];
       ++p_out[(w >> 32) & 15];
       ++p_out[(w >> 36) & 15];
       ++p_out[(w >> 40) & 15];
       ++p_out[(w >> 44) & 15];
       ++p_out[(w >> 48) & 15];
       ++p_out[(w >> 52) & 15];
       ++p_out[(w >> 56) & 15];
       ++p_out[(w >> 60) & 15];
       // %%END FOR j 
       w = v[1];
       // %%FOR j in range(0, 32, 4)
       ++p_out[(w >> 0) & 15];
       ++p_out[(w >> 4) & 15];
       ++p_out[(w >> 8) & 15];
       ++p_out[(w >> 12) & 15];
       ++p_out[(w >> 16) & 15];
       ++p_out[(w >> 20) & 15];
       ++p_out[(w >> 24) & 15];
       ++p_out[(w >> 28) & 15];
       // %%END FOR 
       v += 2;
   }
}


static inline void count_short64(
    uint_mmv_t *v, 
    uint32_t n, 
    uint_fast32_t *p_out
)
{
   uint32_t i;
   for (i = 0; i < (n << 2); ++i) {
       uint_mmv_t w = v[i];
       // %%FOR j in range(0, 64, 4)
       ++p_out[(w >> 0) & 15];
       ++p_out[(w >> 4) & 15];
       ++p_out[(w >> 8) & 15];
       ++p_out[(w >> 12) & 15];
       ++p_out[(w >> 16) & 15];
       ++p_out[(w >> 20) & 15];
       ++p_out[(w >> 24) & 15];
       ++p_out[(w >> 28) & 15];
       ++p_out[(w >> 32) & 15];
       ++p_out[(w >> 36) & 15];
       ++p_out[(w >> 40) & 15];
       ++p_out[(w >> 44) & 15];
       ++p_out[(w >> 48) & 15];
       ++p_out[(w >> 52) & 15];
       ++p_out[(w >> 56) & 15];
       ++p_out[(w >> 60) & 15];
       // %%END FOR 
   }
}


/// @endcond


/**
  @brief Count certain entries of a vector of the monster rep modulo 15

  Let ``v`` be a vector of the monster group representation modulo 15.
  The function counts the absolute values of all entries of the monomial 
  part of ``v``.
   
  Here the monomial part of ``v`` consists of the entries with
  tags 'B', 'C', 'T', 'X'. The coordinates of these entries
  correspond to the short vectors of the Leech lattice.

  Output is written into the array ``p_out`` of length  8.
  Entry ``p_out[i]`` contains the number if entries of the monomial 
  part of ``v`` with absolute value ``i`` for ``0 <= i <= 7``. 
*/
// %%EXPORT px
MM_OP15_API
void mm_op15_eval_X_count_abs(uint_mmv_t *v, uint32_t *p_out)
{
     uint_fast32_t a[16], i;

     for (i = 0; i < 16; ++i) a[i] = 0;
     count_short24(v + MM_OP15_OFS_B, 48, a);
     a[0] = (a[0] + a[15] - 48) >> 1;
     for (i = 1; i < 15; ++i) a[i] >>= 1;
     a[15] = 0;
     count_short64(v + MM_OP15_OFS_T, 759, a);
     count_short24(v + MM_OP15_OFS_X, 2048, a);
     for (i = 0; i < 8; ++i) p_out[i] = a[i] + a[15-i];
}



/*************************************************************************
*** Analyze type of a 2A axis
*************************************************************************/


//  %%GEN h
//  %%GEN c

