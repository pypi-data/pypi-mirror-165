/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm15_op_word.c

 File ``mm15_op_word.c`` implements the operation of the monster
 group on a vector in the representation  \f$\rho_{15}\f$ of the
 monster.

 Here an element of the monster group is implemented as a word of
 atoms as described in the documentation of the header file
 ``mmgroup_generators.h``.

 The representation \f$\rho_{15}\f$ is equal to the
 196884-dimensional representation  \f$\rho\f$ of the monster,
 with coefficients taken modulo 15, as defined in
 section **The representation of the monster group**
 in the **API reference**.

 An element of \f$\rho_{15}\f$ is implemented as an array of
 integers of type ``uint_mmv_t`` as described in
 section **Description of the mmgroup.mm extension** 
 in this document.

 The functions in this module use functions from modules
 ``mm15_op_pi.c``, ``mm15_op_xy.c``, ``mm15_op_t.c``, and
 ``mm15_op_xi.c`` for implementing the operations of the 
 different kinds of atoms generating the monster group.
*/


#include "mm_op15.h"   
   
// %%EXPORT_KWD MM_OP%{P}_API


//  %%GEN h
//  %%GEN c


/// @cond DO_NOT_DOCUMENT 
#define h (s_it.data)
/// @endcond


//////////////////////////////////////////////////////////////////////////
// Operation of a word of the monster group on a vector
//////////////////////////////////////////////////////////////////////////


/** 
  @brief Compute operation of the monster group on a vector

  Let \f$v\f$ be a vector of the representation \f$\rho_{15}\f$
  of the monster group stored in the array referred by ``v``.

  Let \f$g\f$ be the element of the monster group stored in the
  array of length ``len_g`` referred by the pointer ``g``.

  Then the function computes the vector \f$v \cdot g^e\f$  and 
  overwrites the vector in the array ``v`` with that vector.
  Here \f$e\f$ is the exponent given by the integer ``e``.

  The function requires a work buffer (referrd by ``work``), which
  is an array of ``MM_OP{P}_LEN_V`` entries of type ``uint_mmv_t``.
  So the work buffer has the same size as the vector ``v``.

  The function returns 0 in case of success and a nonzero
  value in case of failure.

  Internally, the function simplifies all substrings of the string 
  representing the word \f$g^e\f$, except for atoms corresponding
  to nonzero powers of the generator \f$\xi\f$. So the user need 
  not 'optimize' the input \f$g\f$. Of course, this simplification
  does not change the input array ``g``.
*/ 
// %%EXPORT px
MM_OP15_API
uint32_t mm_op15_word(uint_mmv_t *v, uint32_t *g, int32_t len_g, int32_t e, uint_mmv_t *work)
{
     uint32_t status;
     uint_mmv_t *p0 = v, *p1 = work, *pt;
     mm_group_iter_t s_it;



     mm_group_iter_start(&s_it, g, len_g, e);
     do {
         status = mm_group_iter_next(&s_it);
         if (h[0]) {
             mm_op15_xi(p0, h[0], p1); 
             pt = p0; p0 = p1; p1 = pt;
         }
         if (h[1]) {
             mm_op15_t(p0, h[1], p1);
             pt = p0; p0 = p1; p1 = pt;
         }
         if (h[2] | h[3]) {
             mm_op15_xy(p0, h[2], h[3], h[4], p1);
             h[4] = 0;
             pt = p0; p0 = p1; p1 = pt;
         }
         if (h[5]) {
             mm_op15_pi(p0, h[4], h[5], p1);
             pt = p0; p0 = p1; p1 = pt;
         } else if (h[4]) {
             mm_op15_delta(p0, h[4], p1);
             pt = p0; p0 = p1; p1 = pt;
         }
     } while (status == 0);
     
     if (p0 != v) mm_op15_copy(work, v);
     return status - 1;
}


