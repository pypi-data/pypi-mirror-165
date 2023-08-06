/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm7_op_xi.c

 File ``mm7_op_xi.c`` implements the operation of the element
 \f$\xi^e\f$ of the monster group on a vector in the
 representation \f$\rho_{7}\f$ of the monster.

 Here the generator \f$\xi\f$ of the monster group is defined as 
 in section **The monster group** of the **API reference**.

 The representation \f$\rho_{7}\f$ is equal to the
 196884-dimensional representation  \f$\rho\f$ of the monster,
 with coefficients taken modulo 7, as defined in
 section **The representation of the monster group**
 in the **API reference**.

 An element of \f$\rho_{7}\f$ is implemented as an array of
 integers of type ``uint_mmv_t`` as described in
 section **Description of the mmgroup.mm extension**
 in this document.

 We have \f$\xi^3 = 1\f$, and the opration of \f$\xi^e, e = 1,2\f$
 on \f$\rho\f$ is given in [Seysen19], section 9.4 - 9.6. The
 non-monomial part of the operation of \f$\xi^e\f$ can be decomposed
 into a product of monomial matrices and matrices containing
 blocks of \f$2 \times 2\f$ Hadamard matrices. We use the Python
 functions and classes in files ``hadamard_codegen.py`` and
 ``hadamard_xi.py`` in subdirectory ``mmgroup/dev/hadamard`` for
 generating C code that implements the products of Hadamard
 matrices corresponding to the generator \f$\xi^e\f$.

 Although the monomial part of the operation of \f$\xi^e\f$ is
 described in [Seysen19], we have not found an easy way to 
 convert that description to a C function. So we use (rather
 large) tables for implementing these operations. The C file
 ``mm_tables_xi.c`` contains these tables as static arrays and
 also an array ``mm_sub_table_xi`` that provides public 
 access to these tables. The same tables are used for the
 operations on \f$\rho_p\f$ for all characteritics \f$p\f$. 
*/

#include <string.h>
#include "mat24_functions.h"
#include "mm_op7.h"   

// %%EXPORT_KWD MM_OP%{P}_API


//  %%GEN h
//  %%GEN c




/// @cond DO_NOT_DOCUMENT 

