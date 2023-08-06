/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm15_op_pi.c

 File ``mm15_op_pi.c`` implements the operation of the
 generators \f$x_\pi\f$ and \f$x_\delta\f$ of the monster group
 on a vector in the representation \f$\rho_{15}\f$ of the
 monster.

 Here generators \f$x_\pi\f$ and \f$x_\delta\f$ are defined as
 automorphisms of the Parker loop as in section **The monster group**
 of the **API reference**. An automophism of the Parker loop is
 specified by a pair of integers ``d, p`` as in the constructor
 of the Python class ``AutPL``, see
 section **Automophisms of the Parker loop** in the **API reference**.

 The representation \f$\rho_{15}\f$ is equal to the
 196884-dimensional representation  \f$\rho\f$ of the monster,
 with coefficients taken modulo 15, as defined in
 section **The representation of the monster group**
 in the **API reference**.

 An element of \f$\rho_{15}\f$ is implemented as an array of
 integers of type ``uint_mmv_t`` as described in
 section **Description of the mmgroup.mm extension** 
 in this document.

 The exact operation of an automorphism of the Parker loop on
 \f$\rho\f$ is as defined in [Seysen19].

 Note that the integers ``d, p`` mentioned above describe the
 number of an element of the Golay cocode and the number of a
 permutation in the Mathieu group  \f$M_{24}\f$, respectively.
 Internally, we use the C functions in file ``mat24_functions.c`` 
 and the function ``mm_sub_prep_pi`` in file ``mm_tables.c`` for
 converting the  integers ``d, p`` to mathematical objects that
 can be used for implementing the operation on \f$\rho_{15}\f$.
 These conversions are very fast compared to the cost for
 the operation on \f$\rho_{15}\f$. This helps us to keep
 the C interface for these  operations simple.

*/

#include <string.h>
#include "mm_op15.h"   

// %%EXPORT_KWD MM_OP%{P}_API


//  %%GEN h
//  %%GEN c



/// @cond DO_NOT_DOCUMENT 
   
static const uint_mmv_t MM15_TBL_SCALPROD_HIGH[] = { 
// %%TABLE MMV_TBL_SCALPROD_HIGH, uint%{INT_BITS}
0x0000000000000000ULL,0x0000000000000000ULL,
0xff000000ff000000ULL,0x000000000ff0f0f0ULL,
0xf0f00000f0f00000ULL,0x00000000ff000ff0ULL,
0x0ff000000ff00000ULL,0x00000000f0f0ff00ULL,
0xff0000000000ff00ULL,0x00000000f0f00ff0ULL,
0x00000000ff00ff00ULL,0x00000000ff00ff00ULL,
0x0ff00000f0f0ff00ULL,0x000000000ff00000ULL,
0xf0f000000ff0ff00ULL,0x000000000000f0f0ULL,
0xf0f000000000f0f0ULL,0x000000000ff0ff00ULL,
0x0ff00000ff00f0f0ULL,0x0000000000000ff0ULL,
0x00000000f0f0f0f0ULL,0x00000000f0f0f0f0ULL,
0xff0000000ff0f0f0ULL,0x00000000ff000000ULL,
0x0ff0000000000ff0ULL,0x00000000ff00f0f0ULL,
0xf0f00000ff000ff0ULL,0x00000000f0f00000ULL,
0xff000000f0f00ff0ULL,0x000000000000ff00ULL,
0x000000000ff00ff0ULL,0x000000000ff00ff0ULL,
0x000f000f000ffff0ULL,0x00000000000f000fULL,
0xff0f000fff0ffff0ULL,0x000000000ffff0ffULL,
0xf0ff000ff0fffff0ULL,0x00000000ff0f0fffULL,
0x0fff000f0ffffff0ULL,0x00000000f0ffff0fULL,
0xff0f000f000f00f0ULL,0x00000000f0ff0fffULL,
0x000f000fff0f00f0ULL,0x00000000ff0fff0fULL,
0x0fff000ff0ff00f0ULL,0x000000000fff000fULL,
0xf0ff000f0fff00f0ULL,0x00000000000ff0ffULL,
0xf0ff000f000f0f00ULL,0x000000000fffff0fULL,
0x0fff000fff0f0f00ULL,0x00000000000f0fffULL,
0x000f000ff0ff0f00ULL,0x00000000f0fff0ffULL,
0xff0f000f0fff0f00ULL,0x00000000ff0f000fULL,
0x0fff000f000ff000ULL,0x00000000ff0ff0ffULL,
0xf0ff000fff0ff000ULL,0x00000000f0ff000fULL,
0xff0f000ff0fff000ULL,0x00000000000fff0fULL,
0x000f000f0ffff000ULL,0x000000000fff0fffULL
};

static const uint_mmv_t MM15_TBL_SCALPROD_LOW[] = { 
// %%TABLE MMV_TBL_SCALPROD_LOW, uint%{INT_BITS}
0x0000000000000000ULL,0x0000000000000000ULL,
0xffffffffffff0000ULL,0x00000000ffff0000ULL,
0xffffffffffff0000ULL,0x000000000000ffffULL,
0x0000000000000000ULL,0x00000000ffffffffULL,
0xff00ff0000000000ULL,0x00000000ff00ff00ULL,
0x00ff00ffffff0000ULL,0x0000000000ffff00ULL,
0x00ff00ffffff0000ULL,0x00000000ff0000ffULL,
0xff00ff0000000000ULL,0x0000000000ff00ffULL,
0xf0f0f0f000000000ULL,0x00000000f0f0f0f0ULL,
0x0f0f0f0fffff0000ULL,0x000000000f0ff0f0ULL,
0x0f0f0f0fffff0000ULL,0x00000000f0f00f0fULL,
0xf0f0f0f000000000ULL,0x000000000f0f0f0fULL,
0x0ff00ff000000000ULL,0x000000000ff00ff0ULL,
0xf00ff00fffff0000ULL,0x00000000f00f0ff0ULL,
0xf00ff00fffff0000ULL,0x000000000ff0f00fULL,
0x0ff00ff000000000ULL,0x00000000f00ff00fULL
};

