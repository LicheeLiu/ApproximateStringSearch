# ApproximateStringSearch
This program can be used as spelling auto-correct. Finding the approximate correct spelling in a dictionary that records all possible correct spellings.
The first method is called Global Edit Distance. The idea of Global Edit distance goes like:
From string f to string t, given array of |f| + 1 columns and |t| + 1 rows, we can use the Needle-Wunsch algorithm to determin the 'distance' (approximality) of 2 strings.
For example, if one character match, it gets (+1) mark, and insert/delete/replace get (-1) mark. The string with the maximum mark is the closest approximate string.
The other method is 'N-Gram Distance'. Here I use N=2. In this method, a string is divided into substrings of length 2. The N-Gram distance = the number of substrings of string1 + the number of substrings of string2 - the number of common substrings
The less the N-Gram distance, the better the result.
