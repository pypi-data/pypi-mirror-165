/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm127_op_pi.c

 File ``mm127_op_pi.c`` implements the operation of the
 generators \f$x_\pi\f$ and \f$x_\delta\f$ of the monster group
 on a vector in the representation \f$\rho_{127}\f$ of the
 monster.

 Here generators \f$x_\pi\f$ and \f$x_\delta\f$ are defined as
 automorphisms of the Parker loop as in section **The monster group**
 of the **API reference**. An automophism of the Parker loop is
 specified by a pair of integers ``d, p`` as in the constructor
 of the Python class ``AutPL``, see
 section **Automophisms of the Parker loop** in the **API reference**.

 The representation \f$\rho_{127}\f$ is equal to the
 196884-dimensional representation  \f$\rho\f$ of the monster,
 with coefficients taken modulo 127, as defined in
 section **The representation of the monster group**
 in the **API reference**.

 An element of \f$\rho_{127}\f$ is implemented as an array of
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
 can be used for implementing the operation on \f$\rho_{127}\f$.
 These conversions are very fast compared to the cost for
 the operation on \f$\rho_{127}\f$. This helps us to keep
 the C interface for these  operations simple.

*/

#include <string.h>
#include "mm_op127.h"   

// %%EXPORT_KWD MM_OP%{P}_API


//  %%GEN h
//  %%GEN c



/// @cond DO_NOT_DOCUMENT 
   
static const uint_mmv_t MM127_TBL_SCALPROD_HIGH[] = { 
// %%TABLE MMV_TBL_SCALPROD_HIGH, uint%{INT_BITS}
0x0000000000000000ULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x0000000000000000ULL,
0x7f7f000000000000ULL,0x7f7f000000000000ULL,
0x007f7f007f007f00ULL,0x0000000000000000ULL,
0x7f007f0000000000ULL,0x7f007f0000000000ULL,
0x7f7f0000007f7f00ULL,0x0000000000000000ULL,
0x007f7f0000000000ULL,0x007f7f0000000000ULL,
0x7f007f007f7f0000ULL,0x0000000000000000ULL,
0x000000007f7f0000ULL,0x7f7f000000000000ULL,
0x7f007f00007f7f00ULL,0x0000000000000000ULL,
0x7f7f00007f7f0000ULL,0x0000000000000000ULL,
0x7f7f00007f7f0000ULL,0x0000000000000000ULL,
0x7f007f007f7f0000ULL,0x007f7f0000000000ULL,
0x007f7f0000000000ULL,0x0000000000000000ULL,
0x007f7f007f7f0000ULL,0x7f007f0000000000ULL,
0x000000007f007f00ULL,0x0000000000000000ULL,
0x000000007f007f00ULL,0x7f007f0000000000ULL,
0x007f7f007f7f0000ULL,0x0000000000000000ULL,
0x7f7f00007f007f00ULL,0x007f7f0000000000ULL,
0x00000000007f7f00ULL,0x0000000000000000ULL,
0x7f007f007f007f00ULL,0x0000000000000000ULL,
0x7f007f007f007f00ULL,0x0000000000000000ULL,
0x007f7f007f007f00ULL,0x7f7f000000000000ULL,
0x7f7f000000000000ULL,0x0000000000000000ULL,
0x00000000007f7f00ULL,0x007f7f0000000000ULL,
0x7f7f00007f007f00ULL,0x0000000000000000ULL,
0x7f7f0000007f7f00ULL,0x7f007f0000000000ULL,
0x7f007f0000000000ULL,0x0000000000000000ULL,
0x7f007f00007f7f00ULL,0x7f7f000000000000ULL,
0x000000007f7f0000ULL,0x0000000000000000ULL,
0x007f7f00007f7f00ULL,0x0000000000000000ULL,
0x007f7f00007f7f00ULL,0x0000000000000000ULL,
0x0000007f7f7f7f00ULL,0x0000007f0000007fULL,
0x0000007f0000007fULL,0x0000000000000000ULL,
0x7f7f007f7f7f7f00ULL,0x7f7f007f0000007fULL,
0x007f7f7f7f007f7fULL,0x0000000000000000ULL,
0x7f007f7f7f7f7f00ULL,0x7f007f7f0000007fULL,
0x7f7f007f007f7f7fULL,0x0000000000000000ULL,
0x007f7f7f7f7f7f00ULL,0x007f7f7f0000007fULL,
0x7f007f7f7f7f007fULL,0x0000000000000000ULL,
0x0000007f00007f00ULL,0x7f7f007f0000007fULL,
0x7f007f7f007f7f7fULL,0x0000000000000000ULL,
0x7f7f007f00007f00ULL,0x0000007f0000007fULL,
0x7f7f007f7f7f007fULL,0x0000000000000000ULL,
0x7f007f7f00007f00ULL,0x007f7f7f0000007fULL,
0x007f7f7f0000007fULL,0x0000000000000000ULL,
0x007f7f7f00007f00ULL,0x7f007f7f0000007fULL,
0x0000007f7f007f7fULL,0x0000000000000000ULL,
0x0000007f007f0000ULL,0x7f007f7f0000007fULL,
0x007f7f7f7f7f007fULL,0x0000000000000000ULL,
0x7f7f007f007f0000ULL,0x007f7f7f0000007fULL,
0x0000007f007f7f7fULL,0x0000000000000000ULL,
0x7f007f7f007f0000ULL,0x0000007f0000007fULL,
0x7f007f7f7f007f7fULL,0x0000000000000000ULL,
0x007f7f7f007f0000ULL,0x7f7f007f0000007fULL,
0x7f7f007f0000007fULL,0x0000000000000000ULL,
0x0000007f7f000000ULL,0x007f7f7f0000007fULL,
0x7f7f007f7f007f7fULL,0x0000000000000000ULL,
0x7f7f007f7f000000ULL,0x7f007f7f0000007fULL,
0x7f007f7f0000007fULL,0x0000000000000000ULL,
0x7f007f7f7f000000ULL,0x7f7f007f0000007fULL,
0x0000007f7f7f007fULL,0x0000000000000000ULL,
0x007f7f7f7f000000ULL,0x0000007f0000007fULL,
0x007f7f7f007f7f7fULL,0x0000000000000000ULL
};