/// @endcond 



/***************************************************************
* Auxiliary functions
***************************************************************/

/// @cond DO_NOT_DOCUMENT 

// %%EXPORT
MM_OP15_API
void mm_op15_neg_scalprod_d_i(uint_mmv_t* v)
// negate entries d (x) i with sclar product equal to 1
{
    const uint_mmv_t* p0 = MM15_TBL_SCALPROD_HIGH;
    const uint_mmv_t* p0_end = p0 + 32 * 2;

    // inversion of entries (d (x) i) with scalar product 1
    for (; p0 < p0_end; p0 += 2) {
        const uint_mmv_t* p1 = MM15_TBL_SCALPROD_LOW;
        const uint_mmv_t* p1_end = p1 + 16 * 2;
        for (; p1 < p1_end; p1 += 2) {
            // %%SCALAR_PROD_2048_UNROLL p0, p1, v 
            uint_mmv_t v_t;
            v[0] ^= (v_t = p0[0] ^ p1[0]);
            v[2] ^= v_t ^ 0xffff0000ffff0000ULL;
            v[4] ^= v_t ^ 0xffffffff0000ULL;
            v[6] ^= v_t ^ 0xffffffff00000000ULL;
            v[1] ^= (v_t = p0[1] ^ p1[1]);
            v[3] ^= v_t ^ 0xffffffffULL;
            v[5] ^= v_t ^ 0xffffffffULL;
            v[7] ^= v_t ^ 0x0ULL;
            v +=   4 * 2;
        }
    }
}

/// @endcond



/// @cond DO_NOT_DOCUMENT 

/**
   @brief perform permutation on rows of length 24

*/
static void pi24_n(
   uint_mmv_t * p_src,
   uint16_t * p_perm,
   uint8_t * pf,
   uint_mmv_t * p_dest,
   uint32_t n
)
{
    uint_fast32_t i1;
    for (i1 = 0; i1 < n; ++i1) {
        uint_mmv_t sgn_perm = p_perm[i1];
        uint_mmv_t *ps = p_src + ((sgn_perm & 0x7ff) << 1);

        sgn_perm >>= 15;  // sign for permutation
        sgn_perm = 0 - (sgn_perm & 1);
        // %%FOR i in range(V24_INTS_USED)  
        sgn_perm &= 0xffffffffffffffffULL;
        p_dest[0] = sgn_perm  ^ (
            (((ps[pf[0]] >> pf[1]) & 15) << 0) |
            (((ps[pf[2]] >> pf[3]) & 15) << 4) |
            (((ps[pf[4]] >> pf[5]) & 15) << 8) |
            (((ps[pf[6]] >> pf[7]) & 15) << 12) |
            (((ps[pf[8]] >> pf[9]) & 15) << 16) |
            (((ps[pf[10]] >> pf[11]) & 15) << 20) |
            (((ps[pf[12]] >> pf[13]) & 15) << 24) |
            (((ps[pf[14]] >> pf[15]) & 15) << 28) |
            (((ps[pf[16]] >> pf[17]) & 15) << 32) |
            (((ps[pf[18]] >> pf[19]) & 15) << 36) |
            (((ps[pf[20]] >> pf[21]) & 15) << 40) |
            (((ps[pf[22]] >> pf[23]) & 15) << 44) |
            (((ps[pf[24]] >> pf[25]) & 15) << 48) |
            (((ps[pf[26]] >> pf[27]) & 15) << 52) |
            (((ps[pf[28]] >> pf[29]) & 15) << 56) |
            (((ps[pf[30]] >> pf[31]) & 15) << 60));
        sgn_perm &= 0xffffffffULL;
        p_dest[1] = sgn_perm  ^ (
            (((ps[pf[32]] >> pf[33]) & 15) << 0) |
            (((ps[pf[34]] >> pf[35]) & 15) << 4) |
            (((ps[pf[36]] >> pf[37]) & 15) << 8) |
            (((ps[pf[38]] >> pf[39]) & 15) << 12) |
            (((ps[pf[40]] >> pf[41]) & 15) << 16) |
            (((ps[pf[42]] >> pf[43]) & 15) << 20) |
            (((ps[pf[44]] >> pf[45]) & 15) << 24) |
            (((ps[pf[46]] >> pf[47]) & 15) << 28));
        // %%END FOR   #  FOR i
        p_dest +=  2;      
    }
}



// %%IF PERM24_USE_BENES_NET

