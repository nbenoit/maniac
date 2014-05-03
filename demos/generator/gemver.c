
#define N 4096

#define alpha 1
#define beta 1

void
gemver ( double A[N][N],
         double u1[N],
         double v1[N],
         double u2[N],
         double v2[N],
         double w[N],
         double x[N],
         double y[N],
         double z[N] )
{
    int i, j;

#pragma scop
#pragma live-out w
    for (i=0; i<N; i++)
        for (j=0; j<N; j++)
            A[i][j] = A[i][j] + u1[i]*v1[j] + u2[i]*v2[j];

    for (i=0; i<N; i++)
        for (j=0; j<N; j++)
            x[i] = x[i] + A[j][i]*y[j];

    for (i=0; i<N; i++)
        x[i] = x[i] + z[i];

    for (i=0; i<N; i++)
        for (j=0; j<N; j++)
            w[i] = w[i] +  A[i][j]*x[j];
#pragma endscop
}