static const uint_mmv_t MM127_TBL_SCALPROD_LOW[] = { 
// %%TABLE MMV_TBL_SCALPROD_LOW, uint%{INT_BITS}
0x0000000000000000ULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x0000000000000000ULL,
0x7f7f7f7f00000000ULL,0x7f7f7f7f7f7f7f7fULL,
0x7f7f7f7f00000000ULL,0x0000000000000000ULL,
0x7f7f7f7f00000000ULL,0x7f7f7f7f7f7f7f7fULL,
0x000000007f7f7f7fULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x0000000000000000ULL,
0x7f7f7f7f7f7f7f7fULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x7f7f00007f7f0000ULL,
0x7f7f00007f7f0000ULL,0x0000000000000000ULL,
0x7f7f7f7f00000000ULL,0x00007f7f00007f7fULL,
0x00007f7f7f7f0000ULL,0x0000000000000000ULL,
0x7f7f7f7f00000000ULL,0x00007f7f00007f7fULL,
0x7f7f000000007f7fULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x7f7f00007f7f0000ULL,
0x00007f7f00007f7fULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x7f007f007f007f00ULL,
0x7f007f007f007f00ULL,0x0000000000000000ULL,
0x7f7f7f7f00000000ULL,0x007f007f007f007fULL,
0x007f007f7f007f00ULL,0x0000000000000000ULL,
0x7f7f7f7f00000000ULL,0x007f007f007f007fULL,
0x7f007f00007f007fULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x7f007f007f007f00ULL,
0x007f007f007f007fULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x007f7f00007f7f00ULL,
0x007f7f00007f7f00ULL,0x0000000000000000ULL,
0x7f7f7f7f00000000ULL,0x7f00007f7f00007fULL,
0x7f00007f007f7f00ULL,0x0000000000000000ULL,
0x7f7f7f7f00000000ULL,0x7f00007f7f00007fULL,
0x007f7f007f00007fULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x007f7f00007f7f00ULL,
0x7f00007f7f00007fULL,0x0000000000000000ULL
};

/// @endcond 



/***************************************************************
* Auxiliary functions
***************************************************************/

/// @cond DO_NOT_DOCUMENT 

// %%EXPORT
MM_OP127_API
void mm_op127_neg_scalprod_d_i(uint_mmv_t* v)
// negate entries d (x) i with sclar product equal to 1
{
    const uint_mmv_t* p0 = MM127_TBL_SCALPROD_HIGH;
    const uint_mmv_t* p0_end = p0 + 32 * 4;

    // inversion of entries (d (x) i) with scalar product 1
    for (; p0 < p0_end; p0 += 4) {
        const uint_mmv_t* p1 = MM127_TBL_SCALPROD_LOW;
        const uint_mmv_t* p1_end = p1 + 16 * 4;
        for (; p1 < p1_end; p1 += 4) {
            // %%SCALAR_PROD_2048_UNROLL p0, p1, v 
            uint_mmv_t v_t;
            v[0] ^= (v_t = p0[0] ^ p1[0]);
            v[4] ^= v_t ^ 0x7f7f7f7f00000000ULL;
            v[8] ^= v_t ^ 0x7f7f7f7f00000000ULL;
            v[12] ^= v_t ^ 0x0ULL;
            v[1] ^= (v_t = p0[1] ^ p1[1]);
            v[5] ^= v_t ^ 0x7f7f7f7f00000000ULL;
            v[9] ^= v_t ^ 0x7f7f7f7fULL;
            v[13] ^= v_t ^ 0x7f7f7f7f7f7f7f7fULL;
            v[2] ^= (v_t = p0[2] ^ p1[2]);
            v[6] ^= v_t ^ 0x7f7f7f7f7f7f7f7fULL;
            v[10] ^= v_t ^ 0x7f7f7f7f7f7f7f7fULL;
            v[14] ^= v_t ^ 0x0ULL;
            v +=   4 * 4;
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
        uint_mmv_t *ps = p_src + ((sgn_perm & 0x7ff) << 2);

        sgn_perm >>= 15;  // sign for permutation
        sgn_perm = 0 - (sgn_perm & 1);
        // %%FOR i in range(V24_INTS_USED)  
        sgn_perm &= 0x7f7f7f7f7f7f7f7fULL;
        p_dest[0] = sgn_perm  ^ (
            (((ps[pf[0]] >> pf[1]) & 127) << 0) |
            (((ps[pf[2]] >> pf[3]) & 127) << 8) |
            (((ps[pf[4]] >> pf[5]) & 127) << 16) |
            (((ps[pf[6]] >> pf[7]) & 127) << 24) |
            (((ps[pf[8]] >> pf[9]) & 127) << 32) |
            (((ps[pf[10]] >> pf[11]) & 127) << 40) |
            (((ps[pf[12]] >> pf[13]) & 127) << 48) |
            (((ps[pf[14]] >> pf[15]) & 127) << 56));
        p_dest[1] = sgn_perm  ^ (
            (((ps[pf[16]] >> pf[17]) & 127) << 0) |
            (((ps[pf[18]] >> pf[19]) & 127) << 8) |
            (((ps[pf[20]] >> pf[21]) & 127) << 16) |
            (((ps[pf[22]] >> pf[23]) & 127) << 24) |
            (((ps[pf[24]] >> pf[25]) & 127) << 32) |
            (((ps[pf[26]] >> pf[27]) & 127) << 40) |
            (((ps[pf[28]] >> pf[29]) & 127) << 48) |
            (((ps[pf[30]] >> pf[31]) & 127) << 56));
        p_dest[2] = sgn_perm  ^ (
            (((ps[pf[32]] >> pf[33]) & 127) << 0) |
            (((ps[pf[34]] >> pf[35]) & 127) << 8) |
            (((ps[pf[36]] >> pf[37]) & 127) << 16) |
            (((ps[pf[38]] >> pf[39]) & 127) << 24) |
            (((ps[pf[40]] >> pf[41]) & 127) << 32) |
            (((ps[pf[42]] >> pf[43]) & 127) << 40) |
            (((ps[pf[44]] >> pf[45]) & 127) << 48) |
            (((ps[pf[46]] >> pf[47]) & 127) << 56));
        // %%END FOR   #  FOR i
        p_dest[3] = 0;
        p_dest +=  4;      
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
        uint_mmv_t *ps0 = p_src + ((sgn_perm0 & 0x7ff) << 2);
        // %%PERM24_BENES_DECLARE "v%{i}"
        uint_mmv_t v00, v01, v02;
        uint_mmv_t sgn_perm1 = p_perm[1];
        uint_mmv_t *ps1 = p_src + ((sgn_perm1 & 0x7ff) << 2);
        // %%PERM24_BENES_DECLARE "v%{i}"
        uint_mmv_t v10, v11, v12;
        uint_mmv_t sgn_perm2 = p_perm[2];
        uint_mmv_t *ps2 = p_src + ((sgn_perm2 & 0x7ff) << 2);
        // %%PERM24_BENES_DECLARE "v%{i}"
        uint_mmv_t v20, v21, v22;
        uint_mmv_t sgn_perm3 = p_perm[3];
        uint_mmv_t *ps3 = p_src + ((sgn_perm3 & 0x7ff) << 2);
        // %%PERM24_BENES_DECLARE "v%{i}"
        uint_mmv_t v30, v31, v32;

        // Load 'ps' to temporary variables v00,...
        // %%PERM24_BENES_LOAD ps%{i}, v%{i}
        v00 = (ps0)[0];
        v01 = (ps0)[1];
        v02 = (ps0)[2];
        // Load 'ps' to temporary variables v10,...
        // %%PERM24_BENES_LOAD ps%{i}, v%{i}
        v10 = (ps1)[0];
        v11 = (ps1)[1];
        v12 = (ps1)[2];
        // Load 'ps' to temporary variables v20,...
        // %%PERM24_BENES_LOAD ps%{i}, v%{i}
        v20 = (ps2)[0];
        v21 = (ps2)[1];
        v22 = (ps2)[2];
        // Load 'ps' to temporary variables v30,...
        // %%PERM24_BENES_LOAD ps%{i}, v%{i}
        v30 = (ps3)[0];
        v31 = (ps3)[1];
        v32 = (ps3)[2];

        sgn_perm0 >>= sign_shift;  // sign for permutation
        // Permute and possibly negate data in temp. variables
        // %%PERM24_BENES_PERMUTE benes_mask, sgn_perm%{i}, v%{i}
        // Permute the 24 small integers in '(v00, v01, v02)' 
        // using the Benes network given by 'benes_mask'. All small   
        // integers are negated if bit 0 of 'sign' is set.
        sgn_perm0 = (0-(sgn_perm0 & 0x1ULL)) & 0x7f7f7f7f7f7f7f7fULL;
        v00 ^= sgn_perm0;
        v01 ^= sgn_perm0;
        v02 ^= sgn_perm0;
        sgn_perm0 = (v00 ^ (v00 >> 8)) & benes_mask[0]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 8);
        sgn_perm0 = (v00 ^ (v00 >> 16)) & benes_mask[1]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 16);
        sgn_perm0 = (v00 ^ (v00 >> 32)) & benes_mask[2]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 32);
        sgn_perm0 = (v01 ^ (v01 >> 8)) & benes_mask[3]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 8);
        sgn_perm0 = (v01 ^ (v01 >> 16)) & benes_mask[4]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 16);
        sgn_perm0 = (v01 ^ (v01 >> 32)) & benes_mask[5]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 32);
        sgn_perm0 = (v02 ^ (v02 >> 8)) & benes_mask[6]; 
        v02 ^=  sgn_perm0 ^ (sgn_perm0 << 8);
        sgn_perm0 = (v02 ^ (v02 >> 16)) & benes_mask[7]; 
        v02 ^=  sgn_perm0 ^ (sgn_perm0 << 16);
        sgn_perm0 = (v02 ^ (v02 >> 32)) & benes_mask[8]; 
        v02 ^=  sgn_perm0 ^ (sgn_perm0 << 32);
        sgn_perm0 = (v00 ^ v01) & benes_mask[9]; 
        v00 ^=  sgn_perm0;  v01 ^=  sgn_perm0;
        sgn_perm0 = (v00 ^ v02) & benes_mask[10]; 
        v00 ^=  sgn_perm0;  v02 ^=  sgn_perm0;
        sgn_perm0 = (v00 ^ v01) & benes_mask[11]; 
        v00 ^=  sgn_perm0;  v01 ^=  sgn_perm0;
        sgn_perm0 = (v00 ^ (v00 >> 32)) & benes_mask[12]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 32);
        sgn_perm0 = (v00 ^ (v00 >> 16)) & benes_mask[13]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 16);
        sgn_perm0 = (v00 ^ (v00 >> 8)) & benes_mask[14]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 8);
        sgn_perm0 = (v01 ^ (v01 >> 32)) & benes_mask[15]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 32);
        sgn_perm0 = (v01 ^ (v01 >> 16)) & benes_mask[16]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 16);
        sgn_perm0 = (v01 ^ (v01 >> 8)) & benes_mask[17]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 8);
        sgn_perm0 = (v02 ^ (v02 >> 32)) & benes_mask[18]; 
        v02 ^=  sgn_perm0 ^ (sgn_perm0 << 32);
        sgn_perm0 = (v02 ^ (v02 >> 16)) & benes_mask[19]; 
        v02 ^=  sgn_perm0 ^ (sgn_perm0 << 16);
        sgn_perm0 = (v02 ^ (v02 >> 8)) & benes_mask[20]; 
        v02 ^=  sgn_perm0 ^ (sgn_perm0 << 8);
        // Permutation of small integers done.
        // Store temporary variables to 'p_dest'
        // %%PERM24_BENES_STORE "p_dest + %{int: i * V24_INTS}", v%{i}