/** 
  @brief Restriction of function ``mm_op15_word`` to tag ``A``

  Function ``mm_op15_pi`` computes the operation of an element
  \f$h = g^e\f$ of the monster  group a vector ``v`` and
  overwrites ``v`` with the result of that operation. \f$h\f$
  depends on parameters ``g, len_g,``  and ``e`` of this function.

  Function ``mm_op15_word_tag_A`` computes the same automorphism 
  on the entries of the vector ``v`` with tag ``A`` only, and 
  ignores the other entries of ``v``.
  See section **The representation of the monster group**
  in the **API reference** for tags of entries of a vector in
  the representation of the monster.

  The function overwrites the vector ``v`` with the result. 
  Here only entries of ``v`` with tag ``A`` are changed. 

  Parameters and return value are the same as in function
  ``mm_op15_word``, except that a work buffer is not required
  here. Also, the function fails and returns a nonzero value,
  if the word that makes up the group element \f$h\f$ contains
  any nonzero powers of the generator \f$\tau\f$ of the 
  monster group. Note that such a power of \f$\tau\f$ does 
  not fix the the part of the vector ``v`` with tag ``A``.
  Powers of the generator \f$\tau\f$ correspond to atoms with
  tag ``t``.

  This function is much faster than function ``mm_op15_word``.
*/ 
// %%EXPORT px
MM_OP15_API
int32_t mm_op15_word_tag_A(uint_mmv_t *v, uint32_t *g, int32_t len_g, int32_t e)
{
     uint32_t status;
     mm_group_iter_t s_it;

     mm_group_iter_start(&s_it, g, len_g, e);
     do {
         status = mm_group_iter_next(&s_it);
         if (h[0])  mm_op15_xi_tag_A(v, h[0]); 
         if (h[1])  return -1;
         if (h[2])  mm_op15_xy_tag_ABC(v, h[2], 0, 0, 1);
         if (h[5])  mm_op15_pi_tag_ABC(v, 0, h[5], 1);
     } while (status == 0);
     if (mm_aux_reduce_mmv_fields(15, v, MM_AUX_OFS_B) < 0) return -1;
     return status - 1;
}

/// @cond DO_NOT_DOCUMENT 
#undef  h 
/// @endcond

//////////////////////////////////////////////////////////////////////////
// ABC part of pperation of a word of the monster group on a vector
//////////////////////////////////////////////////////////////////////////


/// @cond DO_NOT_DOCUMENT 

static inline int32_t
extract_BC(uint_mmv_t *v_in, uint32_t *a, uint_mmv_t *v_out)
{
    #define make_index(row, column) (((row) << 5) + (column))
    #define store(index, value) v_out[(index) >> 4] |= \
        (value) << (((index) << 2) & 63)

    uint_fast32_t i, j, index, c, sparse;
    uint_mmv_t value;

    v_out += MM_OP15_OFS_B; // point to part B of output vector
    for (i = 0; i < 96; ++i) v_out[i] = 0;

    for (i = 0; i < 24; ++i) {
        for (j = i + 1; j < 24; ++j) {
            c = a[j];
            sparse = mm_aux_index_leech2_to_sparse(c);
            if (sparse == 0) return -1;
            sparse |= (0 - ((c >> 24) & 1)) & 15;
            value  = mm_aux_mmv_get_sparse(15, v_in, sparse) & 15;
            index = make_index(i, j); 
            store(index, value);
            index = make_index(j, i); 
            store(index, value);

            gen_leech2_def_mul(a[0], a[j], c);
            sparse = mm_aux_index_leech2_to_sparse(c);
            sparse |= (0 - ((c >> 24) & 1)) & 15;
            value  = mm_aux_mmv_get_sparse(15, v_in, sparse) & 15;
            index = make_index(24 + i, j); 
            store(index, value);
            index = make_index(24 + j, i); 
            store(index, value);

            if (j > i + 1) {
                gen_leech2_def_mul(a[i+1], a[j], c);
                a[j] = c;
            }
        }         
    }
    return 0;

    #undef make_index
    #undef store
}

/// @endcond 


