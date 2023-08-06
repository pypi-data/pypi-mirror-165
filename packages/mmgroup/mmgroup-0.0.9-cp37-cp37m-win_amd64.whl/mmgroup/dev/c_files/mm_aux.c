/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm_aux.c

 File ``mm_aux.c`` provides the basic functions for dealing with the
 representations  of the monster group  modulo various small 
 integers ``p = 2**n-1``,  ``2 <= n <= 8``.
 Here the integer ``p`` is called the modulus. 

 Especially, we deal with vectors in such a representation as 
 desrcibed in  *The C interface of the mmgroup project*, 
 section *Description of the mmgroup.mm extension*.

 For such a vector there is an internal representation, an external
 representation, and also a sparse representation, as described in the
 documentation mentioned above.

 The functions in this file provide access to the internal representation 
 of such a vector. The also support the conversion between the differnt 
 representations of a vector.  

 Usually, the order of the parameters of functions in this file is:
      
       1. Modulus p, if present

       2. The input value or the input data array

       3. Any parameters that do not affect the positions in the output array

       4. The output data array

       5. Parameters (e.g. lengths, indices) that affect the positions of the 
          data being modified in the output array

*/



/// @cond DO_NOT_DOCUMENT 
#include <stdlib.h>
#include "clifford12.h"
#include "mm_basics.h"
/// @endcond  

// %%EXPORT_KWD MM_BASICS_API




/// @cond DO_NOT_DOCUMENT 

// %%USE_TABLE
static const uint32_t MMV_CONST_TABLE[] = {
// %%TABLE MMV_CONST_TAB, uint32
0x00044643UL,0x00000000UL,0x00034643UL,0x00011305UL,
0x0003c643UL,0x0002c643UL,0x00022484UL,0x0001a484UL
};


// %%PY_DOCSTR MM_AUX_IO24.abc_table, 1
// Table for expanding entries for tags 'A', 'B', 'C'.
// 
// Entry k0 of the external representation of the monster is
// mapped to location k1 in the internal representation with
// k1 = (Table[k0] & 0x7ff) + k0 - 24. Entry k0 is also copied
// to location k1 - 31 * (Table[k0] >> 11) of the internal rep.
// 
// See comments 'Internal representation of a vector' and
// 'External representation of a vector' for internal and
// external representation of a vector.
static const uint16_t MM_AUX_TBL_ABC[] = {
// %%TABLE MM_AUX_TBL_ABC, uint16
0x0018,0x0038,0x0058,0x0078,0x0098,0x00b8,0x00d8,0x00f8,
0x0118,0x0138,0x0158,0x0178,0x0198,0x01b8,0x01d8,0x01f8,
0x0218,0x0238,0x0258,0x0278,0x0298,0x02b8,0x02d8,0x02f8,
0x0820,0x103f,0x083f,0x185d,0x105d,0x085d,0x207a,0x187a,
0x107a,0x087a,0x2896,0x2096,0x1896,0x1096,0x0896,0x30b1,
0x28b1,0x20b1,0x18b1,0x10b1,0x08b1,0x38cb,0x30cb,0x28cb,
0x20cb,0x18cb,0x10cb,0x08cb,0x40e4,0x38e4,0x30e4,0x28e4,
0x20e4,0x18e4,0x10e4,0x08e4,0x48fc,0x40fc,0x38fc,0x30fc,
0x28fc,0x20fc,0x18fc,0x10fc,0x08fc,0x5113,0x4913,0x4113,
0x3913,0x3113,0x2913,0x2113,0x1913,0x1113,0x0913,0x5929,
0x5129,0x4929,0x4129,0x3929,0x3129,0x2929,0x2129,0x1929,
0x1129,0x0929,0x613e,0x593e,0x513e,0x493e,0x413e,0x393e,
0x313e,0x293e,0x213e,0x193e,0x113e,0x093e,0x6952,0x6152,
0x5952,0x5152,0x4952,0x4152,0x3952,0x3152,0x2952,0x2152,
0x1952,0x1152,0x0952,0x7165,0x6965,0x6165,0x5965,0x5165,
0x4965,0x4165,0x3965,0x3165,0x2965,0x2165,0x1965,0x1165,
0x0965,0x7977,0x7177,0x6977,0x6177,0x5977,0x5177,0x4977,
0x4177,0x3977,0x3177,0x2977,0x2177,0x1977,0x1177,0x0977,
0x8188,0x7988,0x7188,0x6988,0x6188,0x5988,0x5188,0x4988,
0x4188,0x3988,0x3188,0x2988,0x2188,0x1988,0x1188,0x0988,
0x8998,0x8198,0x7998,0x7198,0x6998,0x6198,0x5998,0x5198,
0x4998,0x4198,0x3998,0x3198,0x2998,0x2198,0x1998,0x1198,
0x0998,0x91a7,0x89a7,0x81a7,0x79a7,0x71a7,0x69a7,0x61a7,
0x59a7,0x51a7,0x49a7,0x41a7,0x39a7,0x31a7,0x29a7,0x21a7,
0x19a7,0x11a7,0x09a7,0x99b5,0x91b5,0x89b5,0x81b5,0x79b5,
0x71b5,0x69b5,0x61b5,0x59b5,0x51b5,0x49b5,0x41b5,0x39b5,
0x31b5,0x29b5,0x21b5,0x19b5,0x11b5,0x09b5,0xa1c2,0x99c2,
0x91c2,0x89c2,0x81c2,0x79c2,0x71c2,0x69c2,0x61c2,0x59c2,
0x51c2,0x49c2,0x41c2,0x39c2,0x31c2,0x29c2,0x21c2,0x19c2,
0x11c2,0x09c2,0xa9ce,0xa1ce,0x99ce,0x91ce,0x89ce,0x81ce,
0x79ce,0x71ce,0x69ce,0x61ce,0x59ce,0x51ce,0x49ce,0x41ce,
0x39ce,0x31ce,0x29ce,0x21ce,0x19ce,0x11ce,0x09ce,0xb1d9,
0xa9d9,0xa1d9,0x99d9,0x91d9,0x89d9,0x81d9,0x79d9,0x71d9,
0x69d9,0x61d9,0x59d9,0x51d9,0x49d9,0x41d9,0x39d9,0x31d9,
0x29d9,0x21d9,0x19d9,0x11d9,0x09d9,0xb9e3,0xb1e3,0xa9e3,
0xa1e3,0x99e3,0x91e3,0x89e3,0x81e3,0x79e3,0x71e3,0x69e3,
0x61e3,0x59e3,0x51e3,0x49e3,0x41e3,0x39e3,0x31e3,0x29e3,
0x21e3,0x19e3,0x11e3,0x09e3,0x0a0c,0x122b,0x0a2b,0x1a49,
0x1249,0x0a49,0x2266,0x1a66,0x1266,0x0a66,0x2a82,0x2282,
0x1a82,0x1282,0x0a82,0x329d,0x2a9d,0x229d,0x1a9d,0x129d,
0x0a9d,0x3ab7,0x32b7,0x2ab7,0x22b7,0x1ab7,0x12b7,0x0ab7,
0x42d0,0x3ad0,0x32d0,0x2ad0,0x22d0,0x1ad0,0x12d0,0x0ad0,
0x4ae8,0x42e8,0x3ae8,0x32e8,0x2ae8,0x22e8,0x1ae8,0x12e8,
0x0ae8,0x52ff,0x4aff,0x42ff,0x3aff,0x32ff,0x2aff,0x22ff,
0x1aff,0x12ff,0x0aff,0x5b15,0x5315,0x4b15,0x4315,0x3b15,
0x3315,0x2b15,0x2315,0x1b15,0x1315,0x0b15,0x632a,0x5b2a,
0x532a,0x4b2a,0x432a,0x3b2a,0x332a,0x2b2a,0x232a,0x1b2a,
0x132a,0x0b2a,0x6b3e,0x633e,0x5b3e,0x533e,0x4b3e,0x433e,
0x3b3e,0x333e,0x2b3e,0x233e,0x1b3e,0x133e,0x0b3e,0x7351,
0x6b51,0x6351,0x5b51,0x5351,0x4b51,0x4351,0x3b51,0x3351,
0x2b51,0x2351,0x1b51,0x1351,0x0b51,0x7b63,0x7363,0x6b63,
0x6363,0x5b63,0x5363,0x4b63,0x4363,0x3b63,0x3363,0x2b63,
0x2363,0x1b63,0x1363,0x0b63,0x8374,0x7b74,0x7374,0x6b74,
0x6374,0x5b74,0x5374,0x4b74,0x4374,0x3b74,0x3374,0x2b74,
0x2374,0x1b74,0x1374,0x0b74,0x8b84,0x8384,0x7b84,0x7384,
0x6b84,0x6384,0x5b84,0x5384,0x4b84,0x4384,0x3b84,0x3384,
0x2b84,0x2384,0x1b84,0x1384,0x0b84,0x9393,0x8b93,0x8393,
0x7b93,0x7393,0x6b93,0x6393,0x5b93,0x5393,0x4b93,0x4393,
0x3b93,0x3393,0x2b93,0x2393,0x1b93,0x1393,0x0b93,0x9ba1,
0x93a1,0x8ba1,0x83a1,0x7ba1,0x73a1,0x6ba1,0x63a1,0x5ba1,
0x53a1,0x4ba1,0x43a1,0x3ba1,0x33a1,0x2ba1,0x23a1,0x1ba1,
0x13a1,0x0ba1,0xa3ae,0x9bae,0x93ae,0x8bae,0x83ae,0x7bae,
0x73ae,0x6bae,0x63ae,0x5bae,0x53ae,0x4bae,0x43ae,0x3bae,
0x33ae,0x2bae,0x23ae,0x1bae,0x13ae,0x0bae,0xabba,0xa3ba,
0x9bba,0x93ba,0x8bba,0x83ba,0x7bba,0x73ba,0x6bba,0x63ba,
0x5bba,0x53ba,0x4bba,0x43ba,0x3bba,0x33ba,0x2bba,0x23ba,
0x1bba,0x13ba,0x0bba,0xb3c5,0xabc5,0xa3c5,0x9bc5,0x93c5,
0x8bc5,0x83c5,0x7bc5,0x73c5,0x6bc5,0x63c5,0x5bc5,0x53c5,
0x4bc5,0x43c5,0x3bc5,0x33c5,0x2bc5,0x23c5,0x1bc5,0x13c5,
0x0bc5,0xbbcf,0xb3cf,0xabcf,0xa3cf,0x9bcf,0x93cf,0x8bcf,
0x83cf,0x7bcf,0x73cf,0x6bcf,0x63cf,0x5bcf,0x53cf,0x4bcf,
0x43cf,0x3bcf,0x33cf,0x2bcf,0x23cf,0x1bcf,0x13cf,0x0bcf,
0x0bf8,0x1417,0x0c17,0x1c35,0x1435,0x0c35,0x2452,0x1c52,
0x1452,0x0c52,0x2c6e,0x246e,0x1c6e,0x146e,0x0c6e,0x3489,
0x2c89,0x2489,0x1c89,0x1489,0x0c89,0x3ca3,0x34a3,0x2ca3,
0x24a3,0x1ca3,0x14a3,0x0ca3,0x44bc,0x3cbc,0x34bc,0x2cbc,
0x24bc,0x1cbc,0x14bc,0x0cbc,0x4cd4,0x44d4,0x3cd4,0x34d4,
0x2cd4,0x24d4,0x1cd4,0x14d4,0x0cd4,0x54eb,0x4ceb,0x44eb,
0x3ceb,0x34eb,0x2ceb,0x24eb,0x1ceb,0x14eb,0x0ceb,0x5d01,
0x5501,0x4d01,0x4501,0x3d01,0x3501,0x2d01,0x2501,0x1d01,
0x1501,0x0d01,0x6516,0x5d16,0x5516,0x4d16,0x4516,0x3d16,
0x3516,0x2d16,0x2516,0x1d16,0x1516,0x0d16,0x6d2a,0x652a,
0x5d2a,0x552a,0x4d2a,0x452a,0x3d2a,0x352a,0x2d2a,0x252a,
0x1d2a,0x152a,0x0d2a,0x753d,0x6d3d,0x653d,0x5d3d,0x553d,
0x4d3d,0x453d,0x3d3d,0x353d,0x2d3d,0x253d,0x1d3d,0x153d,
0x0d3d,0x7d4f,0x754f,0x6d4f,0x654f,0x5d4f,0x554f,0x4d4f,
0x454f,0x3d4f,0x354f,0x2d4f,0x254f,0x1d4f,0x154f,0x0d4f,
0x8560,0x7d60,0x7560,0x6d60,0x6560,0x5d60,0x5560,0x4d60,
0x4560,0x3d60,0x3560,0x2d60,0x2560,0x1d60,0x1560,0x0d60,
0x8d70,0x8570,0x7d70,0x7570,0x6d70,0x6570,0x5d70,0x5570,
0x4d70,0x4570,0x3d70,0x3570,0x2d70,0x2570,0x1d70,0x1570,
0x0d70,0x957f,0x8d7f,0x857f,0x7d7f,0x757f,0x6d7f,0x657f,
0x5d7f,0x557f,0x4d7f,0x457f,0x3d7f,0x357f,0x2d7f,0x257f,
0x1d7f,0x157f,0x0d7f,0x9d8d,0x958d,0x8d8d,0x858d,0x7d8d,
0x758d,0x6d8d,0x658d,0x5d8d,0x558d,0x4d8d,0x458d,0x3d8d,
0x358d,0x2d8d,0x258d,0x1d8d,0x158d,0x0d8d,0xa59a,0x9d9a,
0x959a,0x8d9a,0x859a,0x7d9a,0x759a,0x6d9a,0x659a,0x5d9a,
0x559a,0x4d9a,0x459a,0x3d9a,0x359a,0x2d9a,0x259a,0x1d9a,
0x159a,0x0d9a,0xada6,0xa5a6,0x9da6,0x95a6,0x8da6,0x85a6,
0x7da6,0x75a6,0x6da6,0x65a6,0x5da6,0x55a6,0x4da6,0x45a6,
0x3da6,0x35a6,0x2da6,0x25a6,0x1da6,0x15a6,0x0da6,0xb5b1,
0xadb1,0xa5b1,0x9db1,0x95b1,0x8db1,0x85b1,0x7db1,0x75b1,
0x6db1,0x65b1,0x5db1,0x55b1,0x4db1,0x45b1,0x3db1,0x35b1,
0x2db1,0x25b1,0x1db1,0x15b1,0x0db1,0xbdbb,0xb5bb,0xadbb,
0xa5bb,0x9dbb,0x95bb,0x8dbb,0x85bb,0x7dbb,0x75bb,0x6dbb,
0x65bb,0x5dbb,0x55bb,0x4dbb,0x45bb,0x3dbb,0x35bb,0x2dbb,
0x25bb,0x1dbb,0x15bb,0x0dbb
};