static void pi24_2048(
   uint_mmv_t * p_src,
   uint16_t * p_perm,
   uint_mmv_t * benes_mask,
   uint_fast32_t sign_shift,
   uint_mmv_t * p_dest
)
{
    uint_fast32_t i1;
    for (i1 = 0; i1 < 2048; i1 += 4) {
        uint_mmv_t sgn_perm0 = p_perm[0];
        uint_mmv_t *ps0 = p_src + ((sgn_perm0 & 0x7ff) << 1);
        // %%PERM24_BENES_DECLARE "v%{i}"
        uint_mmv_t v00, v01;
        uint_mmv_t sgn_perm1 = p_perm[1];
        uint_mmv_t *ps1 = p_src + ((sgn_perm1 & 0x7ff) << 1);
        // %%PERM24_BENES_DECLARE "v%{i}"
        uint_mmv_t v10, v11;
        uint_mmv_t sgn_perm2 = p_perm[2];
        uint_mmv_t *ps2 = p_src + ((sgn_perm2 & 0x7ff) << 1);
        // %%PERM24_BENES_DECLARE "v%{i}"
        uint_mmv_t v20, v21;
        uint_mmv_t sgn_perm3 = p_perm[3];
        uint_mmv_t *ps3 = p_src + ((sgn_perm3 & 0x7ff) << 1);
        // %%PERM24_BENES_DECLARE "v%{i}"
        uint_mmv_t v30, v31;

        // Load 'ps' to temporary variables v00,...
        // %%PERM24_BENES_LOAD ps%{i}, v%{i}
        v00 = (ps0)[0];
        v01 = (ps0)[1];
        // Load 'ps' to temporary variables v10,...
        // %%PERM24_BENES_LOAD ps%{i}, v%{i}
        v10 = (ps1)[0];
        v11 = (ps1)[1];
        // Load 'ps' to temporary variables v20,...
        // %%PERM24_BENES_LOAD ps%{i}, v%{i}
        v20 = (ps2)[0];
        v21 = (ps2)[1];
        // Load 'ps' to temporary variables v30,...
        // %%PERM24_BENES_LOAD ps%{i}, v%{i}
        v30 = (ps3)[0];
        v31 = (ps3)[1];

        sgn_perm0 >>= sign_shift;  // sign for permutation
        // Permute and possibly negate data in temp. variables
        // %%PERM24_BENES_PERMUTE benes_mask, sgn_perm%{i}, v%{i}
        // Permute the 24 small integers in '(v00, v01)' 
        // using the Benes network given by 'benes_mask'. All small   
        // integers are negated if bit 0 of 'sign' is set.
        sgn_perm0 = (0-(sgn_perm0 & 0x1ULL)) & 0xffffffffffffffffULL;
        v00 ^= sgn_perm0;
        sgn_perm0 &= 0xffffffffULL;
        v01 ^= sgn_perm0;
        sgn_perm0 = (v00 ^ (v00 >> 4)) & benes_mask[0]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 4);
        sgn_perm0 = (v00 ^ (v00 >> 8)) & benes_mask[1]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 8);
        sgn_perm0 = (v00 ^ (v00 >> 16)) & benes_mask[2]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 16);
        sgn_perm0 = (v00 ^ (v00 >> 32)) & benes_mask[3]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 32);
        sgn_perm0 = (v01 ^ (v01 >> 4)) & benes_mask[4]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 4);
        sgn_perm0 = (v01 ^ (v01 >> 8)) & benes_mask[5]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 8);
        sgn_perm0 = (v01 ^ (v01 >> 16)) & benes_mask[6]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 16);
        sgn_perm0 = (v00 ^ v01) & benes_mask[7]; 
        v00 ^=  sgn_perm0;  v01 ^=  sgn_perm0;
        sgn_perm0 = (v00 ^ (v00 >> 32)) & benes_mask[8]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 32);
        sgn_perm0 = (v00 ^ (v00 >> 16)) & benes_mask[9]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 16);
        sgn_perm0 = (v00 ^ (v00 >> 8)) & benes_mask[10]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 8);
        sgn_perm0 = (v00 ^ (v00 >> 4)) & benes_mask[11]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 4);
        sgn_perm0 = (v01 ^ (v01 >> 16)) & benes_mask[12]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 16);
        sgn_perm0 = (v01 ^ (v01 >> 8)) & benes_mask[13]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 8);
        sgn_perm0 = (v01 ^ (v01 >> 4)) & benes_mask[14]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 4);
        // Permutation of small integers done.
        // Store temporary variables to 'p_dest'
        // %%PERM24_BENES_STORE "p_dest + %{int: i * V24_INTS}", v%{i}
(p_dest + 0)[0] = v00 ;
(p_dest + 0)[1] = v01 ;
        sgn_perm1 >>= sign_shift;  // sign for permutation
        // Permute and possibly negate data in temp. variables
        // %%PERM24_BENES_PERMUTE benes_mask, sgn_perm%{i}, v%{i}
// Permute the 24 small integers in '(v10, v11)' 
// using the Benes network given by 'benes_mask'. All small   
// integers are negated if bit 0 of 'sign' is set.
sgn_perm1 = (0-(sgn_perm1 & 0x1ULL)) & 0xffffffffffffffffULL;
v10 ^= sgn_perm1;
sgn_perm1 &= 0xffffffffULL;
v11 ^= sgn_perm1;
sgn_perm1 = (v10 ^ (v10 >> 4)) & benes_mask[0]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 4);
sgn_perm1 = (v10 ^ (v10 >> 8)) & benes_mask[1]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 8);
sgn_perm1 = (v10 ^ (v10 >> 16)) & benes_mask[2]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 16);
sgn_perm1 = (v10 ^ (v10 >> 32)) & benes_mask[3]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 32);
sgn_perm1 = (v11 ^ (v11 >> 4)) & benes_mask[4]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 4);
sgn_perm1 = (v11 ^ (v11 >> 8)) & benes_mask[5]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 8);
sgn_perm1 = (v11 ^ (v11 >> 16)) & benes_mask[6]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 16);
sgn_perm1 = (v10 ^ v11) & benes_mask[7]; 
v10 ^=  sgn_perm1;  v11 ^=  sgn_perm1;
sgn_perm1 = (v10 ^ (v10 >> 32)) & benes_mask[8]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 32);
sgn_perm1 = (v10 ^ (v10 >> 16)) & benes_mask[9]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 16);
sgn_perm1 = (v10 ^ (v10 >> 8)) & benes_mask[10]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 8);
sgn_perm1 = (v10 ^ (v10 >> 4)) & benes_mask[11]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 4);
sgn_perm1 = (v11 ^ (v11 >> 16)) & benes_mask[12]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 16);
sgn_perm1 = (v11 ^ (v11 >> 8)) & benes_mask[13]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 8);
sgn_perm1 = (v11 ^ (v11 >> 4)) & benes_mask[14]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 4);
// Permutation of small integers done.
        // Store temporary variables to 'p_dest'
        // %%PERM24_BENES_STORE "p_dest + %{int: i * V24_INTS}", v%{i}
(p_dest + 2)[0] = v10 ;
(p_dest + 2)[1] = v11 ;
        sgn_perm2 >>= sign_shift;  // sign for permutation
        // Permute and possibly negate data in temp. variables
        // %%PERM24_BENES_PERMUTE benes_mask, sgn_perm%{i}, v%{i}