(p_dest + 0)[0] = v00 ;
(p_dest + 0)[1] = v01 ;
(p_dest + 0)[2] = v02 ;
(p_dest + 0)[3] = 0;
        sgn_perm1 >>= sign_shift;  // sign for permutation
        // Permute and possibly negate data in temp. variables
        // %%PERM24_BENES_PERMUTE benes_mask, sgn_perm%{i}, v%{i}
// Permute the 24 small integers in '(v10, v11, v12)' 
// using the Benes network given by 'benes_mask'. All small   
// integers are negated if bit 0 of 'sign' is set.
sgn_perm1 = (0-(sgn_perm1 & 0x1ULL)) & 0x7f7f7f7f7f7f7f7fULL;
v10 ^= sgn_perm1;
v11 ^= sgn_perm1;
v12 ^= sgn_perm1;
sgn_perm1 = (v10 ^ (v10 >> 8)) & benes_mask[0]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 8);
sgn_perm1 = (v10 ^ (v10 >> 16)) & benes_mask[1]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 16);
sgn_perm1 = (v10 ^ (v10 >> 32)) & benes_mask[2]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 32);
sgn_perm1 = (v11 ^ (v11 >> 8)) & benes_mask[3]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 8);
sgn_perm1 = (v11 ^ (v11 >> 16)) & benes_mask[4]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 16);
sgn_perm1 = (v11 ^ (v11 >> 32)) & benes_mask[5]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 32);
sgn_perm1 = (v12 ^ (v12 >> 8)) & benes_mask[6]; 
v12 ^=  sgn_perm1 ^ (sgn_perm1 << 8);
sgn_perm1 = (v12 ^ (v12 >> 16)) & benes_mask[7]; 
v12 ^=  sgn_perm1 ^ (sgn_perm1 << 16);
sgn_perm1 = (v12 ^ (v12 >> 32)) & benes_mask[8]; 
v12 ^=  sgn_perm1 ^ (sgn_perm1 << 32);
sgn_perm1 = (v10 ^ v11) & benes_mask[9]; 
v10 ^=  sgn_perm1;  v11 ^=  sgn_perm1;
sgn_perm1 = (v10 ^ v12) & benes_mask[10]; 
v10 ^=  sgn_perm1;  v12 ^=  sgn_perm1;
sgn_perm1 = (v10 ^ v11) & benes_mask[11]; 
v10 ^=  sgn_perm1;  v11 ^=  sgn_perm1;
sgn_perm1 = (v10 ^ (v10 >> 32)) & benes_mask[12]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 32);
sgn_perm1 = (v10 ^ (v10 >> 16)) & benes_mask[13]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 16);
sgn_perm1 = (v10 ^ (v10 >> 8)) & benes_mask[14]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 8);
sgn_perm1 = (v11 ^ (v11 >> 32)) & benes_mask[15]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 32);
sgn_perm1 = (v11 ^ (v11 >> 16)) & benes_mask[16]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 16);
sgn_perm1 = (v11 ^ (v11 >> 8)) & benes_mask[17]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 8);
sgn_perm1 = (v12 ^ (v12 >> 32)) & benes_mask[18]; 
v12 ^=  sgn_perm1 ^ (sgn_perm1 << 32);
sgn_perm1 = (v12 ^ (v12 >> 16)) & benes_mask[19]; 
v12 ^=  sgn_perm1 ^ (sgn_perm1 << 16);
sgn_perm1 = (v12 ^ (v12 >> 8)) & benes_mask[20]; 
v12 ^=  sgn_perm1 ^ (sgn_perm1 << 8);
// Permutation of small integers done.
        // Store temporary variables to 'p_dest'
        // %%PERM24_BENES_STORE "p_dest + %{int: i * V24_INTS}", v%{i}