// %%PY_DOCSTR MM_AUX_IO24.reduce_table, 1
// Masks for reducing the fields of an uint_mmv_t modulo p
// 
// Table entries 2*i-2 and 2*i-1 refer to modulus p = 2**i-1 for
// i = 2,...,8. In the standard case, when i is not a power of
// two, entries 2*i-2 and  2*i-1 have the following values:
// 
// Index  Table entry
// 2*i-2: A mask containg the value 1 in each field.
// 2*i-1: A mask containg the value 2**i-1 in each field.
// 
// If i is a power of two then table entry 2*i-1 is mask containing
// the  value 2**(i/2)-1 in each field.
// 
// The reason for that special case is that there is no space for
// a carry bit between two adjacent fields if i is a power of two.
// In that case we need a special trick for detecting the value
// 2**i-i in a field.
static const uint_mmv_t MM_AUX_TBL_REDUCE[] = {
// %%TABLE MM_AUX_TBL_REDUCE, uint%{INT_BITS}
0x5555555555555555ULL,0x5555555555555555ULL,
0x1111111111111111ULL,0x7777777777777777ULL,
0x1111111111111111ULL,0x3333333333333333ULL,
0x0101010101010101ULL,0x1f1f1f1f1f1f1f1fULL,
0x0101010101010101ULL,0x3f3f3f3f3f3f3f3fULL,
0x0101010101010101ULL,0x7f7f7f7f7f7f7f7fULL,
0x0101010101010101ULL,0x0f0f0f0f0f0f0f0fULL
};

/// @endcond  





// %%GEN ch
#ifdef __cplusplus
extern "C" {
#endif
// %%GEN c

//  %%GEN h
//  %%GEN c



/**********************************************************************
*** Low-level functions supporting vectors of type uint_mmv_t[]
**********************************************************************/



/**
  @brief Read entries from vector in internal representation

  Read entries of vector ``mv`` (stored in internal representation
  with modulus ``p``) and store these entries  in the array ``b``.
  Here ``len`` is the number of entries to be read. ``len`` must 
  be a multiple of the number of entries in an integer
  of ``type uint_mmv_t``. It is ok if ``len`` is a multiple of 32. 
  Output vector ``b`` is reduced modulo ``p``.

  Here ``p`` must be a legal modulus.
*/
// %%EXPORT px
MM_BASICS_API
void mm_aux_read_mmv1(uint32_t p, uint_mmv_t *mv, uint8_t *b, uint32_t len)
{
    uint_fast32_t i, sh, tmp;  
    uint_mmv_t source;
    // %%MMV_LOAD_CONST  p, i
    // Store constant table for p to i
    i = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    sh = ((i >> 15) & 15);        // This is P_BITS
    i = ((i >> 9) & 3); // This is LOG_FIELD_BITS
    len >>= 6 - i;

    switch (i) {
        // %%FOR LOG_F in [1, 2, 3]
        case 1:
            while (len--) {
                source = *mv++;
                // %%FOR jj in range(0, INT_BITS, 1 << LOG_F)
                tmp = (source >> 0) & p;
                b[0] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 2) & p;
                b[1] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 4) & p;
                b[2] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 6) & p;
                b[3] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 8) & p;
                b[4] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 10) & p;
                b[5] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 12) & p;
                b[6] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 14) & p;
                b[7] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 16) & p;
                b[8] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 18) & p;
                b[9] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 20) & p;
                b[10] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 22) & p;
                b[11] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 24) & p;
                b[12] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 26) & p;
                b[13] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 28) & p;
                b[14] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 30) & p;
                b[15] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 32) & p;
                b[16] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 34) & p;
                b[17] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 36) & p;
                b[18] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 38) & p;
                b[19] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 40) & p;
                b[20] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 42) & p;
                b[21] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 44) & p;
                b[22] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 46) & p;
                b[23] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 48) & p;
                b[24] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 50) & p;
                b[25] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 52) & p;
                b[26] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 54) & p;
                b[27] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 56) & p;
                b[28] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 58) & p;
                b[29] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 60) & p;
                b[30] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 62) & p;
                b[31] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                // %%END FOR
                b += 32;
            }
            break;
        case 2:
            while (len--) {
                source = *mv++;
                // %%FOR jj in range(0, INT_BITS, 1 << LOG_F)
                tmp = (source >> 0) & p;
                b[0] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 4) & p;
                b[1] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 8) & p;
                b[2] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 12) & p;
                b[3] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 16) & p;
                b[4] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 20) & p;
                b[5] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 24) & p;
                b[6] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 28) & p;
                b[7] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 32) & p;
                b[8] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 36) & p;
                b[9] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 40) & p;
                b[10] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 44) & p;
                b[11] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 48) & p;
                b[12] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 52) & p;
                b[13] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 56) & p;
                b[14] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 60) & p;
                b[15] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                // %%END FOR
                b += 16;
            }
            break;
        case 3:
            while (len--) {
                source = *mv++;
                // %%FOR jj in range(0, INT_BITS, 1 << LOG_F)
                tmp = (source >> 0) & p;
                b[0] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 8) & p;
                b[1] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 16) & p;
                b[2] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 24) & p;
                b[3] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 32) & p;
                b[4] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 40) & p;
                b[5] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 48) & p;
                b[6] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 56) & p;
                b[7] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                // %%END FOR
                b += 8;
            }
            break;
        // %%END FOR
    }
}


/**
  @brief Read entries from vector in internal representation

  Same operation as in function ``mm_aux_read_mmv1()``, but the
  output vector ``b`` is not reduced. This is for debugging and less 
  optimized than ``mm_aux_read_mmv1()``. 

  Here ``p`` must be a legal modulus.
*/
// %%EXPORT px
MM_BASICS_API
void mm_aux_read_direct_mmv1(uint32_t p, uint_mmv_t *mv, uint8_t *b, uint32_t len)
{
    uint_fast32_t i, j;  
    uint_mmv_t source;
    // %%MMV_LOAD_CONST  p, i
    // Store constant table for p to i
    i = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    i = ((i >> 9) & 3); // This is LOG_FIELD_BITS
    len >>= 6 - i;
    i = 1 << i;                       // This is FIELD_BITS

    while (len--) {
        source = *mv++;
        for (j = 0; j < 64; j += i) 
            *b++ = (uint8_t)((source >> j) & p);
    }
}


/**
  @brief Write data to a vector in internal representation

  Write data from the array ``b`` to the vector ``mv`` (stored 
  in internal representation with modulus ``p``). Here ``len`` is 
  the number of entries to be written. ``len`` must be a multiple 
  of the number of entries in an integer of type ``uint_mmv_t``. 
  It is ok if len is a multiple of 32. 

  Here ``p`` must be a legal modulus.
*/
// %%EXPORT px
MM_BASICS_API
void mm_aux_write_mmv1(uint32_t p, uint8_t *b, uint_mmv_t *mv, uint32_t len)
{
    uint_fast32_t i;  
    uint_mmv_t dest;
    // %%MMV_LOAD_CONST  p, i
    // Store constant table for p to i
    i = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    i = ((i >> 9) & 3); // This is LOG_FIELD_BITS
    len >>= 6 - i;
    
    switch(i) {
        // %%FOR LOG_F in [1, 2, 3]
        case 1:
            while (len--) {
                dest =  0;
                // %%FOR jj in range(0, INT_BITS, 1 << LOG_F)
                dest +=  (uint_mmv_t)(b[0]) << 0;
                dest +=  (uint_mmv_t)(b[1]) << 2;
                dest +=  (uint_mmv_t)(b[2]) << 4;
                dest +=  (uint_mmv_t)(b[3]) << 6;
                dest +=  (uint_mmv_t)(b[4]) << 8;
                dest +=  (uint_mmv_t)(b[5]) << 10;
                dest +=  (uint_mmv_t)(b[6]) << 12;
                dest +=  (uint_mmv_t)(b[7]) << 14;
                dest +=  (uint_mmv_t)(b[8]) << 16;
                dest +=  (uint_mmv_t)(b[9]) << 18;
                dest +=  (uint_mmv_t)(b[10]) << 20;
                dest +=  (uint_mmv_t)(b[11]) << 22;
                dest +=  (uint_mmv_t)(b[12]) << 24;
                dest +=  (uint_mmv_t)(b[13]) << 26;
                dest +=  (uint_mmv_t)(b[14]) << 28;
                dest +=  (uint_mmv_t)(b[15]) << 30;
                dest +=  (uint_mmv_t)(b[16]) << 32;
                dest +=  (uint_mmv_t)(b[17]) << 34;
                dest +=  (uint_mmv_t)(b[18]) << 36;
                dest +=  (uint_mmv_t)(b[19]) << 38;
                dest +=  (uint_mmv_t)(b[20]) << 40;
                dest +=  (uint_mmv_t)(b[21]) << 42;
                dest +=  (uint_mmv_t)(b[22]) << 44;
                dest +=  (uint_mmv_t)(b[23]) << 46;
                dest +=  (uint_mmv_t)(b[24]) << 48;
                dest +=  (uint_mmv_t)(b[25]) << 50;
                dest +=  (uint_mmv_t)(b[26]) << 52;
                dest +=  (uint_mmv_t)(b[27]) << 54;
                dest +=  (uint_mmv_t)(b[28]) << 56;
                dest +=  (uint_mmv_t)(b[29]) << 58;
                dest +=  (uint_mmv_t)(b[30]) << 60;
                dest +=  (uint_mmv_t)(b[31]) << 62;
                // %%END FOR
                *mv++ = dest;
                b += 32;
            }
            break;
        case 2:
            while (len--) {
                dest =  0;
                // %%FOR jj in range(0, INT_BITS, 1 << LOG_F)
                dest +=  (uint_mmv_t)(b[0]) << 0;
                dest +=  (uint_mmv_t)(b[1]) << 4;
                dest +=  (uint_mmv_t)(b[2]) << 8;
                dest +=  (uint_mmv_t)(b[3]) << 12;
                dest +=  (uint_mmv_t)(b[4]) << 16;
                dest +=  (uint_mmv_t)(b[5]) << 20;
                dest +=  (uint_mmv_t)(b[6]) << 24;
                dest +=  (uint_mmv_t)(b[7]) << 28;
                dest +=  (uint_mmv_t)(b[8]) << 32;
                dest +=  (uint_mmv_t)(b[9]) << 36;
                dest +=  (uint_mmv_t)(b[10]) << 40;
                dest +=  (uint_mmv_t)(b[11]) << 44;
                dest +=  (uint_mmv_t)(b[12]) << 48;
                dest +=  (uint_mmv_t)(b[13]) << 52;
                dest +=  (uint_mmv_t)(b[14]) << 56;
                dest +=  (uint_mmv_t)(b[15]) << 60;
                // %%END FOR
                *mv++ = dest;
                b += 16;
            }
            break;
        case 3:
            while (len--) {
                dest =  0;
                // %%FOR jj in range(0, INT_BITS, 1 << LOG_F)
                dest +=  (uint_mmv_t)(b[0]) << 0;
                dest +=  (uint_mmv_t)(b[1]) << 8;
                dest +=  (uint_mmv_t)(b[2]) << 16;
                dest +=  (uint_mmv_t)(b[3]) << 24;
                dest +=  (uint_mmv_t)(b[4]) << 32;
                dest +=  (uint_mmv_t)(b[5]) << 40;
                dest +=  (uint_mmv_t)(b[6]) << 48;
                dest +=  (uint_mmv_t)(b[7]) << 56;
                // %%END FOR
                *mv++ = dest;
                b += 8;
            }
            break;
        // %%END FOR
    }
}