// Permute the 24 small integers in '(v20, v21)' 
// using the Benes network given by 'benes_mask'. All small   
// integers are negated if bit 0 of 'sign' is set.
sgn_perm2 = (0-(sgn_perm2 & 0x1ULL)) & 0xffffffffffffffffULL;
v20 ^= sgn_perm2;
sgn_perm2 &= 0xffffffffULL;
v21 ^= sgn_perm2;
sgn_perm2 = (v20 ^ (v20 >> 4)) & benes_mask[0]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 4);
sgn_perm2 = (v20 ^ (v20 >> 8)) & benes_mask[1]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 8);
sgn_perm2 = (v20 ^ (v20 >> 16)) & benes_mask[2]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 16);
sgn_perm2 = (v20 ^ (v20 >> 32)) & benes_mask[3]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 32);
sgn_perm2 = (v21 ^ (v21 >> 4)) & benes_mask[4]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 4);
sgn_perm2 = (v21 ^ (v21 >> 8)) & benes_mask[5]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 8);
sgn_perm2 = (v21 ^ (v21 >> 16)) & benes_mask[6]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 16);
sgn_perm2 = (v20 ^ v21) & benes_mask[7]; 
v20 ^=  sgn_perm2;  v21 ^=  sgn_perm2;
sgn_perm2 = (v20 ^ (v20 >> 32)) & benes_mask[8]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 32);
sgn_perm2 = (v20 ^ (v20 >> 16)) & benes_mask[9]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 16);
sgn_perm2 = (v20 ^ (v20 >> 8)) & benes_mask[10]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 8);
sgn_perm2 = (v20 ^ (v20 >> 4)) & benes_mask[11]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 4);
sgn_perm2 = (v21 ^ (v21 >> 16)) & benes_mask[12]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 16);
sgn_perm2 = (v21 ^ (v21 >> 8)) & benes_mask[13]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 8);
sgn_perm2 = (v21 ^ (v21 >> 4)) & benes_mask[14]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 4);
// Permutation of small integers done.
        // Store temporary variables to 'p_dest'
        // %%PERM24_BENES_STORE "p_dest + %{int: i * V24_INTS}", v%{i}
(p_dest + 4)[0] = v20 ;
(p_dest + 4)[1] = v21 ;
        sgn_perm3 >>= sign_shift;  // sign for permutation
        // Permute and possibly negate data in temp. variables
        // %%PERM24_BENES_PERMUTE benes_mask, sgn_perm%{i}, v%{i}
// Permute the 24 small integers in '(v30, v31)' 
// using the Benes network given by 'benes_mask'. All small   
// integers are negated if bit 0 of 'sign' is set.
sgn_perm3 = (0-(sgn_perm3 & 0x1ULL)) & 0xffffffffffffffffULL;
v30 ^= sgn_perm3;
sgn_perm3 &= 0xffffffffULL;
v31 ^= sgn_perm3;
sgn_perm3 = (v30 ^ (v30 >> 4)) & benes_mask[0]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 4);
sgn_perm3 = (v30 ^ (v30 >> 8)) & benes_mask[1]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 8);
sgn_perm3 = (v30 ^ (v30 >> 16)) & benes_mask[2]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 16);
sgn_perm3 = (v30 ^ (v30 >> 32)) & benes_mask[3]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 32);
sgn_perm3 = (v31 ^ (v31 >> 4)) & benes_mask[4]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 4);
sgn_perm3 = (v31 ^ (v31 >> 8)) & benes_mask[5]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 8);
sgn_perm3 = (v31 ^ (v31 >> 16)) & benes_mask[6]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 16);
sgn_perm3 = (v30 ^ v31) & benes_mask[7]; 
v30 ^=  sgn_perm3;  v31 ^=  sgn_perm3;
sgn_perm3 = (v30 ^ (v30 >> 32)) & benes_mask[8]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 32);
sgn_perm3 = (v30 ^ (v30 >> 16)) & benes_mask[9]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 16);
sgn_perm3 = (v30 ^ (v30 >> 8)) & benes_mask[10]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 8);
sgn_perm3 = (v30 ^ (v30 >> 4)) & benes_mask[11]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 4);
sgn_perm3 = (v31 ^ (v31 >> 16)) & benes_mask[12]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 16);
sgn_perm3 = (v31 ^ (v31 >> 8)) & benes_mask[13]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 8);
sgn_perm3 = (v31 ^ (v31 >> 4)) & benes_mask[14]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 4);
// Permutation of small integers done.
        // Store temporary variables to 'p_dest'
        // %%PERM24_BENES_STORE "p_dest + %{int: i * V24_INTS}", v%{i}
(p_dest + 6)[0] = v30 ;
(p_dest + 6)[1] = v31 ;

        p_perm += 4;
        p_dest += 8;
        }
}