static void mm_op7_xi_mon(
    uint_mmv_t * v_in,  
    uint32_t exp1, 
    uint_mmv_t * v_out
)
{
    // Caution: this uses v_out[MM_OP7_OFS_Z:] as temporary storage
    uint_mmv_t *p_src, *p_dest;
    uint_fast32_t i, j;
    uint_fast32_t diff = exp1 ? 2048 : 0;
    uint8_t *b =  (uint8_t*)(v_out + MM_OP7_OFS_Z), *p_b;
    mm_sub_table_xi_type *p_tables = mm_sub_table_xi[exp1];
    uint16_t *p_perm;
    uint32_t *p_sign;



    ///////////////////////////////////////////////////////////////
    // Map tag BC to tag BC.
    ///////////////////////////////////////////////////////////////
    p_src = v_in + 48;
    p_dest = v_out + 48;
    p_sign = p_tables[0].p_sign;
    p_perm = p_tables[0].p_perm;

    for (i = 0; i < 1; ++i) {
        p_b = b;
        
        for (j = 0; j < 78; ++j) {
           // %%OP_XI_LOAD p_src, p_b, %{i_src.SHAPE[2]}, uint8_t
           uint_mmv_t r0, r1;
           r0 =  (p_src)[0];
           r1 = (r0 >> 4) & 0x707070707070707ULL;
           r0 &= 0x707070707070707ULL;
           (p_b)[0] = (uint8_t)(r0 >> 0);
           (p_b)[1] = (uint8_t)(r1 >> 0);
           (p_b)[2] = (uint8_t)(r0 >> 8);
           (p_b)[3] = (uint8_t)(r1 >> 8);
           (p_b)[4] = (uint8_t)(r0 >> 16);
           (p_b)[5] = (uint8_t)(r1 >> 16);
           (p_b)[6] = (uint8_t)(r0 >> 24);
           (p_b)[7] = (uint8_t)(r1 >> 24);
           (p_b)[8] = (uint8_t)(r0 >> 32);
           (p_b)[9] = (uint8_t)(r1 >> 32);
           (p_b)[10] = (uint8_t)(r0 >> 40);
           (p_b)[11] = (uint8_t)(r1 >> 40);
           (p_b)[12] = (uint8_t)(r0 >> 48);
           (p_b)[13] = (uint8_t)(r1 >> 48);
           (p_b)[14] = (uint8_t)(r0 >> 56);
           (p_b)[15] = (uint8_t)(r1 >> 56);
           r0 =  (p_src)[1];
           r1 = (r0 >> 4) & 0x707070707070707ULL;
           r0 &= 0x707070707070707ULL;
           (p_b)[16] = (uint8_t)(r0 >> 0);
           (p_b)[17] = (uint8_t)(r1 >> 0);
           (p_b)[18] = (uint8_t)(r0 >> 8);
           (p_b)[19] = (uint8_t)(r1 >> 8);
           (p_b)[20] = (uint8_t)(r0 >> 16);
           (p_b)[21] = (uint8_t)(r1 >> 16);
           (p_b)[22] = (uint8_t)(r0 >> 24);
           (p_b)[23] = (uint8_t)(r1 >> 24);
           (p_b)[24] = (uint8_t)(r0 >> 32);
           (p_b)[25] = (uint8_t)(r1 >> 32);
           (p_b)[26] = (uint8_t)(r0 >> 40);
           (p_b)[27] = (uint8_t)(r1 >> 40);
           (p_b)[28] = (uint8_t)(r0 >> 48);
           (p_b)[29] = (uint8_t)(r1 >> 48);
           (p_b)[30] = (uint8_t)(r0 >> 56);
           (p_b)[31] = (uint8_t)(r1 >> 56);
           p_src += 2;
           p_b += 32;
        }
        
        for (j = 0; j < 78; ++j) {
           // %%OP_XI_STORE b, p_perm, p_sign, p_dest, %{i_dest.SHAPE[2]}
           uint_mmv_t r0, r1;
           r0 = ((uint_mmv_t)(b[p_perm[0]]) << 0)
             + ((uint_mmv_t)(b[p_perm[1]]) << 4)
             + ((uint_mmv_t)(b[p_perm[2]]) << 8)
             + ((uint_mmv_t)(b[p_perm[3]]) << 12)
             + ((uint_mmv_t)(b[p_perm[4]]) << 16)
             + ((uint_mmv_t)(b[p_perm[5]]) << 20)
             + ((uint_mmv_t)(b[p_perm[6]]) << 24)
             + ((uint_mmv_t)(b[p_perm[7]]) << 28)
             + ((uint_mmv_t)(b[p_perm[8]]) << 32)
             + ((uint_mmv_t)(b[p_perm[9]]) << 36)
             + ((uint_mmv_t)(b[p_perm[10]]) << 40)
             + ((uint_mmv_t)(b[p_perm[11]]) << 44)
             + ((uint_mmv_t)(b[p_perm[12]]) << 48)
             + ((uint_mmv_t)(b[p_perm[13]]) << 52)
             + ((uint_mmv_t)(b[p_perm[14]]) << 56)
             + ((uint_mmv_t)(b[p_perm[15]]) << 60);
           r1 = (p_sign)[0] >> 0;
           // Spread bits 0,...,15 of r1 to the (4-bit long) fields
           // of r1. A field of r1 is set to 0x7 if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xffULL) + ((r1 & 0xff00ULL) << 24);
           r1 = (r1 & 0xf0000000fULL) 
               +  ((r1 & 0xf0000000f0ULL) << 12);
           r1 = (r1 & 0x3000300030003ULL) 
               +  ((r1 & 0xc000c000c000cULL) << 6);
           r1 = (r1 & 0x101010101010101ULL) 
               +  ((r1 & 0x202020202020202ULL) << 3);
           r1 *= 7;
           // Bit spreading done.
           (p_dest)[0] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[16]]) << 0)
             + ((uint_mmv_t)(b[p_perm[17]]) << 4)
             + ((uint_mmv_t)(b[p_perm[18]]) << 8)
             + ((uint_mmv_t)(b[p_perm[19]]) << 12)
             + ((uint_mmv_t)(b[p_perm[20]]) << 16)
             + ((uint_mmv_t)(b[p_perm[21]]) << 20)
             + ((uint_mmv_t)(b[p_perm[22]]) << 24)
             + ((uint_mmv_t)(b[p_perm[23]]) << 28)
             + ((uint_mmv_t)(b[p_perm[24]]) << 32)
             + ((uint_mmv_t)(b[p_perm[25]]) << 36)
             + ((uint_mmv_t)(b[p_perm[26]]) << 40)
             + ((uint_mmv_t)(b[p_perm[27]]) << 44)
             + ((uint_mmv_t)(b[p_perm[28]]) << 48)
             + ((uint_mmv_t)(b[p_perm[29]]) << 52)
             + ((uint_mmv_t)(b[p_perm[30]]) << 56)
             + ((uint_mmv_t)(b[p_perm[31]]) << 60);
           r1 = (p_sign)[0] >> 16;
           // Spread bits 0,...,15 of r1 to the (4-bit long) fields
           // of r1. A field of r1 is set to 0x7 if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xffULL) + ((r1 & 0xff00ULL) << 24);
           r1 = (r1 & 0xf0000000fULL) 
               +  ((r1 & 0xf0000000f0ULL) << 12);
           r1 = (r1 & 0x3000300030003ULL) 
               +  ((r1 & 0xc000c000c000cULL) << 6);
           r1 = (r1 & 0x101010101010101ULL) 
               +  ((r1 & 0x202020202020202ULL) << 3);
           r1 *= 7;
           // Bit spreading done.
           (p_dest)[1] = r0 ^ r1;
           p_dest += 2;
           p_perm += 32;
           p_sign += 1;
        }
        
    }

    ///////////////////////////////////////////////////////////////
    // Map tag T0 to tag T0.
    ///////////////////////////////////////////////////////////////
    p_src = v_in + 204;
    p_dest = v_out + 204;
    p_sign = p_tables[1].p_sign;
    p_perm = p_tables[1].p_perm;

    for (i = 0; i < 45; ++i) {
        p_b = b;
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_LOAD p_src, p_b, %{i_src.SHAPE[2]}, uint8_t
           uint_mmv_t r0, r1;
           r0 =  (p_src)[0];
           r1 = (r0 >> 4) & 0x707070707070707ULL;
           r0 &= 0x707070707070707ULL;
           (p_b)[0] = (uint8_t)(r0 >> 0);
           (p_b)[1] = (uint8_t)(r1 >> 0);
           (p_b)[2] = (uint8_t)(r0 >> 8);
           (p_b)[3] = (uint8_t)(r1 >> 8);
           (p_b)[4] = (uint8_t)(r0 >> 16);
           (p_b)[5] = (uint8_t)(r1 >> 16);
           (p_b)[6] = (uint8_t)(r0 >> 24);
           (p_b)[7] = (uint8_t)(r1 >> 24);
           (p_b)[8] = (uint8_t)(r0 >> 32);
           (p_b)[9] = (uint8_t)(r1 >> 32);
           (p_b)[10] = (uint8_t)(r0 >> 40);
           (p_b)[11] = (uint8_t)(r1 >> 40);
           (p_b)[12] = (uint8_t)(r0 >> 48);
           (p_b)[13] = (uint8_t)(r1 >> 48);
           (p_b)[14] = (uint8_t)(r0 >> 56);
           (p_b)[15] = (uint8_t)(r1 >> 56);
           r0 =  (p_src)[1];
           r1 = (r0 >> 4) & 0x707070707070707ULL;
           r0 &= 0x707070707070707ULL;
           (p_b)[16] = (uint8_t)(r0 >> 0);
           (p_b)[17] = (uint8_t)(r1 >> 0);
           (p_b)[18] = (uint8_t)(r0 >> 8);
           (p_b)[19] = (uint8_t)(r1 >> 8);
           (p_b)[20] = (uint8_t)(r0 >> 16);
           (p_b)[21] = (uint8_t)(r1 >> 16);
           (p_b)[22] = (uint8_t)(r0 >> 24);
           (p_b)[23] = (uint8_t)(r1 >> 24);
           (p_b)[24] = (uint8_t)(r0 >> 32);
           (p_b)[25] = (uint8_t)(r1 >> 32);
           (p_b)[26] = (uint8_t)(r0 >> 40);
           (p_b)[27] = (uint8_t)(r1 >> 40);
           (p_b)[28] = (uint8_t)(r0 >> 48);
           (p_b)[29] = (uint8_t)(r1 >> 48);
           (p_b)[30] = (uint8_t)(r0 >> 56);
           (p_b)[31] = (uint8_t)(r1 >> 56);
           p_src += 2;
           p_b += 32;
        }
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_STORE b, p_perm, p_sign, p_dest, %{i_dest.SHAPE[2]}
           uint_mmv_t r0, r1;
           r0 = ((uint_mmv_t)(b[p_perm[0]]) << 0)
             + ((uint_mmv_t)(b[p_perm[1]]) << 4)
             + ((uint_mmv_t)(b[p_perm[2]]) << 8)
             + ((uint_mmv_t)(b[p_perm[3]]) << 12)
             + ((uint_mmv_t)(b[p_perm[4]]) << 16)
             + ((uint_mmv_t)(b[p_perm[5]]) << 20)
             + ((uint_mmv_t)(b[p_perm[6]]) << 24)
             + ((uint_mmv_t)(b[p_perm[7]]) << 28)
             + ((uint_mmv_t)(b[p_perm[8]]) << 32)
             + ((uint_mmv_t)(b[p_perm[9]]) << 36)
             + ((uint_mmv_t)(b[p_perm[10]]) << 40)
             + ((uint_mmv_t)(b[p_perm[11]]) << 44)
             + ((uint_mmv_t)(b[p_perm[12]]) << 48)
             + ((uint_mmv_t)(b[p_perm[13]]) << 52)
             + ((uint_mmv_t)(b[p_perm[14]]) << 56)
             + ((uint_mmv_t)(b[p_perm[15]]) << 60);
           r1 = (p_sign)[0] >> 0;
           // Spread bits 0,...,15 of r1 to the (4-bit long) fields
           // of r1. A field of r1 is set to 0x7 if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xffULL) + ((r1 & 0xff00ULL) << 24);
           r1 = (r1 & 0xf0000000fULL) 
               +  ((r1 & 0xf0000000f0ULL) << 12);
           r1 = (r1 & 0x3000300030003ULL) 
               +  ((r1 & 0xc000c000c000cULL) << 6);
           r1 = (r1 & 0x101010101010101ULL) 
               +  ((r1 & 0x202020202020202ULL) << 3);
           r1 *= 7;
           // Bit spreading done.
           (p_dest)[0] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[16]]) << 0)
             + ((uint_mmv_t)(b[p_perm[17]]) << 4)
             + ((uint_mmv_t)(b[p_perm[18]]) << 8)
             + ((uint_mmv_t)(b[p_perm[19]]) << 12)
             + ((uint_mmv_t)(b[p_perm[20]]) << 16)
             + ((uint_mmv_t)(b[p_perm[21]]) << 20)
             + ((uint_mmv_t)(b[p_perm[22]]) << 24)
             + ((uint_mmv_t)(b[p_perm[23]]) << 28)
             + ((uint_mmv_t)(b[p_perm[24]]) << 32)
             + ((uint_mmv_t)(b[p_perm[25]]) << 36)
             + ((uint_mmv_t)(b[p_perm[26]]) << 40)
             + ((uint_mmv_t)(b[p_perm[27]]) << 44)
             + ((uint_mmv_t)(b[p_perm[28]]) << 48)
             + ((uint_mmv_t)(b[p_perm[29]]) << 52)
             + ((uint_mmv_t)(b[p_perm[30]]) << 56)
             + ((uint_mmv_t)(b[p_perm[31]]) << 60);
           r1 = (p_sign)[0] >> 16;
           // Spread bits 0,...,15 of r1 to the (4-bit long) fields
           // of r1. A field of r1 is set to 0x7 if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xffULL) + ((r1 & 0xff00ULL) << 24);
           r1 = (r1 & 0xf0000000fULL) 
               +  ((r1 & 0xf0000000f0ULL) << 12);
           r1 = (r1 & 0x3000300030003ULL) 
               +  ((r1 & 0xc000c000c000cULL) << 6);
           r1 = (r1 & 0x101010101010101ULL) 
               +  ((r1 & 0x202020202020202ULL) << 3);
           r1 *= 7;
           // Bit spreading done.
           (p_dest)[1] = r0 ^ r1;
           p_dest += 2;
           p_perm += 32;
           p_sign += 1;
        }
        
    }

    ///////////////////////////////////////////////////////////////
    // Map tag T1 to tag X0 if e = 1
    // Map tag T1 to tag X1 if e = 2
    ///////////////////////////////////////////////////////////////
    p_src = v_in + 1644;
    p_dest = v_out + 3180;
    p_dest += diff;
    p_sign = p_tables[2].p_sign;
    p_perm = p_tables[2].p_perm;

    for (i = 0; i < 64; ++i) {
        p_b = b;
        
        for (j = 0; j < 12; ++j) {
           // %%OP_XI_LOAD p_src, p_b, %{i_src.SHAPE[2]}, uint8_t
           uint_mmv_t r0, r1;
           r0 =  (p_src)[0];
           r1 = (r0 >> 4) & 0x707070707070707ULL;
           r0 &= 0x707070707070707ULL;
           (p_b)[0] = (uint8_t)(r0 >> 0);
           (p_b)[1] = (uint8_t)(r1 >> 0);
           (p_b)[2] = (uint8_t)(r0 >> 8);
           (p_b)[3] = (uint8_t)(r1 >> 8);
           (p_b)[4] = (uint8_t)(r0 >> 16);
           (p_b)[5] = (uint8_t)(r1 >> 16);
           (p_b)[6] = (uint8_t)(r0 >> 24);
           (p_b)[7] = (uint8_t)(r1 >> 24);
           (p_b)[8] = (uint8_t)(r0 >> 32);
           (p_b)[9] = (uint8_t)(r1 >> 32);
           (p_b)[10] = (uint8_t)(r0 >> 40);
           (p_b)[11] = (uint8_t)(r1 >> 40);
           (p_b)[12] = (uint8_t)(r0 >> 48);
           (p_b)[13] = (uint8_t)(r1 >> 48);
           (p_b)[14] = (uint8_t)(r0 >> 56);
           (p_b)[15] = (uint8_t)(r1 >> 56);
           r0 =  (p_src)[1];
           r1 = (r0 >> 4) & 0x707070707070707ULL;
           r0 &= 0x707070707070707ULL;
           (p_b)[16] = (uint8_t)(r0 >> 0);
           (p_b)[17] = (uint8_t)(r1 >> 0);
           (p_b)[18] = (uint8_t)(r0 >> 8);
           (p_b)[19] = (uint8_t)(r1 >> 8);
           (p_b)[20] = (uint8_t)(r0 >> 16);
           (p_b)[21] = (uint8_t)(r1 >> 16);
           (p_b)[22] = (uint8_t)(r0 >> 24);
           (p_b)[23] = (uint8_t)(r1 >> 24);
           (p_b)[24] = (uint8_t)(r0 >> 32);
           (p_b)[25] = (uint8_t)(r1 >> 32);
           (p_b)[26] = (uint8_t)(r0 >> 40);
           (p_b)[27] = (uint8_t)(r1 >> 40);
           (p_b)[28] = (uint8_t)(r0 >> 48);
           (p_b)[29] = (uint8_t)(r1 >> 48);
           (p_b)[30] = (uint8_t)(r0 >> 56);
           (p_b)[31] = (uint8_t)(r1 >> 56);
           p_src += 2;
           p_b += 32;
        }
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_STORE b, p_perm, p_sign, p_dest, %{i_dest.SHAPE[2]}
           uint_mmv_t r0, r1;
           r0 = ((uint_mmv_t)(b[p_perm[0]]) << 0)
             + ((uint_mmv_t)(b[p_perm[1]]) << 4)
             + ((uint_mmv_t)(b[p_perm[2]]) << 8)
             + ((uint_mmv_t)(b[p_perm[3]]) << 12)
             + ((uint_mmv_t)(b[p_perm[4]]) << 16)
             + ((uint_mmv_t)(b[p_perm[5]]) << 20)
             + ((uint_mmv_t)(b[p_perm[6]]) << 24)
             + ((uint_mmv_t)(b[p_perm[7]]) << 28)
             + ((uint_mmv_t)(b[p_perm[8]]) << 32)
             + ((uint_mmv_t)(b[p_perm[9]]) << 36)
             + ((uint_mmv_t)(b[p_perm[10]]) << 40)
             + ((uint_mmv_t)(b[p_perm[11]]) << 44)
             + ((uint_mmv_t)(b[p_perm[12]]) << 48)
             + ((uint_mmv_t)(b[p_perm[13]]) << 52)
             + ((uint_mmv_t)(b[p_perm[14]]) << 56)
             + ((uint_mmv_t)(b[p_perm[15]]) << 60);
           r1 = (p_sign)[0] >> 0;
           // Spread bits 0,...,15 of r1 to the (4-bit long) fields
           // of r1. A field of r1 is set to 0x7 if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xffULL) + ((r1 & 0xff00ULL) << 24);
           r1 = (r1 & 0xf0000000fULL) 
               +  ((r1 & 0xf0000000f0ULL) << 12);
           r1 = (r1 & 0x3000300030003ULL) 
               +  ((r1 & 0xc000c000c000cULL) << 6);
           r1 = (r1 & 0x101010101010101ULL) 
               +  ((r1 & 0x202020202020202ULL) << 3);
           r1 *= 7;
           // Bit spreading done.
           (p_dest)[0] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[16]]) << 0)
             + ((uint_mmv_t)(b[p_perm[17]]) << 4)
             + ((uint_mmv_t)(b[p_perm[18]]) << 8)
             + ((uint_mmv_t)(b[p_perm[19]]) << 12)
             + ((uint_mmv_t)(b[p_perm[20]]) << 16)
             + ((uint_mmv_t)(b[p_perm[21]]) << 20)
             + ((uint_mmv_t)(b[p_perm[22]]) << 24)
             + ((uint_mmv_t)(b[p_perm[23]]) << 28);
           r1 = (p_sign)[0] >> 16;
           // Spread bits 0,...,15 of r1 to the (4-bit long) fields
           // of r1. A field of r1 is set to 0x7 if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xffULL) + ((r1 & 0xff00ULL) << 24);
           r1 = (r1 & 0xf0000000fULL) 
               +  ((r1 & 0xf0000000f0ULL) << 12);
           r1 = (r1 & 0x3000300030003ULL) 
               +  ((r1 & 0xc000c000c000cULL) << 6);
           r1 = (r1 & 0x101010101010101ULL) 
               +  ((r1 & 0x202020202020202ULL) << 3);
           r1 *= 7;
           // Bit spreading done.
           (p_dest)[1] = r0 ^ r1;
           p_dest += 2;
           p_perm += 24;
           p_sign += 1;
        }
        
    }

    ///////////////////////////////////////////////////////////////
    // Map tag X0 to tag X1 if e = 1
    // Map tag X1 to tag X0 if e = 2
    ///////////////////////////////////////////////////////////////
    p_src = v_in + 3180;
    p_src += diff;
    p_dest = v_out + 5228;
    p_dest -= diff;
    p_sign = p_tables[3].p_sign;
    p_perm = p_tables[3].p_perm;

    for (i = 0; i < 64; ++i) {
        p_b = b;
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_LOAD p_src, p_b, %{i_src.SHAPE[2]}, uint8_t
           uint_mmv_t r0, r1;
           r0 =  (p_src)[0];
           r1 = (r0 >> 4) & 0x707070707070707ULL;
           r0 &= 0x707070707070707ULL;
           (p_b)[0] = (uint8_t)(r0 >> 0);
           (p_b)[1] = (uint8_t)(r1 >> 0);
           (p_b)[2] = (uint8_t)(r0 >> 8);
           (p_b)[3] = (uint8_t)(r1 >> 8);
           (p_b)[4] = (uint8_t)(r0 >> 16);
           (p_b)[5] = (uint8_t)(r1 >> 16);
           (p_b)[6] = (uint8_t)(r0 >> 24);
           (p_b)[7] = (uint8_t)(r1 >> 24);
           (p_b)[8] = (uint8_t)(r0 >> 32);
           (p_b)[9] = (uint8_t)(r1 >> 32);
           (p_b)[10] = (uint8_t)(r0 >> 40);
           (p_b)[11] = (uint8_t)(r1 >> 40);
           (p_b)[12] = (uint8_t)(r0 >> 48);
           (p_b)[13] = (uint8_t)(r1 >> 48);
           (p_b)[14] = (uint8_t)(r0 >> 56);
           (p_b)[15] = (uint8_t)(r1 >> 56);
           r0 =  (p_src)[1];
           r1 = (r0 >> 4) & 0x707070707070707ULL;
           r0 &= 0x707070707070707ULL;
           (p_b)[16] = (uint8_t)(r0 >> 0);
           (p_b)[17] = (uint8_t)(r1 >> 0);
           (p_b)[18] = (uint8_t)(r0 >> 8);
           (p_b)[19] = (uint8_t)(r1 >> 8);
           (p_b)[20] = (uint8_t)(r0 >> 16);
           (p_b)[21] = (uint8_t)(r1 >> 16);
           (p_b)[22] = (uint8_t)(r0 >> 24);
           (p_b)[23] = (uint8_t)(r1 >> 24);
           p_src += 2;
           p_b += 32;
        }
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_STORE b, p_perm, p_sign, p_dest, %{i_dest.SHAPE[2]}
           uint_mmv_t r0, r1;
           r0 = ((uint_mmv_t)(b[p_perm[0]]) << 0)
             + ((uint_mmv_t)(b[p_perm[1]]) << 4)
             + ((uint_mmv_t)(b[p_perm[2]]) << 8)
             + ((uint_mmv_t)(b[p_perm[3]]) << 12)
             + ((uint_mmv_t)(b[p_perm[4]]) << 16)
             + ((uint_mmv_t)(b[p_perm[5]]) << 20)
             + ((uint_mmv_t)(b[p_perm[6]]) << 24)
             + ((uint_mmv_t)(b[p_perm[7]]) << 28)
             + ((uint_mmv_t)(b[p_perm[8]]) << 32)
             + ((uint_mmv_t)(b[p_perm[9]]) << 36)
             + ((uint_mmv_t)(b[p_perm[10]]) << 40)
             + ((uint_mmv_t)(b[p_perm[11]]) << 44)
             + ((uint_mmv_t)(b[p_perm[12]]) << 48)
             + ((uint_mmv_t)(b[p_perm[13]]) << 52)
             + ((uint_mmv_t)(b[p_perm[14]]) << 56)
             + ((uint_mmv_t)(b[p_perm[15]]) << 60);
           r1 = (p_sign)[0] >> 0;
           // Spread bits 0,...,15 of r1 to the (4-bit long) fields
           // of r1. A field of r1 is set to 0x7 if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xffULL) + ((r1 & 0xff00ULL) << 24);
           r1 = (r1 & 0xf0000000fULL) 
               +  ((r1 & 0xf0000000f0ULL) << 12);
           r1 = (r1 & 0x3000300030003ULL) 
               +  ((r1 & 0xc000c000c000cULL) << 6);
           r1 = (r1 & 0x101010101010101ULL) 
               +  ((r1 & 0x202020202020202ULL) << 3);
           r1 *= 7;
           // Bit spreading done.
           (p_dest)[0] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[16]]) << 0)
             + ((uint_mmv_t)(b[p_perm[17]]) << 4)
             + ((uint_mmv_t)(b[p_perm[18]]) << 8)
             + ((uint_mmv_t)(b[p_perm[19]]) << 12)
             + ((uint_mmv_t)(b[p_perm[20]]) << 16)
             + ((uint_mmv_t)(b[p_perm[21]]) << 20)
             + ((uint_mmv_t)(b[p_perm[22]]) << 24)
             + ((uint_mmv_t)(b[p_perm[23]]) << 28);
           r1 = (p_sign)[0] >> 16;
           // Spread bits 0,...,15 of r1 to the (4-bit long) fields
           // of r1. A field of r1 is set to 0x7 if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xffULL) + ((r1 & 0xff00ULL) << 24);
           r1 = (r1 & 0xf0000000fULL) 
               +  ((r1 & 0xf0000000f0ULL) << 12);
           r1 = (r1 & 0x3000300030003ULL) 
               +  ((r1 & 0xc000c000c000cULL) << 6);
           r1 = (r1 & 0x101010101010101ULL) 
               +  ((r1 & 0x202020202020202ULL) << 3);
           r1 *= 7;
           // Bit spreading done.
           (p_dest)[1] = r0 ^ r1;
           p_dest += 2;
           p_perm += 24;
           p_sign += 1;
        }
        
    }

    ///////////////////////////////////////////////////////////////
    // Map tag X1 to tag T1 if e = 1
    // Map tag X0 to tag T1 if e = 2
    ///////////////////////////////////////////////////////////////
    p_src = v_in + 5228;
    p_src -= diff;
    p_dest = v_out + 1644;
    p_sign = p_tables[4].p_sign;
    p_perm = p_tables[4].p_perm;

    for (i = 0; i < 64; ++i) {
        p_b = b;
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_LOAD p_src, p_b, %{i_src.SHAPE[2]}, uint8_t
           uint_mmv_t r0, r1;
           r0 =  (p_src)[0];
           r1 = (r0 >> 4) & 0x707070707070707ULL;
           r0 &= 0x707070707070707ULL;
           (p_b)[0] = (uint8_t)(r0 >> 0);
           (p_b)[1] = (uint8_t)(r1 >> 0);
           (p_b)[2] = (uint8_t)(r0 >> 8);
           (p_b)[3] = (uint8_t)(r1 >> 8);
           (p_b)[4] = (uint8_t)(r0 >> 16);
           (p_b)[5] = (uint8_t)(r1 >> 16);
           (p_b)[6] = (uint8_t)(r0 >> 24);
           (p_b)[7] = (uint8_t)(r1 >> 24);
           (p_b)[8] = (uint8_t)(r0 >> 32);
           (p_b)[9] = (uint8_t)(r1 >> 32);
           (p_b)[10] = (uint8_t)(r0 >> 40);
           (p_b)[11] = (uint8_t)(r1 >> 40);
           (p_b)[12] = (uint8_t)(r0 >> 48);
           (p_b)[13] = (uint8_t)(r1 >> 48);
           (p_b)[14] = (uint8_t)(r0 >> 56);
           (p_b)[15] = (uint8_t)(r1 >> 56);
           r0 =  (p_src)[1];
           r1 = (r0 >> 4) & 0x707070707070707ULL;
           r0 &= 0x707070707070707ULL;
           (p_b)[16] = (uint8_t)(r0 >> 0);
           (p_b)[17] = (uint8_t)(r1 >> 0);
           (p_b)[18] = (uint8_t)(r0 >> 8);
           (p_b)[19] = (uint8_t)(r1 >> 8);
           (p_b)[20] = (uint8_t)(r0 >> 16);
           (p_b)[21] = (uint8_t)(r1 >> 16);
           (p_b)[22] = (uint8_t)(r0 >> 24);
           (p_b)[23] = (uint8_t)(r1 >> 24);
           p_src += 2;
           p_b += 32;
        }
        
        for (j = 0; j < 12; ++j) {
           // %%OP_XI_STORE b, p_perm, p_sign, p_dest, %{i_dest.SHAPE[2]}
           uint_mmv_t r0, r1;
           r0 = ((uint_mmv_t)(b[p_perm[0]]) << 0)
             + ((uint_mmv_t)(b[p_perm[1]]) << 4)
             + ((uint_mmv_t)(b[p_perm[2]]) << 8)
             + ((uint_mmv_t)(b[p_perm[3]]) << 12)
             + ((uint_mmv_t)(b[p_perm[4]]) << 16)
             + ((uint_mmv_t)(b[p_perm[5]]) << 20)
             + ((uint_mmv_t)(b[p_perm[6]]) << 24)
             + ((uint_mmv_t)(b[p_perm[7]]) << 28)
             + ((uint_mmv_t)(b[p_perm[8]]) << 32)
             + ((uint_mmv_t)(b[p_perm[9]]) << 36)
             + ((uint_mmv_t)(b[p_perm[10]]) << 40)
             + ((uint_mmv_t)(b[p_perm[11]]) << 44)
             + ((uint_mmv_t)(b[p_perm[12]]) << 48)
             + ((uint_mmv_t)(b[p_perm[13]]) << 52)
             + ((uint_mmv_t)(b[p_perm[14]]) << 56)
             + ((uint_mmv_t)(b[p_perm[15]]) << 60);
           r1 = (p_sign)[0] >> 0;
           // Spread bits 0,...,15 of r1 to the (4-bit long) fields
           // of r1. A field of r1 is set to 0x7 if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xffULL) + ((r1 & 0xff00ULL) << 24);
           r1 = (r1 & 0xf0000000fULL) 
               +  ((r1 & 0xf0000000f0ULL) << 12);
           r1 = (r1 & 0x3000300030003ULL) 
               +  ((r1 & 0xc000c000c000cULL) << 6);
           r1 = (r1 & 0x101010101010101ULL) 
               +  ((r1 & 0x202020202020202ULL) << 3);
           r1 *= 7;
           // Bit spreading done.
           (p_dest)[0] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[16]]) << 0)
             + ((uint_mmv_t)(b[p_perm[17]]) << 4)
             + ((uint_mmv_t)(b[p_perm[18]]) << 8)
             + ((uint_mmv_t)(b[p_perm[19]]) << 12)
             + ((uint_mmv_t)(b[p_perm[20]]) << 16)
             + ((uint_mmv_t)(b[p_perm[21]]) << 20)
             + ((uint_mmv_t)(b[p_perm[22]]) << 24)
             + ((uint_mmv_t)(b[p_perm[23]]) << 28)
             + ((uint_mmv_t)(b[p_perm[24]]) << 32)
             + ((uint_mmv_t)(b[p_perm[25]]) << 36)
             + ((uint_mmv_t)(b[p_perm[26]]) << 40)
             + ((uint_mmv_t)(b[p_perm[27]]) << 44)
             + ((uint_mmv_t)(b[p_perm[28]]) << 48)
             + ((uint_mmv_t)(b[p_perm[29]]) << 52)
             + ((uint_mmv_t)(b[p_perm[30]]) << 56)
             + ((uint_mmv_t)(b[p_perm[31]]) << 60);
           r1 = (p_sign)[0] >> 16;
           // Spread bits 0,...,15 of r1 to the (4-bit long) fields
           // of r1. A field of r1 is set to 0x7 if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xffULL) + ((r1 & 0xff00ULL) << 24);
           r1 = (r1 & 0xf0000000fULL) 
               +  ((r1 & 0xf0000000f0ULL) << 12);
           r1 = (r1 & 0x3000300030003ULL) 
               +  ((r1 & 0xc000c000c000cULL) << 6);
           r1 = (r1 & 0x101010101010101ULL) 
               +  ((r1 & 0x202020202020202ULL) << 3);
           r1 *= 7;
           // Bit spreading done.
           (p_dest)[1] = r0 ^ r1;
           p_dest += 2;
           p_perm += 32;
           p_sign += 1;
        }
        
    }
}

