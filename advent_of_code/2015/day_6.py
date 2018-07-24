""" Advent to code day 6 """

import re

SANTA_INST = [
    "turnon 887 9 thr 959 629", "turnon 454 398 thr 844 448", "turnof 539 243 thr 559 965",
    "turnof 370 819 thr 676 868", "turnof 145 40 thr 370 997", "turnof 301 3 thr 808 453",
    "turnon 351 678 thr 951 908", "toggle 720 196 thr 897 994", "toggle 831 394 thr 904 860",
    "toggle 753 664 thr 970 926", "turnof 150 300 thr 213 740", "turnon 141 242 thr 932 871",
    "toggle 294 259 thr 474 326", "toggle 678 333 thr 752 957", "toggle 393 804 thr 510 976",
    "turnof 6 964 thr 411 976", "turnof 33 572 thr 978 590", "turnon 579 693 thr 650 978",
    "turnon 150 20 thr 652 719", "turnof 782 143 thr 808 802", "turnof 240 377 thr 761 468",
    "turnof 899 828 thr 958 967", "turnon 613 565 thr 952 659", "turnon 295 36 thr 964 978",
    "toggle 846 296 thr 969 528", "turnof 211 254 thr 529 491", "turnof 231 594 thr 406 794",
    "turnof 169 791 thr 758 942", "turnon 955 440 thr 980 477", "toggle 944 498 thr 995 928",
    "turnon 519 391 thr 605 718", "toggle 521 303 thr 617 366", "turnof 524 349 thr 694 791",
    "toggle 391 87 thr 499 792", "toggle 562 527 thr 668 935", "turnof 68 358 thr 857 453",
    "toggle 815 811 thr 889 828", "turnof 666 61 thr 768 87", "turnon 27 501 thr 921 952",
    "turnon 953 102 thr 983 471", "turnon 277 552 thr 451 723", "turnof 64 253 thr 655 960",
    "turnon 47 485 thr 734 977", "turnof 59 119 thr 699 734", "toggle 407 898 thr 493 955",
    "toggle 912 966 thr 949 991", "turnon 479 990 thr 895 990", "toggle 390 589 thr 869 766",
    "toggle 593 903 thr 926 943", "toggle 358 439 thr 870 528", "turnof 649 410 thr 652 875",
    "turnon 629 834 thr 712 895", "toggle 254 555 thr 770 901", "toggle 641 832 thr 947 850",
    "turnon 268 448 thr 743 777", "turnof 512 123 thr 625 874", "turnof 498 262 thr 930 811",
    "turnof 835 158 thr 886 242", "toggle 546 310 thr 607 773", "turnon 501 505 thr 896 909",
    "turnof 666 796 thr 817 924", "toggle 987 789 thr 993 809", "toggle 745 8 thr 860 693",
    "toggle 181 983 thr 731 988", "turnon 826 174 thr 924 883", "turnon 239 228 thr 843 993",
    "turnon 205 613 thr 891 667", "toggle 867 873 thr 984 896", "turnon 628 251 thr 677 681",
    "toggle 276 956 thr 631 964", "turnon 78 358 thr 974 713", "turnon 521 360 thr 773 597",
    "turnof 963 52 thr 979 502", "turnon 117 151 thr 934 622", "toggle 237 91 thr 528 164",
    "turnon 944 269 thr 975 453", "toggle 979 460 thr 988 964", "turnof 440 254 thr 681 507",
    "toggle 347 100 thr 896 785", "turnof 329 592 thr 369 985", "turnon 931 960 thr 979 985",
    "toggle 703 3 thr 776 36", "toggle 798 120 thr 908 550", "turnof 186 605 thr 914 709",
    "turnof 921 725 thr 979 956", "toggle 167 34 thr 735 249", "turnon 726 781 thr 987 936",
    "toggle 720 336 thr 847 756", "turnon 171 630 thr 656 769", "turnof 417 276 thr 751 500",
    "toggle 559 485 thr 584 534", "turnon 568 629 thr 690 873", "toggle 248 712 thr 277 988",
    "toggle 345 594 thr 812 723", "turnof 800 108 thr 834 618", "turnof 967 439 thr 986 869",
    "turnon 842 209 thr 955 529", "turnon 132 653 thr 357 696", "turnon 817 38 thr 973 662",
    "turnof 569 816 thr 721 861", "turnon 568 429 thr 945 724", "turnon 77 458 thr 844 685",
    "turnof 138 78 thr 498 851", "turnon 136 21 thr 252 986", "turnof 2 460 thr 863 472",
    "turnon 172 81 thr 839 332", "turnon 123 216 thr 703 384", "turnof 879 644 thr 944 887",
    "toggle 227 491 thr 504 793", "toggle 580 418 thr 741 479", "toggle 65 276 thr 414 299",
    "toggle 482 486 thr 838 931", "turnof 557 768 thr 950 927", "turnof 615 617 thr 955 864",
    "turnon 859 886 thr 923 919", "turnon 391 330 thr 499 971", "toggle 521 835 thr 613 847",
    "turnon 822 787 thr 989 847", "turnon 192 142 thr 357 846", "turnof 564 945 thr 985 945",
    "turnof 479 361 thr 703 799", "toggle 56 481 thr 489 978", "turnof 632 991 thr 774 998",
    "toggle 723 526 thr 945 792", "turnon 344 149 thr 441 640", "toggle 568 927 thr 624 952",
    "turnon 621 784 thr 970 788", "toggle 665 783 thr 795 981", "toggle 386 610 thr 817 730",
    "toggle 440 399 thr 734 417", "toggle 939 201 thr 978 803", "turnof 395 883 thr 554 929",
    "turnon 340 309 thr 637 561", "turnof 875 147 thr 946 481", "turnof 945 837 thr 957 922",
    "turnof 429 982 thr 691 991", "toggle 227 137 thr 439 822", "toggle 4 848 thr 7 932",
    "turnof 545 146 thr 756 943", "turnon 763 863 thr 937 994", "turnon 232 94 thr 404 502",
    "turnof 742 254 thr 930 512", "turnon 91 931 thr 101 942", "toggle 585 106 thr 651 425",
    "turnon 506 700 thr 567 960", "turnof 548 44 thr 718 352", "turnof 194 827 thr 673 859",
    "turnof 6 645 thr 509 764", "turnof 13 230 thr 821 361", "turnon 734 629 thr 919 631",
    "toggle 788 552 thr 957 972", "toggle 244 747 thr 849 773", "turnof 162 553 thr 276 887",
    "turnof 569 577 thr 587 604", "turnof 799 482 thr 854 956", "turnon 744 535 thr 909 802",
    "toggle 330 641 thr 396 986", "turnof 927 458 thr 966 564", "toggle 984 486 thr 986 913",
    "toggle 519 682 thr 632 708", "turnon 984 977 thr 989 986", "toggle 766 423 thr 934 495",
    "turnon 17 509 thr 947 718", "turnon 413 783 thr 631 903", "turnon 482 370 thr 493 688",
    "turnon 433 859 thr 628 938", "turnof 769 549 thr 945 810", "turnon 178 853 thr 539 941",
    "turnof 203 251 thr 692 433", "turnof 525 638 thr 955 794", "turnon 169 70 thr 764 939",
    "toggle 59 352 thr 896 404", "toggle 143 245 thr 707 320", "turnof 103 35 thr 160 949",
    "toggle 496 24 thr 669 507", "turnof 581 847 thr 847 903", "turnon 689 153 thr 733 562",
    "turnon 821 487 thr 839 699", "turnon 837 627 thr 978 723", "toggle 96 748 thr 973 753",
    "toggle 99 818 thr 609 995", "turnon 731 193 thr 756 509", "turnof 622 55 thr 813 365",
    "turnon 456 490 thr 576 548", "turnon 48 421 thr 163 674", "turnof 853 861 thr 924 964",
    "turnof 59 963 thr 556 987", "turnon 458 710 thr 688 847", "toggle 12 484 thr 878 562",
    "turnof 241 964 thr 799 983", "turnof 434 299 thr 845 772", "toggle 896 725 thr 956 847",
    "turnon 740 289 thr 784 345", "turnof 395 840 thr 822 845", "turnon 955 224 thr 996 953",
    "turnof 710 186 thr 957 722", "turnof 485 949 thr 869 985", "turnon 848 209 thr 975 376",
    "toggle 221 241 thr 906 384", "turnon 588 49 thr 927 496", "turnon 273 332 thr 735 725",
    "turnon 505 962 thr 895 962", "toggle 820 112 thr 923 143", "turnon 919 792 thr 978 982",
    "toggle 489 461 thr 910 737", "turnof 202 642 thr 638 940", "turnof 708 953 thr 970 960",
    "toggle 437 291 thr 546 381", "turnon 409 358 thr 837 479", "turnof 756 279 thr 870 943",
    "turnof 154 657 thr 375 703", "turnof 524 622 thr 995 779", "toggle 514 221 thr 651 850",
    "toggle 808 464 thr 886 646", "toggle 483 537 thr 739 840", "toggle 654 769 thr 831 825",
    "turnof 326 37 thr 631 69", "turnof 590 570 thr 926 656", "turnof 881 913 thr 911 998",
    "turnon 996 102 thr 998 616", "turnof 677 503 thr 828 563", "turnon 860 251 thr 877 441",
    "turnof 964 100 thr 982 377", "toggle 888 403 thr 961 597", "turnof 632 240 thr 938 968",
    "toggle 731 176 thr 932 413", "turnon 5 498 thr 203 835", "turnon 819 352 thr 929 855",
    "toggle 393 813 thr 832 816", "toggle 725 689 thr 967 888", "turnon 968 950 thr 969 983",
    "turnof 152 628 thr 582 896", "turnof 165 844 thr 459 935", "turnof 882 741 thr 974 786",
    "turnof 283 179 thr 731 899", "toggle 197 366 thr 682 445", "turnon 106 309 thr 120 813",
    "toggle 950 387 thr 967 782", "turnof 274 603 thr 383 759", "turnof 155 665 thr 284 787",
    "toggle 551 871 thr 860 962", "turnof 30 826 thr 598 892", "toggle 76 552 thr 977 888",
    "turnon 938 180 thr 994 997", "toggle 62 381 thr 993 656", "toggle 625 861 thr 921 941",
    "turnon 685 311 thr 872 521", "turnon 124 934 thr 530 962", "turnon 606 379 thr 961 867",
    "turnof 792 735 thr 946 783", "turnon 417 480 thr 860 598", "toggle 178 91 thr 481 887",
    "turnof 23 935 thr 833 962", "toggle 317 14 thr 793 425", "turnon 986 89 thr 999 613",
    "turnof 359 201 thr 560 554", "turnof 729 494 thr 942 626", "turnon 204 143 thr 876 610",
    "toggle 474 97 thr 636 542", "turnof 902 924 thr 976 973", "turnof 389 442 thr 824 638",
    "turnof 622 863 thr 798 863", "turnon 840 622 thr 978 920", "toggle 567 374 thr 925 439",
    "turnof 643 319 thr 935 662", "toggle 185 42 thr 294 810", "turnon 47 124 thr 598 880",
    "toggle 828 303 thr 979 770", "turnof 174 272 thr 280 311", "turnof 540 50 thr 880 212",
    "turnon 141 994 thr 221 998", "turnon 476 695 thr 483 901", "turnon 960 216 thr 972 502",
    "toggle 752 335 thr 957 733", "turnof 419 713 thr 537 998", "toggle 772 846 thr 994 888",
    "turnon 881 159 thr 902 312", "turnof 537 651 thr 641 816", "toggle 561 947 thr 638 965",
    "turnon 368 458 thr 437 612", "turnon 290 149 thr 705 919", "turnon 711 918 thr 974 945",
    "toggle 916 242 thr 926 786", "toggle 522 272 thr 773 314", "turnon 432 897 thr 440 954",
    "turnof 132 169 thr 775 380", "toggle 52 205 thr 693 747", "toggle 926 309 thr 976 669",
    "turnof 838 342 thr 938 444", "turnon 144 431 thr 260 951", "toggle 780 318 thr 975 495",
    "turnof 185 412 thr 796 541", "turnon 879 548 thr 892 860", "turnon 294 132 thr 460 338",
    "turnon 823 500 thr 899 529", "turnof 225 603 thr 483 920", "toggle 717 493 thr 930 875",
    "toggle 534 948 thr 599 968", "turnon 522 730 thr 968 950", "turnof 102 229 thr 674 529"]

def part_1(instructions):
    """ Part 1 of day 6 """

    lit = 0
    lights = [[0 for i in range(1000)] for j in range(1000)]

    for inst in instructions:
        command = inst.split()[0]
        numbers = [int(s) for s in re.findall(r'\b\d+\b', inst)]

        if command == "turnon":
            for i in range(numbers[1], numbers[3] + 1):
                for j in range(numbers[0], numbers[2] + 1):
                    lights[i][j] = 1
        elif command == "turnoff":
            for i in range(numbers[1], numbers[3] + 1):
                for j in range(numbers[0], numbers[2] + 1):
                    lights[i][j] = 0
        elif command == "toggle":
            for i in range(numbers[1], numbers[3] + 1):
                for j in range(numbers[0], numbers[2] + 1):
                    lights[i][j] ^= 1

    lit = (sum(sum(l) for l in lights))

    print("{} lights are lit".format(lit))

part_1(SANTA_INST)