static void pi24_72(
   uint_mmv_t * p_src,
   uint16_t * p_perm,
   uint_mmv_t * benes_mask,
   uint_mmv_t * p_dest
)
{
    uint_fast32_t i1;
    for (i1 = 0; i1 < 72; ++i1) {
        uint_mmv_t sgn_perm = p_perm[i1];
        uint_mmv_t *ps = p_src + ((sgn_perm & 0x7ff) << 1);
        // The following mask is used by the actual permutation code
        // %%PERM24_BENES_DECLARE "v"
uint_mmv_t v0, v1;

        sgn_perm >>= 15;  // sign for permutation
        // Load 'ps' to temporary variables v0,...
        // %%PERM24_BENES_LOAD ps
v0 = (ps)[0];
v1 = (ps)[1];
        // Permute and possibly negate data in temp. variables
        // %%PERM24_BENES_PERMUTE benes_mask, sgn_perm
// Permute the 24 small integers in '(v0, v1)' 
// using the Benes network given by 'benes_mask'. All small   
// integers are negated if bit 0 of 'sign' is set.
sgn_perm = (0-(sgn_perm & 0x1ULL)) & 0xffffffffffffffffULL;
v0 ^= sgn_perm;
sgn_perm &= 0xffffffffULL;
v1 ^= sgn_perm;
sgn_perm = (v0 ^ (v0 >> 4)) & benes_mask[0]; 
v0 ^=  sgn_perm ^ (sgn_perm << 4);
sgn_perm = (v0 ^ (v0 >> 8)) & benes_mask[1]; 
v0 ^=  sgn_perm ^ (sgn_perm << 8);
sgn_perm = (v0 ^ (v0 >> 16)) & benes_mask[2]; 
v0 ^=  sgn_perm ^ (sgn_perm << 16);
sgn_perm = (v0 ^ (v0 >> 32)) & benes_mask[3]; 
v0 ^=  sgn_perm ^ (sgn_perm << 32);
sgn_perm = (v1 ^ (v1 >> 4)) & benes_mask[4]; 
v1 ^=  sgn_perm ^ (sgn_perm << 4);
sgn_perm = (v1 ^ (v1 >> 8)) & benes_mask[5]; 
v1 ^=  sgn_perm ^ (sgn_perm << 8);
sgn_perm = (v1 ^ (v1 >> 16)) & benes_mask[6]; 
v1 ^=  sgn_perm ^ (sgn_perm << 16);
sgn_perm = (v0 ^ v1) & benes_mask[7]; 
v0 ^=  sgn_perm;  v1 ^=  sgn_perm;
sgn_perm = (v0 ^ (v0 >> 32)) & benes_mask[8]; 
v0 ^=  sgn_perm ^ (sgn_perm << 32);
sgn_perm = (v0 ^ (v0 >> 16)) & benes_mask[9]; 
v0 ^=  sgn_perm ^ (sgn_perm << 16);
sgn_perm = (v0 ^ (v0 >> 8)) & benes_mask[10]; 
v0 ^=  sgn_perm ^ (sgn_perm << 8);
sgn_perm = (v0 ^ (v0 >> 4)) & benes_mask[11]; 
v0 ^=  sgn_perm ^ (sgn_perm << 4);
sgn_perm = (v1 ^ (v1 >> 16)) & benes_mask[12]; 
v1 ^=  sgn_perm ^ (sgn_perm << 16);
sgn_perm = (v1 ^ (v1 >> 8)) & benes_mask[13]; 
v1 ^=  sgn_perm ^ (sgn_perm << 8);
sgn_perm = (v1 ^ (v1 >> 4)) & benes_mask[14]; 
v1 ^=  sgn_perm ^ (sgn_perm << 4);
// Permutation of small integers done.
        // Store temporary variables to 'p_dest'
        // %%PERM24_BENES_STORE p_dest
(p_dest)[0] = v0 ;
(p_dest)[1] = v1 ;
        p_dest +=  2;      
        }
}

// %%END IF





/// @endcond  


/***************************************************************
* Operation x_delta * x_pi
***************************************************************/

/// @cond DO_NOT_DOCUMENT 


