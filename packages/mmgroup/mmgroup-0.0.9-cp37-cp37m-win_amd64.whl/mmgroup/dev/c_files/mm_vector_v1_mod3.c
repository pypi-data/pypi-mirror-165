/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm_vector_v1_mod3.c

 File ``mm_vector_v1_mod3`` contains a precomuted vector ``v1_mod3``
 of the representtion of the monster group (mod 3). This vector can
 be used for obtaining an (unknown) element \f$g\f$ of the
 subgroup \f$G_{x0}\f$ of the monster from and image of that vector
 under \f$g\f$.

 So the functions in this module are similar to those in
 module ``mm_order.c``, but faster.

 Note that we cannot check membership in \f$G_{x0}\f$
 with the functions in this module!

 This module is yet a stub!!!
*/

/// @cond DO_NOT_DOCUMENT 
#include "mat24_functions.h"
#include "clifford12.h"
#include "mm_op3.h"   
#include "mm_reduce.h"   
/// @endcond

   
// %%EXPORT_KWD MM_REDUCE_API




//  %%GEN h
//  %%GEN c


/************************************************************************
** order vector tag table
************************************************************************/

/// @cond DO_NOT_DOCUMENT 

static  uint32_t V1_MOD3_DATA[] = {
// %%TABLE V1_MOD3_DATA, uint32
0x02004002UL,0x02008002UL,0x0200c002UL,0x02010002UL,
0x02014002UL,0x02018002UL,0x02020002UL,0x02024002UL,
0x02028002UL,0x02030002UL,0x02040002UL,0x04004002UL,
0x04008002UL,0x0400c002UL,0x04010002UL,0x04014002UL,
0x04018002UL,0x04020002UL,0x04024002UL,0x04028002UL,
0x04030002UL,0x04040002UL,0x06004002UL,0x0a000002UL,
0x0a004002UL,0x0a008002UL,0x0a010002UL,0x0a020002UL,
0x0a040002UL,0x0a080002UL,0x0a100002UL,0x0a200002UL,
0x0a400002UL,0x0a800002UL,0x0b000002UL,0x0c000202UL,
0x0c000301UL,0x02000002UL,0x0201c702UL,0x0202cb02UL,
0x02034d02UL,0x02038e02UL,0x0203cf02UL,0x02045102UL,
0x02049202UL,0x0204d302UL,0x02051402UL,0x02055502UL,
0x02059601UL,0x02024601UL,0x02018601UL,0x02024802UL,
0x02024502UL,0x02024301UL,0x02020401UL,0x02008202UL,
0x02010101UL,0x02028a01UL,0x02040501UL,0x02014501UL,
0x02014201UL,0x02018301UL,0x0fded102UL,0x0f84d201UL,
0x0ef49202UL,0x0ef08c01UL,0x0f48d302UL,0x0ee2c002UL,
0x0ee3cb01UL,0x0f10cc02UL,0x0f654401UL,0x0ea5cd02UL
};


// %%USE_TABLE
static  uint32_t V1_MOD3_TAG_DATA[] = {
// %%TABLE V1_MOD3_TAG_DATA, uint32
0x00000017UL,0x0000800cUL,0x00008021UL,0x00008410UL,
0x00008423UL,0x00008849UL,0x00100416UL,0x0010840aUL,
0x00108446UL,0x02004002UL,0x02008002UL,0x0200c002UL,
0x02010002UL,0x02014002UL,0x02018002UL,0x02020002UL,
0x02024002UL,0x02028002UL,0x02030002UL,0x02040002UL,
0x000005f8UL,0x000006f8UL,0x000007f8UL,0x000000c7UL,
0x00000080UL,0x00000040UL,0x00000039UL,0x00000020UL,
0x00000010UL,0x0000000aUL,0x0000000cUL,0x00000600UL,
0x00000500UL,0x00000700UL,0x0000040fUL,0x0000008fUL,
0x0000004fUL,0x0000040eUL,0x0000002eUL,0x0000001eUL,
0x0000040dUL,0x0000040bUL,0x00800600UL,0x00000800UL,
0x0000180eUL,0x0000280dUL,0x0000480bUL,0x00008807UL,
0x0001080fUL,0x0002080fUL,0x0004080eUL,0x0008080eUL,
0x00100c01UL,0x00200c01UL,0x00400800UL,0x005f8bf7UL,
0x006f83f7UL,0x007f83f7UL,0x000c7338UL,0x00080000UL,
0x00040000UL,0x000393c9UL,0x00020000UL,0x00010000UL,
0x0000a00aUL,0x0000c00cUL,0x00000800UL,0x008007ffUL,
0x00000001UL,0x00000002UL,0x00000004UL,0x00000008UL,
0x00000010UL,0x00000020UL,0x00000040UL,0x00000080UL,
0x00000100UL,0x00000200UL,0x00000400UL
};


// Length of table V1_MOD3_DATA
#define LEN_V1_MOD3  72

/// @endcond 





/************************************************************************
** load order vector
************************************************************************/

/// @cond DO_NOT_DOCUMENT 



// Offsets in order vector stored in the table
#define OFS3_WATERMARK_PERM  0
#define OFS3_TAGS_Y          9
#define OFS3_SOLVE_Y        20
#define OFS3_TAGS_X         31
#define OFS3_SOLVE_X        55