(p_dest + 4)[0] = v10 ;
(p_dest + 4)[1] = v11 ;
(p_dest + 4)[2] = v12 ;
(p_dest + 4)[3] = 0;
        sgn_perm2 >>= sign_shift;  // sign for permutation
        // Permute and possibly negate data in temp. variables
        // %%PERM24_BENES_PERMUTE benes_mask, sgn_perm%{i}, v%{i}
// Permute the 24 small integers in '(v20, v21, v22)' 
// using the Benes network given by 'benes_mask'. All small   
// integers are negated if bit 0 of 'sign' is set.
sgn_perm2 = (0-(sgn_perm2 & 0x1ULL)) & 0x7f7f7f7f7f7f7f7fULL;
v20 ^= sgn_perm2;
v21 ^= sgn_perm2;
v22 ^= sgn_perm2;
sgn_perm2 = (v20 ^ (v20 >> 8)) & benes_mask[0]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 8);
sgn_perm2 = (v20 ^ (v20 >> 16)) & benes_mask[1]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 16);
sgn_perm2 = (v20 ^ (v20 >> 32)) & benes_mask[2]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 32);
sgn_perm2 = (v21 ^ (v21 >> 8)) & benes_mask[3]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 8);
sgn_perm2 = (v21 ^ (v21 >> 16)) & benes_mask[4]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 16);
sgn_perm2 = (v21 ^ (v21 >> 32)) & benes_mask[5]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 32);
sgn_perm2 = (v22 ^ (v22 >> 8)) & benes_mask[6]; 
v22 ^=  sgn_perm2 ^ (sgn_perm2 << 8);
sgn_perm2 = (v22 ^ (v22 >> 16)) & benes_mask[7]; 
v22 ^=  sgn_perm2 ^ (sgn_perm2 << 16);
sgn_perm2 = (v22 ^ (v22 >> 32)) & benes_mask[8]; 
v22 ^=  sgn_perm2 ^ (sgn_perm2 << 32);
sgn_perm2 = (v20 ^ v21) & benes_mask[9]; 
v20 ^=  sgn_perm2;  v21 ^=  sgn_perm2;
sgn_perm2 = (v20 ^ v22) & benes_mask[10]; 
v20 ^=  sgn_perm2;  v22 ^=  sgn_perm2;
sgn_perm2 = (v20 ^ v21) & benes_mask[11]; 
v20 ^=  sgn_perm2;  v21 ^=  sgn_perm2;
sgn_perm2 = (v20 ^ (v20 >> 32)) & benes_mask[12]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 32);
sgn_perm2 = (v20 ^ (v20 >> 16)) & benes_mask[13]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 16);
sgn_perm2 = (v20 ^ (v20 >> 8)) & benes_mask[14]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 8);
sgn_perm2 = (v21 ^ (v21 >> 32)) & benes_mask[15]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 32);
sgn_perm2 = (v21 ^ (v21 >> 16)) & benes_mask[16]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 16);
sgn_perm2 = (v21 ^ (v21 >> 8)) & benes_mask[17]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 8);
sgn_perm2 = (v22 ^ (v22 >> 32)) & benes_mask[18]; 
v22 ^=  sgn_perm2 ^ (sgn_perm2 << 32);
sgn_perm2 = (v22 ^ (v22 >> 16)) & benes_mask[19]; 
v22 ^=  sgn_perm2 ^ (sgn_perm2 << 16);
sgn_perm2 = (v22 ^ (v22 >> 8)) & benes_mask[20]; 
v22 ^=  sgn_perm2 ^ (sgn_perm2 << 8);
// Permutation of small integers done.
        // Store temporary variables to 'p_dest'
        // %%PERM24_BENES_STORE "p_dest + %{int: i * V24_INTS}", v%{i}
(p_dest + 8)[0] = v20 ;
(p_dest + 8)[1] = v21 ;
(p_dest + 8)[2] = v22 ;
(p_dest + 8)[3] = 0;
        sgn_perm3 >>= sign_shift;  // sign for permutation
        // Permute and possibly negate data in temp. variables
        // %%PERM24_BENES_PERMUTE benes_mask, sgn_perm%{i}, v%{i}
// Permute the 24 small integers in '(v30, v31, v32)' 
// using the Benes network given by 'benes_mask'. All small   
// integers are negated if bit 0 of 'sign' is set.
sgn_perm3 = (0-(sgn_perm3 & 0x1ULL)) & 0x7f7f7f7f7f7f7f7fULL;
v30 ^= sgn_perm3;
v31 ^= sgn_perm3;
v32 ^= sgn_perm3;
sgn_perm3 = (v30 ^ (v30 >> 8)) & benes_mask[0]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 8);
sgn_perm3 = (v30 ^ (v30 >> 16)) & benes_mask[1]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 16);
sgn_perm3 = (v30 ^ (v30 >> 32)) & benes_mask[2]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 32);
sgn_perm3 = (v31 ^ (v31 >> 8)) & benes_mask[3]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 8);
sgn_perm3 = (v31 ^ (v31 >> 16)) & benes_mask[4]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 16);
sgn_perm3 = (v31 ^ (v31 >> 32)) & benes_mask[5]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 32);
sgn_perm3 = (v32 ^ (v32 >> 8)) & benes_mask[6]; 
v32 ^=  sgn_perm3 ^ (sgn_perm3 << 8);
sgn_perm3 = (v32 ^ (v32 >> 16)) & benes_mask[7]; 
v32 ^=  sgn_perm3 ^ (sgn_perm3 << 16);
sgn_perm3 = (v32 ^ (v32 >> 32)) & benes_mask[8]; 
v32 ^=  sgn_perm3 ^ (sgn_perm3 << 32);
sgn_perm3 = (v30 ^ v31) & benes_mask[9]; 
v30 ^=  sgn_perm3;  v31 ^=  sgn_perm3;
sgn_perm3 = (v30 ^ v32) & benes_mask[10]; 
v30 ^=  sgn_perm3;  v32 ^=  sgn_perm3;
sgn_perm3 = (v30 ^ v31) & benes_mask[11]; 
v30 ^=  sgn_perm3;  v31 ^=  sgn_perm3;
sgn_perm3 = (v30 ^ (v30 >> 32)) & benes_mask[12]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 32);
sgn_perm3 = (v30 ^ (v30 >> 16)) & benes_mask[13]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 16);
sgn_perm3 = (v30 ^ (v30 >> 8)) & benes_mask[14]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 8);
sgn_perm3 = (v31 ^ (v31 >> 32)) & benes_mask[15]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 32);
sgn_perm3 = (v31 ^ (v31 >> 16)) & benes_mask[16]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 16);
sgn_perm3 = (v31 ^ (v31 >> 8)) & benes_mask[17]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 8);
sgn_perm3 = (v32 ^ (v32 >> 32)) & benes_mask[18]; 
v32 ^=  sgn_perm3 ^ (sgn_perm3 << 32);
sgn_perm3 = (v32 ^ (v32 >> 16)) & benes_mask[19]; 
v32 ^=  sgn_perm3 ^ (sgn_perm3 << 16);
sgn_perm3 = (v32 ^ (v32 >> 8)) & benes_mask[20]; 
v32 ^=  sgn_perm3 ^ (sgn_perm3 << 8);
// Permutation of small integers done.
        // Store temporary variables to 'p_dest'
        // %%PERM24_BENES_STORE "p_dest + %{int: i * V24_INTS}", v%{i}