/**
  @brief Read blocks of length 24 from vector in internal representation

  Read entries of vector ``mv`` with modulus ``p`` and store these 
  entries in the array ``b``. Here ``mv`` is a vector of blocks
  of 24  entries, with 8 entries slack after each block. ``len``
  is the number of such blocks to be read. So  altogether 24 * ``len``
  entries are read from ``mv`` and written to array ``b``; the 8
  bytes slack after each 24-byte block are dropped.
  Vector ``b`` is reduced modulo ``p``.

  Here ``p`` must be a legal modulus.
*/
// %%EXPORT px
MM_BASICS_API
void mm_aux_read_mmv24(uint32_t p, uint_mmv_t *mv, uint8_t *b, uint32_t len)
{
    uint_fast32_t i, sh, tmp;  
    uint_mmv_t source;
    // %%MMV_LOAD_CONST  p, i
    // Store constant table for p to i
    i = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    sh = ((i >> 15) & 15);        // This is P_BITS
    i = ((i >> 9) & 3); // This is LOG_FIELD_BITS

    switch(i) {
        // %%FOR LOG_F in [1, 2, 3]
        case 1:
            while (len--) {
                // %%FOR j in range(0, 24)         
                source = *mv++;                 
                tmp = (source >> 0) & p;
                b[0] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 2) & p;
                b[1] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 4) & p;
                b[2] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 6) & p;
                b[3] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 8) & p;
                b[4] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 10) & p;
                b[5] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 12) & p;
                b[6] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 14) & p;
                b[7] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 16) & p;
                b[8] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 18) & p;
                b[9] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 20) & p;
                b[10] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 22) & p;
                b[11] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 24) & p;
                b[12] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 26) & p;
                b[13] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 28) & p;
                b[14] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 30) & p;
                b[15] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 32) & p;
                b[16] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 34) & p;
                b[17] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 36) & p;
                b[18] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 38) & p;
                b[19] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 40) & p;
                b[20] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 42) & p;
                b[21] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 44) & p;
                b[22] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 46) & p;
                b[23] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                // %%END FOR                           
                b += 24;
            }
            break;
        case 2:
            while (len--) {
                // %%FOR j in range(0, 24)         
                source = *mv++;                 
                tmp = (source >> 0) & p;
                b[0] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 4) & p;
                b[1] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 8) & p;
                b[2] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 12) & p;
                b[3] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 16) & p;
                b[4] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 20) & p;
                b[5] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 24) & p;
                b[6] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 28) & p;
                b[7] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 32) & p;
                b[8] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 36) & p;
                b[9] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 40) & p;
                b[10] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 44) & p;
                b[11] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 48) & p;
                b[12] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 52) & p;
                b[13] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 56) & p;
                b[14] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 60) & p;
                b[15] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                source = *mv++;                 
                tmp = (source >> 0) & p;
                b[16] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 4) & p;
                b[17] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 8) & p;
                b[18] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 12) & p;
                b[19] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 16) & p;
                b[20] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 20) & p;
                b[21] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 24) & p;
                b[22] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 28) & p;
                b[23] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                // %%END FOR                           
                b += 24;
            }
            break;
        case 3:
            while (len--) {
                // %%FOR j in range(0, 24)         
                source = *mv++;                 
                tmp = (source >> 0) & p;
                b[0] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 8) & p;
                b[1] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 16) & p;
                b[2] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 24) & p;
                b[3] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 32) & p;
                b[4] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 40) & p;
                b[5] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 48) & p;
                b[6] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 56) & p;
                b[7] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                source = *mv++;                 
                tmp = (source >> 0) & p;
                b[8] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 8) & p;
                b[9] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 16) & p;
                b[10] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 24) & p;
                b[11] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 32) & p;
                b[12] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 40) & p;
                b[13] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 48) & p;
                b[14] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 56) & p;
                b[15] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                source = *mv++;                 
                tmp = (source >> 0) & p;
                b[16] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 8) & p;
                b[17] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 16) & p;
                b[18] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 24) & p;
                b[19] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 32) & p;
                b[20] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 40) & p;
                b[21] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 48) & p;
                b[22] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                tmp = (source >> 56) & p;
                b[23] = (uint8_t)((tmp + ((tmp + 1) >> sh)) & p);
                // %%END FOR                           
                b += 24;
                mv += 1;
            }
            break;
        // %%END FOR
    }
}    


/**
  @brief Write blocks of length 24 to vector in internal representation

  Write data from the array ``b`` to the vector ``mv`` with 
  modulus ``p``. We take ``24 * len`` bytes from the array b
  and write them to the vector ``mv``. Here ``mv`` is considered
  as a vector of blocks of 24 entries, with 8 entries slack 
  after each block; so ``len`` is the number of such 24-byte
  blocks to be written. The entries in the slack after each 
  block written to ``mv`` are set to zero.

  Here ``p`` must be a legal modulus.
*/
// %%EXPORT px
MM_BASICS_API
void mm_aux_write_mmv24(uint32_t p, uint8_t *b, uint_mmv_t *mv, uint32_t len)
{
    uint_fast32_t i;  
    uint_mmv_t dest;
    // %%MMV_LOAD_CONST  p, i
    // Store constant table for p to i
    i = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    i = ((i >> 9) & 3); // This is LOG_FIELD_BITS


    switch(i) {
        // %%FOR LOG_F in [1, 2, 3]
        case 1:
            while (len--) {
                // %%FOR j in range(0, 24)             
                dest = 0;
                dest += (uint_mmv_t)(b[0] & p) << 0;
                dest += (uint_mmv_t)(b[1] & p) << 2;
                dest += (uint_mmv_t)(b[2] & p) << 4;
                dest += (uint_mmv_t)(b[3] & p) << 6;
                dest += (uint_mmv_t)(b[4] & p) << 8;
                dest += (uint_mmv_t)(b[5] & p) << 10;
                dest += (uint_mmv_t)(b[6] & p) << 12;
                dest += (uint_mmv_t)(b[7] & p) << 14;
                dest += (uint_mmv_t)(b[8] & p) << 16;
                dest += (uint_mmv_t)(b[9] & p) << 18;
                dest += (uint_mmv_t)(b[10] & p) << 20;
                dest += (uint_mmv_t)(b[11] & p) << 22;
                dest += (uint_mmv_t)(b[12] & p) << 24;
                dest += (uint_mmv_t)(b[13] & p) << 26;
                dest += (uint_mmv_t)(b[14] & p) << 28;
                dest += (uint_mmv_t)(b[15] & p) << 30;
                dest += (uint_mmv_t)(b[16] & p) << 32;
                dest += (uint_mmv_t)(b[17] & p) << 34;
                dest += (uint_mmv_t)(b[18] & p) << 36;
                dest += (uint_mmv_t)(b[19] & p) << 38;
                dest += (uint_mmv_t)(b[20] & p) << 40;
                dest += (uint_mmv_t)(b[21] & p) << 42;
                dest += (uint_mmv_t)(b[22] & p) << 44;
                dest += (uint_mmv_t)(b[23] & p) << 46;
                // %%END FOR                           
                *mv++ = dest;                
                b += 24;
            }
            break;
        case 2:
            while (len--) {
                // %%FOR j in range(0, 24)             
                dest = 0;
                dest += (uint_mmv_t)(b[0] & p) << 0;
                dest += (uint_mmv_t)(b[1] & p) << 4;
                dest += (uint_mmv_t)(b[2] & p) << 8;
                dest += (uint_mmv_t)(b[3] & p) << 12;
                dest += (uint_mmv_t)(b[4] & p) << 16;
                dest += (uint_mmv_t)(b[5] & p) << 20;
                dest += (uint_mmv_t)(b[6] & p) << 24;
                dest += (uint_mmv_t)(b[7] & p) << 28;
                dest += (uint_mmv_t)(b[8] & p) << 32;
                dest += (uint_mmv_t)(b[9] & p) << 36;
                dest += (uint_mmv_t)(b[10] & p) << 40;
                dest += (uint_mmv_t)(b[11] & p) << 44;
                dest += (uint_mmv_t)(b[12] & p) << 48;
                dest += (uint_mmv_t)(b[13] & p) << 52;
                dest += (uint_mmv_t)(b[14] & p) << 56;
                dest += (uint_mmv_t)(b[15] & p) << 60;
                *mv++ = dest;                
                dest = 0;
                dest += (uint_mmv_t)(b[16] & p) << 0;
                dest += (uint_mmv_t)(b[17] & p) << 4;
                dest += (uint_mmv_t)(b[18] & p) << 8;
                dest += (uint_mmv_t)(b[19] & p) << 12;
                dest += (uint_mmv_t)(b[20] & p) << 16;
                dest += (uint_mmv_t)(b[21] & p) << 20;
                dest += (uint_mmv_t)(b[22] & p) << 24;
                dest += (uint_mmv_t)(b[23] & p) << 28;
                // %%END FOR                           
                *mv++ = dest;                
                b += 24;
            }
            break;
        case 3:
            while (len--) {
                // %%FOR j in range(0, 24)             
                dest = 0;
                dest += (uint_mmv_t)(b[0] & p) << 0;
                dest += (uint_mmv_t)(b[1] & p) << 8;
                dest += (uint_mmv_t)(b[2] & p) << 16;
                dest += (uint_mmv_t)(b[3] & p) << 24;
                dest += (uint_mmv_t)(b[4] & p) << 32;
                dest += (uint_mmv_t)(b[5] & p) << 40;
                dest += (uint_mmv_t)(b[6] & p) << 48;
                dest += (uint_mmv_t)(b[7] & p) << 56;
                *mv++ = dest;                
                dest = 0;
                dest += (uint_mmv_t)(b[8] & p) << 0;
                dest += (uint_mmv_t)(b[9] & p) << 8;
                dest += (uint_mmv_t)(b[10] & p) << 16;
                dest += (uint_mmv_t)(b[11] & p) << 24;
                dest += (uint_mmv_t)(b[12] & p) << 32;
                dest += (uint_mmv_t)(b[13] & p) << 40;
                dest += (uint_mmv_t)(b[14] & p) << 48;
                dest += (uint_mmv_t)(b[15] & p) << 56;
                *mv++ = dest;                
                dest = 0;
                dest += (uint_mmv_t)(b[16] & p) << 0;
                dest += (uint_mmv_t)(b[17] & p) << 8;
                dest += (uint_mmv_t)(b[18] & p) << 16;
                dest += (uint_mmv_t)(b[19] & p) << 24;
                dest += (uint_mmv_t)(b[20] & p) << 32;
                dest += (uint_mmv_t)(b[21] & p) << 40;
                dest += (uint_mmv_t)(b[22] & p) << 48;
                dest += (uint_mmv_t)(b[23] & p) << 56;
                // %%END FOR                           
                *mv++ = dest;                
                *mv++ = 0;
                b += 24;
            }
            break;
        // %%END FOR
    }

} 


