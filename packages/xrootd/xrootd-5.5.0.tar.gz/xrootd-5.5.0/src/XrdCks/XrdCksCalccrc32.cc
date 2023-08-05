/******************************************************************************/
/*                                                                            */
/*                    X r d C k s C a l c c r c 3 2 . c c                     */
/*                                                                            */
/* (c) 2011 by the Board of Trustees of the Leland Stanford, Jr., University  */
/*                            All Rights Reserved                             */
/*   Produced by Andrew Hanushevsky for Stanford University under contract    */
/*              DE-AC02-76-SFO0515 with the Department of Energy              */
/*                                                                            */
/* This file is part of the XRootD software suite.                            */
/*                                                                            */
/* XRootD is free software: you can redistribute it and/or modify it under    */
/* the terms of the GNU Lesser General Public License as published by the     */
/* Free Software Foundation, either version 3 of the License, or (at your     */
/* option) any later version.                                                 */
/*                                                                            */
/* XRootD is distributed in the hope that it will be useful, but WITHOUT      */
/* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or      */
/* FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public       */
/* License for more details.                                                  */
/*                                                                            */
/* You should have received a copy of the GNU Lesser General Public License   */
/* along with XRootD in a file called COPYING.LESSER (LGPL license) and file  */
/* COPYING (GPL license).  If not, see <http://www.gnu.org/licenses/>.        */
/*                                                                            */
/* The copyright holder's institutional names and contributor's names may not */
/* be used to endorse or promote products derived from this software without  */
/* specific prior written permission of the institution or contributor.       */
/******************************************************************************/

#include "XrdCks/XrdCksCalccrc32.hh"

/*
   C++ implementation of CRC-32 checksums.  Code is based
   upon and utilizes algorithm published by Ross Williams
   as initially implemented by Eric Durbin.

   This file contains:
      CRC lookup table
      function CalcCRC32 for calculating CRC-32 checksum

   Provided by:
      Eric Durbin
      Kentucky Cancer Registry
      University of Kentucky
      October 14, 1998

   Status:
      Public Domain
*/

/*****************************************************************/
/*                                                               */
/* CRC LOOKUP TABLE                                              */
/* ================                                              */
/* The following CRC lookup table was generated automagically    */
/* by the Rocksoft^tm Model CRC Algorithm Table Generation       */
/* Program V1.0 using the following model parameters:            */
/*                                                               */
/*    Width   : 4 bytes.                                         */
/*    Poly    : 0x04C11DB7L                                      */
/*    Reverse : FALSE                                            */
/*                                                               */
/* For more information on the Rocksoft^tm Model CRC Algorithm,  */
/* see the document titled "A Painless Guide to CRC Error        */
/* Detection Algorithms" by Ross Williams                        */
/* (ross@guest.adelaide.edu.au.). This document is likely to be  */
/* in the FTP archive "ftp.adelaide.edu.au/pub/rocksoft".        */
/*                                                               */
/*****************************************************************/

