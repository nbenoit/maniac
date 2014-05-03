
unsigned int
syracuse ( unsigned int n )
{
  unsigned int c = 0;

  while ( n != 1 )
    {
      if ( n & 1 )
        {
          n = (3*n + 1) / 2;
          ++c;
        }
      else
        n = n / 2;

      ++c;
    }

  return c;
}

#ifdef MANIAC
void
mania_entry ( )
{
  unsigned int i;
  for ( i=1; i<3000000; ++i )
    {
      syracuse ( i );
    }
}
#endif