/**
  @brief Read one entry from vector in internal representation

  The  function returns the entry with index ``i`` of the
  vector ``mv`` with modulus ``p``. The return value
  is reduced modulo ``p``.

  Here ``p`` must be a legal modulus.
*/
// %%EXPORT px
MM_BASICS_API
uint8_t mm_aux_get_mmv1(uint32_t p, uint_mmv_t *mv, uint32_t i)
{
    uint_fast32_t  c, j, res;

    // %%MMV_LOAD_CONST p, c
    // Store constant table for p to c
    c = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    j = ((c) & 7); // This is LOG_INT_FIELDS
    mv += i >> j;
    i &= (1 << j) - 1;
    j = 6 - j;           // This is LOG_FIELD_BITS
    res = (mv[0] >> (i << j)) & p;    // This is the result
    j = ((c >> 15) & 15);         // This is P_BITS
    // return result reduced modulo p
    return (uint8_t) ( (res + ((res + 1) >> j)) & p );
}


/**
  @brief Write one entry to a vector in internal representation

  The  function set the entry of the vector ``mv`` with modulus ``p``
  at the index ``i`` to the given value. ``0 <= value <= p``
  must hold.

  Caution:

  This is a low-level function. An illegal write operation might
  lead to an inconsistent vector ``mv``!

  Here ``p`` must be a legal modulus.
*/
// %%EXPORT px
MM_BASICS_API
void mm_aux_put_mmv1(uint32_t p, uint8_t value, uint_mmv_t *mv, uint32_t i)
// Set the entry of the vector mv with modulus p at the  index i  
// to the given value. 0 <= value <= p must hold.
{
    uint_fast32_t  j;

    // %%MMV_LOAD_CONST  p, j
    // Store constant table for p to j
    j = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    j = ((j) & 7); // This is LOG_INT_FIELDS
    mv += i >> j;
    i &= (1 << j) - 1;
    j = 6 - j;           // This is LOG_FIELD_BITS
    i <<= j;
    mv[0] &= ~(((uint_mmv_t)p) << i);
    mv[0] |= ((uint_mmv_t)(value & p)) << i;
}


/**********************************************************************
*** Functions for data transfer from and to vectors in R_p.
*** Here such a vector is given in internal representation and of type 
*** uint_mmv_t[]. For modulus p, p + 1 must be a power of two.
**********************************************************************/

/**
  @brief Return the size of a vector in internal representation

  The  function  return number of integers of type ``uint_mmv_t``
  required to store a vector with modulus ``p`` in internal
  representation.

  The functiion returns 0 if ``p`` is illegal modulus.
*/
// %%EXPORT px
MM_BASICS_API
uint32_t mm_aux_mmv_size(uint32_t p)
// Returns the number of integers of type uint_mmv_t required to store
// a vector of the representation R_p for a given p.
{
    uint_fast32_t tbl;
    if (mm_aux_bad_p(p)) return 0;
    // %%MMV_LOAD_CONST  p, tbl
    // Store constant table for p to tbl
    tbl = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    // return the value MMV_INTS for the specified p
    return(247488 >> ((tbl) & 7));
}


/**
  @brief Zero a vector in internal representation

  The  function sets all entries of the vector ``mv`` with 
  modulus ``p`` in internal  representation to zero.
*/
// %%EXPORT px
MM_BASICS_API
void mm_aux_zero_mmv(uint32_t p, uint_mmv_t *mv)
// Zero the vector of the representation R_p referred by mv,
{
    uint_fast32_t j;
    if (mm_aux_bad_p(p)) return;
    // %%MMV_LOAD_CONST  p, j
    // Store constant table for p to j
    j = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    j = (247488 >> ((j) & 7));
    do {
        *mv++ = 0;
    } while(--j);
}



/**
  @brief Read entry at index from vector in internal representation

  The  function returns the entry with index ``i`` of the
  vector ``mv`` with modulus ``p``. The return value is reduced 
  modulo ``p``. Index ``i`` must be given in external 
  representation. The function returns 0 in case  ``i >= 198884``.
*/
// %%EXPORT px
MM_BASICS_API
uint8_t mm_aux_get_mmv(uint32_t p, uint_mmv_t *mv, uint32_t i)
// Return the entry of the vector mv in R_p at  index  i.
{
    uint_fast32_t  j, c, res;
    if (mm_aux_bad_p(p)) return 0;
    if (i <  MM_AUX_XOFS_X) {
        if (i <  MM_AUX_XOFS_T) {
            // Tags A, B, C
            i = (MM_AUX_TBL_ABC[i] & 0x7ff) + i - 24;
        } else {
            // Tag T
            i += MM_AUX_OFS_T - MM_AUX_XOFS_T;
        } 
    } else {
        if (i >=  MM_AUX_XLEN_V) return 0;
        // Tags X, Z, Y
        i -=  MM_AUX_XOFS_X;
        // Put i += 8 * floor(i/24), for i <  3 * 2048 * 24
        i += (((i >> 3) * 0xaaab) >> 17) << 3; 
        i += MM_AUX_OFS_X;
    }

    // %%MMV_LOAD_CONST  p, c
    // Store constant table for p to c
    c = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    j = ((c) & 7); // This is LOG_INT_FIELDS
    mv += i >> j;
    i = (i & ((1 << j) - 1)) << (6 - j);
    res = (mv[0] >> i) & p;             // This is the result
    //Reduce reult modulo p
    c = ((c >> 15) & 15); // This is P_BITS
    return (uint8_t)((res + ((res + 1) >> c)) & p);
}










/**
  @brief Write entry to a vector at an index in internal representation

  The  function sets the entry of the vector ``mv`` with modulus ``p``
  at the index ``i`` to the given value. ``0 <= value <= p``
  must hold.

  Here the index ``i`` must be given in external representation.
  Writing at an index ``i >= 198884`` performs no action.
*/
// %%EXPORT px
MM_BASICS_API
void mm_aux_put_mmv(uint32_t p, uint8_t value, uint_mmv_t *mv, uint32_t i)
{

    uint_fast32_t  j, sh, diff;
    if (mm_aux_bad_p(p)) return;
    value &= p;

    // %%MMV_LOAD_CONST  p, j
    // Store constant table for p to j
    j = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    j = ((j) & 7); // This is LOG_INT_FIELDS

    if (i <  MM_AUX_XOFS_X) {
        if (i <  MM_AUX_XOFS_T) {
            // Tags A, B, C
            diff = 31 * (MM_AUX_TBL_ABC[i] >> 11);
            i = (MM_AUX_TBL_ABC[i] & 0x7ff) + i - 24;
            sh = (i & ((1 << j) - 1)) << (6 - j);
            mv[i >> j] = (mv[i >> j] &  ~(((uint_mmv_t)p) << sh))
                  |   ((uint_mmv_t)(value)) << sh;
            i -= diff;
        } else {
            // Tag T
            i += MM_AUX_OFS_T - MM_AUX_XOFS_T;
        } 
    } else {
        if (i >=  MM_AUX_XLEN_V) return;
        // Tags X, Z, Y
        i -=  MM_AUX_XOFS_X;
        // Put i += 8 * floor(i/24), for i <  3 * 2048 * 24
        i += (((i >> 3) * 0xaaab) >> 17) << 3; 
        i += MM_AUX_OFS_X;
    }

    mv += i >> j;
    sh = (i & ((1 << j) - 1)) << (6 - j);
    mv[0] = (mv[0] &  ~(((uint_mmv_t)p) << sh))
              |   ((uint_mmv_t)(value)) << sh;
}


/**
  @brief Randomize a vector in internal representation

  The function randomizes all entries of the vector ``mv`` with 
  modulus ``p`` in internal representation uniformly using the 
  internal random generator in file ``gen_random.c``. 
  Parameter ``seed`` must be a seed for a random generator as 
  described in file ``gen_random.c``.
*/
// %%EXPORT px
MM_BASICS_API
void mm_aux_random_mmv(uint32_t p, uint_mmv_t *mv, uint64_t *seed)
{
    uint8_t b1[3072];
    uint_fast32_t i, c;

    if (mm_aux_bad_p(p)) return;
    // %%MMV_LOAD_CONST p, c
    // Store constant table for p to c
    c = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    c = ((c) & 7); // This is LOG_INT_FIELDS

    // Do the small part
    gen_rng_bytes_modp(p,  (uint8_t *)(mv), 24 + 3 * 276, seed);
    mm_aux_small24_expand((uint8_t *)(mv), b1);
    mm_aux_write_mmv24(p, b1, mv, 72);
    mv += MM_AUX_OFS_T >> c;

    // Do the 759 * 64 vector; note that 759 = 11 * 69
    for (i = 0; i < 22; ++i) {
        gen_rng_bytes_modp(p, b1, 69 * 32, seed);
        mm_aux_write_mmv1(p, b1, mv, 69 * 32);
        mv += (69 * 32) >> c;
    } 

    // Do the 6144 * 24 vector
    for (i = 0; i < 48; ++i) {  
        gen_rng_bytes_modp(p, b1, 3072, seed);
        mm_aux_write_mmv24(p, b1, mv, 128);
        mv += 4096 >> c;
    } 
}


/**********************************************************************
*** Reducing and checking a vector in R_p
**********************************************************************/

/**
  @brief Reduce a vector in internal representation

  The function reduces all entries of the vector ``mv`` with 
  modulus ``p`` in internal representation to a standard form, so 
  that equal vectors are represented by equal arrays of integers.

  Note that a zero entry in such a vactor can be represented either 
  by the bit string  ``0...0`` or by ``1...1``. This functions sets 
  all zero entries of the vector to ``0...0``.

  The function returns 0 if it detects no error.
  It may return the following error codes:

  -1: Bad modulus ``p``

  -2: A one bit outside a valid bit field for an entry has been found
*/
// %%EXPORT px
MM_BASICS_API
int32_t mm_aux_reduce_mmv(uint32_t p, uint_mmv_t *mv)
{
    return mm_aux_reduce_mmv_fields(p, mv, MM_AUX_LEN_V);
}

/**
  @brief Auxiliary function of function ``mm_aux_reduce_mmv``

  The function performs the same operation as 
  function ``mm_aux_reduce_mmv``. But instead of all entries 
  of the vector ``mv``, it reduces the first ``len`` entries
  only.
*/
// %%EXPORT px
MM_BASICS_API
int32_t mm_aux_reduce_mmv_fields(uint32_t p, uint_mmv_t *mv, uint32_t nfields)
{
    uint_fast32_t i, sh;
    uint_mmv_t data, cy, mask_1, mask_p, acc;

    if (mm_aux_bad_p(p)) return -1;
    // %%MMV_LOAD_CONST  p, i
    // Store constant table for p to i
    i = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    sh = ((i >> 15) & 15);          // This is P_BITS
    i = ((i) & 7);   // This is LOG_INT_FIELDS
    i = nfields >> i;                     // No of unit_mmv_t to process
    mask_1 =  MM_AUX_TBL_REDUCE[2*sh-4];
    mask_p =  MM_AUX_TBL_REDUCE[2*sh-3];
    if (sh & (sh - 1)) {
        // case P_BITS is not a power of two
        acc = 0;      // use acc for accumulating error bits
        do {
            data = *mv;
            acc |= data;
            data &= mask_p;
            cy = (data + mask_1) & ~mask_p;
            data += (cy >> sh) - cy;
            *mv++ = data;
        } while (--i);
        if (acc & ~mask_p) return -2;
    } else {
        // case P_BITS is a power of two
        // use acc for  (<high half> & <low half>) of fields
        sh >>= 1;   // halved P_BITS
        do {
            data = *mv;
            acc = data & (data >> sh) & mask_p;
            cy = (acc + mask_1) & ~mask_p;
            data += (cy >> sh) - (cy << sh);
            *mv++ = data;
        } while (--i);
    }
    return 0;
}



/// @cond DO_NOT_DOCUMENT 

static int32_t check24(uint32_t p, uint_mmv_t *mv, uint32_t length)
{
    uint_fast32_t d;
    uint_mmv_t  acc = 0, mask;

    // %%MMV_LOAD_CONST  p, d
    // Store constant table for p to d
    d = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    // Put d =  5 - LOG_INT_FIELDS
    d = 5 - ((d) & 7); 
    switch (d) {
        // %%IF %{INT_BITS} == 64
        case 0:
            mask = 0xffff000000000000ULL;
            while (length--) acc |= *mv++ & mask;
            break;
        // %%END IF
        case 1:
            mask = 0xffffffff00000000ULL;
            while (length--) {
                acc |= mv[1] & mask; mv += 2;
            }
            break;
        case 2:
            while (length--) {
                acc |= mv[3]; mv += 4;
            }
            break;
        // %%IF %{INT_BITS} == 32
        // %%END IF
        break;
    }
    return acc ? -3 : 0;
}