/** 
  @brief Compute ABC part of the operation of the monster group on a vector

  Let \f$v\f$ be a vector of the representation \f$\rho_{15}\f$
  of the monster group stored in the array referred by ``v``.

  Let \f$g\f$ be the element of the monster group stored in the
  array of length ``len_g`` referred by the pointer ``g``. Here
  \f$g\f$, and also all prefixes of the word representing \f$g\f$,
  must be in the set \f$G_{x0} \cdot N_0\f$.

  The function computes the parts with tags ``A``, ``B``, and ``C``
  of the vector \f$v \cdot g\f$  and stores the result in the
  array ``v_out``. The other parts of the vector \f$v \cdot g\f$
  are not computed. Here the array ``a_out`` must have at
  least 144 entries of type ``uint_mmv_t``.

  This function is much faster than function ``mm_op15_word``.
  It is mainly used for dealing with a 2A axis \f$v\f$.
*/
// %%EXPORT px
MM_OP15_API
int32_t mm_op15_word_ABC(uint_mmv_t *v, uint32_t *g, int32_t len_g, uint_mmv_t *v_out)
{
    uint32_t g1[12], *pg1;
    int32_t len_g1;
    len_g1 = mm_group_prepare_op_ABC(g, len_g, g1);
    if ((len_g1 & 0xff) > 11) return  -300003;
    if (len_g1 < 0) return len_g1 - 100000;
    if (len_g1 & 0x100) {
        uint32_t i;
        for (i = 0; i < 144; ++i) v_out[i] = v[i];
        len_g1 &= 0xff;
        pg1 = g1;
    } else {
        uint32_t i, subframe[24];
        int32_t len_g0, res;
        len_g1 &= 0xff;  
        for (i = 0; i < 48; ++i) v_out[i] = v[i];
        len_g0 =  gen_leech2_prefix_Gx0(g1, len_g1);
        res = mm_op15_word_tag_A(v_out, g1, len_g0, 1);
        if (res < 0) return res - 400000;
        mm_group_invert_word(g1, len_g0);
        res = gen_leech2_map_std_subframe(g1, len_g0, subframe);
        if (res != len_g0) return (len_g0 < 0) ? len_g0 - 200000 :-300001;
        if (extract_BC(v, subframe, v_out)) return -300002;
        if (res < 0) return res - 500000;
        pg1 = g1 + len_g0; len_g1 -= len_g0;
    }

    if (len_g1 == 0) return 0;
    // Set Termination atom in order to simplify scanning subwords of g1
    pg1[len_g1] = 0xffffffff; 

    // Deal with tag t
    if (((pg1[0] >> 28) & 0xf) == 5) {
        mm_op15_t_ABC(v_out, pg1[0] & 0xfffffff);
        pg1++; len_g1--;
    }

    if (len_g1 == 0) return 0;
    {
        // Deal with tag sequence 'y', 'x', 'd'
        uint32_t y = 0, x = 0, d = 0, *pg2 = pg1;

        // tags x_e, y_e, x_\epsilon perform no action on part ABC
        // of the vector if e in \{+-1, +-\Omega\} or if \epsilon
        // is an even cocode element. 
        if (((pg2[0] >> 28) & 0xf) == 4)  y = *pg2++ & 0x7ff;
        if (((pg2[0] >> 28) & 0xf) == 3)  x = *pg2++ & 0x7ff;
        if (x | y && ((pg2[0] >> 28) & 0xf) == 1) d = *pg2++ & 0xfff; 
        if (pg2 > pg1) {
            if (x | y) mm_op15_xy_tag_ABC(v_out, y, x, d, 0);
            len_g1 -= (uint32_t)(pg2 - pg1);
            if (len_g1 == 0) return 0;
            pg1 = pg2;
        }
    }

    {
        // Deal with tag sequence 'd', 'p'
        uint32_t d = 0, pi = 0, *pg2 = pg1;

        if (((pg2[0] >> 28) & 0xf) == 1)  d = *pg2++ & 0x800;
        if (((pg2[0] >> 28) & 0xf) == 2)  pi = *pg2++ & 0xfffffff;
        if (pg2 > pg1) {
            if (pi) mm_op15_pi_tag_ABC(v_out, d, pi, 0);
            else if (d) mm_op15_delta_tag_ABC(v_out, d, 0);
            len_g1 -= (uint32_t)(pg2 - pg1);
        }
    }
    return len_g1 ? -600000 - len_g1 : 0;
}




//  %%GEN h
//  %%GEN c