static uint_mmv_t TAB7_XI64_MASK[] = {
// %%TABLE TABLE_MUL_MATRIX_XI64, uint%{INT_BITS}
0x0007000700070007ULL,0x0000000000000000ULL,
0x0007000700070007ULL,0x7777777777777777ULL,
0x0000000000000000ULL,0x0007000700070007ULL,
0x7777777777777777ULL,0x0007000700070007ULL
};


#define HALF_YZ_SHIFT 11

static uint32_t TAB7_XI64_OFFSET[2][4] = {
    {
        MM_OP7_OFS_Z + (2 << HALF_YZ_SHIFT),
        MM_OP7_OFS_Z + (0 << HALF_YZ_SHIFT),
        MM_OP7_OFS_Z + (1 << HALF_YZ_SHIFT),
        MM_OP7_OFS_Z + (3 << HALF_YZ_SHIFT)
    },
    {
        MM_OP7_OFS_Z + (1 << HALF_YZ_SHIFT),
        MM_OP7_OFS_Z + (2 << HALF_YZ_SHIFT),
        MM_OP7_OFS_Z + (0 << HALF_YZ_SHIFT),
        MM_OP7_OFS_Z + (3 << HALF_YZ_SHIFT)
    },
};




static void mm_op7_xi_yz(uint_mmv_t *v_in,  uint32_t exp1, uint_mmv_t *v_out)
{
    uint_fast32_t i1;
    uint_mmv_t *p_mask =  TAB7_XI64_MASK + exp1;
    for (i1 = 0; i1 < 64; ++i1) {
        // %%MUL_MATRIX_XI64 v_in, p_mask, v_out

        // This is an automatically generated matrix operation, do not change!
        {
        uint_mmv_t r0, r1, r2, r3, r4;
        uint_mmv_t r5, r6, r7, r8, r9;

        uint_mmv_t a[24];
        uint_fast32_t i;

        // TODO: write comment!!!
        // 
        r0 = v_in[0] ^  p_mask[2];
        r9 = ((r0 ^ (r0 >> 4)) & 0x70007000700070ULL); // 3 ops
        r0 ^= (r9 | (r9 << 4)); // 3 ops
        r8 = v_in[28] ^  p_mask[0];
        r9 = ((r8 ^ (r8 >> 4)) & 0x70007000700070ULL); // 3 ops
        r8 ^= (r9 | (r9 << 4)); // 3 ops
        a[8] = (((r0 >> 32) & 0x77777777ULL)
            | (r8 & 0x7777777700000000ULL)); // 4 ops
        r0 = ((r0 & 0x77777777ULL)
            | ((r8 << 32) & 0x7777777700000000ULL)); // 4 ops
        a[16] = v_in[1] ^  p_mask[2];
        r9 = ((a[16] ^ (a[16] >> 4))
            & 0x70007000700070ULL); // 3 ops
        a[16] ^= (r9 | (r9 << 4)); // 3 ops
        r8 = v_in[29] ^  p_mask[0];
        r9 = ((r8 ^ (r8 >> 4)) & 0x70007000700070ULL); // 3 ops
        r8 ^= (r9 | (r9 << 4)); // 3 ops
        a[16] = ((a[16] & 0x77777777ULL)
            | ((r8 << 32) & 0x7777777700000000ULL)); // 4 ops
        r1 = v_in[26] ^  p_mask[0];
        r9 = ((r1 ^ (r1 >> 4)) & 0x70007000700070ULL); // 3 ops
        r1 ^= (r9 | (r9 << 4)); // 3 ops
        r8 = v_in[6] ^  p_mask[0];
        r9 = ((r8 ^ (r8 >> 4)) & 0x70007000700070ULL); // 3 ops
        r8 ^= (r9 | (r9 << 4)); // 3 ops
        a[9] = (((r1 >> 32) & 0x77777777ULL)
            | (r8 & 0x7777777700000000ULL)); // 4 ops
        r1 = ((r1 & 0x77777777ULL)
            | ((r8 << 32) & 0x7777777700000000ULL)); // 4 ops
        a[17] = v_in[27] ^  p_mask[0];
        r9 = ((a[17] ^ (a[17] >> 4))
            & 0x70007000700070ULL); // 3 ops
        a[17] ^= (r9 | (r9 << 4)); // 3 ops
        r8 = v_in[7] ^  p_mask[0];
        r9 = ((r8 ^ (r8 >> 4)) & 0x70007000700070ULL); // 3 ops
        r8 ^= (r9 | (r9 << 4)); // 3 ops
        a[17] = ((a[17] & 0x77777777ULL)
            | ((r8 << 32) & 0x7777777700000000ULL)); // 4 ops
        r2 = v_in[22] ^  p_mask[0];
        r9 = ((r2 ^ (r2 >> 4)) & 0x70007000700070ULL); // 3 ops
        r2 ^= (r9 | (r9 << 4)); // 3 ops
        r8 = v_in[10] ^  p_mask[0];
        r9 = ((r8 ^ (r8 >> 4)) & 0x70007000700070ULL); // 3 ops
        r8 ^= (r9 | (r9 << 4)); // 3 ops
        a[10] = (((r2 >> 32) & 0x77777777ULL)
            | (r8 & 0x7777777700000000ULL)); // 4 ops
        r2 = ((r2 & 0x77777777ULL)
            | ((r8 << 32) & 0x7777777700000000ULL)); // 4 ops
        a[18] = v_in[23] ^  p_mask[0];
        r9 = ((a[18] ^ (a[18] >> 4))
            & 0x70007000700070ULL); // 3 ops
        a[18] ^= (r9 | (r9 << 4)); // 3 ops
        r8 = v_in[11] ^  p_mask[0];
        r9 = ((r8 ^ (r8 >> 4)) & 0x70007000700070ULL); // 3 ops
        r8 ^= (r9 | (r9 << 4)); // 3 ops
        a[18] = ((a[18] & 0x77777777ULL)
            | ((r8 << 32) & 0x7777777700000000ULL)); // 4 ops
        r3 = v_in[12] ^  p_mask[0];
        r9 = ((r3 ^ (r3 >> 4)) & 0x70007000700070ULL); // 3 ops
        r3 ^= (r9 | (r9 << 4)); // 3 ops
        r8 = v_in[16] ^  p_mask[2];
        r9 = ((r8 ^ (r8 >> 4)) & 0x70007000700070ULL); // 3 ops
        r8 ^= (r9 | (r9 << 4)); // 3 ops
        a[11] = (((r3 >> 32) & 0x77777777ULL)
            | (r8 & 0x7777777700000000ULL)); // 4 ops
        r3 = ((r3 & 0x77777777ULL)
            | ((r8 << 32) & 0x7777777700000000ULL)); // 4 ops
        a[19] = v_in[13] ^  p_mask[0];
        r9 = ((a[19] ^ (a[19] >> 4))
            & 0x70007000700070ULL); // 3 ops
        a[19] ^= (r9 | (r9 << 4)); // 3 ops
        r8 = v_in[17] ^  p_mask[2];
        r9 = ((r8 ^ (r8 >> 4)) & 0x70007000700070ULL); // 3 ops
        r8 ^= (r9 | (r9 << 4)); // 3 ops
        a[19] = ((a[19] & 0x77777777ULL)
            | ((r8 << 32) & 0x7777777700000000ULL)); // 4 ops
        r4 = v_in[14] ^  p_mask[0];
        r9 = ((r4 ^ (r4 >> 4)) & 0x70007000700070ULL); // 3 ops
        r4 ^= (r9 | (r9 << 4)); // 3 ops
        r8 = v_in[18] ^  p_mask[0];
        r9 = ((r8 ^ (r8 >> 4)) & 0x70007000700070ULL); // 3 ops
        r8 ^= (r9 | (r9 << 4)); // 3 ops
        a[12] = (((r4 >> 32) & 0x77777777ULL)
            | (r8 & 0x7777777700000000ULL)); // 4 ops
        r4 = ((r4 & 0x77777777ULL)
            | ((r8 << 32) & 0x7777777700000000ULL)); // 4 ops
        a[20] = v_in[15] ^  p_mask[0];
        r9 = ((a[20] ^ (a[20] >> 4))
            & 0x70007000700070ULL); // 3 ops
        a[20] ^= (r9 | (r9 << 4)); // 3 ops
        r8 = v_in[19] ^  p_mask[0];
        r9 = ((r8 ^ (r8 >> 4)) & 0x70007000700070ULL); // 3 ops
        r8 ^= (r9 | (r9 << 4)); // 3 ops
        a[20] = ((a[20] & 0x77777777ULL)
            | ((r8 << 32) & 0x7777777700000000ULL)); // 4 ops
        r5 = v_in[20] ^  p_mask[0];
        r9 = ((r5 ^ (r5 >> 4)) & 0x70007000700070ULL); // 3 ops
        r5 ^= (r9 | (r9 << 4)); // 3 ops
        r8 = v_in[8] ^  p_mask[2];
        r9 = ((r8 ^ (r8 >> 4)) & 0x70007000700070ULL); // 3 ops
        r8 ^= (r9 | (r9 << 4)); // 3 ops
        a[13] = (((r5 >> 32) & 0x77777777ULL)
            | (r8 & 0x7777777700000000ULL)); // 4 ops
        r5 = ((r5 & 0x77777777ULL)
            | ((r8 << 32) & 0x7777777700000000ULL)); // 4 ops
        a[21] = v_in[21] ^  p_mask[0];
        r9 = ((a[21] ^ (a[21] >> 4))
            & 0x70007000700070ULL); // 3 ops
        a[21] ^= (r9 | (r9 << 4)); // 3 ops
        r8 = v_in[9] ^  p_mask[2];
        r9 = ((r8 ^ (r8 >> 4)) & 0x70007000700070ULL); // 3 ops
        r8 ^= (r9 | (r9 << 4)); // 3 ops
        a[21] = ((a[21] & 0x77777777ULL)
            | ((r8 << 32) & 0x7777777700000000ULL)); // 4 ops
        r6 = v_in[24] ^  p_mask[0];
        r9 = ((r6 ^ (r6 >> 4)) & 0x70007000700070ULL); // 3 ops
        r6 ^= (r9 | (r9 << 4)); // 3 ops
        r8 = v_in[4] ^  p_mask[2];
        r9 = ((r8 ^ (r8 >> 4)) & 0x70007000700070ULL); // 3 ops
        r8 ^= (r9 | (r9 << 4)); // 3 ops
        a[14] = (((r6 >> 32) & 0x77777777ULL)
            | (r8 & 0x7777777700000000ULL)); // 4 ops
        r6 = ((r6 & 0x77777777ULL)
            | ((r8 << 32) & 0x7777777700000000ULL)); // 4 ops
        a[22] = v_in[25] ^  p_mask[0];
        r9 = ((a[22] ^ (a[22] >> 4))
            & 0x70007000700070ULL); // 3 ops
        a[22] ^= (r9 | (r9 << 4)); // 3 ops
        r8 = v_in[5] ^  p_mask[2];
        r9 = ((r8 ^ (r8 >> 4)) & 0x70007000700070ULL); // 3 ops
        r8 ^= (r9 | (r9 << 4)); // 3 ops
        a[22] = ((a[22] & 0x77777777ULL)
            | ((r8 << 32) & 0x7777777700000000ULL)); // 4 ops
        r7 = v_in[2] ^  p_mask[2];
        r9 = ((r7 ^ (r7 >> 4)) & 0x70007000700070ULL); // 3 ops
        r7 ^= (r9 | (r9 << 4)); // 3 ops
        r8 = v_in[30] ^  p_mask[2];
        r9 = ((r8 ^ (r8 >> 4)) & 0x70007000700070ULL); // 3 ops
        r8 ^= (r9 | (r9 << 4)); // 3 ops
        a[15] = (((r7 >> 32) & 0x77777777ULL)
            | (r8 & 0x7777777700000000ULL)); // 4 ops
        r7 = ((r7 & 0x77777777ULL)
            | ((r8 << 32) & 0x7777777700000000ULL)); // 4 ops
        a[23] = v_in[3] ^  p_mask[2];
        r9 = ((a[23] ^ (a[23] >> 4))
            & 0x70007000700070ULL); // 3 ops
        a[23] ^= (r9 | (r9 << 4)); // 3 ops
        r8 = v_in[31] ^  p_mask[2];
        r9 = ((r8 ^ (r8 >> 4)) & 0x70007000700070ULL); // 3 ops
        r8 ^= (r9 | (r9 << 4)); // 3 ops
        a[23] = ((a[23] & 0x77777777ULL)
            | ((r8 << 32) & 0x7777777700000000ULL)); // 4 ops
        // 120 lines of code, 288 operations
        i = 0;
        goto l_mmv7_op_l64_2;
        l_mmv7_op_l64_1:
        a[(i) + 0] = r0;
        a[(i) + 1] = r1;
        a[(i) + 2] = r2;
        a[(i) + 3] = r3;
        a[(i) + 4] = r4;
        a[(i) + 5] = r5;
        a[(i) + 6] = r6;
        a[(i) + 7] = r7;
        i += 8;
        r0 = a[(i) + 0];
        r1 = a[(i) + 1];
        r2 = a[(i) + 2];
        r3 = a[(i) + 3];
        r4 = a[(i) + 4];
        r5 = a[(i) + 5];
        r6 = a[(i) + 6];
        r7 = a[(i) + 7];
        l_mmv7_op_l64_2:
        // Butterfly: v[i], v[i+1] = v[i]+v[i+1], v[i]-v[i+1]
        r8 = (((r0 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r0 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r0 = ((r0 ^ 0x7070707070707070ULL) + r8); // 2 ops
        r8 = (r0 & 0x8888888888888888ULL);
        r0 = ((r0 - r8) + (r8 >> 3)); // 3 ops
        r8 = (((r1 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r1 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r1 = ((r1 ^ 0x7070707070707070ULL) + r8); // 2 ops
        r8 = (r1 & 0x8888888888888888ULL);
        r1 = ((r1 - r8) + (r8 >> 3)); // 3 ops
        r8 = (((r2 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r2 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r2 = ((r2 ^ 0x7070707070707070ULL) + r8); // 2 ops
        r8 = (r2 & 0x8888888888888888ULL);
        r2 = ((r2 - r8) + (r8 >> 3)); // 3 ops
        r8 = (((r3 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r3 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r3 = ((r3 ^ 0x7070707070707070ULL) + r8); // 2 ops
        r8 = (r3 & 0x8888888888888888ULL);
        r3 = ((r3 - r8) + (r8 >> 3)); // 3 ops
        r8 = (((r4 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r4 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r4 = ((r4 ^ 0x7070707070707070ULL) + r8); // 2 ops
        r8 = (r4 & 0x8888888888888888ULL);
        r4 = ((r4 - r8) + (r8 >> 3)); // 3 ops
        r8 = (((r5 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r5 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r5 = ((r5 ^ 0x7070707070707070ULL) + r8); // 2 ops
        r8 = (r5 & 0x8888888888888888ULL);
        r5 = ((r5 - r8) + (r8 >> 3)); // 3 ops
        r8 = (((r6 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r6 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r6 = ((r6 ^ 0x7070707070707070ULL) + r8); // 2 ops
        r8 = (r6 & 0x8888888888888888ULL);
        r6 = ((r6 - r8) + (r8 >> 3)); // 3 ops
        r8 = (((r7 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r7 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r7 = ((r7 ^ 0x7070707070707070ULL) + r8); // 2 ops
        r8 = (r7 & 0x8888888888888888ULL);
        r7 = ((r7 - r8) + (r8 >> 3)); // 3 ops
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        // Butterfly: v[i], v[i+2] = v[i]+v[i+2], v[i]-v[i+2]
        r8 = (((r0 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r0 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r0 = ((r0 ^ 0x7700770077007700ULL) + r8); // 2 ops
        r8 = (r0 & 0x8888888888888888ULL);
        r0 = ((r0 - r8) + (r8 >> 3)); // 3 ops
        r8 = (((r1 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r1 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r1 = ((r1 ^ 0x7700770077007700ULL) + r8); // 2 ops
        r8 = (r1 & 0x8888888888888888ULL);
        r1 = ((r1 - r8) + (r8 >> 3)); // 3 ops
        r8 = (((r2 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r2 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r2 = ((r2 ^ 0x7700770077007700ULL) + r8); // 2 ops
        r8 = (r2 & 0x8888888888888888ULL);
        r2 = ((r2 - r8) + (r8 >> 3)); // 3 ops
        r8 = (((r3 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r3 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r3 = ((r3 ^ 0x7700770077007700ULL) + r8); // 2 ops
        r8 = (r3 & 0x8888888888888888ULL);
        r3 = ((r3 - r8) + (r8 >> 3)); // 3 ops
        r8 = (((r4 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r4 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r4 = ((r4 ^ 0x7700770077007700ULL) + r8); // 2 ops
        r8 = (r4 & 0x8888888888888888ULL);
        r4 = ((r4 - r8) + (r8 >> 3)); // 3 ops
        r8 = (((r5 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r5 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r5 = ((r5 ^ 0x7700770077007700ULL) + r8); // 2 ops
        r8 = (r5 & 0x8888888888888888ULL);
        r5 = ((r5 - r8) + (r8 >> 3)); // 3 ops
        r8 = (((r6 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r6 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r6 = ((r6 ^ 0x7700770077007700ULL) + r8); // 2 ops
        r8 = (r6 & 0x8888888888888888ULL);
        r6 = ((r6 - r8) + (r8 >> 3)); // 3 ops
        r8 = (((r7 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r7 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r7 = ((r7 ^ 0x7700770077007700ULL) + r8); // 2 ops
        r8 = (r7 & 0x8888888888888888ULL);
        r7 = ((r7 - r8) + (r8 >> 3)); // 3 ops
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        // Butterfly: v[i], v[i+8] = v[i]+v[i+8], v[i]-v[i+8]
        r8 = ((r0 << 32) | (r0 >> 32)); // 3 ops
        r0 = ((r0 ^ 0x7777777700000000ULL) + r8); // 2 ops
        r8 = (r0 & 0x8888888888888888ULL);
        r0 = ((r0 - r8) + (r8 >> 3)); // 3 ops
        r8 = ((r1 << 32) | (r1 >> 32)); // 3 ops
        r1 = ((r1 ^ 0x7777777700000000ULL) + r8); // 2 ops
        r8 = (r1 & 0x8888888888888888ULL);
        r1 = ((r1 - r8) + (r8 >> 3)); // 3 ops
        r8 = ((r2 << 32) | (r2 >> 32)); // 3 ops
        r2 = ((r2 ^ 0x7777777700000000ULL) + r8); // 2 ops
        r8 = (r2 & 0x8888888888888888ULL);
        r2 = ((r2 - r8) + (r8 >> 3)); // 3 ops
        r8 = ((r3 << 32) | (r3 >> 32)); // 3 ops
        r3 = ((r3 ^ 0x7777777700000000ULL) + r8); // 2 ops
        r8 = (r3 & 0x8888888888888888ULL);
        r3 = ((r3 - r8) + (r8 >> 3)); // 3 ops
        r8 = ((r4 << 32) | (r4 >> 32)); // 3 ops
        r4 = ((r4 ^ 0x7777777700000000ULL) + r8); // 2 ops
        r8 = (r4 & 0x8888888888888888ULL);
        r4 = ((r4 - r8) + (r8 >> 3)); // 3 ops
        r8 = ((r5 << 32) | (r5 >> 32)); // 3 ops
        r5 = ((r5 ^ 0x7777777700000000ULL) + r8); // 2 ops
        r8 = (r5 & 0x8888888888888888ULL);
        r5 = ((r5 - r8) + (r8 >> 3)); // 3 ops
        r8 = ((r6 << 32) | (r6 >> 32)); // 3 ops
        r6 = ((r6 ^ 0x7777777700000000ULL) + r8); // 2 ops
        r8 = (r6 & 0x8888888888888888ULL);
        r6 = ((r6 - r8) + (r8 >> 3)); // 3 ops
        r8 = ((r7 << 32) | (r7 >> 32)); // 3 ops
        r7 = ((r7 ^ 0x7777777700000000ULL) + r8); // 2 ops
        r8 = (r7 & 0x8888888888888888ULL);
        r7 = ((r7 - r8) + (r8 >> 3)); // 3 ops
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        // Butterfly: v[i], v[i+16] = v[i]+v[i+16], v[i]-v[i+16]
        r8 = (r0 + (r1 ^ 0x7777777777777777ULL)); // 2 ops
        r0 = (r0 + r1);
        r1 = (r8 & 0x8888888888888888ULL);
        r1 = ((r8 - r1) + (r1 >> 3)); // 3 ops
        r8 = (r0 & 0x8888888888888888ULL);
        r0 = ((r0 - r8) + (r8 >> 3)); // 3 ops
        r8 = (r2 + (r3 ^ 0x7777777777777777ULL)); // 2 ops
        r2 = (r2 + r3);
        r3 = (r8 & 0x8888888888888888ULL);
        r3 = ((r8 - r3) + (r3 >> 3)); // 3 ops
        r8 = (r2 & 0x8888888888888888ULL);
        r2 = ((r2 - r8) + (r8 >> 3)); // 3 ops
        r8 = (r4 + (r5 ^ 0x7777777777777777ULL)); // 2 ops
        r4 = (r4 + r5);
        r5 = (r8 & 0x8888888888888888ULL);
        r5 = ((r8 - r5) + (r5 >> 3)); // 3 ops
        r8 = (r4 & 0x8888888888888888ULL);
        r4 = ((r4 - r8) + (r8 >> 3)); // 3 ops
        r8 = (r6 + (r7 ^ 0x7777777777777777ULL)); // 2 ops
        r6 = (r6 + r7);
        r7 = (r8 & 0x8888888888888888ULL);
        r7 = ((r8 - r7) + (r7 >> 3)); // 3 ops
        r8 = (r6 & 0x8888888888888888ULL);
        r6 = ((r6 - r8) + (r8 >> 3)); // 3 ops
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        // Butterfly: v[i], v[i+32] = v[i]+v[i+32], v[i]-v[i+32]
        r8 = (r0 + (r2 ^ 0x7777777777777777ULL)); // 2 ops
        r0 = (r0 + r2);
        r2 = (r8 & 0x8888888888888888ULL);
        r2 = ((r8 - r2) + (r2 >> 3)); // 3 ops
        r8 = (r0 & 0x8888888888888888ULL);
        r0 = ((r0 - r8) + (r8 >> 3)); // 3 ops
        r8 = (r1 + (r3 ^ 0x7777777777777777ULL)); // 2 ops
        r1 = (r1 + r3);
        r3 = (r8 & 0x8888888888888888ULL);
        r3 = ((r8 - r3) + (r3 >> 3)); // 3 ops
        r8 = (r1 & 0x8888888888888888ULL);
        r1 = ((r1 - r8) + (r8 >> 3)); // 3 ops
        r8 = (r4 + (r6 ^ 0x7777777777777777ULL)); // 2 ops
        r4 = (r4 + r6);
        r6 = (r8 & 0x8888888888888888ULL);
        r6 = ((r8 - r6) + (r6 >> 3)); // 3 ops
        r8 = (r4 & 0x8888888888888888ULL);
        r4 = ((r4 - r8) + (r8 >> 3)); // 3 ops
        r8 = (r5 + (r7 ^ 0x7777777777777777ULL)); // 2 ops
        r5 = (r5 + r7);
        r7 = (r8 & 0x8888888888888888ULL);
        r7 = ((r8 - r7) + (r7 >> 3)); // 3 ops
        r8 = (r5 & 0x8888888888888888ULL);
        r5 = ((r5 - r8) + (r8 >> 3)); // 3 ops
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        // Butterfly: v[i], v[i+64] = v[i]+v[i+64], v[i]-v[i+64]
        r8 = (r0 + (r4 ^ 0x7777777777777777ULL)); // 2 ops
        r0 = (r0 + r4);
        r4 = (r8 & 0x8888888888888888ULL);
        r4 = ((r8 - r4) + (r4 >> 3)); // 3 ops
        r8 = (r0 & 0x8888888888888888ULL);
        r0 = ((r0 - r8) + (r8 >> 3)); // 3 ops
        r8 = (r1 + (r5 ^ 0x7777777777777777ULL)); // 2 ops
        r1 = (r1 + r5);
        r5 = (r8 & 0x8888888888888888ULL);
        r5 = ((r8 - r5) + (r5 >> 3)); // 3 ops
        r8 = (r1 & 0x8888888888888888ULL);
        r1 = ((r1 - r8) + (r8 >> 3)); // 3 ops
        r8 = (r2 + (r6 ^ 0x7777777777777777ULL)); // 2 ops
        r2 = (r2 + r6);
        r6 = (r8 & 0x8888888888888888ULL);
        r6 = ((r8 - r6) + (r6 >> 3)); // 3 ops
        r8 = (r2 & 0x8888888888888888ULL);
        r2 = ((r2 - r8) + (r8 >> 3)); // 3 ops
        r8 = (r3 + (r7 ^ 0x7777777777777777ULL)); // 2 ops
        r3 = (r3 + r7);
        r7 = (r8 & 0x8888888888888888ULL);
        r7 = ((r8 - r7) + (r7 >> 3)); // 3 ops
        r8 = (r3 & 0x8888888888888888ULL);
        r3 = ((r3 - r8) + (r8 >> 3)); // 3 ops
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        // Multiplication by 2**-3 is trivial mod 7
        // 184 lines of code, 380 operations
        if (i < 16) goto l_mmv7_op_l64_1;
        r8 = ((a[0] & 0x77777777ULL)
            | ((a[8] << 32) & 0x7777777700000000ULL)); // 4 ops
        v_out[0] = r8 ^  p_mask[6];
        a[0] = (((a[0] >> 32) & 0x77777777ULL)
            | (a[8] & 0x7777777700000000ULL)); // 4 ops
        v_out[2] = a[0] ^  p_mask[6];
        r8 = (r0 & 0x77777777ULL);
        v_out[1] = (r8 ^  p_mask[6]) & 0x77777777ULL;
        r0 = ((r0 >> 32) & 0x77777777ULL); // 2 ops
        v_out[3] = (r0 ^  p_mask[6]) & 0x77777777ULL;
        r8 = ((a[1] & 0x77777777ULL)
            | ((a[9] << 32) & 0x7777777700000000ULL)); // 4 ops
        v_out[4] = r8 ^  p_mask[6];
        a[1] = (((a[1] >> 32) & 0x77777777ULL)
            | (a[9] & 0x7777777700000000ULL)); // 4 ops
        v_out[6] = a[1] ^  p_mask[4];
        r8 = (r1 & 0x77777777ULL);
        v_out[5] = (r8 ^  p_mask[6]) & 0x77777777ULL;
        r1 = ((r1 >> 32) & 0x77777777ULL); // 2 ops
        v_out[7] = (r1 ^  p_mask[4]) & 0x77777777ULL;
        r8 = ((a[2] & 0x77777777ULL)
            | ((a[10] << 32) & 0x7777777700000000ULL)); // 4 ops
        v_out[8] = r8 ^  p_mask[6];
        a[2] = (((a[2] >> 32) & 0x77777777ULL)
            | (a[10] & 0x7777777700000000ULL)); // 4 ops
        v_out[10] = a[2] ^  p_mask[4];
        r8 = (r2 & 0x77777777ULL);
        v_out[9] = (r8 ^  p_mask[6]) & 0x77777777ULL;
        r2 = ((r2 >> 32) & 0x77777777ULL); // 2 ops
        v_out[11] = (r2 ^  p_mask[4]) & 0x77777777ULL;
        r8 = ((a[3] & 0x77777777ULL)
            | ((a[11] << 32) & 0x7777777700000000ULL)); // 4 ops
        v_out[12] = r8 ^  p_mask[4];
        a[3] = (((a[3] >> 32) & 0x77777777ULL)
            | (a[11] & 0x7777777700000000ULL)); // 4 ops
        v_out[14] = a[3] ^  p_mask[4];
        r8 = (r3 & 0x77777777ULL);
        v_out[13] = (r8 ^  p_mask[4]) & 0x77777777ULL;
        r3 = ((r3 >> 32) & 0x77777777ULL); // 2 ops
        v_out[15] = (r3 ^  p_mask[4]) & 0x77777777ULL;
        r8 = ((a[4] & 0x77777777ULL)
            | ((a[12] << 32) & 0x7777777700000000ULL)); // 4 ops
        v_out[16] = r8 ^  p_mask[6];
        a[4] = (((a[4] >> 32) & 0x77777777ULL)
            | (a[12] & 0x7777777700000000ULL)); // 4 ops
        v_out[18] = a[4] ^  p_mask[4];
        r8 = (r4 & 0x77777777ULL);
        v_out[17] = (r8 ^  p_mask[6]) & 0x77777777ULL;
        r4 = ((r4 >> 32) & 0x77777777ULL); // 2 ops
        v_out[19] = (r4 ^  p_mask[4]) & 0x77777777ULL;
        r8 = ((a[5] & 0x77777777ULL)
            | ((a[13] << 32) & 0x7777777700000000ULL)); // 4 ops
        v_out[20] = r8 ^  p_mask[4];
        a[5] = (((a[5] >> 32) & 0x77777777ULL)
            | (a[13] & 0x7777777700000000ULL)); // 4 ops
        v_out[22] = a[5] ^  p_mask[4];
        r8 = (r5 & 0x77777777ULL);
        v_out[21] = (r8 ^  p_mask[4]) & 0x77777777ULL;
        r5 = ((r5 >> 32) & 0x77777777ULL); // 2 ops
        v_out[23] = (r5 ^  p_mask[4]) & 0x77777777ULL;
        r8 = ((a[6] & 0x77777777ULL)
            | ((a[14] << 32) & 0x7777777700000000ULL)); // 4 ops
        v_out[24] = r8 ^  p_mask[4];
        a[6] = (((a[6] >> 32) & 0x77777777ULL)
            | (a[14] & 0x7777777700000000ULL)); // 4 ops
        v_out[26] = a[6] ^  p_mask[4];
        r8 = (r6 & 0x77777777ULL);
        v_out[25] = (r8 ^  p_mask[4]) & 0x77777777ULL;
        r6 = ((r6 >> 32) & 0x77777777ULL); // 2 ops
        v_out[27] = (r6 ^  p_mask[4]) & 0x77777777ULL;
        r8 = ((a[7] & 0x77777777ULL)
            | ((a[15] << 32) & 0x7777777700000000ULL)); // 4 ops
        v_out[28] = r8 ^  p_mask[4];
        a[7] = (((a[7] >> 32) & 0x77777777ULL)
            | (a[15] & 0x7777777700000000ULL)); // 4 ops
        v_out[30] = a[7] ^  p_mask[6];
        r8 = (r7 & 0x77777777ULL);
        v_out[29] = (r8 ^  p_mask[4]) & 0x77777777ULL;
        r7 = ((r7 >> 32) & 0x77777777ULL); // 2 ops
        v_out[31] = (r7 ^  p_mask[6]) & 0x77777777ULL;
        v_in += 32;
        v_out += 32;
        // 64 lines of code, 136 operations
        }
        // End of automatically generated matrix operation.
 
    }
}  


static void mm_op7_xi_a(uint_mmv_t *v_in,  uint32_t exp1, uint_mmv_t *v_out)
{
    uint_fast32_t i1;
    uint_mmv_t e_mask =  0 - ((uint_mmv_t)exp1 & 0x1ULL);
    for (i1 = 0; i1 < 6; ++i1) {
        // %%MUL_MATRIX_XI16 v_in, e_mask, v_out

        // This is an automatically generated matrix operation, do not change!
        {
        uint_mmv_t r0, r1, r2, r3, r4;

        uint_fast32_t i;
        // TODO: write comment!!!
        // 
        for (i = 0; i < 2; ++i) {
        e_mask = ~(e_mask);
        r0 = v_in[0] ^  (0x7770777077707770ULL & e_mask);
        r4 = ((r0 ^ (r0 >> 4)) & 0x70007000700070ULL); // 3 ops
        r0 ^= (r4 | (r4 << 4)); // 3 ops
        r1 = v_in[4] ^  (0x7000700070007ULL & e_mask);
        r4 = ((r1 ^ (r1 >> 4)) & 0x70007000700070ULL); // 3 ops
        r1 ^= (r4 | (r4 << 4)); // 3 ops
        r2 = v_in[2] ^  (0x7000700070007ULL & e_mask);
        r4 = ((r2 ^ (r2 >> 4)) & 0x70007000700070ULL); // 3 ops
        r2 ^= (r4 | (r4 << 4)); // 3 ops
        r3 = v_in[6] ^  (0x7000700070007ULL & e_mask);
        r4 = ((r3 ^ (r3 >> 4)) & 0x70007000700070ULL); // 3 ops
        r3 ^= (r4 | (r4 << 4)); // 3 ops
        // Butterfly: v[i], v[i+1] = v[i]+v[i+1], v[i]-v[i+1]
        r4 = (((r0 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r0 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r0 = ((r0 ^ 0x7070707070707070ULL) + r4); // 2 ops
        r4 = (r0 & 0x8888888888888888ULL);
        r0 = ((r0 - r4) + (r4 >> 3)); // 3 ops
        r4 = (((r1 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r1 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r1 = ((r1 ^ 0x7070707070707070ULL) + r4); // 2 ops
        r4 = (r1 & 0x8888888888888888ULL);
        r1 = ((r1 - r4) + (r4 >> 3)); // 3 ops
        r4 = (((r2 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r2 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r2 = ((r2 ^ 0x7070707070707070ULL) + r4); // 2 ops
        r4 = (r2 & 0x8888888888888888ULL);
        r2 = ((r2 - r4) + (r4 >> 3)); // 3 ops
        r4 = (((r3 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r3 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r3 = ((r3 ^ 0x7070707070707070ULL) + r4); // 2 ops
        r4 = (r3 & 0x8888888888888888ULL);
        r3 = ((r3 - r4) + (r4 >> 3)); // 3 ops
        // Vector is now  r(i) for i = 0,1,2,3
        // Butterfly: v[i], v[i+2] = v[i]+v[i+2], v[i]-v[i+2]
        r4 = (((r0 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r0 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r0 = ((r0 ^ 0x7700770077007700ULL) + r4); // 2 ops
        r4 = (r0 & 0x8888888888888888ULL);
        r0 = ((r0 - r4) + (r4 >> 3)); // 3 ops
        r4 = (((r1 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r1 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r1 = ((r1 ^ 0x7700770077007700ULL) + r4); // 2 ops
        r4 = (r1 & 0x8888888888888888ULL);
        r1 = ((r1 - r4) + (r4 >> 3)); // 3 ops
        r4 = (((r2 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r2 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r2 = ((r2 ^ 0x7700770077007700ULL) + r4); // 2 ops
        r4 = (r2 & 0x8888888888888888ULL);
        r2 = ((r2 - r4) + (r4 >> 3)); // 3 ops
        r4 = (((r3 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r3 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r3 = ((r3 ^ 0x7700770077007700ULL) + r4); // 2 ops
        r4 = (r3 & 0x8888888888888888ULL);
        r3 = ((r3 - r4) + (r4 >> 3)); // 3 ops
        // Vector is now  r(i) for i = 0,1,2,3
        // Butterfly: v[i], v[i+16] = v[i]+v[i+16], v[i]-v[i+16]
        r4 = (r0 + (r1 ^ 0x7777777777777777ULL)); // 2 ops
        r0 = (r0 + r1);
        r1 = (r4 & 0x8888888888888888ULL);
        r1 = ((r4 - r1) + (r1 >> 3)); // 3 ops
        r4 = (r0 & 0x8888888888888888ULL);
        r0 = ((r0 - r4) + (r4 >> 3)); // 3 ops
        r4 = (r2 + (r3 ^ 0x7777777777777777ULL)); // 2 ops
        r2 = (r2 + r3);
        r3 = (r4 & 0x8888888888888888ULL);
        r3 = ((r4 - r3) + (r3 >> 3)); // 3 ops
        r4 = (r2 & 0x8888888888888888ULL);
        r2 = ((r2 - r4) + (r4 >> 3)); // 3 ops
        // Vector is now  r(i) for i = 0,1,2,3
        // Butterfly: v[i], v[i+32] = v[i]+v[i+32], v[i]-v[i+32]
        r4 = (r0 + (r2 ^ 0x7777777777777777ULL)); // 2 ops
        r0 = (r0 + r2);
        r2 = (r4 & 0x8888888888888888ULL);
        r2 = ((r4 - r2) + (r2 >> 3)); // 3 ops
        r4 = (r0 & 0x8888888888888888ULL);
        r0 = ((r0 - r4) + (r4 >> 3)); // 3 ops
        r4 = (r1 + (r3 ^ 0x7777777777777777ULL)); // 2 ops
        r1 = (r1 + r3);
        r3 = (r4 & 0x8888888888888888ULL);
        r3 = ((r4 - r3) + (r3 >> 3)); // 3 ops
        r4 = (r1 & 0x8888888888888888ULL);
        r1 = ((r1 - r4) + (r4 >> 3)); // 3 ops
        // Vector is now  r(i) for i = 0,1,2,3
        // Multiplication by 2**0 is trivial mod 7
        e_mask = ~(e_mask);
        r0 = (((r0 & 0x3333333333333333ULL) << 1)
            | ((r0 & 0x4444444444444444ULL) >> 2)); // 5 ops
        v_out[0] = r0 ^ (e_mask & 0x7770777077707770ULL);
        r1 = (((r1 & 0x3333333333333333ULL) << 1)
            | ((r1 & 0x4444444444444444ULL) >> 2)); // 5 ops
        v_out[2] = r1 ^ (e_mask & 0x7000700070007ULL);
        r2 = (((r2 & 0x3333333333333333ULL) << 1)
            | ((r2 & 0x4444444444444444ULL) >> 2)); // 5 ops
        v_out[4] = r2 ^ (e_mask & 0x7000700070007ULL);
        r3 = (((r3 & 0x3333333333333333ULL) << 1)
            | ((r3 & 0x4444444444444444ULL) >> 2)); // 5 ops
        v_out[6] = r3 ^ (e_mask & 0x7000700070007ULL);
        // 78 lines of code, 186 operations
        v_in++;
        v_out++;
        }
        v_out[-1] &= 0x77777777ULL;
        v_out[1] &= 0x77777777ULL;
        v_out[3] &= 0x77777777ULL;
        v_out[5] &= 0x77777777ULL;
        v_in += 6;
        v_out += 6;
        }
        // End of automatically generated matrix operation.
 
    }
}  

/// @endcond 


/**
  @brief Compute an operation of the monster group on a vector

  Let ``v_in`` be a vector of the representation \f$\rho_{7}\f$
  of the monster group.

  The function implements the operation of the element \f$\xi^e\f$ 
  of the monster group  on a vector ``v_in`` in the 
  representation \f$\rho_{7}\f$ of the monster.

  Parameter ``exp`` is the exponent \f$e\f$ of the generator 
  \f$\xi^e\f$. The function computes the operation of \f$\xi^e\f$  
  on the input  vector ``v_in`` and  stores the result in the output 
  vector ``v_out.`` 

  Input vector  ``v_in`` is not changed.
*/
// %%EXPORT px
MM_OP7_API
void mm_op7_xi(uint_mmv_t *v_in,  uint32_t exp, uint_mmv_t *v_out)
{
    uint_mmv_t i;
    uint32_t exp1;

    exp %= 3;
    if (exp == 0) {
        for (i = 0; i < 15468; ++i) v_out[i] = v_in[i];
        return;
    }
    exp1 =  exp - 1;

    // Do monomial part, i.e. tags B, C, T, X
    // Caution: this uses v_out[MM_OP7_OFS_Z:] as temporary storage
    mm_op7_xi_mon(v_in, exp1, v_out);

    // Do tag A
    mm_op7_xi_a(v_in, exp1, v_out); 

    // Do tags X, Y
    for (i = 0; i < 4; ++i) {
        uint_mmv_t *p_src = v_in + MM_OP7_OFS_Z + (i << HALF_YZ_SHIFT);
        mm_op7_xi_yz(p_src, exp1, v_out + TAB7_XI64_OFFSET[exp1][i]);
    }
}

/**
  @brief Restriction of function ``mm_op7_xi`` to tag ``A``

  Function ``mm_op7_xi`` computes a certain operation of the
  monster group on a vector ``v_in``. That operation depends
  on a parameter ``exp``.
  
  Function ``mm_op7_xi_tag_A`` computes the same
  operation on the entries of the vector ``v = v_in`` with
  tag ``A`` only, and ignores the other entries of ``v``.
  See section **The representation of the monster group**
  in the **API reference** for tags of entries of a vector in
  the representation of the monster.

  The function overwrites the vector ``v`` with the result.
  Here only entries of ``v`` with tag ``A`` are changed. This 
  function is much faster than function ``mm_op7_xy``.
*/
// %%EXPORT px
MM_OP7_API
void mm_op7_xi_tag_A(uint_mmv_t *v,  uint32_t exp)
{
    uint_mmv_t v_tmp[24 * 2];
    uint_fast32_t i;
    
    exp %= 3;
    if (exp == 0) return;
    mm_op7_xi_a(v, exp - 1, v_tmp);
    for (i = 0; i < 24 * 2; ++i) v[i] = v_tmp[i];
}


//  %%GEN h
//  %%GEN c