static int32_t check_sym(uint32_t p, uint_mmv_t *mv, uint8_t * buffer)
// buffer is a work buffer of size at least 72 * 32
// Side effect: Tmv entries with tags A, B, C are read to the buffer
{
    uint_fast32_t i, acc = 0;
    uint8_t  *p_row, *p_col;
    mm_aux_read_direct_mmv1(p, mv, buffer, 72*32);
    for(i = 768; i < 1536; i += 33)  
        acc |= buffer[i] | buffer[i + 768];
    if (acc) return -4;
    p_row = buffer;
    acc = 0;
    for (p_col = buffer; p_col < buffer + 24; ++p_col) {
         for (i = 0; i < 24; ++i)
             acc |= (p_row[i] ^ p_col[i << 5]) 
                  | (p_row[i + 768] ^ p_col[(i << 5) + 768])
                  | (p_row[i + 1536] ^ p_col[(i << 5) + 1536]);
         p_row+= 32;
    }
    return acc ? -5 : 0;
}



static int32_t check_mmv_buffer(uint32_t p, uint_mmv_t *mv, uint8_t * buffer)
// Workhorse for function mm_aux_check_mmv. buffer must have size 72*32.
// Side effect: mv entries with tags A, B, C are read to the buffer
{
    uint_fast32_t i;
    i = mm_aux_reduce_mmv(p, mv);
    if (i) return i;                 // Errors -1, -2 may occur here
    i = check24(p, mv, 72);          // check tags A,B,C
    if (i) return i;                 // Error -3 may occur here
    // %%MMV_LOAD_CONST  p, i
    // Store constant table for p to i
    i = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    i = ((i) & 7); //  LOG_INT_FIELDS
    i = check24(p, mv + (MM_AUX_OFS_X >> i), 6144); // check tags X,Y,Z
    if (i) return i - 100;                 // Error -3 may occur here
    return check_sym(p, mv, buffer); // Errors -4, -5 may occur here
}

/// @endcond


/**
  @brief Check a vector in internal representation for errors

  The function checks all entries of the vector ``mv`` with 
  modulus ``p`` in internal representation for errors. It returns 0 
  if it detects no error. It may return the following error codes:

  -1: Bad modulus ``p``

  -2: A one bit outside a valid bit field for an entry has been found

  -3: A subfield of 24 entries has an illegal nonzero entry at index >= 24

  -4: The vector has an illegal nonzero diagonal entry 

  -5: The symmetric part of the vector is not actually symmetric 

As a side effect, ``mv`` is reduced with function ``mm_aux_reduce_mmv``.
*/
// %%EXPORT px
MM_BASICS_API
int32_t mm_aux_check_mmv(uint32_t p, uint_mmv_t *mv)
{
    uint8_t buffer[72*32];
    return check_mmv_buffer(p, mv, buffer);
}

/**********************************************************************
*** Low-level functions supperting external rep of vectors in R_p
**********************************************************************/

/** 
  @brief Convert part of vector from external to internal representation

  Conversion between the internal and the external representation 
  of a vector is straightforward, except for entries with
  tags ``A, B, C``. The entries with these tags are stored in the 
  first 852 entries of the external representation. In the internal
  representation the entries with these tags are spread over three
  symmetric 24 times 24 times matrices. 
 
  This function maps the 852 entries of the array ``b_src`` 
  (corresponding to tags ``A, B, C``) to the array ``b_dest`` of
  size 3 * 24 * 24 (corrsponding to three
  symmetric 24 times 24 times matrices). 
  Function ``mm_aux_write_mmv24`` can be used to write the data
  from the array ``b_dest`` to the initial segment of the internal
  representation of a vector.
  
*/
// %%EXPORT px
MM_BASICS_API
void mm_aux_small24_expand(uint8_t *b_src, uint8_t *b_dest)
//
{
    uint_fast16_t j0, j1t, j1e;
    uint8_t *b_transpose = b_dest;
    for (j0 = 0; j0 < 24 * 25; j0 += 25) {
        b_dest[j0] = *b_src++;
        b_dest[j0 + 1152] =  b_dest[j0 + 576] = 0;
    }

    for (j0 = 0; j0 < 24; ++j0)  {
        j1e = 24 * j0;
        for (j1t = 0; j1t < j1e; j1t += 24) {
            b_transpose[j1t] = b_dest[0] = b_src[0];
            b_transpose[j1t + 576] = b_dest[576] = b_src[276];
            b_transpose[j1t + 1152] = b_dest[1152] = b_src[552];
            ++b_dest; ++b_src;
        }
        b_dest += 24 - j0;
        ++b_transpose;
    }
}

/** 
  @brief Convert part of vector from internal to external representation

  Conversion between the internal and the external representation 
  of a vector is straightforward, except for entries with
  tags ``A, B, C``. The entries with these tags are stored in the 
  first 852 entries of the external representation. In the internal
  representation the entries with these tags are spread over three
  symmetric 24 times 24 times matrices. 
 
  This function maps the 3 * 24 * 24 entries of the array ``b_src``
  (corrsponding to three symmetric 24 times 24 times matrices)
  to the  852 entries of the array ``b_dest``  (corresponding to 
  tags ``A, B, C`` in external representation).

  This reverses the effect of function ``mm_aux_small24_expand``.
  Function ``mm_aux_read_mmv24`` can be used to read the data
  from the initial segment of the internal representation of a 
  vector to the array ``b_src``, before calling this function. 
*/
// %%EXPORT px
MM_BASICS_API
void mm_aux_small24_compress(uint8_t *b_src, uint8_t *b_dest)
//
{
    uint_fast16_t  j0, j1;
    for (j0 = 0; j0 < 24 * 25; j0 += 25) 
        *b_dest++ = b_src[j0];
    for (j0 = 0; j0 < 24; ++j0)  {
        for (j1 = j0; j1; --j1) {
            b_dest[0] = b_src[0];
            b_dest[276] = b_src[576];
            b_dest[552] = b_src[1152];
            ++b_dest; ++b_src;
        } 
        b_src += 24 - j0;
    }
}






/**********************************************************************
*** Conversion between internal and external rep of vectors in R_p
**********************************************************************/







/**
  @brief Convert vector from internal to external representation

  Read all entries of vector ``mv`` (stored in internal
  representation with modulus ``p``) and store these entries 
  in the array ``b`` in external representation.

  Output vector ``b`` is reduced modulo ``p``. It must have 
  length 196884.
*/
// %%EXPORT px
MM_BASICS_API
void mm_aux_mmv_to_bytes(uint32_t p, uint_mmv_t *mv, uint8_t *b)
{
    uint8_t b1[3*576]; 
    uint_fast32_t c;

    if (mm_aux_bad_p(p)) return;
    // %%MMV_LOAD_CONST  p, c
    // Store constant table for p to c
    c = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    c = ((c) & 7); // This is LOG_INT_FIELDS
    
    mm_aux_read_mmv24(p, mv, b1, 72);
    mm_aux_small24_compress(b1, b);
    mv += MM_AUX_OFS_T >> c;
    b +=  MM_AUX_XOFS_T;
    mm_aux_read_mmv1(p, mv, b,  759*64);
    mv += (MM_AUX_OFS_X - MM_AUX_OFS_T) >> c;
    b +=  (MM_AUX_XOFS_X - MM_AUX_XOFS_T);
    mm_aux_read_mmv24(p, mv, b, 6144);
}


/**
  @brief Convert vector from external to internal representation

  Read all entries of the array ```b`` (of length 196884, containing 
  a vector in external representation) and store these entries the 
  vector ``mv``. Here ``mv`` is a vector stored in internal
  representation with modulus ``p``. 

  Any entry ``x`` in the array ``b`` must satisfy ``0 <= x <= p``.
  The vector ``mv`` is an array of ``n`` integers of type
  ``uint_mmv_t`` with ``n =  mm_aux_mmv_size(p)``.
*/
// %%EXPORT px
MM_BASICS_API
void mm_aux_bytes_to_mmv(uint32_t p, uint8_t *b, uint_mmv_t *mv)
{
    uint8_t b1[3*576];
    uint_fast32_t  c;

    if (mm_aux_bad_p(p)) return;
    // %%MMV_LOAD_CONST  p, c
    // Store constant table for p to c
    c = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    c = ((c) & 7); // This is LOG_INT_FIELDS

    mm_aux_small24_expand(b, b1);   
    mm_aux_write_mmv24(p, b1, mv, 72);
    mv += MM_AUX_OFS_T >> c;
    b +=  MM_AUX_XOFS_T;
    mm_aux_write_mmv1(p, b, mv, 759*64);
    mv += (MM_AUX_OFS_X - MM_AUX_OFS_T) >> c;
    b +=  (MM_AUX_XOFS_X - MM_AUX_XOFS_T);
    mm_aux_write_mmv24(p, b, mv, 6144);
}




/**********************************************************************
*** Conversion between internal and sparse rep of vectors in R_p
**********************************************************************/

/**
  @brief Convert vector from internal to sparse representation

  Read all entries of vector ``mv`` (stored in internal
  representation with modulus ``p``) and store these entries
  in the array ``sp`` in sparse representation. Each entry
  in the array ``sp`` represents a nonzero entry of the vector.
  The function returns the length of the output array ``sp``
  or an negative value in case of error. Negative return
  values are as in function ``check_mmv_buffer``.

  Output vector ``sp`` is reduced modulo ``p``. The buffer for
  array ``sp`` must have length 196884. Input vector ``mv``
  is checked with function ``check_mmv_buffer``.
*/
// %%EXPORT px
MM_BASICS_API
int32_t mm_aux_mmv_to_sparse(uint32_t p, uint_mmv_t *mv, uint32_t *sp)
{
    int32_t status;
    uint_fast32_t row, row_end,i, j, isp = 0, value;
    uint_fast32_t field_bits, lg_int_fields, ofs, sh;
    uint_mmv_t source;
    uint8_t b[72*32], *p_row;

    if ((status = check_mmv_buffer(p, mv, b)) != 0) return status;
    
    // %%MMV_LOAD_CONST  p, j
    // Store constant table for p to j
    j = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    field_bits = ((j >> 11) & 15); // This is FIELD_BITS
    lg_int_fields = ((j) & 7); // This is LOG_INT_FIELDS
    sh = 8 - 6 + lg_int_fields; // This is 8 - LOG_FIELD_BITS; 
 
    // Do tags A, B, C
    p_row = b;
    for (row = 0; row < 3; ++row) for (i = 0; i < 24; ++i) {
         for (j = 0; j <= i; ++j) {
            if ((value = p_row[j]) != 0)  sp[isp++] =
                0x2000000 + (row << 25) + (i << 14) + (j << 8) + value; 
        } 
        p_row += 32;
    }
    
    // Do tag T
    mv += MM_AUX_OFS_T >> lg_int_fields;
    row_end = (MM_AUX_OFS_X - MM_AUX_OFS_T) >> lg_int_fields;
    for (row = 0; row < row_end; ++row) if ((source = *mv++) != 0) {
        ofs = 0x8000000 + (row << (8 + lg_int_fields));
        for (j = 0; j < 64; j += field_bits) {
            if ((value = (source >> j) & p) != 0)  {
                sp[isp++] = ofs + (j << sh) + value;
            } 
        }           
    }

    row_end = (MM_AUX_LEN_V - MM_AUX_OFS_X) >> lg_int_fields;
    for (row = 0; row < row_end; ++row) if ((source = *mv++) != 0) {
        ofs = 0x5000000 + (row << (8 + lg_int_fields));
        ofs += ofs & 0xfffe000;
        for (j = 0; j < 64; j += field_bits) {
            if ((value = (source >> j) & p) != 0)  {
                 sp[isp++] = ofs + (j << sh) + value;
            } 
        }           
    }

    return (int32_t)isp; 
}