(p_dest + 12)[0] = v30 ;
(p_dest + 12)[1] = v31 ;
(p_dest + 12)[2] = v32 ;
(p_dest + 12)[3] = 0;

        p_perm += 4;
        p_dest += 16;
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
        uint_mmv_t *ps = p_src + ((sgn_perm & 0x7ff) << 2);
        // The following mask is used by the actual permutation code
        // %%PERM24_BENES_DECLARE "v"
uint_mmv_t v0, v1, v2;

        sgn_perm >>= 15;  // sign for permutation
        // Load 'ps' to temporary variables v0,...
        // %%PERM24_BENES_LOAD ps
v0 = (ps)[0];
v1 = (ps)[1];
v2 = (ps)[2];
        // Permute and possibly negate data in temp. variables
        // %%PERM24_BENES_PERMUTE benes_mask, sgn_perm
// Permute the 24 small integers in '(v0, v1, v2)' 
// using the Benes network given by 'benes_mask'. All small   
// integers are negated if bit 0 of 'sign' is set.
sgn_perm = (0-(sgn_perm & 0x1ULL)) & 0x7f7f7f7f7f7f7f7fULL;
v0 ^= sgn_perm;
v1 ^= sgn_perm;
v2 ^= sgn_perm;
sgn_perm = (v0 ^ (v0 >> 8)) & benes_mask[0]; 
v0 ^=  sgn_perm ^ (sgn_perm << 8);
sgn_perm = (v0 ^ (v0 >> 16)) & benes_mask[1]; 
v0 ^=  sgn_perm ^ (sgn_perm << 16);
sgn_perm = (v0 ^ (v0 >> 32)) & benes_mask[2]; 
v0 ^=  sgn_perm ^ (sgn_perm << 32);
sgn_perm = (v1 ^ (v1 >> 8)) & benes_mask[3]; 
v1 ^=  sgn_perm ^ (sgn_perm << 8);
sgn_perm = (v1 ^ (v1 >> 16)) & benes_mask[4]; 
v1 ^=  sgn_perm ^ (sgn_perm << 16);
sgn_perm = (v1 ^ (v1 >> 32)) & benes_mask[5]; 
v1 ^=  sgn_perm ^ (sgn_perm << 32);
sgn_perm = (v2 ^ (v2 >> 8)) & benes_mask[6]; 
v2 ^=  sgn_perm ^ (sgn_perm << 8);
sgn_perm = (v2 ^ (v2 >> 16)) & benes_mask[7]; 
v2 ^=  sgn_perm ^ (sgn_perm << 16);
sgn_perm = (v2 ^ (v2 >> 32)) & benes_mask[8]; 
v2 ^=  sgn_perm ^ (sgn_perm << 32);
sgn_perm = (v0 ^ v1) & benes_mask[9]; 
v0 ^=  sgn_perm;  v1 ^=  sgn_perm;
sgn_perm = (v0 ^ v2) & benes_mask[10]; 
v0 ^=  sgn_perm;  v2 ^=  sgn_perm;
sgn_perm = (v0 ^ v1) & benes_mask[11]; 
v0 ^=  sgn_perm;  v1 ^=  sgn_perm;
sgn_perm = (v0 ^ (v0 >> 32)) & benes_mask[12]; 
v0 ^=  sgn_perm ^ (sgn_perm << 32);
sgn_perm = (v0 ^ (v0 >> 16)) & benes_mask[13]; 
v0 ^=  sgn_perm ^ (sgn_perm << 16);
sgn_perm = (v0 ^ (v0 >> 8)) & benes_mask[14]; 
v0 ^=  sgn_perm ^ (sgn_perm << 8);
sgn_perm = (v1 ^ (v1 >> 32)) & benes_mask[15]; 
v1 ^=  sgn_perm ^ (sgn_perm << 32);
sgn_perm = (v1 ^ (v1 >> 16)) & benes_mask[16]; 
v1 ^=  sgn_perm ^ (sgn_perm << 16);
sgn_perm = (v1 ^ (v1 >> 8)) & benes_mask[17]; 
v1 ^=  sgn_perm ^ (sgn_perm << 8);
sgn_perm = (v2 ^ (v2 >> 32)) & benes_mask[18]; 
v2 ^=  sgn_perm ^ (sgn_perm << 32);
sgn_perm = (v2 ^ (v2 >> 16)) & benes_mask[19]; 
v2 ^=  sgn_perm ^ (sgn_perm << 16);
sgn_perm = (v2 ^ (v2 >> 8)) & benes_mask[20]; 
v2 ^=  sgn_perm ^ (sgn_perm << 8);
// Permutation of small integers done.
        // Store temporary variables to 'p_dest'
        // %%PERM24_BENES_STORE p_dest
(p_dest)[0] = v0 ;
(p_dest)[1] = v1 ;
(p_dest)[2] = v2 ;
(p_dest)[3] = 0;
        p_dest +=  4;      
        }
}

// %%END IF





/// @endcond  


/***************************************************************
* Operation x_delta * x_pi
***************************************************************/

/// @cond DO_NOT_DOCUMENT 