#define OFS3_Z  (116416 >> 5)



/// @endcond 

/** 
  @brief Load order vector from tables to a buffer

  The function stores the precomputed vector ``v1_mod3`` into the
  array referred by ``p_dest``. That array must must be sufficiently
  long to store a vector of the representation  \f$\rho_{3}\f$.
 
*/
// %%EXPORT px
MM_REDUCE_API
void mm_order_load_vector_v1_mod3(uint_mmv_t *p_dest)
{
    mm_aux_zero_mmv(3, p_dest);
    mm_aux_mmv_add_sparse(3, V1_MOD3_DATA, 72, p_dest);
}


/************************************************************************
** Check if a vector is equal to the order vector
************************************************************************/




/** 
  @brief Compare vector with precomputed order vector
  
  The function compares the vector \f$v\f$ in the
  representation \f$\rho_{3}\f$ of the monster group referred
  by ``v`` with  \f$v_1\f$ , where  \f$v_1\f$ is
  the precomute vector ``v1_mod3``.

  The function returns 0 in case of equality and 1 otherwise.
  It destroys the vector in the buffer ``v``.
*/
// %%EXPORT px
MM_REDUCE_API
int32_t mm_order_compare_v1_mod3(uint_mmv_t *v)
{  
    uint32_t a[LEN_V1_MOD3];
    uint32_t i;
    for (i = 0; i < LEN_V1_MOD3; ++i) {
        a[i] = V1_MOD3_DATA[i] ^3;
    }
    mm_aux_mmv_add_sparse(3, a, LEN_V1_MOD3, v);
    return mm_op3_checkzero(v);
}



/************************************************************************
** Find an element of G_x0
************************************************************************/


/// @cond DO_NOT_DOCUMENT 

#define error(pos, err) (int32_t)(((-pos << 24) + err) | 0x80000000UL)

/// @endcond 



/** 
  @brief Find an element \f$g\f$ of the subgroup \f$G_{x0}\f$ 

  Yet to be documented!!!
*/
// %%EXPORT px
MM_REDUCE_API
int32_t mm_order_find_Gx0_via_v1_mod3(uint_mmv_t *v,  uint32_t *g)
{
    uint64_t w3 = mm_op3_eval_A_rank_mod3(v, 0);
    uint32_t w_type4 = (uint32_t)(gen_leech3to2_type4(w3));
    int32_t len, i, res, v_y, y, v_x, x;
    uint64_t A[24], elem_g_i[26];
    uint32_t perm_num, g_inv[8], v_sign, aa, sign;


    if ((w3 >> 48) != 23 || (w3 & 0xffffffffffffULL) == 0) return -0x101;
    if (w_type4 == 0) return -0x102;
    len = gen_leech2_reduce_type4(w_type4, g);
    if (len < 0) return error(2, len);
    for (i = 0; i < 24; ++i) A[i] = v[i];
    res = mm_op3_word_tag_A(A, g, len, 1);
    if (res < 0) return error(3, res);
    res =  mm_op3_watermark_A_perm_num(
        V1_MOD3_TAG_DATA +  OFS3_WATERMARK_PERM, A);
    if (res < 0) return error(4, res);
    perm_num = res;
    if (perm_num) {
        g[len] = 0xA0000000UL + perm_num;
        res = mm_op3_word_tag_A(A, g + len, 1, 1);
        if (res < 0) return error(5, res);
        len += 1;
    }
    v_y = mm_aux_mmv_extract_sparse_signs(3, A, 
        V1_MOD3_TAG_DATA + OFS3_TAGS_Y, 11);
    if (v_y < 0) return  error(6, v_y);
    y = leech2matrix_solve_eqn(
        V1_MOD3_TAG_DATA + OFS3_SOLVE_Y, 11, v_y);
    if (y > 0) {
        g[len] = 0xC0000000 + y;
        res = mm_op15_word_tag_A(A, g + len, 1, 1);
        if (res < 0) return error(7, res);
        len += 1;
    }

    for (i = 0; i < len; ++i) g_inv[i] = g[len-1-i] ^ 0x80000000;
    res = xsp2co1_set_elem_word(elem_g_i, g_inv, len);
    if (res < 0) return error(8, res);
    v_x = mm_aux_mmv_extract_x_signs(3, v, elem_g_i, 
        V1_MOD3_TAG_DATA + OFS3_TAGS_X, 24);
    if (v_x < 0) return  error(9, v_x);
    x = leech2matrix_solve_eqn(V1_MOD3_TAG_DATA + OFS3_SOLVE_X, 24, v_x);
    v_sign = ((x >> 12) & 0x7ff) ^ (x & 0x800);
    aa = xsp2co1_elem_read_mod3(v + OFS3_Z, elem_g_i, v_sign, 24); 
    sign = aa - 1;
    if (sign & 0xfffffffe) return -0x104;
    sign ^= uint64_parity(x & (x >> 12) & 0x7ff);
    x ^= sign << 24;

    x ^= mat24_ploop_theta(x >> 12);
    if (x & 0xfff)  g[len++] = 0x90000000 + (x & 0xfff); 
    x = (x >> 12) & 0x1fff;
    if (x) g[len++] = 0xB0000000 + x;
    return len;
}



//  %%GEN h
//  %%GEN c