/**
  @brief Extract entries from a vector in internal representation

  The function extracts certain entries from the vector ``mv`` 
  depending on the vector ``sp``. Here ``mv`` is a vector stored 
  in internal representation with modulus ``p``.  Vector ``sp``
  is a vector of length ``length`` in sparse representation.

  The entries of vector ``sp`` are updated with the corresponding 
  entries of ``mv``. If ``sp`` has an entry with a certain label
  then the coordinate of that entry is set to the corresponding 
  coordinate of vector ``mv``. If several entries of ``sp`` have the 
  same label then the same coordinate is taken from ``mv`` 
  several times.

  Bit 7,...,0 of any entry of ``sp`` should be either 0 or p. If that
  value is 0 then the coordinate is read to bits 7,...,0 of that entry. 
  If that entry is ``p`` then the negative coordinate is read instead. 
  Other values of these bits are strongly discouraged; but technically 
  we XOR the corresponding coordinate of vector ``mv`` to these bits; 
  and we then change a result ``p`` to zero. There is a special case 
  where this detail is relevant.   
*/
// %%EXPORT px
MM_BASICS_API
void mm_aux_mmv_extract_sparse(uint32_t p, uint_mmv_t *mv, uint32_t *sp, uint32_t length)
{
    uint_fast32_t i0, lg_int_fields, lg_field_bits, p_bits, index_mask;

    if (mm_aux_bad_p(p)) return;
    // %%MMV_LOAD_CONST  p, i0
    // Store constant table for p to i0
    i0 = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    p_bits = ((i0 >> 15) & 15); // This is P_BITS
    lg_field_bits = ((i0 >> 9) & 3); // This is LOG_FIELD_BITS
    lg_int_fields = ((i0) & 7); // This is LOG_INT_FIELDS
    index_mask = (1 << lg_int_fields) - 1;

    for ( ;length--; ++sp) {
        uint_fast32_t v = *sp, index;
        uint_fast32_t tag = v >> 25,i = (v >> 14) & 0x7ff, j = (v >> 8) & 0x3f;
        switch (tag) {
            case 2:  // tag B
            case 3:  // tag C
                if (i == j) continue;
                // Fall trough to case tag A
            case 1:  // tag A
                if (i >= 24 || j >= 24) continue;
                index = (tag - 1) * 768  + (i << 5) + j;
                break;
            case 4:  // tag T
                if (i >= 759) continue;
                index = MM_AUX_OFS_T + (i << 6) + j;
                break;
            case 5:  // tag X
            case 6:  // tag Z
            case 7:  // tag Y
                if (j >= 24) continue;
                index = ((v >> 14) << 5) + j - 0x50000 + MM_AUX_OFS_X;
                break;
            default:
                continue;
        }
        i = ((index) & index_mask) << lg_field_bits; 
        i = ((mv[index >> lg_int_fields] >> i) ^ v) & p; 
        // i is the (possibly negated) entry of vector mv. reduce i mod p.
        i = (i + ((i + 1) >> p_bits)) & p;
        *sp = (v & 0xffffff00) + i; 
    }
}


/**
  @brief Extract one entry of a vector in internal representation

  The statement ``uint32_t sp1 = mm_aux_mmv_get_sparse(p, mv, sp);`` 
  is equivalent to

        uint32_t sp1 = sp; mm_aux_mmv_extract_sparse(p, mv, &sp1, 1);
      
*/
// %%EXPORT px
MM_BASICS_API
uint32_t mm_aux_mmv_get_sparse(uint32_t p, uint_mmv_t *mv, uint32_t sp)
{
     mm_aux_mmv_extract_sparse(p, mv, &sp, 1);
     return sp;
}


/// @cond DO_NOT_DOCUMENT 

#define add_sparse_value(index, value) \
    { \
        uint_fast32_t idx = (index) >> lg_int_fields; \
        uint_fast32_t sh = ((index) & index_mask) << lg_field_bits; \
        uint_mmv_t old_value = (mv[idx] >> sh)  & p; \
        uint_mmv_t new_value = old_value + (value & p); \
        new_value = (new_value + (new_value >> p_bits)) & p; \
        mv[idx]  ^=  (old_value ^ new_value) << sh; \
    }
 
/// @endcond 

       

/**
  @brief Add vector in sparse rep to vector in internal representation

  The function adds a vector ``sp`` in sparse representation to a
  vector ``mv`` in internal representation with modulus ``p``. 
  Vector ``sp`` has length ``length``, and each value ``x`` in an 
  entry of vector ``sp`` must satisfy ``0 <= x <= p``. Different 
  entries in ``sp`` with the same index are added up.
*/
// %%EXPORT px
MM_BASICS_API
void mm_aux_mmv_add_sparse(uint32_t p, uint32_t *sp, uint32_t length, uint_mmv_t *mv)
{
    uint_fast32_t i0, lg_int_fields, lg_field_bits, p_bits, index_mask;

    if (mm_aux_bad_p(p)) return;
    // %%MMV_LOAD_CONST  p, i0
    // Store constant table for p to i0
    i0 = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    lg_field_bits = ((i0 >> 9) & 3); // This is LOG_FIELD_BITS
    lg_int_fields = ((i0) & 7); // This is LOG_INT_FIELDS
    p_bits = ((i0 >> 15) & 15);               // This is P_BITS
    index_mask = (1 << lg_int_fields) - 1;

    for ( ;length--; ++sp) {
        uint_fast32_t v = *sp, index;
        uint_fast32_t tag = v >> 25,i = (v >> 14) & 0x7ff, j = (v >> 8) & 0x3f;
        switch (tag) {
            case 2:  // tag B
            case 3:  // tag C
                if (i == j) continue;
                // Fall trough to case tag A
            case 1:  // tag A
                if (i >= 24 || j >= 24) continue;
                index = (tag - 1) * 768 + (i << 5) + j;
                if (i != j) add_sparse_value(index, v);
                index += 31 * (j - i);
                break;
            case 4:  // tag T
                if (i >= 759) continue;
                index = MM_AUX_OFS_T + (i << 6) + j;
                break;
            case 5:  // tag X
            case 6:  // tag Z
            case 7:  // tag Y
                if (j >= 24) continue;
                index = ((v >> 14) << 5) + j - 0x50000 + MM_AUX_OFS_X;
                break;
            default:
                continue;
        }
        add_sparse_value(index, v);
    }
}



    
/// @cond DO_NOT_DOCUMENT 

#define set_sparse_value(index, v) \
    { \
        uint_fast32_t idx = (index) >> lg_int_fields; \
        uint_fast32_t sh = ((index) & index_mask) << lg_field_bits; \
        uint_mmv_t value = ((mv[idx] >> sh)  ^ v) & p; \
        mv[idx]  ^= value << sh; \
    }

/// @endcond  


/**
  @brief Set certain entries of a vector in internal representation

  The function sets certain entries of the vector ``mv `` depending on 
  the vector ``sp ``. Vector ``mv`` is given in internal representation 
  with modulus ``p``.  Vector ``sp`` is given in sparse representation 
  and has length ``length``. 

  If  ``sp `` has an entry with a certain label then the corresponding 
  entry of ``mv `` is set to to the value coded in that entry of ``sp ``.
  Each of these values ``x`` must  satisfy ``0 <= x <= p``. 
  Duplicate entries in ``sp `` with the same label and different values
  are illegal; in that case the value of ``mv `` is undefined.
*/
// %%EXPORT px
MM_BASICS_API
void mm_aux_mmv_set_sparse(uint32_t p, uint_mmv_t *mv, uint32_t *sp, uint32_t length)
// Set certain entries of the vector   ``mv `` depending on the vector
//  ``sp ``. Here  ``mv `` in and  ``sp `` are vectors in the representation R_p 
// of the monster, with  ``mv `` given in internal representation and 
//  ``sp `` given in sparse format.  ``sp `` has  length  ``length ``.
// If  ``sp `` has an entry with label  ``l `` then the corresponding entry 
// of  ``mv `` is set to to the value coded in the entry of  ``sp ``.
{
    uint_fast32_t i0, lg_int_fields, lg_field_bits, index_mask;

    if (mm_aux_bad_p(p)) return;
    // %%MMV_LOAD_CONST  p, i0
    // Store constant table for p to i0
    i0 = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    lg_field_bits = ((i0 >> 9) & 3); // This is LOG_FIELD_BITS
    lg_int_fields = ((i0) & 7); // This is LOG_INT_FIELDS
    index_mask = (1 << lg_int_fields) - 1;

    for ( ;length--; ++sp) {
        uint_fast32_t v = *sp, index;
        uint_fast32_t tag = v >> 25, i = (v >> 14) & 0x7ff, j = (v >> 8) & 0x3f;
        switch (tag) {
            case 2:  // tag B
            case 3:  // tag C
                if (i == j) continue;
                // Fall trough to case tag A
            case 1:  // tag A
                if (i >= 24 || j >= 24) continue;
                index = (tag - 1) * 768 + (i << 5) + j;
                set_sparse_value(index, v);
                index += 31 * (j - i);
                break;
            case 4:  // tag T
                if (i >= 759) continue;
                index = MM_AUX_OFS_T + (i << 6) + j;
                break;
            case 5:  // tag X
            case 6:  // tag Z
            case 7:  // tag Y
                if (j >= 24) continue;
                index = ((v >> 14) << 5) + j - 0x50000 + MM_AUX_OFS_X;
                break;
            default:
                continue;
        }
        set_sparse_value(index, v);
    }
}



/**
  @brief Extract signs of a vector in internal representation

  The function extracts the signs of certain entries of the
  vector ``mv`` depending on the vector ``sp ``. Vector ``mv`` is 
  given in internal representation  with modulus ``p``.  Vector ``sp`` 
  is given in sparse representation  and has length ``n``. 

  Entry ``sp[i]`` specifies a multiple ``c[i] * u[i]`` of a unit 
  vector ``u[i]``. Let ``m[i]`` be the coordinate of
  vector ``mv`` with respect to the unit vector ``u[i]``. We
  put ``s[i] = 0`` if ``m[i] = c[i]`` and ``s[i] = 1`` 
  if ``m[i] = -c[i]``. In all other cases we assign a random
  value 0 or 1 to ``s[i]``. Then the function returns the sum of
  the values ``s[i] << i``, where ``i`` ranges from ``0``
  to ``n - 1``.
*/
// %%EXPORT px
MM_BASICS_API
int32_t mm_aux_mmv_extract_sparse_signs(uint32_t p, uint_mmv_t *mv, uint32_t *sp, uint32_t n)
{
    uint_fast32_t i, v1 = 0, t;
    uint32_t sp1[32];

    if (mm_aux_bad_p(p)) return -1L;
    if (n > 31) return -1L;
    for (i = 0; i < n; ++i) sp1[i] = sp[i] & 0xffffff00UL;
    mm_aux_mmv_extract_sparse(p, mv, sp1, n);
    for (i = 0; i < n; ++i) {
        if ((sp1[i] & p) == 0) return -1L;
        t = (sp[i] ^ sp1[i]) & p;
        if ((t != 0) && (t != p)) return -1L;
        v1 |= (t & 1) << i;
    }
    return (int32_t)v1;
}




/**
  @brief Extract some bits of a vector in internal representation

  The function extracts the least significant bits of certain entries
  of the vector ``mv`` depending on the vector ``a``. Vector ``mv`` is
  given in internal representation  of the Monster with modulus ``p``.
 
  Vector ``a`` is a an array of ``n`` elements of the group ``Q_x0``
  of structure \f$2^{1+24}\f$, with each element given
  in **Leech lattice encoding**. Here each element of ``Q_x0`` must
  correspond to a Leech lattice vector of type 2; otherwise the
  function fails.

  The array ``elem`` represents an element of the group ``G_x0`` of
  stucture \f$2^{1+24}.\mbox{Co}_1\f$, given in **G_x0 representation**.
  Internally, the function transforms (i.e. conjugates) all elements
  of ``Q_x0`` in the array ``a`` with the element ``elem``, i.e. it
  calculates the element ``a'[i] = elem^-1 * a[i] * elem`` of ``Q_x0``.
  Then it extracts the least significant bit ``b[i]`` of the entry of
  the vector ``mv`` with the coordinate labelled by ``a'[i]``.

  Note theat negating ``a'[i]`` corresponds to negating the coordinate
  with label ``a'[i]`` in the vector ``mv``. Hence when
  negating ``a'[i]`` we also have to flip the bit ``b[i]``.
  The function fails in case ``a'[i] = 0``.

  The function returns the sum of the values ``b[i] << i``,
  where ``i`` ranges from ``0`` to ``n - 1``. The function also fails
  in case ``i > 31``. It returns a negative value in case of failure.

  Assume that a vector ``mv' = mv * q * g`` is given with a known
  vector ``mv``, a  known ``g`` in ``G_x0``, and an unknown ``q``
  in ``Q_x0``. Then the  main use case of this function  is to
  find the element ``q`` (up to sign)  without modifying ``mv'``.
*/
// %%EXPORT px
MM_BASICS_API
int32_t mm_aux_mmv_extract_x_signs(uint32_t p, uint_mmv_t *mv, uint64_t *elem, uint32_t *a, uint32_t n)
{
    uint_fast32_t i, v1 = 0, b;
    uint32_t sp1[32];
    uint64_t ax[32];
    int32_t res;

    if (mm_aux_bad_p(p)) return -10001L;
    if (n > 31) return -10002L;
    for (i = 0; i < n; ++i) ax[i] = a[i];
    res = xsp2co1_xspecial_conjugate(elem, n, ax, 1);
    if (res < 0) return res;
    for (i = 0; i < n; ++i) {
        res = mm_aux_index_leech2_to_sparse((uint32_t)ax[i]);
        if (res == 0) return -10003L;
        sp1[i] = res & 0xffffff00;
    }
    mm_aux_mmv_extract_sparse(p, mv, sp1, n);
    for (i = 0; i < n; ++i) {
        if ((sp1[i] & p) == 0) return -10004L;
        b =  (sp1[i] ^ (uint_fast32_t)(ax[i] >> 24)) & 1;
        v1 |= b << i;
    }
    return (int32_t)v1;
}