/**
  @brief Workhorse for function ``mm_op15_pi``

  ``mm_op15_pi(v_in, delta, pi, v_out)`` is equivalent to

        mm_sub_op_pi_type s_op; // defined in mm_basics.h
        // Borrow memory from v_out suficient for an array of 759
        // entries of type  ``mm_sub_op_pi64_type``
        s_op.tbl_perm64 = (mm_sub_op_pi64_type*)(v_out + MM_OP15_OFS_X);
        mm_sub_prep_pi(delta, pi, &s_op);
        mm_op15_do_pi(v_in, &s_op, v_out);

   So the functions called by function ``mm_op15_pi``
   can be tested individually.
*/
static
void mm_op15_do_pi(uint_mmv_t *v_in, mm_sub_op_pi_type *p_op, uint_mmv_t * v_out)
{
    uint_mmv_t *a_src[3], *a_dest[3];
    uint16_t *p_perm1 = p_op->tbl_perm24_big;

    // %%IF PERM24_USE_BENES_NET
    uint_mmv_t small_perm[15]; 

    // Prepare mask array from Benes network
    // %%PERM24_BENES_PREPARE "p_op->benes_net", small_perm
{
    uint_mmv_t tmp; 
    uint_fast8_t i;
    static uint8_t tbl[] = {
        // %%TABLE table_prepare_perm24, uint8_t
    0x00,0x01,0x02,0x03,0x10,0x11,0x12,0x04,
    0x05,0x06,0x07,0x08,0x16,0x17,0x18
    };

    for(i = 0; i < 15; ++i) {
        tmp = tbl[i]; tmp = (p_op->benes_net)[tmp & 15] >> (tmp & 0xf0);
        // %%MMV_UINT_SPREAD tmp, tmp
        // Spread bits 0,...,15 of tmp to the (4-bit long) fields
        // of tmp. A field of tmp is set to 0xf if its 
        // corresponding bit in input tmp is one and to 0 otherwise.
        tmp = (tmp & 0xffULL) + ((tmp & 0xff00ULL) << 24);
        tmp = (tmp & 0xf0000000fULL) 
            +  ((tmp & 0xf0000000f0ULL) << 12);
        tmp = (tmp & 0x3000300030003ULL) 
            +  ((tmp & 0xc000c000c000cULL) << 6);
        tmp = (tmp & 0x101010101010101ULL) 
            +  ((tmp & 0x202020202020202ULL) << 3);
        tmp *= 15;
        // Bit spreading done.
        small_perm[i] = tmp;
    }
}
    pi24_72(v_in, p_perm1 + 2048, small_perm, v_out);
    // %%END IF
    

    // Step 1: do rows with 64 entries // TODO: comment properly!!!!
    {
        // TODO: check this !!!!!!!!!!!!
        mm_sub_op_pi64_type *p_perm = p_op->tbl_perm64;
        uint8_t bytes[64];
        uint_mmv_t *p_out = v_out + MM_OP15_OFS_T;
        uint_mmv_t *p_end = p_out + 759 * 4;
        uint_mmv_t *v1_in =  v_in + MM_OP15_OFS_T;
        for (; p_out < p_end; p_out += 4) {
            {
               uint_mmv_t v = p_perm->preimage;
               uint_mmv_t *p_in = v1_in + ((v & 0x3ff) << 2);
               // %%LOAD_PERM64 p_in, bytes, v, uint8_t
               uint_mmv_t r0, r1;
               v = (0-((v >> 12) & 1)) & 0xffffffffffffffffULL;
               r0 =  (p_in)[0] ^ (v);
               r1 = (r0 >> 4) & 0xf0f0f0f0f0f0f0fULL;
               r0 &= 0xf0f0f0f0f0f0f0fULL;
               (bytes)[0] = (uint8_t)(r0 >> 0);
               (bytes)[1] = (uint8_t)(r1 >> 0);
               (bytes)[2] = (uint8_t)(r0 >> 8);
               (bytes)[3] = (uint8_t)(r1 >> 8);
               (bytes)[4] = (uint8_t)(r0 >> 16);
               (bytes)[5] = (uint8_t)(r1 >> 16);
               (bytes)[6] = (uint8_t)(r0 >> 24);
               (bytes)[7] = (uint8_t)(r1 >> 24);
               (bytes)[8] = (uint8_t)(r0 >> 32);
               (bytes)[9] = (uint8_t)(r1 >> 32);
               (bytes)[10] = (uint8_t)(r0 >> 40);
               (bytes)[11] = (uint8_t)(r1 >> 40);
               (bytes)[12] = (uint8_t)(r0 >> 48);
               (bytes)[13] = (uint8_t)(r1 >> 48);
               (bytes)[14] = (uint8_t)(r0 >> 56);
               (bytes)[15] = (uint8_t)(r1 >> 56);
               r0 =  (p_in)[1] ^ (v);
               r1 = (r0 >> 4) & 0xf0f0f0f0f0f0f0fULL;
               r0 &= 0xf0f0f0f0f0f0f0fULL;
               (bytes)[16] = (uint8_t)(r0 >> 0);
               (bytes)[17] = (uint8_t)(r1 >> 0);
               (bytes)[18] = (uint8_t)(r0 >> 8);
               (bytes)[19] = (uint8_t)(r1 >> 8);
               (bytes)[20] = (uint8_t)(r0 >> 16);
               (bytes)[21] = (uint8_t)(r1 >> 16);
               (bytes)[22] = (uint8_t)(r0 >> 24);
               (bytes)[23] = (uint8_t)(r1 >> 24);
               (bytes)[24] = (uint8_t)(r0 >> 32);
               (bytes)[25] = (uint8_t)(r1 >> 32);
               (bytes)[26] = (uint8_t)(r0 >> 40);
               (bytes)[27] = (uint8_t)(r1 >> 40);
               (bytes)[28] = (uint8_t)(r0 >> 48);
               (bytes)[29] = (uint8_t)(r1 >> 48);
               (bytes)[30] = (uint8_t)(r0 >> 56);
               (bytes)[31] = (uint8_t)(r1 >> 56);
               r0 =  (p_in)[2] ^ (v);
               r1 = (r0 >> 4) & 0xf0f0f0f0f0f0f0fULL;
               r0 &= 0xf0f0f0f0f0f0f0fULL;
               (bytes)[32] = (uint8_t)(r0 >> 0);
               (bytes)[33] = (uint8_t)(r1 >> 0);
               (bytes)[34] = (uint8_t)(r0 >> 8);
               (bytes)[35] = (uint8_t)(r1 >> 8);
               (bytes)[36] = (uint8_t)(r0 >> 16);
               (bytes)[37] = (uint8_t)(r1 >> 16);
               (bytes)[38] = (uint8_t)(r0 >> 24);
               (bytes)[39] = (uint8_t)(r1 >> 24);
               (bytes)[40] = (uint8_t)(r0 >> 32);
               (bytes)[41] = (uint8_t)(r1 >> 32);
               (bytes)[42] = (uint8_t)(r0 >> 40);
               (bytes)[43] = (uint8_t)(r1 >> 40);
               (bytes)[44] = (uint8_t)(r0 >> 48);
               (bytes)[45] = (uint8_t)(r1 >> 48);
               (bytes)[46] = (uint8_t)(r0 >> 56);
               (bytes)[47] = (uint8_t)(r1 >> 56);
               r0 =  (p_in)[3] ^ (v);
               r1 = (r0 >> 4) & 0xf0f0f0f0f0f0f0fULL;
               r0 &= 0xf0f0f0f0f0f0f0fULL;
               (bytes)[48] = (uint8_t)(r0 >> 0);
               (bytes)[49] = (uint8_t)(r1 >> 0);
               (bytes)[50] = (uint8_t)(r0 >> 8);
               (bytes)[51] = (uint8_t)(r1 >> 8);
               (bytes)[52] = (uint8_t)(r0 >> 16);
               (bytes)[53] = (uint8_t)(r1 >> 16);
               (bytes)[54] = (uint8_t)(r0 >> 24);
               (bytes)[55] = (uint8_t)(r1 >> 24);
               (bytes)[56] = (uint8_t)(r0 >> 32);
               (bytes)[57] = (uint8_t)(r1 >> 32);
               (bytes)[58] = (uint8_t)(r0 >> 40);
               (bytes)[59] = (uint8_t)(r1 >> 40);
               (bytes)[60] = (uint8_t)(r0 >> 48);
               (bytes)[61] = (uint8_t)(r1 >> 48);
               (bytes)[62] = (uint8_t)(r0 >> 56);
               (bytes)[63] = (uint8_t)(r1 >> 56);
            }
            {
               // %%STORE_PERM64 bytes, p_out, "(p_perm->perm)"
               uint_mmv_t v;
               uint_fast8_t ri, r0, r1, r2, r3;
               r0 = (p_perm->perm)[0];
               r1 = (p_perm->perm)[1];
               r2 = (p_perm->perm)[2];
               r3 = (p_perm->perm)[3];
               ri = r0;
               v = (uint_mmv_t)(bytes[0]) << 0;
               v += (uint_mmv_t)(bytes[ri]) << 4;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 12;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 20;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 28;
               ri ^= r3;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 36;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 44;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 52;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 60;
               p_out[0] = v ;
               ri ^= (p_perm->perm)[4];
               v = (uint_mmv_t)(bytes[ri]) << 0;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 4;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 12;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 20;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 28;
               ri ^= r3;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 36;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 44;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 52;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 60;
               p_out[1] = v ;
               ri ^= (p_perm->perm)[5];
               v = (uint_mmv_t)(bytes[ri]) << 0;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 4;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 12;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 20;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 28;
               ri ^= r3;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 36;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 44;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 52;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 60;
               p_out[2] = v ;
               ri ^= (p_perm->perm)[4];
               v = (uint_mmv_t)(bytes[ri]) << 0;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 4;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 12;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 20;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 28;
               ri ^= r3;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 36;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 44;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 52;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 60;
               p_out[3] = v ;
            }
            ++p_perm;
        } 
    }

    // Step 2: do rows with 24 entries 
    // TODO: comment properly!!!!
    a_src[0] = v_in + MM_OP15_OFS_X;
    a_dest[0] = v_out + MM_OP15_OFS_X;
    a_src[1] = v_in + MM_OP15_OFS_Z;
    a_src[2] = v_in + MM_OP15_OFS_Y;
    if (p_op->eps & 0x800) {
        a_dest[1] = v_out + MM_OP15_OFS_Y;
        a_dest[2] = v_out + MM_OP15_OFS_Z;
    } else {
        a_dest[1] = v_out + MM_OP15_OFS_Z;
        a_dest[2] = v_out + MM_OP15_OFS_Y;
    }

    {
        uint_fast32_t i;
        for (i = 0; i < 3; ++i) 
            pi24_2048(a_src[i], p_perm1, small_perm, i + 12, a_dest[i]);
    }


    // If d is odd: negate some entries    
    if (p_op->eps & 0x800) {
        uint_fast16_t i;
        uint_mmv_t *v = v_out + MM_OP15_OFS_T;

        // Step odd 1:  negate suboctads of weight 4n+2 for tag T
        for (i = 0; i < 759; ++i) {
            // %%INVERT_PERM64 v
            v[0] ^= 0xf0fff0ffffff0ULL;
            v[1] ^= 0xf000000f000f0fffULL;
            v[2] ^= 0xf000000f000f0fffULL;
            v[3] ^= 0xfff0f000f000000fULL;
            v += 4;
        }

        mm_op15_neg_scalprod_d_i(v); 
    }
} 

