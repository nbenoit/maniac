
void
syracuse_27 ( unsigned int *array )
{
  unsigned int n = 27;
  unsigned int c = 0;

  array[0] = 27;

  do
    {
      if ( n & 1 )
        n = 3*n + 1;
      else
        n = n / 2;

      ++c;
      array[c] = n + (c==16); /* bug introduced at index 16 */
    }
  while ( n != 1 );
}

#ifdef MANIAC
unsigned int array[111];

void
mania_entry ( )
{
  syracuse_27 ( &array );
}
#endif