unsigned int XrdCksCalccrc32::crctable[256] =
{
 0x00000000L, 0x04C11DB7L, 0x09823B6EL, 0x0D4326D9L,
 0x130476DCL, 0x17C56B6BL, 0x1A864DB2L, 0x1E475005L,
 0x2608EDB8L, 0x22C9F00FL, 0x2F8AD6D6L, 0x2B4BCB61L,
 0x350C9B64L, 0x31CD86D3L, 0x3C8EA00AL, 0x384FBDBDL,
 0x4C11DB70L, 0x48D0C6C7L, 0x4593E01EL, 0x4152FDA9L,
 0x5F15ADACL, 0x5BD4B01BL, 0x569796C2L, 0x52568B75L,
 0x6A1936C8L, 0x6ED82B7FL, 0x639B0DA6L, 0x675A1011L,
 0x791D4014L, 0x7DDC5DA3L, 0x709F7B7AL, 0x745E66CDL,
 0x9823B6E0L, 0x9CE2AB57L, 0x91A18D8EL, 0x95609039L,
 0x8B27C03CL, 0x8FE6DD8BL, 0x82A5FB52L, 0x8664E6E5L,
 0xBE2B5B58L, 0xBAEA46EFL, 0xB7A96036L, 0xB3687D81L,
 0xAD2F2D84L, 0xA9EE3033L, 0xA4AD16EAL, 0xA06C0B5DL,
 0xD4326D90L, 0xD0F37027L, 0xDDB056FEL, 0xD9714B49L,
 0xC7361B4CL, 0xC3F706FBL, 0xCEB42022L, 0xCA753D95L,
 0xF23A8028L, 0xF6FB9D9FL, 0xFBB8BB46L, 0xFF79A6F1L,
 0xE13EF6F4L, 0xE5FFEB43L, 0xE8BCCD9AL, 0xEC7DD02DL,
 0x34867077L, 0x30476DC0L, 0x3D044B19L, 0x39C556AEL,
 0x278206ABL, 0x23431B1CL, 0x2E003DC5L, 0x2AC12072L,
 0x128E9DCFL, 0x164F8078L, 0x1B0CA6A1L, 0x1FCDBB16L,
 0x018AEB13L, 0x054BF6A4L, 0x0808D07DL, 0x0CC9CDCAL,
 0x7897AB07L, 0x7C56B6B0L, 0x71159069L, 0x75D48DDEL,
 0x6B93DDDBL, 0x6F52C06CL, 0x6211E6B5L, 0x66D0FB02L,
 0x5E9F46BFL, 0x5A5E5B08L, 0x571D7DD1L, 0x53DC6066L,
 0x4D9B3063L, 0x495A2DD4L, 0x44190B0DL, 0x40D816BAL,
 0xACA5C697L, 0xA864DB20L, 0xA527FDF9L, 0xA1E6E04EL,
 0xBFA1B04BL, 0xBB60ADFCL, 0xB6238B25L, 0xB2E29692L,
 0x8AAD2B2FL, 0x8E6C3698L, 0x832F1041L, 0x87EE0DF6L,
 0x99A95DF3L, 0x9D684044L, 0x902B669DL, 0x94EA7B2AL,
 0xE0B41DE7L, 0xE4750050L, 0xE9362689L, 0xEDF73B3EL,
 0xF3B06B3BL, 0xF771768CL, 0xFA325055L, 0xFEF34DE2L,
 0xC6BCF05FL, 0xC27DEDE8L, 0xCF3ECB31L, 0xCBFFD686L,
 0xD5B88683L, 0xD1799B34L, 0xDC3ABDEDL, 0xD8FBA05AL,
 0x690CE0EEL, 0x6DCDFD59L, 0x608EDB80L, 0x644FC637L,
 0x7A089632L, 0x7EC98B85L, 0x738AAD5CL, 0x774BB0EBL,
 0x4F040D56L, 0x4BC510E1L, 0x46863638L, 0x42472B8FL,
 0x5C007B8AL, 0x58C1663DL, 0x558240E4L, 0x51435D53L,
 0x251D3B9EL, 0x21DC2629L, 0x2C9F00F0L, 0x285E1D47L,
 0x36194D42L, 0x32D850F5L, 0x3F9B762CL, 0x3B5A6B9BL,
 0x0315D626L, 0x07D4CB91L, 0x0A97ED48L, 0x0E56F0FFL,
 0x1011A0FAL, 0x14D0BD4DL, 0x19939B94L, 0x1D528623L,
 0xF12F560EL, 0xF5EE4BB9L, 0xF8AD6D60L, 0xFC6C70D7L,
 0xE22B20D2L, 0xE6EA3D65L, 0xEBA91BBCL, 0xEF68060BL,
 0xD727BBB6L, 0xD3E6A601L, 0xDEA580D8L, 0xDA649D6FL,
 0xC423CD6AL, 0xC0E2D0DDL, 0xCDA1F604L, 0xC960EBB3L,
 0xBD3E8D7EL, 0xB9FF90C9L, 0xB4BCB610L, 0xB07DABA7L,
 0xAE3AFBA2L, 0xAAFBE615L, 0xA7B8C0CCL, 0xA379DD7BL,
 0x9B3660C6L, 0x9FF77D71L, 0x92B45BA8L, 0x9675461FL,
 0x8832161AL, 0x8CF30BADL, 0x81B02D74L, 0x857130C3L,
 0x5D8A9099L, 0x594B8D2EL, 0x5408ABF7L, 0x50C9B640L,
 0x4E8EE645L, 0x4A4FFBF2L, 0x470CDD2BL, 0x43CDC09CL,
 0x7B827D21L, 0x7F436096L, 0x7200464FL, 0x76C15BF8L,
 0x68860BFDL, 0x6C47164AL, 0x61043093L, 0x65C52D24L,
 0x119B4BE9L, 0x155A565EL, 0x18197087L, 0x1CD86D30L,
 0x029F3D35L, 0x065E2082L, 0x0B1D065BL, 0x0FDC1BECL,
 0x3793A651L, 0x3352BBE6L, 0x3E119D3FL, 0x3AD08088L,
 0x2497D08DL, 0x2056CD3AL, 0x2D15EBE3L, 0x29D4F654L,
 0xC5A92679L, 0xC1683BCEL, 0xCC2B1D17L, 0xC8EA00A0L,
 0xD6AD50A5L, 0xD26C4D12L, 0xDF2F6BCBL, 0xDBEE767CL,
 0xE3A1CBC1L, 0xE760D676L, 0xEA23F0AFL, 0xEEE2ED18L,
 0xF0A5BD1DL, 0xF464A0AAL, 0xF9278673L, 0xFDE69BC4L,
 0x89B8FD09L, 0x8D79E0BEL, 0x803AC667L, 0x84FBDBD0L,
 0x9ABC8BD5L, 0x9E7D9662L, 0x933EB0BBL, 0x97FFAD0CL,
 0xAFB010B1L, 0xAB710D06L, 0xA6322BDFL, 0xA2F33668L,
 0xBCB4666DL, 0xB8757BDAL, 0xB5365D03L, 0xB1F740B4L
};

/*****************************************************************/
/*                   End of CRC Lookup Table                     */
/*****************************************************************/

/* Calculate CRC-32 Checksum for NAACCR Record,
   skipping area of record containing checksum field.

   Uses non-reflected table driven method documented by Ross Williams.

   PARAMETERS:
     unsigned char *p           Record Buffer
     unsigned long reclen       Record Length

   RETURNS:
     checksum value

   Author:
     Eric Durbin 1998-10-14
     Simplified by Andrew Hanushevsky 2007-07-20

   Status:
     Public Domain

   Changes:
     Compute CRC for complete buffer
     Use unsigned int instead of long to insure 32 bit values.
     Include length bits at the end to correspond to the Posix 1003.2 spec.
     Make this a C++ class.
*/
void XrdCksCalccrc32::Update(const char *p, int reclen)
{

// Process each byte
//
   TotLen += reclen;
   while(reclen-- > 0)
        C32Result = (C32Result<<8) 
                  ^ crctable[(unsigned char)((C32Result>>24)^*p++)];
}