/**********************************************************************
*** Operation on a sparse rep of a vector in R_p
**********************************************************************/

/**
  @brief Scalar multiplication and modular reduction in sparse representation

  The function multiplies a vector ``sp`` in sparse representation 
  with a factor ``f`` and reduces the result modulo a number ``p1``.
  
  The vector ``sp`` has length ``length`` and is stored in sparse
  representation as a vector modulo an odd number ``2 < p < 256``.
  The result is reduced modulo the number ``p1`` and stored in 
  sparse representation in the array ``sp1``.
  
  The number ``p1`` must be odd and satisfy ``2 < p < 256``. In case 
  ``f != 0`` the number ``p1`` must divide  ``p * abs(f)``.
  
  The function returns the length of the array ``sp1`` in case of 
  success and ``-1`` in case of failure. 
  
  The two arrays ``sp`` and ``sp1`` may be non overlapping or equal.
  
*/
// %%EXPORT px
MM_BASICS_API
int32_t mm_aux_mul_sparse(uint32_t p, uint32_t *sp, uint32_t length, int64_t f, uint32_t p1, uint32_t *sp1)
{
    uint8_t a[256], bad[256];
    uint_fast32_t mask = 4, i, is_bad = 0, difficult;
    
    if (p < 3 ||  p > 255 || (p & 1) == 0 ||
       p1 < 3 || p1 > 255 || (p1 & 1) == 0) return -1;
        
    f = f % (int64_t)p1;
    while (f < 0) f += p1;
    difficult = (f * p) % p1 != 0;

    if (f == 0) {
        mask = 0xffffff00;
        for (i = 0; i < length; ++i) sp1[i] = sp[i] & mask;
        return 0;
    }
    while (mask < p) mask += mask;
    if (mask > 256) return -1;
    --mask;
    if (p == p1 && f == 1) {
        mask |= 0xffffff00;
        for (i = 0; i < length; ++i) sp1[i] = sp[i] & mask;
        return length;
    }
    for (i = 0; i <= mask; ++i) a[i] = (uint8_t)((i * f) % p1);
    if (!difficult) {
        for (i = 0; i < length; ++i) {
            sp1[i] = (sp[i] & 0xffffff00) | a[sp[i] & mask]; 
        }
    } else {
        for (i = 0; i <= mask; ++i) {
            bad[i] = (uint8_t)((i * f * p) % p1);
        }
        for (i = 0; i < length; ++i) {
            sp1[i] = (sp[i] & 0xffffff00) | a[sp[i] & mask]; 
            is_bad |= bad[sp[i] & mask]; 
        }
    } 
    return is_bad ? -1 : length;
}

/**********************************************************************
*** Index conversion between external and sparse rep of vectors in R_p
**********************************************************************/


/**
  @brief Convert an index from external to sparse representation

  The function converts an index ``i`` for the external representation 
  of a vector to an index for the sparse representation of a vector
  and returns the converted index. The function returns 0 in case
  ``i >= 196884```. 

  Indices for the sparse representation are defined as 
  in ``enum MM_SPACE_TAG`` in file ``mm_basics.h``.
*/
// %%EXPORT px
MM_BASICS_API
uint32_t mm_aux_index_extern_to_sparse(uint32_t i)
// Convert external index i to sparse index.
// Return 0 if index i is bad
{
    if (i <  MM_AUX_XOFS_X) {
        if (i <  MM_AUX_XOFS_T) {
            // Tags A, B, C
            i = (MM_AUX_TBL_ABC[i] & 0x7ff) + i - 24;
            // put i += (i / 0x300) * 0x100; assuming 0 <= i < 0x900 
            i += (0x2A54000 >> ((i >> 8) << 1)) & 0x300;
            // now 0 <= i < 0xc00. output bits of old i as 
            // (tag - 1) = bits 11..10, i = bits 9..5, j = bits 4..0
            return 0x2000000 + ((i & 0xc00) << 15) +
                   ((i & 0x3e0) << 9) + ((i & 0x1f) << 8);
        } else {
            // Tag T
            i += 0x80000 - MM_AUX_XOFS_T;
            return i << 8;
        } 
    } else if (i <  MM_AUX_XLEN_V) {
        // Tags X, Z, Y
        i -=  MM_AUX_XOFS_X;
        // Put i += 8 * floor(i/24), for i <  3 * 2048 * 24
        i += (((i >> 3) * 0xaaab) >> 17) << 3; 
        // shift bits 17..5 of i to bit positions 18...6
        i += i & 0x3ffe0;
        i += 0xA0000;
        return i << 8;
    } else return 0;
}


/**
  @brief Convert index array from external to sparse representation

  The function converts an array ``a`` of indices for the external 
  representation to an array of indices for the sparse representation 
  of a vector. All indices in the array ``a`` of length ``len`` are
  converted in place, using function ``mm_aux_index_extern_to_sparse``.
*/
// %%EXPORT px
MM_BASICS_API
void mm_aux_array_extern_to_sparse(uint32_t *a, uint32_t len)
{
    for(; len--; ++a) *a = mm_aux_index_extern_to_sparse(*a); 
}


/**
  @brief Convert an index from sparse to external representation

  The function converts an index ``i`` for the sparse representation 
  of a vector to an index for the external representation of a vector
  and returns the converted index. The function returns -1 if the
  input ``i`` denots an illegal index. The coordinate value encoded
  in the input ``i`` is ignored.
 
  Indices for the sparse representation are defined as 
  in ``enum MM_SPACE_TAG`` in file ``mm_basics.h``.
*/
// %%EXPORT px
MM_BASICS_API
int32_t mm_aux_index_sparse_to_extern(uint32_t i)
{
    uint_fast32_t tag = i >> 25, j = (i >> 8) & 0x3f;
    i = (i >> 14) & 0x7ff;
    switch (tag) {
        case 2:  // tag B
        case 3:  // tag C
            if (i == j) return -1;
            // Fall trough to case tag A
        case 1:  // tag A
            if (i >= 24 || j >= 24) return -1;
            if (i == j) return i;
            return  MM_AUX_XOFS_A - 276 + tag * 276 
                  + ((i * i - i) >> 1) + j;
        case 4:  // tag T
            if (i >= 759) return -1;
            return MM_AUX_XOFS_T + (i << 6) + j;
        case 5:  // tag X
        case 6:  // tag Z
        case 7:  // tag Y
            if (j >= 24) return -1;
            return  MM_AUX_XOFS_X - 0x3c000
                + 24 * ((tag << 11) + i) + j; 
        default:
            return -1;
    }
}

/**
  @brief Convert sparse index to a short vector in the Leech lattice

  The function converts an index ``i`` for the sparse representation
  of a vector to a vector ``v`` in the Leech lattice. This conversion 
  is successful if ``i`` denotes a legal index for one of the tags
  tags ``B, C, T, X``. Then the function computes a short Leech 
  lattice vector  (scaled to norm 32)  in the array ``v``. 
  Output ``v`` is determined up to sign only; that sign is 
  implementation dependent.

  The function returns 0 in case of a successful conversion and -1
  in case of failure.
*/
// %%EXPORT px
MM_BASICS_API
int32_t mm_aux_index_sparse_to_leech(uint32_t i, int32_t *v)
// Convert sparse index i to a short vector v in the Leech lattice.
// Vector v has norm 32. The sign of v is implementation dependent.
// Return -1 if index i is bad or does not map to a short vector
{
    uint_fast32_t tag = i >> 25, j = (i >> 8) & 0x3f, k, w, u_sub;
    i = (i >> 14) & 0x7ff;
    switch (tag) {
        case 2:  // tag B
        case 3:  // tag C
            if (i == j || i >= 24 || j >= 24) return -1;
            for (k = 0; k < 24; ++k) v[k] = 0;
            v[i] = v[j] = 4;
            if (i < j) i = j;
            if ((tag & 1) == 0) v[i] = -4;
            return 0;
        case 4:  // tag T
            if (i >= 759) return -1;
            w = mat24_octad_to_vect(i);
            // Put k = parity of j
            k = (0x96 >> ((j ^ (j >> 3)) & 7)) & 1;  
            // Let u_sub be a vector representing suboctad j of w 
            j = k + (j << 1);  // even-parity adjusted j
            u_sub = mat24_spread_b24(j, w);
            for (k = 0; k < 24; ++k) v[k] = 
                 2 * ((w >> k) & 1) - 4 * ((u_sub >> k) & 1);
            return 0;
        case 5:  // tag X
            if (j >= 24) return -1;
            w = mat24_gcode_to_vect(i);
            for (k = 0; k < 24; ++k) v[k] = 1 - 2 * ((w >> k) & 1);
            v[j] = v[j] < 0 ? 3 : -3;
            return  0; 
        default:
            return -1;
    }
}


/**
  @brief Convert sparse index to a short vector in the Leech lattice mod 2

  The function converts an index ``i`` for the sparse representation
  of a vector to a vector ``v`` in the Leech lattice mod 2. This 
  conversion  is successful if ``i`` denotes a legal index for one of 
  the tags tags ``B, C, T, X``. The function returns a short Leech 
  lattice vector modulo 2, encoded in **Leech lattice encoding**, as
  descrbed in 
  section **Description of the mmgroup.generators extension**. 

  The function returns 0 in case of failure.
*/
// %%EXPORT px
MM_BASICS_API
uint32_t mm_aux_index_sparse_to_leech2(uint32_t i)
{
    uint_fast32_t tag = i >> 25, j = (i >> 8) & 0x3f,  res = 0;
    i = (i >> 14) & 0x7ff;
    switch (tag) {
        case 3:  // tag C
            res = 0x800000;
        case 2:  // tag B
            if (i == j || i >= 24 || j >= 24) return 0;
            return res + mat24_vect_to_cocode((1 << i) ^ (1 << j));
        case 4:  // tag T
            if (i >= 759) return 0;
            {
                uint_fast32_t w, gcode, cocode, v;
                // Put w = bitweight(j)  (mod 4)
                w = (j & 0x15) + ((j >> 1) & 0x15);
                w = w + (w >> 2) + (w >> 4);
                // Double j and adjust parity of j to even
                j = (j << 1) + (w & 1);
                gcode = MAT24_OCT_DEC_TABLE[i] & 0xfff;
                v = mat24_gcode_to_vect(gcode);
                cocode = mat24_vect_to_cocode(mat24_spread_b24(j, v));
                // Put w = bitweight(adjusted j)   (mod 4)
                w += w & 1;
                gcode ^= ((w >> 1) & 1) << 11;
                cocode ^= MAT24_THETA_TABLE[gcode & 0x7ff] & 0xfff;
                res = (gcode << 12) + cocode;
            }
            return res;
        case 5:  // tag X
            if (j >= 24) return 0;
            {
                uint_fast32_t w, gcode, cocode, theta;
                cocode = mat24_vect_to_cocode(1 << j);
                theta = MAT24_THETA_TABLE[i & 0x7ff];
                w = ((theta >> 12) & 1) ^ (i & cocode);
                mat24_def_parity12(w);
                gcode = i ^ (w << 11); 
                cocode ^= theta & 0xfff;
                res = (gcode << 12) + cocode;
            }
            return res;
        default:
            return 0;
    }
}