/// @endcond 



/**
  @brief Compute automophism of the Parker loop on a vector

  Let ``v_in`` be a vector of the representation \f$\rho_{15}\f$
  of the monster group. 

  The integers ``d`` and ``p`` describe an automorphism of the
  Parker loop as indicated in the header of this file. The function
  computes this automorphism on the input  vector ``v_in`` and 
  stores the result in the output vector ``v_out.`` 

  Input vector  ``v_in`` is not changed.
*/
// %%EXPORT px
MM_OP15_API
void mm_op15_pi(uint_mmv_t *v_in, uint32_t delta, uint32_t pi, uint_mmv_t * v_out)
{
    mm_sub_op_pi_type s_op;
    // Borrow memory from v_out
    s_op.tbl_perm64 = (mm_sub_op_pi64_type *)(v_out + MM_OP15_OFS_X);
    mm_sub_prep_pi(delta, pi, &s_op);
    mm_op15_do_pi(v_in, &s_op, v_out);
}


/**
  @brief Simplified version of function ``mm_op15_pi``

  ``mm_op15_delta(v_in, delta, v_out)`` is equivalent to
  ``mm_op15_pi(v_in, 0, delta, v_out)``, but much faster.
  
*/
// %%EXPORT px
MM_OP15_API
void mm_op15_delta(uint_mmv_t *v_in, uint32_t delta, uint_mmv_t * v_out)
{
    uint_fast32_t i, i1;
    // Borrow space from ``v_out`` sufficient for an array of length 2048
    uint8_t *signs = (uint8_t*)(v_out + MM_OP15_OFS_T);
    uint_mmv_t *a_src[3], *a_dest[3];

    mat24_op_all_cocode(delta, signs);
    for (i = 0; i < 72; ++i) signs[i] &= 7;
    for (i = 48; i < 72; ++i) signs[i] |= (delta & 0x800) >> (11 - 3);

    a_src[0] = v_in + MM_OP15_OFS_X;
    a_dest[0] = v_out + MM_OP15_OFS_X;
    a_src[1] = v_in + MM_OP15_OFS_Z;
    a_src[2] = v_in + MM_OP15_OFS_Y;
    if (delta & 0x800) {
        a_dest[1] = v_out + MM_OP15_OFS_Y;
        a_dest[2] = v_out + MM_OP15_OFS_Z;
    } else {
        a_dest[1] = v_out + MM_OP15_OFS_Z;
        a_dest[2] = v_out + MM_OP15_OFS_Y;
    }

    // Step 1: do rows with 24 entries 
    // TODO: comment properly!!!!
    for (i = 0; i < 3; ++i)  {
        for (i1 = 0; i1 < 2048; ++i1) {
            uint_mmv_t *p_src = a_src[i] + (i1 << 1);
            uint_mmv_t *p_dest = a_dest[i] + (i1 << 1);
            uint_mmv_t sgn = -((signs[i1] >> i) & 1);
            // %%FOR i in range(V24_INTS_USED)
            sgn &= 0xffffffffffffffffULL;
            p_dest[0] = p_src[0]  ^ sgn;
            sgn &= 0xffffffffULL;
            p_dest[1] = p_src[1]  ^ sgn;
            // %%END FOR
        }        
    }    

    {
        uint_mmv_t *p_src = v_in + MM_OP15_OFS_A;
        uint_mmv_t *p_dest = v_out + MM_OP15_OFS_A;
        for (i1 = 0; i1 < 72; ++i1) {
            uint_mmv_t sgn = -((signs[i1] >> i) & 1);
            // %%FOR i in range(V24_INTS_USED)
            sgn &= 0xffffffffffffffffULL;
            p_dest[0] = p_src[0]  ^ sgn;
            sgn &= 0xffffffffULL;
            p_dest[1] = p_src[1]  ^ sgn;
            // %%END FOR
            p_src +=  2;      
            p_dest +=  2;      
        }        
    }    


    // Step 2: do rows with 64 entries 
    // TODO: comment properly!!!!
    {
        v_in +=  MM_OP15_OFS_T;
        v_out += MM_OP15_OFS_T;
        for (i = 0; i < 759; ++i) {
            uint_mmv_t sign = mat24_def_octad_to_gcode(i) & delta;
            mat24_def_parity12(sign);
            sign = 0 - sign;
            sign &= 0xffffffffffffffffULL;
            // %%FOR i in range(%{V64_INTS})
            v_out[0] = v_in[0]  ^  sign;
            v_out[1] = v_in[1]  ^  sign;
            v_out[2] = v_in[2]  ^  sign;
            v_out[3] = v_in[3]  ^  sign;
            // %%END FOR
            v_in += 4;
            v_out += 4;
        } 
        v_out -= 759 * 4 +  MM_OP15_OFS_T; // restore v_out
    }

    // If d is odd: negate some entries    
    if (delta & 0x800) {
        uint_mmv_t *v = v_out + MM_OP15_OFS_T;

        // Step odd 1:  negate suboctads of weight 4n+2 for tag T
        for (i = 0; i < 759; ++i) {
            // %%INVERT_PERM64 v
v[0] ^= 0xf0fff0ffffff0ULL;
v[1] ^= 0xf000000f000f0fffULL;
v[2] ^= 0xf000000f000f0fffULL;
v[3] ^= 0xfff0f000f000000fULL;
            v += 4;
        }

        mm_op15_neg_scalprod_d_i(v); 
    }
}