/**
  @brief Workhorse for function ``mm_op127_pi``

  ``mm_op127_pi(v_in, delta, pi, v_out)`` is equivalent to

        mm_sub_op_pi_type s_op; // defined in mm_basics.h
        // Borrow memory from v_out suficient for an array of 759
        // entries of type  ``mm_sub_op_pi64_type``
        s_op.tbl_perm64 = (mm_sub_op_pi64_type*)(v_out + MM_OP127_OFS_X);
        mm_sub_prep_pi(delta, pi, &s_op);
        mm_op127_do_pi(v_in, &s_op, v_out);

   So the functions called by function ``mm_op127_pi``
   can be tested individually.
*/
static
void mm_op127_do_pi(uint_mmv_t *v_in, mm_sub_op_pi_type *p_op, uint_mmv_t * v_out)
{
    uint_mmv_t *a_src[3], *a_dest[3];
    uint16_t *p_perm1 = p_op->tbl_perm24_big;

    // %%IF PERM24_USE_BENES_NET
    uint_mmv_t small_perm[21]; 

    // Prepare mask array from Benes network
    // %%PERM24_BENES_PREPARE "p_op->benes_net", small_perm
{
    uint_mmv_t tmp; 
    uint_fast8_t i;
    static uint8_t tbl[] = {
        // %%TABLE table_prepare_perm24, uint8_t
    0x00,0x01,0x02,0x10,0x11,0x12,0x20,0x21,
    0x22,0x03,0x04,0x05,0x06,0x07,0x08,0x16,
    0x17,0x18,0x26,0x27,0x28
    };

    for(i = 0; i < 21; ++i) {
        tmp = tbl[i];
        tmp = (p_op->benes_net)[tmp & 15] >> ((tmp & 0xf0) >> 1);
        // %%MMV_UINT_SPREAD tmp, tmp
        // Spread bits 0,...,7 of tmp to the (8-bit long) fields
        // of tmp. A field of tmp is set to 0x7f if its 
        // corresponding bit in input tmp is one and to 0 otherwise.
        tmp = (tmp & 0xfULL) + ((tmp & 0xf0ULL) << 28);
        tmp = (tmp & 0x300000003ULL) 
            +  ((tmp & 0xc0000000cULL) << 14);
        tmp = (tmp & 0x1000100010001ULL) 
            +  ((tmp & 0x2000200020002ULL) << 7);
        tmp *= 127;
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
        uint_mmv_t *p_out = v_out + MM_OP127_OFS_T;
        uint_mmv_t *p_end = p_out + 759 * 8;
        uint_mmv_t *v1_in =  v_in + MM_OP127_OFS_T;
        for (; p_out < p_end; p_out += 8) {
            {
               uint_mmv_t v = p_perm->preimage;
               uint_mmv_t *p_in = v1_in + ((v & 0x3ff) << 3);
               // %%LOAD_PERM64 p_in, bytes, v, uint8_t
               uint_mmv_t r0;
               v = (0-((v >> 12) & 1)) & 0x7f7f7f7f7f7f7f7fULL;
               r0 =  (p_in)[0] ^ (v);
               r0 &= 0x7f7f7f7f7f7f7f7fULL;
               (bytes)[0] = (uint8_t)(r0 >> 0);
               (bytes)[1] = (uint8_t)(r0 >> 8);
               (bytes)[2] = (uint8_t)(r0 >> 16);
               (bytes)[3] = (uint8_t)(r0 >> 24);
               (bytes)[4] = (uint8_t)(r0 >> 32);
               (bytes)[5] = (uint8_t)(r0 >> 40);
               (bytes)[6] = (uint8_t)(r0 >> 48);
               (bytes)[7] = (uint8_t)(r0 >> 56);
               r0 =  (p_in)[1] ^ (v);
               r0 &= 0x7f7f7f7f7f7f7f7fULL;
               (bytes)[8] = (uint8_t)(r0 >> 0);
               (bytes)[9] = (uint8_t)(r0 >> 8);
               (bytes)[10] = (uint8_t)(r0 >> 16);
               (bytes)[11] = (uint8_t)(r0 >> 24);
               (bytes)[12] = (uint8_t)(r0 >> 32);
               (bytes)[13] = (uint8_t)(r0 >> 40);
               (bytes)[14] = (uint8_t)(r0 >> 48);
               (bytes)[15] = (uint8_t)(r0 >> 56);
               r0 =  (p_in)[2] ^ (v);
               r0 &= 0x7f7f7f7f7f7f7f7fULL;
               (bytes)[16] = (uint8_t)(r0 >> 0);
               (bytes)[17] = (uint8_t)(r0 >> 8);
               (bytes)[18] = (uint8_t)(r0 >> 16);
               (bytes)[19] = (uint8_t)(r0 >> 24);
               (bytes)[20] = (uint8_t)(r0 >> 32);
               (bytes)[21] = (uint8_t)(r0 >> 40);
               (bytes)[22] = (uint8_t)(r0 >> 48);
               (bytes)[23] = (uint8_t)(r0 >> 56);
               r0 =  (p_in)[3] ^ (v);
               r0 &= 0x7f7f7f7f7f7f7f7fULL;
               (bytes)[24] = (uint8_t)(r0 >> 0);
               (bytes)[25] = (uint8_t)(r0 >> 8);
               (bytes)[26] = (uint8_t)(r0 >> 16);
               (bytes)[27] = (uint8_t)(r0 >> 24);
               (bytes)[28] = (uint8_t)(r0 >> 32);
               (bytes)[29] = (uint8_t)(r0 >> 40);
               (bytes)[30] = (uint8_t)(r0 >> 48);
               (bytes)[31] = (uint8_t)(r0 >> 56);
               r0 =  (p_in)[4] ^ (v);
               r0 &= 0x7f7f7f7f7f7f7f7fULL;
               (bytes)[32] = (uint8_t)(r0 >> 0);
               (bytes)[33] = (uint8_t)(r0 >> 8);
               (bytes)[34] = (uint8_t)(r0 >> 16);
               (bytes)[35] = (uint8_t)(r0 >> 24);
               (bytes)[36] = (uint8_t)(r0 >> 32);
               (bytes)[37] = (uint8_t)(r0 >> 40);
               (bytes)[38] = (uint8_t)(r0 >> 48);
               (bytes)[39] = (uint8_t)(r0 >> 56);
               r0 =  (p_in)[5] ^ (v);
               r0 &= 0x7f7f7f7f7f7f7f7fULL;
               (bytes)[40] = (uint8_t)(r0 >> 0);
               (bytes)[41] = (uint8_t)(r0 >> 8);
               (bytes)[42] = (uint8_t)(r0 >> 16);
               (bytes)[43] = (uint8_t)(r0 >> 24);
               (bytes)[44] = (uint8_t)(r0 >> 32);
               (bytes)[45] = (uint8_t)(r0 >> 40);
               (bytes)[46] = (uint8_t)(r0 >> 48);
               (bytes)[47] = (uint8_t)(r0 >> 56);
               r0 =  (p_in)[6] ^ (v);
               r0 &= 0x7f7f7f7f7f7f7f7fULL;
               (bytes)[48] = (uint8_t)(r0 >> 0);
               (bytes)[49] = (uint8_t)(r0 >> 8);
               (bytes)[50] = (uint8_t)(r0 >> 16);
               (bytes)[51] = (uint8_t)(r0 >> 24);
               (bytes)[52] = (uint8_t)(r0 >> 32);
               (bytes)[53] = (uint8_t)(r0 >> 40);
               (bytes)[54] = (uint8_t)(r0 >> 48);
               (bytes)[55] = (uint8_t)(r0 >> 56);
               r0 =  (p_in)[7] ^ (v);
               r0 &= 0x7f7f7f7f7f7f7f7fULL;
               (bytes)[56] = (uint8_t)(r0 >> 0);
               (bytes)[57] = (uint8_t)(r0 >> 8);
               (bytes)[58] = (uint8_t)(r0 >> 16);
               (bytes)[59] = (uint8_t)(r0 >> 24);
               (bytes)[60] = (uint8_t)(r0 >> 32);
               (bytes)[61] = (uint8_t)(r0 >> 40);
               (bytes)[62] = (uint8_t)(r0 >> 48);
               (bytes)[63] = (uint8_t)(r0 >> 56);
            }
            {
               // %%STORE_PERM64 bytes, p_out, "(p_perm->perm)"
               uint_mmv_t v;
               uint_fast8_t ri, r0, r1, r2;
               r0 = (p_perm->perm)[0];
               r1 = (p_perm->perm)[1];
               r2 = (p_perm->perm)[2];
               ri = r0;
               v = (uint_mmv_t)(bytes[0]) << 0;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               p_out[0] = v ;
               ri ^= (p_perm->perm)[3];
               v = (uint_mmv_t)(bytes[ri]) << 0;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               p_out[1] = v ;
               ri ^= (p_perm->perm)[4];
               v = (uint_mmv_t)(bytes[ri]) << 0;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               p_out[2] = v ;
               ri ^= (p_perm->perm)[3];
               v = (uint_mmv_t)(bytes[ri]) << 0;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               p_out[3] = v ;
               ri ^= (p_perm->perm)[5];
               v = (uint_mmv_t)(bytes[ri]) << 0;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               p_out[4] = v ;
               ri ^= (p_perm->perm)[3];
               v = (uint_mmv_t)(bytes[ri]) << 0;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               p_out[5] = v ;
               ri ^= (p_perm->perm)[4];
               v = (uint_mmv_t)(bytes[ri]) << 0;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               p_out[6] = v ;
               ri ^= (p_perm->perm)[3];
               v = (uint_mmv_t)(bytes[ri]) << 0;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               p_out[7] = v ;
            }
            ++p_perm;
        } 
    }

    // Step 2: do rows with 24 entries 
    // TODO: comment properly!!!!
    a_src[0] = v_in + MM_OP127_OFS_X;
    a_dest[0] = v_out + MM_OP127_OFS_X;
    a_src[1] = v_in + MM_OP127_OFS_Z;
    a_src[2] = v_in + MM_OP127_OFS_Y;
    if (p_op->eps & 0x800) {
        a_dest[1] = v_out + MM_OP127_OFS_Y;
        a_dest[2] = v_out + MM_OP127_OFS_Z;
    } else {
        a_dest[1] = v_out + MM_OP127_OFS_Z;
        a_dest[2] = v_out + MM_OP127_OFS_Y;
    }

    {
        uint_fast32_t i;
        for (i = 0; i < 3; ++i) 
            pi24_2048(a_src[i], p_perm1, small_perm, i + 12, a_dest[i]);
    }


    // If d is odd: negate some entries    
    if (p_op->eps & 0x800) {
        uint_fast16_t i;
        uint_mmv_t *v = v_out + MM_OP127_OFS_T;

        // Step odd 1:  negate suboctads of weight 4n+2 for tag T
        for (i = 0; i < 759; ++i) {
            // %%INVERT_PERM64 v
            v[0] ^= 0x7f7f7f7f7f7f00ULL;
            v[1] ^= 0x7f007f7f7fULL;
            v[2] ^= 0x7f007f7f7fULL;
            v[3] ^= 0x7f0000000000007fULL;
            v[4] ^= 0x7f007f7f7fULL;
            v[5] ^= 0x7f0000000000007fULL;
            v[6] ^= 0x7f0000000000007fULL;
            v[7] ^= 0x7f7f7f007f000000ULL;
            v += 8;
        }

        mm_op127_neg_scalprod_d_i(v); 
    }
} 

/// @endcond 



/**
  @brief Compute automophism of the Parker loop on a vector

  Let ``v_in`` be a vector of the representation \f$\rho_{127}\f$
  of the monster group. 

  The integers ``d`` and ``p`` describe an automorphism of the
  Parker loop as indicated in the header of this file. The function
  computes this automorphism on the input  vector ``v_in`` and 
  stores the result in the output vector ``v_out.`` 

  Input vector  ``v_in`` is not changed.
*/
// %%EXPORT px
MM_OP127_API
void mm_op127_pi(uint_mmv_t *v_in, uint32_t delta, uint32_t pi, uint_mmv_t * v_out)
{
    mm_sub_op_pi_type s_op;
    // Borrow memory from v_out
    s_op.tbl_perm64 = (mm_sub_op_pi64_type *)(v_out + MM_OP127_OFS_X);
    mm_sub_prep_pi(delta, pi, &s_op);
    mm_op127_do_pi(v_in, &s_op, v_out);
}


/**
  @brief Simplified version of function ``mm_op127_pi``

  ``mm_op127_delta(v_in, delta, v_out)`` is equivalent to
  ``mm_op127_pi(v_in, 0, delta, v_out)``, but much faster.
  
*/
// %%EXPORT px
MM_OP127_API
void mm_op127_delta(uint_mmv_t *v_in, uint32_t delta, uint_mmv_t * v_out)
{
    uint_fast32_t i, i1;
    // Borrow space from ``v_out`` sufficient for an array of length 2048
    uint8_t *signs = (uint8_t*)(v_out + MM_OP127_OFS_T);
    uint_mmv_t *a_src[3], *a_dest[3];

    mat24_op_all_cocode(delta, signs);
    for (i = 0; i < 72; ++i) signs[i] &= 7;
    for (i = 48; i < 72; ++i) signs[i] |= (delta & 0x800) >> (11 - 3);

    a_src[0] = v_in + MM_OP127_OFS_X;
    a_dest[0] = v_out + MM_OP127_OFS_X;
    a_src[1] = v_in + MM_OP127_OFS_Z;
    a_src[2] = v_in + MM_OP127_OFS_Y;
    if (delta & 0x800) {
        a_dest[1] = v_out + MM_OP127_OFS_Y;
        a_dest[2] = v_out + MM_OP127_OFS_Z;
    } else {
        a_dest[1] = v_out + MM_OP127_OFS_Z;
        a_dest[2] = v_out + MM_OP127_OFS_Y;
    }

    // Step 1: do rows with 24 entries 
    // TODO: comment properly!!!!
    for (i = 0; i < 3; ++i)  {
        for (i1 = 0; i1 < 2048; ++i1) {
            uint_mmv_t *p_src = a_src[i] + (i1 << 2);
            uint_mmv_t *p_dest = a_dest[i] + (i1 << 2);
            uint_mmv_t sgn = -((signs[i1] >> i) & 1);
            // %%FOR i in range(V24_INTS_USED)
            sgn &= 0x7f7f7f7f7f7f7f7fULL;
            p_dest[0] = p_src[0]  ^ sgn;
            p_dest[1] = p_src[1]  ^ sgn;
            p_dest[2] = p_src[2]  ^ sgn;
            // %%END FOR
            p_dest[3] = 0;
        }        
    }    

    {
        uint_mmv_t *p_src = v_in + MM_OP127_OFS_A;
        uint_mmv_t *p_dest = v_out + MM_OP127_OFS_A;
        for (i1 = 0; i1 < 72; ++i1) {
            uint_mmv_t sgn = -((signs[i1] >> i) & 1);
            // %%FOR i in range(V24_INTS_USED)
            sgn &= 0x7f7f7f7f7f7f7f7fULL;
            p_dest[0] = p_src[0]  ^ sgn;
            p_dest[1] = p_src[1]  ^ sgn;
            p_dest[2] = p_src[2]  ^ sgn;
            // %%END FOR
            p_dest[3] = 0;
            p_src +=  4;      
            p_dest +=  4;      
        }        
    }    


    // Step 2: do rows with 64 entries 
    // TODO: comment properly!!!!
    {
        v_in +=  MM_OP127_OFS_T;
        v_out += MM_OP127_OFS_T;
        for (i = 0; i < 759; ++i) {
            uint_mmv_t sign = mat24_def_octad_to_gcode(i) & delta;
            mat24_def_parity12(sign);
            sign = 0 - sign;
            sign &= 0x7f7f7f7f7f7f7f7fULL;
            // %%FOR i in range(%{V64_INTS})
            v_out[0] = v_in[0]  ^  sign;
            v_out[1] = v_in[1]  ^  sign;
            v_out[2] = v_in[2]  ^  sign;
            v_out[3] = v_in[3]  ^  sign;
            v_out[4] = v_in[4]  ^  sign;
            v_out[5] = v_in[5]  ^  sign;
            v_out[6] = v_in[6]  ^  sign;
            v_out[7] = v_in[7]  ^  sign;
            // %%END FOR
            v_in += 8;
            v_out += 8;
        } 
        v_out -= 759 * 8 +  MM_OP127_OFS_T; // restore v_out
    }

    // If d is odd: negate some entries    
    if (delta & 0x800) {
        uint_mmv_t *v = v_out + MM_OP127_OFS_T;

        // Step odd 1:  negate suboctads of weight 4n+2 for tag T
        for (i = 0; i < 759; ++i) {
            // %%INVERT_PERM64 v
v[0] ^= 0x7f7f7f7f7f7f00ULL;
v[1] ^= 0x7f007f7f7fULL;
v[2] ^= 0x7f007f7f7fULL;
v[3] ^= 0x7f0000000000007fULL;
v[4] ^= 0x7f007f7f7fULL;
v[5] ^= 0x7f0000000000007fULL;
v[6] ^= 0x7f0000000000007fULL;
v[7] ^= 0x7f7f7f007f000000ULL;
            v += 8;
        }

        mm_op127_neg_scalprod_d_i(v); 
    }
}

/**
  @brief Restriction of function ``mm_op127_pi`` to tag ``ABC``

  Function ``mm_op127_pi`` computes an automorphism of the
  Parker loop on a vector ``v_in`` and stores the result
  in ``v_out``. That automorphism depends on parameters
  ``delta``  and ``p``.
  
  Function ``mm_op127_pi_tag_ABC`` computes the same
  automorphism on the entries of the vector ``v = v_in`` with
  tags ``ABC`` only, and ignores the other entries of ``v``.
  See section **The representation of the monster group**
  in the **API reference** for tags of entries of a vector in
  the representation of the monster.

  The function overwrites the vector ``v`` with the result.
  Here only entries of ``v`` with tag ``ABC`` are changed.

  If parameter ``mode`` is set then we perform the operation on
  entries with tag ``A`` only. This  function is much faster 
  than function ``mm_op127_pi``.
*/
// %%EXPORT px
MM_OP127_API
void mm_op127_pi_tag_ABC(uint_mmv_t *v, uint32_t delta, uint32_t pi, uint32_t mode)
{
    uint_mmv_t v_tmp[24 *  4];
    uint16_t row_perm[24];
    uint8_t perm[24], col_perm[48];
    uint_fast32_t i, j;

    pi %= MAT24_ORDER;
    mat24_m24num_to_perm(pi, perm);
    
    for(i = 0; i < 24; ++i) {
        j = perm[i];
        row_perm[j] = (uint16_t)i;
        col_perm[j+j] = ((uint8_t)i >> 3);
        col_perm[j+j+1] 
            = ((uint8_t)i & 0x7ULL) << 3;
    }
    pi24_n(v, row_perm, col_perm, v_tmp, 24);
    for (i = 0; i < 24 *  4; ++i) v[i] = v_tmp[i];
    if (mode) return;

    v += 24 *  4;
    pi24_n(v, row_perm, col_perm, v_tmp, 24);
    for (i = 0; i < 24 *  4; ++i) v[i] = v_tmp[i];

    v += 24 *  4;
    if (delta & 0x800) for(i = 0; i < 24; ++i) row_perm[i] ^= 0x8000;
    pi24_n(v, row_perm, col_perm, v_tmp, 24);
    for (i = 0; i < 24 *  4; ++i) v[i] = v_tmp[i];
 
}




/**
  @brief Restriction of function ``mm_op127_pi`` to tag ``ABC``

  Function ``mm_op127_delta`` computes an automorphism of the
  Parker loop on a vector ``v_in`` and stores the result
  in ``v_out``. That automorphism depends on parameter ``d``.
  
  Function ``mm_op127_delta_tag_ABC`` computes the same
  automorphism on the entries of the vector ``v = v_in`` with
  tags ``ABC`` only, and ignores the other entries of ``v``.
  See section **The representation of the monster group**
  in the **API reference** for tags of entries of a vector in
  the representation of the monster.

  The function overwrites the vector ``v`` with the result.
  Here only entries of ``v`` with tag ``ABC`` are changed.

  If parameter ``mode`` is set then we perform the operation on
  entries with tag ``A`` only. This  function is much faster 
  than function ``mm_op127_delta``.
*/
// %%EXPORT px
MM_OP127_API
void mm_op127_delta_tag_ABC(uint_mmv_t *v, uint32_t d, uint32_t mode)
{
    uint32_t i1;

    if (mode || (d & 0x800) == 0) return;
    v += 2 * 24 * 4;
    for (i1 = 0; i1 < 24; ++i1) {
        v[0] ^=  0x7f7f7f7f7f7f7f7fULL;
        v[1] ^=  0x7f7f7f7f7f7f7f7fULL;
        v[2] ^=  0x7f7f7f7f7f7f7f7fULL;
        v +=  4;      
    }
}



//  %%GEN h
//  %%GEN c

