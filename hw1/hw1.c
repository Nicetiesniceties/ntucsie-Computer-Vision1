#include <stdio.h>
#include "hvision.h"

   IMAGE *im, *im_updown, *im_rightleft, *im_diagonal;

main (int argc, char **argv)
{
    int i, j;

    if (argc != 2) {
        printf("usage: hw1 *.im\n");
        exit(1);
    } /* if */

    /* Read in the original image */
    im = hvReadImage(argv[1]);
    if (im == NULL) {
        printf("cannot open file %s\n",argv[1]);
        exit(1);
    } /*if*/

    im_updown = hvCopyImage(im);
    im_rightleft = hvCopyImage(im);
    im_diagonal = hvCopyImage(im);

    for (i=0; i<im->height; i++) {
        for (j=0; j<im->width; j++) {
            B_PIX(im_updown, i, j) = B_PIX(im, im->height-i-1, j);
            B_PIX(im_rightleft, i, j) = B_PIX(im, i, im->width-j-1);
	            B_PIX(im_diagonal, i, j) = B_PIX(im, j, i);
        } /*j*/
    } /*i*/

    hvWriteImage(im_updown, "lena_updown.im");
    hvWriteImage(im_rightleft, "lena_rightleft.im");
    hvWriteImage(im_diagonal, "lena_diagonal.im");
} /*main*/