/**
  @brief Convert short vector in the Leech lattice mod 2 to sparse rep

  The function converts an value ``v2`` representing a vector in
  the Leech lattice mod 2 to a sparse index and returns that sparse
  index. It returns 0 if ``v2`` is not a short Leech lattice vector.
*/
// %%EXPORT px
MM_BASICS_API
uint32_t mm_aux_index_leech2_to_sparse(uint32_t v2)
{
    uint_fast32_t theta, syn, scalar, w, coc, octad, cw, lsb, cocodev, sub;

    // in the sequel we cut and paste the code for the detection of 
    // a short vector v2 in the Leech lattice mod 2 from 
    // function ``gen_leech2_type2`` in file ``gen_leech.c``.
    // After detecting such a short vector we convert that
    // vector to a sparse index.

    // Deal with odd cocode words
    if (v2 & 0x800) {   // Deal with odd cocode words
         // Let syn be the syndrome table entry for the cocode part
         theta = MAT24_THETA_TABLE[(v2 >> 12) & 0x7ff];
         syn = MAT24_SYNDROME_TABLE[(theta ^ v2) & 0x7ff];
         // Return 0 if syn does not encode a cocode word of length 1
         if ((syn & 0x3ff) < (24 << 5)) return 0;
         // Return  0 if scalar product <code, cocode> == 1  (mod 2)
         scalar = (v2 >> 12) &  v2 & 0xfff;
         mat24_def_parity12(scalar);
         if (scalar) return 0;
         // Here v2 is a short vector of shape (3^1,^1^23)
         // Return sparse vector with tag X
         return 0xA000000 + ((v2 & 0x7ff000) << 2) + ((syn & 0x1f) << 8);
    }
    // Deal with Golay code word 0
    if ((v2 & 0x7ff000L) == 0) {
         // Let syn be the syndrome table entry for the cocode part 
         syn = MAT24_SYNDROME_TABLE[v2 & 0x7ff];
         // Return 1 iff tab does not encode a cocode word of length 2
         if ((syn & 0x8000) == 0) return 0;

         // Compute cocode entries of v2
         syn = MAT24_SYNDROME_TABLE[(v2 ^ MAT24_RECIP_BASIS[23]) & 0x7ff];
         syn &= 0x3ff;
         // Bits 9..5 and bits 4..0 contain high and low cocode bit index.
         // Change a high cocode bit index 24 to 23.
         syn -= ((syn + 0x100) & 0x400) >> 5;

         // Return sparse vector with tag B is bit 23 of v2 is 0
         // and with tag C otherwise.
         return  ((syn >> 5) << 14) + ((syn & 0x1f) << 8) + 0x4000000 
                 + ((0x800000 & v2) << 2);
    }

    theta = MAT24_THETA_TABLE[(v2 >> 12) & 0x7ff];

    // Here (theta >> 12) & 7 is the bit weight of 
    // v2 + Omega * b23, where b23 is bit 23 of v2.
    // If bit 12 of theta is odd then v2 is a dodecad
    // and hence never short.
    if (theta & 0x1000) return 0;
    // Now v2 is a (possibly complemented) octad.
    // Put w = 1 if v2 is an octad and w = 0 otherwise.
    w = ((theta >> 13) ^ (v2 >> 23)) & 1;
    // XOR v2 with Omega if it has weight 16
    v2 ^= (1 - w) << 23;
    // Let coc be the cocode part of v2 (this is even)
    coc = (v2 ^ theta) & 0x7ff;
    // Let octad be the octad in vector representaition
    octad = mat24_def_gcode_to_vect(v2 >> 12); 

    // Now we proceed as in function suboctad_type(octad, w, coc)

    // Let cw be the halved bit weight of coc
    cw = MAT24_SYNDROME_TABLE[coc & 0x7ff] >> 15;
    // Put cocodev = cocode word of v (in vector rep), such 
    // that the cocode word is a suboctad of octad if possible.
    lsb = mat24_def_lsbit24(octad);
    coc ^= MAT24_RECIP_BASIS[lsb];
    syn = MAT24_SYNDROME_TABLE[coc & 0x7ff];
    cocodev = mat24_def_syndrome_from_table(syn) ^ (1UL << lsb);
    // Set sub = 0 iff cocodev is a subset of octad.
    sub = (octad & cocodev) != cocodev;
    // Check if v2 is short as in function suboctad_type().
    // Return 0 if this is not the case
    if (((~w ^ cw) & 1) | sub) return 0;

    // Here v2 is of type 2 and 'cocodev' is the cocode vector. 
    // Now we compute the number of the octad and the suboctad.
    v2 = mat24_def_gcode_to_octad(v2 >> 12); // Number of octad
    // Compute the suboctad in w
    w = mat24_extract_b24(cocodev, octad);   // This is the suboctad
    // Compute the number of the suboctad in w
    if (w & 0x80) w ^= 0xff;                 // Clear MSBit of suboctad
    w = (w >> 1) & 63;                       // Number of suboctad
    // Return sparse vector with tag 'T', octad, and suboctad
    return 0x8000000 + (v2 << 14) + (w << 8);
}



/**********************************************************************
*** Index conversion between internal and sparse rep of vectors in R_p
**********************************************************************/

/**
  @brief Convert an index from internal to sparse representation

  The function converts an index ``i`` for the internal representation 
  of a vector to an index for the sparse representation of a vector
  and returns the converted index. The function returns 0 in case
  of a bad index. 

  Indices for the sparse representation are defined as 
  in ``enum MM_SPACE_TAG`` in file ``mm_basics.h``.
*/
// %%EXPORT px
MM_BASICS_API
uint32_t mm_aux_index_intern_to_sparse(uint32_t i)
// Convert internal index i to sparse index.
// Return 0 if index i is bad
{
    uint32_t t, i0, i1, tmp;
    if (i <  MM_AUX_OFS_X) {
        if (i <  MM_AUX_OFS_T) {
            // put t =  (i / 0x300); assuming 0 <= i < 0x900 
            t = (0x2A540 >> ((i >> 8) << 1)) & 3;
            i0 = i - t * 0x300;
            i1 = i0 & 31;
            i0 >>= 5;
            if (i0 < i1) {
                tmp = i0; i0 = i1; i1 = tmp;
            }
            if (i0 >= 24) return 0;
            if (t && i0 == i1) return 0;
            return ((t + 1) << 25) + (i0 << 14) + (i1 << 8);
        } else {
            // Tag T
            i += 0x80000 - MM_AUX_OFS_T;
            return i << 8;
        } 
    } else if (i < MM_AUX_LEN_V) {
        // Tags X, Z, Y
        i -=  MM_AUX_OFS_X;
        i0 = i >> 5;
        i1 = i & 31;
        if (i1 >= 24) return 0;
        return  MM_SPACE_TAG_X + (i0 << 14) + (i1 << 8);
    } else return 0;
}




/**
  @brief Read entry from vector in internal rep indexed by Leech lattice 

  The  function returns the entry with index ``i`` of the
  vector ``mv`` with modulus ``p``. Here ``i`` must be an index
  referring to a vector of type 2 in the Leech lattice modulo 2
  in **Leech lattice encoding**. The sign bit 24 of ``i`` is
  evaluated as expected. The return value is reduced modulo ``p``.

  The function returns a negative value if ``i`` is not a vector of
  type 2 in the Leech lattice modulo 2 or ``p`` is not a legal modulus.
*/
// %%EXPORT px
MM_BASICS_API
int32_t mm_aux_get_mmv_leech2(uint32_t p, uint_mmv_t *mv, uint32_t v2)
{
    uint32_t ind = mm_aux_index_leech2_to_sparse(v2 & 0xffffffUL);
    if (ind == 0 || mm_aux_bad_p(p)) return -1; 
    ind += (0 - ((v2 >> 24) & 1)) & p;
    mm_aux_mmv_extract_sparse(p, mv, &ind, 1);    
    return ind & p;
}



/**********************************************************************
*** hashing
**********************************************************************/

/// @cond DO_NOT_DOCUMENT 


#define CH 0x9e3779b97f4a7c15ULL // close to 2**63 * (sqrt(5)-1)
#define HASH_MAX_NOTZERO 2
#define LOG2_NHASH 3
#define HASH_MIN_GAP 512

/**
  @brief Compute hash value of vector of given length

  The  function returns a hash value of the  vector ``mv`` with 
  modulus ``p``. Here ``mv`` has ``n`` entries of type ``uint_mmv_t``.
  Parameter ``mask_1`` must have the value ``1`` in ech bit field
  of an integer of type ``uint_mmv_t``.

  The value of parameter ``hash`` (e.g. from a previously computed 
  hash value) will enter into the returned hash value.

  We first scan over blocks of four integers of type ``uint_mmv_t``
  until a such a block with at least one nonzero is found.
  The we enter the index of that block and the four entires of
  the block into the hash value. After having 
  found ``HASH_MAX_NOTZERO`` such blocks, we will hash 
  over ``1 << LOG2_NHASH`` more integers of type ``uint_mmv_t``,
  at fixed positions in the remaining part of the vector.
  We hash over the remaining part of the vector only if it
  contains at least ``HASH_MIN_GAP`` integers.
   
  Note that ``n`` might be rounded up to a multiple of four.
  This is no problem if a possible slack is still within 
  the original vector to be hashed. 
*/
static inline uint64_t do_hash(
    uint_mmv_t *mv,
    uint32_t n,
    uint32_t p,
    uint_mmv_t mask_1,
    uint64_t hash
)
{
    uint_mmv_t *m_end = mv + ((n + 3) & (0 - 4ULL));
    uint_mmv_t mask_p = (uint_mmv_t)(p) * mask_1;
    uint_mmv_t mask_ph = (mask_p & ~mask_1) >> 1;
    uint_mmv_t v, w;
    int32_t k = 0, j, d;

    while (mv < m_end) {
        w = mv[0];
        v = w ^ (w >> 1);
        w = mv[1];
        v |= w ^ (w >> 1);
        w = mv[2];
        v |= w ^ (w >> 1);
        w = mv[3];
        v |= w ^ (w >> 1);
        if (v & mask_ph) {
            hash = hash * CH + (uint64_t)(m_end - mv);
            for (j = 0; j < 4; ++j) {
                v = mv[j] & mask_p;
                v ^= (v >> 1) & mask_ph;    // map 11..1 to 10..0
                w = (v & mask_ph) + mask_1; // high bit is 0 iff v = x0..0
                v &= w | mask_ph;           // map 10..0 to 00..0
                hash = hash * CH + (uint64_t)v;
            }
            if (++k >= HASH_MAX_NOTZERO) {
                mv += 4;
                break;
            }
        }
        mv += 4;
    }
    hash = hash * CH + (uint64_t)(m_end + 1 - mv);
    d = (int32_t)(m_end - mv);
    if (d < HASH_MIN_GAP) return hash;
    d = (d >> LOG2_NHASH) - ((d & 1) ^ 1);
    for (j = d >> 1; j < d << LOG2_NHASH; j += d) {
        v = mv[j] & mask_p;
        v ^= (v >> 1) & mask_ph;
        w = (v & mask_ph) + mask_1;
        v &= w | mask_ph;
        hash = hash * CH + (uint64_t)v;   
    }
    return hash;
}

static uint32_t HASH_SECTIONS[6] = {
        MM_AUX_OFS_A,  MM_AUX_OFS_B, MM_AUX_OFS_T,
        MM_AUX_OFS_X, MM_AUX_OFS_Z, MM_AUX_LEN_V
};  



/// @endcond 


/**
  @brief Compute hash value of vector in internal

  The  function returns a hash value of the  vector ``mv`` with
  modulus ``p``. It also tries to distinguish between different
  sparse vectors. Therefore it tries to hash over about 100 nonzero
  integers of type ``uint_mmv_t``. So if ``mv`` is sparse then the
  function might have to scan considerably  more zero entries.
*/
// %%EXPORT px
MM_BASICS_API
uint64_t mm_aux_hash(uint32_t p, uint_mmv_t *mv)
{

    uint_fast32_t i, p_bits, l_if;
    uint_mmv_t mask_1; 
    uint64_t hash = p; 

    if (mm_aux_bad_p(p)) return 0;
    // %%MMV_LOAD_CONST  p, i
    // Store constant table for p to i
    i = MMV_CONST_TABLE[((((p) + 1) * 232) >> 8) & 7];
    p_bits = ((i >> 15) & 15);         // This is P_BITS
    l_if = ((i) & 7);   // This is LOG_INT_FIELDS
    mask_1 =  MM_AUX_TBL_REDUCE[2*p_bits-4];

    for (i = 0; i < 5; ++i) hash = do_hash(
        mv + (HASH_SECTIONS[i] >> l_if),
        (HASH_SECTIONS[i+1] - HASH_SECTIONS[i]) >> l_if,
        p,
        mask_1,
        hash
    );
    return hash;
}


//  %%GEN h
//  %%GEN c


// %%GEN ch
#ifdef __cplusplus
}
#endif
//  %%GEN c