/**
  @brief Restriction of function ``mm_op15_pi`` to tag ``ABC``

  Function ``mm_op15_pi`` computes an automorphism of the
  Parker loop on a vector ``v_in`` and stores the result
  in ``v_out``. That automorphism depends on parameters
  ``delta``  and ``p``.
  
  Function ``mm_op15_pi_tag_ABC`` computes the same
  automorphism on the entries of the vector ``v = v_in`` with
  tags ``ABC`` only, and ignores the other entries of ``v``.
  See section **The representation of the monster group**
  in the **API reference** for tags of entries of a vector in
  the representation of the monster.

  The function overwrites the vector ``v`` with the result.
  Here only entries of ``v`` with tag ``ABC`` are changed.

  If parameter ``mode`` is set then we perform the operation on
  entries with tag ``A`` only. This  function is much faster 
  than function ``mm_op15_pi``.
*/
// %%EXPORT px
MM_OP15_API
void mm_op15_pi_tag_ABC(uint_mmv_t *v, uint32_t delta, uint32_t pi, uint32_t mode)
{
    uint_mmv_t v_tmp[24 *  2];
    uint16_t row_perm[24];
    uint8_t perm[24], col_perm[48];
    uint_fast32_t i, j;

    pi %= MAT24_ORDER;
    mat24_m24num_to_perm(pi, perm);
    
    for(i = 0; i < 24; ++i) {
        j = perm[i];
        row_perm[j] = (uint16_t)i;
        col_perm[j+j] = ((uint8_t)i >> 4);
        col_perm[j+j+1] 
            = ((uint8_t)i & 0xfULL) << 2;
    }
    pi24_n(v, row_perm, col_perm, v_tmp, 24);
    for (i = 0; i < 24 *  2; ++i) v[i] = v_tmp[i];
    if (mode) return;

    v += 24 *  2;
    pi24_n(v, row_perm, col_perm, v_tmp, 24);
    for (i = 0; i < 24 *  2; ++i) v[i] = v_tmp[i];

    v += 24 *  2;
    if (delta & 0x800) for(i = 0; i < 24; ++i) row_perm[i] ^= 0x8000;
    pi24_n(v, row_perm, col_perm, v_tmp, 24);
    for (i = 0; i < 24 *  2; ++i) v[i] = v_tmp[i];
 
}




/**
  @brief Restriction of function ``mm_op15_pi`` to tag ``ABC``

  Function ``mm_op15_delta`` computes an automorphism of the
  Parker loop on a vector ``v_in`` and stores the result
  in ``v_out``. That automorphism depends on parameter ``d``.
  
  Function ``mm_op15_delta_tag_ABC`` computes the same
  automorphism on the entries of the vector ``v = v_in`` with
  tags ``ABC`` only, and ignores the other entries of ``v``.
  See section **The representation of the monster group**
  in the **API reference** for tags of entries of a vector in
  the representation of the monster.

  The function overwrites the vector ``v`` with the result.
  Here only entries of ``v`` with tag ``ABC`` are changed.

  If parameter ``mode`` is set then we perform the operation on
  entries with tag ``A`` only. This  function is much faster 
  than function ``mm_op15_delta``.
*/
// %%EXPORT px
MM_OP15_API
void mm_op15_delta_tag_ABC(uint_mmv_t *v, uint32_t d, uint32_t mode)
{
    uint32_t i1;

    if (mode || (d & 0x800) == 0) return;
    v += 2 * 24 * 2;
    for (i1 = 0; i1 < 24; ++i1) {
        v[0] ^=  0xffffffffffffffffULL;
        v[1] ^= 0xffffffffULL;
        v +=  2;      
    }
}



//  %%GEN h
//  %%GEN c

