//mpicc -O3 -w -o tcom tcom.c -lm
#include <math.h>
#include <stdio.h>
#include <mpi.h>

int main(int argc, char **argv)
{
	
	int myrank, numprocs,numit=0,i,valido = 0, operacion = 0,init = 0,size=0,k;
	char name[MPI_MAX_PROCESSOR_NAME],dato=NULL;
	
	double start_time, end_time, t_beta=0.0,t_tau = 0.0,t_comm,expo,tam; 
	double* mensaje;
		
	MPI_Status estado; 
	MPI_Init(&argc,&argv);
	MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
	MPI_Comm_size(MPI_COMM_WORLD, &numprocs);

if(init == 0 && myrank == 0) // inicializamos los datos necesarios para las operaciones
{
	printf("Pon el numero de iteraciones");
	scanf("%d",&numit);
	MPI_Send(&numit,1,MPI_INT,1,8,MPI_COMM_WORLD);
	init = 1;
}
//Calculamos beta

if (operacion == 0)
{
	if (myrank == 0)
	{

		start_time = MPI_Wtime();
		for (i = 0; i < numit; i++)
		{

				
				MPI_Send(&dato,1,MPI_BYTE,1,8,MPI_COMM_WORLD);
				MPI_Recv(&dato,1,MPI_BYTE,1,8,MPI_COMM_WORLD,&estado);

		}
		end_time = MPI_Wtime();	
		t_beta = (end_time - start_time)/(2 * numit);
	
	}
		
	
	else
	{
		MPI_Recv(&numit,1,MPI_INT,0,8,MPI_COMM_WORLD,&estado);
		
		for (i = 0; i < numit; i++)
		{
			MPI_Recv(&dato,1,MPI_BYTE,0,8,MPI_COMM_WORLD,&estado);

			MPI_Send(&dato,1,MPI_BYTE,0,8,MPI_COMM_WORLD);
		}	
	}

	operacion = 1;
}
if(operacion == 1) {
	
for(k=5;k<19; k++)
{	
	size = pow(2,k);
	mensaje = malloc(size*sizeof(double));
	
	

//Calculamos tau
if (myrank == 0)
	{
		start_time = MPI_Wtime();
		
		int j;
		
		for (i = 0; i<numit; i++)
		{
			
				
				MPI_Send(mensaje,size,MPI_DOUBLE,1,8,MPI_COMM_WORLD);
				
				MPI_Recv(mensaje,size,MPI_DOUBLE,1,8,MPI_COMM_WORLD,&estado);

				
			
		}
		end_time = MPI_Wtime();
		
		t_comm = (end_time - start_time)/(2*numit);
	
		//Calculamos las medias...
				
		t_tau = (t_comm - t_beta)/(8*size);
	
		printf("Tamaño del mensaje: \t %d Kbytes\n",size);
		printf("El tiempo de comunicación: \t %f us\t\n",t_comm * pow(10,6));
		printf ("El parámetro beta: \t %f us\n",t_beta* pow(10,6));
		printf("El parámetro tau: \t %f us/bytes\n\n\n",t_tau* pow(10,6));
		
	}
else
{
	
	for (i = 0; i<numit; i++)
	{
		MPI_Recv(mensaje,size,MPI_DOUBLE,0,8,MPI_COMM_WORLD,&estado);
		
		MPI_Send(mensaje,size,MPI_DOUBLE,0,8,MPI_COMM_WORLD);
		
	}
		
}

free(mensaje);
mensaje = NULL;

}
}


MPI_Finalize();

}


